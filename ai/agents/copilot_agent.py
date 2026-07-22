import json
import logging
from typing import Dict, Any, List, AsyncGenerator

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from ai.retrieval.hybrid import HybridRetriever
from ai.llm_factory import get_llm
from tenacity import retry, stop_after_attempt, wait_exponential

logger = logging.getLogger(__name__)

COPILOT_SYSTEM_PROMPT = """You are OpsPilot AI Copilot — an expert enterprise knowledge assistant for professionals across any industry.

You answer questions about:
- Operational processes, resources, and failure analysis
- Standard operating procedures (SOPs) and best practices
- Inspection records and compliance requirements
- Root cause analysis support
- Operational history, documentation, and entity relationships

IMPORTANT RULES:
1. Base your answer ONLY on the provided context. Do not invent facts.
2. Always mention the source document or section you used.
3. If the context is insufficient, clearly say so and suggest what additional information would help.
4. Give concise, actionable answers suitable for domain professionals.
5. Rate your confidence (High / Medium / Low) based on how well the context matches the question.
6. Adapt your language and terminology to the domain and context of the question.

Context from Knowledge Base:
{context}

Question: {question}

Respond with:
- A clear, structured answer
- Source references (e.g. "Source: Operations Manual, Section 3")
- Confidence: [High/Medium/Low] — [brief reason]
"""


class CopilotAgent:
    def __init__(self):
        self.retriever = HybridRetriever()
        self._llm = None
        self._chain = None

    def _get_chain(self):
        """Lazy-initialize the LangChain chain."""
        if self._chain is None:
            # Use model from settings (GEMINI_MODEL in .env)
            llm = get_llm(temperature=0.1)
            prompt = ChatPromptTemplate.from_template(COPILOT_SYSTEM_PROMPT)
            self._chain = prompt | llm | StrOutputParser()
        return self._chain

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=20))
    async def _invoke_chain_with_retry(self, context_text: str, query: str) -> str:
        chain = self._get_chain()
        return await chain.ainvoke({
            "context": context_text,
            "question": query,
        })

    async def chat(self, user_id: str, query: str) -> Dict[str, Any]:
        """
        Process a user query using Hybrid RAG and return a cited AI response.
        """
        logger.info(f"Copilot query from {user_id}: {query[:80]}")

        # 1. Retrieve context from vector DB + knowledge graph
        context_items: List[Dict] = await self.retriever.retrieve_context(query, top_k=5)

        # 2. Format context for the prompt
        if context_items:
            context_parts = []
            for i, item in enumerate(context_items, 1):
                source = item.get("source", item.get("type", "Knowledge Base"))
                metadata = item.get("metadata", {})
                page = metadata.get("page_no")
                section = metadata.get("section")
                
                meta_str = f"Source: {source}"
                if page:
                    meta_str += f", Page {page}"
                if section:
                    meta_str += f", Section '{section}'"
                    
                content = item.get("content", "")
                context_parts.append(f"[{i}] ({meta_str})\n{content}")
            context_text = "\n\n".join(context_parts)
        else:
            context_text = "No specific documents found in the knowledge base for this query."

        # 3. Call LLM with automatic retry for rate limits
        try:
            answer = await self._invoke_chain_with_retry(context_text, query)
        except Exception as e:
            logger.error(f"LLM call failed: {e}")
            answer = (
                f"I retrieved {len(context_items)} relevant documents but encountered an error "
                f"generating the response. Please check the API key configuration.\n\nError: {str(e)}"
            )

        # 4. Parse confidence from the answer text (simple heuristic)
        confidence_score = 0.9 if "High" in answer else (0.6 if "Medium" in answer else 0.4)

        return {
            "answer": answer,
            "context_used": context_items,
            "sources_count": len(context_items),
            "confidence": confidence_score,
        }

    async def chat_stream(self, user_id: str, query: str) -> AsyncGenerator[str, None]:
        """
        Process a user query and stream the response back as Server-Sent Events (SSE).
        First yields the retrieved context, then yields the AI answer chunks.
        """
        logger.info(f"Copilot stream query from {user_id}: {query[:80]}")

        # 1. Retrieve context
        context_items = await self.retriever.retrieve_context(query, top_k=5)
        
        # 2. Yield context first so the UI can show sources immediately
        initial_data = {
            "type": "context",
            "context_used": context_items,
            "sources_count": len(context_items)
        }
        yield f"data: {json.dumps(initial_data)}\n\n"

        # 3. Format context
        if context_items:
            context_parts = []
            for i, item in enumerate(context_items, 1):
                source = item.get("source", item.get("type", "Knowledge Base"))
                metadata = item.get("metadata", {})
                page = metadata.get("page_no")
                section = metadata.get("section")
                
                meta_str = f"Source: {source}"
                if page:
                    meta_str += f", Page {page}"
                if section:
                    meta_str += f", Section '{section}'"
                    
                content = item.get("content", "")
                context_parts.append(f"[{i}] ({meta_str})\n{content}")
            context_text = "\n\n".join(context_parts)
        else:
            context_text = "No specific documents found in the knowledge base for this query."

        # 4. Stream LLM chunks
        chain = self._get_chain()
        try:
            async for chunk in chain.astream({
                "context": context_text,
                "question": query,
            }):
                chunk_data = {"type": "chunk", "content": chunk}
                yield f"data: {json.dumps(chunk_data)}\n\n"
        except Exception as e:
            logger.error(f"LLM stream failed: {e}")
            error_data = {"type": "chunk", "content": f"\n\n[Error generating response: {str(e)}]"}
            yield f"data: {json.dumps(error_data)}\n\n"
        
        # 5. Signal end of stream
        yield "data: [DONE]\n\n"
