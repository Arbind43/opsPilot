import os
from dotenv import load_dotenv

load_dotenv()

def test_embed(model_name):
    try:
        from langchain_google_genai import GoogleGenerativeAIEmbeddings
        print(f"Testing Gemini Embeddings with {model_name}...")
        embedder = GoogleGenerativeAIEmbeddings(
            model=model_name,
            google_api_key=os.getenv("GOOGLE_API_KEY")
        )
        res = embedder.embed_query("Hello world")
        print(f"Success! {model_name} Vector length: {len(res)}")
    except Exception as e:
        print(f"Error {model_name}: {e}")

if __name__ == "__main__":
    test_embed("models/embedding-001")
    test_embed("models/text-embedding-004")
    test_embed("models/text-embedding-004")
    test_embed("models/gemini-embedding-2")
    test_embed("models/gemini-embedding-2-preview")
