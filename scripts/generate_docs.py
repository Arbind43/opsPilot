"""
Generates the OpsPilot AI Project Documentation HTML file.
Run this script from the project root: python scripts/generate_docs.py
"""

import os

OUTPUT_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "OpsPilot_Project_Documentation.html")

HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1.0"/>
<title>OpsPilot AI — Project Documentation</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500&display=swap');
:root{--primary:#2563eb;--accent:#f97316;--dark:#0f172a;--text:#1e293b;--muted:#64748b;--border:#e2e8f0;--light:#f8fafc;}
*{margin:0;padding:0;box-sizing:border-box;}
body{font-family:'Inter',sans-serif;color:var(--text);background:#fff;font-size:10pt;line-height:1.65;}
@media print{
  body{font-size:9pt;}
  .pb{page-break-before:always;}
  .nopb{page-break-inside:avoid;}
  header,th,.arch-box,.role-card,.flow-step{-webkit-print-color-adjust:exact;print-color-adjust:exact;}
  .fab{display:none;}
}
/* COVER */
header{background:linear-gradient(135deg,#0f172a 0%,#1e3a5f 55%,#1d4ed8 100%);color:#fff;padding:52px 72px 44px;position:relative;overflow:hidden;}
header::after{content:'';position:absolute;top:-100px;right:-100px;width:380px;height:380px;border-radius:50%;background:radial-gradient(circle,rgba(99,179,237,.1) 0%,transparent 70%);pointer-events:none;}
.c-tag{display:inline-block;background:rgba(249,115,22,.22);color:#fdba74;border:1px solid rgba(249,115,22,.4);border-radius:20px;padding:4px 14px;font-size:7.5pt;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;margin-bottom:16px;}
header h1{font-size:34pt;font-weight:900;letter-spacing:-1px;line-height:1.1;}
header h1 span{color:#60a5fa;}
.subtitle{font-size:12pt;color:#93c5fd;margin-top:8px;margin-bottom:26px;}
.cover-meta{display:flex;flex-wrap:wrap;gap:36px;margin-top:24px;}
.cm label{display:block;font-size:7pt;color:#94a3b8;text-transform:uppercase;letter-spacing:1px;font-weight:600;}
.cm span{display:block;font-size:9.5pt;font-weight:600;color:#e2e8f0;margin-top:2px;}
.badges{display:flex;flex-wrap:wrap;gap:8px;margin-top:24px;}
.badge{padding:4px 12px;border-radius:20px;border:1px solid rgba(255,255,255,.18);color:#e2e8f0;font-size:7.5pt;font-weight:500;}
/* STATS */
.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin:16px 0;}
.stat{background:var(--light);border:1px solid var(--border);border-radius:10px;padding:13px;text-align:center;}
.stat .n{font-size:21pt;font-weight:900;color:var(--primary);line-height:1;}
.stat .l{font-size:7pt;color:var(--muted);font-weight:600;text-transform:uppercase;letter-spacing:.5px;margin-top:3px;}
/* LAYOUT */
a{color:var(--primary);text-decoration:none;}
a:hover{text-decoration:underline;}
.wrap{max-width:980px;margin:0 auto;padding:0 40px;}
.sec{padding:34px 0;border-bottom:1px solid var(--border);}
.sec:last-child{border-bottom:none;}
.sec-hd{display:flex;align-items:center;gap:10px;margin-bottom:16px;}
.sec-n{width:27px;height:27px;background:var(--primary);color:#fff;border-radius:7px;display:flex;align-items:center;justify-content:center;font-size:8.5pt;font-weight:700;flex-shrink:0;}
h2{font-size:14pt;font-weight:800;color:var(--dark);}
h3{font-size:11pt;font-weight:700;color:var(--dark);margin:18px 0 7px;}
h4{font-size:9.5pt;font-weight:600;color:#1d4ed8;margin:12px 0 5px;}
p{margin-bottom:9px;color:#334155;}
ul,ol{padding-left:18px;margin-bottom:9px;}
li{margin-bottom:4px;color:#334155;}
strong{color:var(--dark);}
code{font-family:'JetBrains Mono',monospace;background:#f1f5f9;padding:1px 5px;border-radius:4px;font-size:8pt;}
/* CALLOUTS */
.info{background:#eff6ff;border-left:4px solid var(--primary);border-radius:0 8px 8px 0;padding:12px 16px;margin:14px 0;}
.info p{margin:0;color:#1e3a5f;font-style:italic;}
.warn{background:#fff7ed;border-left:4px solid var(--accent);border-radius:0 8px 8px 0;padding:12px 16px;margin:14px 0;}
.warn p{margin:0;color:#7c3106;}
/* CARDS */
.grid2{display:grid;grid-template-columns:repeat(2,1fr);gap:14px;margin:14px 0;}
.grid3{display:grid;grid-template-columns:repeat(3,1fr);gap:11px;margin:14px 0;}
.grid4{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin:14px 0;}
.card{background:var(--light);border:1px solid var(--border);border-radius:9px;padding:14px;}
.card h4{margin-top:0;}
/* ARCH BOXES */
.ab{border-radius:9px;padding:13px;text-align:center;}
.ab h4{font-size:8pt;margin:0 0 5px;color:#1e293b;}
.ab p{font-size:7.5pt;margin:0;color:#475569;line-height:1.5;}
.ab.blue{background:#dbeafe;border:1px solid #93c5fd;}
.ab.green{background:#dcfce7;border:1px solid #86efac;}
.ab.purple{background:#ede9fe;border:1px solid #c4b5fd;}
.ab.orange{background:#ffedd5;border:1px solid #fdba74;}
.ab.teal{background:#ccfbf1;border:1px solid #5eead4;}
.ab.slate{background:#f1f5f9;border:1px solid #cbd5e1;}
/* TABLE */
table{width:100%;border-collapse:collapse;margin:14px 0;font-size:8.5pt;}
th{background:var(--dark);color:#fff;padding:8px 11px;text-align:left;font-weight:600;font-size:8pt;}
td{padding:7px 11px;border-bottom:1px solid var(--border);vertical-align:top;}
tr:nth-child(even) td{background:var(--light);}
/* TAGS */
.tag{display:inline-block;padding:2px 8px;border-radius:20px;font-size:7pt;font-weight:600;margin:1px;}
.tag.g{background:#dcfce7;color:#15803d;}
.tag.b{background:#dbeafe;color:#1d4ed8;}
.tag.o{background:#ffedd5;color:#c2410c;}
/* FLOW */
.flow{display:flex;flex-wrap:wrap;align-items:center;gap:6px;margin:13px 0;}
.fs{background:var(--dark);color:#fff;padding:6px 13px;border-radius:20px;font-size:7.5pt;font-weight:600;white-space:nowrap;}
.fs.a{background:var(--primary);}
.fa{color:var(--muted);font-size:13pt;}
/* ENDPOINTS */
.ep{display:flex;gap:9px;align-items:center;padding:5px 0;border-bottom:1px solid #f8fafc;font-size:8pt;}
.m{padding:2px 7px;border-radius:4px;font-size:7pt;font-weight:700;font-family:'JetBrains Mono',monospace;min-width:38px;text-align:center;}
.m.get{background:#dcfce7;color:#15803d;}
.m.post{background:#dbeafe;color:#1d4ed8;}
.m.put{background:#ffedd5;color:#c2410c;}
.m.del{background:#fee2e2;color:#dc2626;}
.path{font-family:'JetBrains Mono',monospace;color:#1e3a5f;font-weight:500;}
/* FEATURE ROW */
.fr{display:flex;gap:12px;padding:11px 0;border-bottom:1px solid #f1f5f9;align-items:flex-start;}
.fr:last-child{border-bottom:none;}
.fi{font-size:20px;flex-shrink:0;margin-top:1px;}
.fb h4{margin-top:0;margin-bottom:3px;}
.fb p{margin:0;font-size:8.5pt;}
/* ROLE CARDS */
.role-card{border-radius:9px;padding:13px;text-align:center;}
.role-card h4{margin-top:0;font-size:9pt;}
.role-card p{font-size:7.5pt;margin:0;}
.role-card.admin{background:#fef3c7;border:1px solid #fde68a;}
.role-card.eng{background:#dbeafe;border:1px solid #93c5fd;}
.role-card.op{background:#dcfce7;border:1px solid #86efac;}
.role-card.view{background:#f3f4f6;border:1px solid #d1d5db;}
/* TOC */
.toc-row{padding:5px 0;border-bottom:1px dotted #e2e8f0;display:flex;justify-content:space-between;font-size:9pt;}
.toc-row .num{color:var(--primary);font-weight:600;margin-right:6px;}
/* FAB */
.fab{position:fixed;bottom:22px;right:22px;background:#2563eb;color:#fff;border:none;padding:11px 22px;border-radius:11px;font-size:13px;font-weight:700;cursor:pointer;box-shadow:0 4px 20px rgba(37,99,235,.4);font-family:Inter,sans-serif;z-index:999;}
/* FOOTER */
footer{background:var(--dark);color:#94a3b8;padding:22px 72px;font-size:8pt;display:flex;justify-content:space-between;align-items:center;margin-top:16px;}
footer strong{color:#e2e8f0;}
</style>
</head>
<body>

<!-- COVER -->
<header>
  <div class="c-tag">&#127942; ET AI Hackathon 2.0 &mdash; Problem Statement #8</div>
  <h1>OpsPilot <span>AI</span></h1>
  <div class="subtitle">AI for Industrial Knowledge Intelligence: Unified Asset &amp; Operations Brain</div>
  <div class="stats" style="max-width:640px;margin-top:22px;">
    <div class="stat" style="background:rgba(255,255,255,.08);border-color:rgba(255,255,255,.12);">
      <div class="n" style="color:#60a5fa;">4</div><div class="l" style="color:#94a3b8;">AI Agents</div></div>
    <div class="stat" style="background:rgba(255,255,255,.08);border-color:rgba(255,255,255,.12);">
      <div class="n" style="color:#60a5fa;">12+</div><div class="l" style="color:#94a3b8;">API Modules</div></div>
    <div class="stat" style="background:rgba(255,255,255,.08);border-color:rgba(255,255,255,.12);">
      <div class="n" style="color:#60a5fa;">4</div><div class="l" style="color:#94a3b8;">Databases</div></div>
    <div class="stat" style="background:rgba(255,255,255,.08);border-color:rgba(255,255,255,.12);">
      <div class="n" style="color:#60a5fa;">4</div><div class="l" style="color:#94a3b8;">User Roles</div></div>
  </div>
    <div class="cm"><label>Team Name</label><span>Infinite Loop</span></div>
    <div class="cm"><label>Members</label><span>Samar Pratap, Lokesh Ganesh Bawariya, Gaurav Jaiswal, Arbind Kumar Munda</span></div>
    <div class="cm"><label>Repository</label><span><a href="https://github.com/Arbind43/opsPilot" target="_blank">github.com/Arbind43/opsPilot</a></span></div>
    <div class="cm"><label>Live Frontend</label><span><a href="https://ops-pilot-hjur.vercel.app" target="_blank">ops-pilot-hjur.vercel.app</a></span></div>
    <div class="cm"><label>Backend API</label><span><a href="https://opspilot-1-bwho.onrender.com" target="_blank">opspilot-1-bwho.onrender.com</a></span></div>
  </div>
  <div class="badges">
    <div class="badge">FastAPI</div><div class="badge">React 19</div>
    <div class="badge">LangChain + LangGraph</div><div class="badge">MongoDB Atlas</div>
    <div class="badge">Neo4j Knowledge Graph</div><div class="badge">Pinecone Vector DB</div>
    <div class="badge">Groq Llama-3.3-70b</div><div class="badge">Google Gemini</div>
  </div>
</header>

<div class="wrap">

<!-- TOC -->
<div class="sec">
  <div class="sec-hd"><div class="sec-n">&#128203;</div><h2>Table of Contents</h2></div>
  <div class="toc-row"><span><span class="num">1.</span> Problem Context &amp; Challenge Statement</span></div>
  <div class="toc-row"><span><span class="num">2.</span> Our Solution &mdash; OpsPilot AI</span></div>
  <div class="toc-row"><span><span class="num">3.</span> System Architecture</span></div>
  <div class="toc-row"><span><span class="num">4.</span> AI Engine &mdash; Agents &amp; Core Intelligence</span></div>
  <div class="toc-row"><span><span class="num">5.</span> Backend &mdash; FastAPI Service &amp; API Reference</span></div>
  <div class="toc-row"><span><span class="num">6.</span> Frontend &mdash; User Interface &amp; Dashboards</span></div>
  <div class="toc-row"><span><span class="num">7.</span> Database Architecture (Polyglot Persistence)</span></div>
  <div class="toc-row"><span><span class="num">8.</span> Role-Based Access Control (RBAC)</span></div>
  <div class="toc-row"><span><span class="num">9.</span> Key Features Deep Dive</span></div>
  <div class="toc-row"><span><span class="num">10.</span> Full Technology Stack</span></div>
  <div class="toc-row"><span><span class="num">11.</span> Deployment Architecture</span></div>
  <div class="toc-row"><span><span class="num">12.</span> Alignment with Hackathon Requirements</span></div>
</div>

<!-- SEC 1 -->
<div class="sec pb">
  <div class="sec-hd"><div class="sec-n">1</div><h2>Problem Context &amp; Challenge Statement</h2></div>
  <div class="info"><p><strong>Theme:</strong> Industrial Intelligence / Document Management / Knowledge Engineering / Quality &mdash; Problem Statement #8 of the ET AI Hackathon.</p></div>
  <h3>The Problem</h3>
  <p>A 2024 McKinsey global survey found that professionals in asset-intensive industries spend an average of <strong>35% of their working hours</strong> searching for information, clarifying instructions, or recreating documents that already exist somewhere in the organisation.</p>
  <p>In India specifically, a NASSCOM-EY study of manufacturing and energy companies found that the average large plant operates across <strong>7&ndash;12 disconnected document systems</strong> &mdash; P&amp;IDs and engineering drawings in one place, maintenance work orders in another, operating procedures in a third, inspection records in a fourth, and regulatory submissions scattered across email archives.</p>
  <div class="grid2">
    <div class="card nopb"><h4>&#9888;&#65039; 18&ndash;22% Unplanned Downtime</h4><p>BIS Research estimated that knowledge fragmentation contributes to 18&ndash;22% of unplanned downtime events in Indian heavy industry, as maintenance teams make decisions without complete equipment history or failure pattern context.</p></div>
    <div class="card nopb"><h4>&#129493; The Knowledge Cliff</h4><p>An estimated 25% of India&rsquo;s experienced industrial engineers and operators will retire within the next decade, taking decades of undocumented operational knowledge with them. Once gone, it cannot be recovered.</p></div>
    <div class="card nopb"><h4>&#128196; Document Fragmentation</h4><p>P&amp;IDs, maintenance work orders, safety procedures, operating instructions, inspection records, and regulatory submissions all sit in separate, siloed systems with no unified intelligence layer connecting them.</p></div>
    <div class="card nopb"><h4>&#128274; Compliance Risk</h4><p>Manual compliance tracking against regulatory frameworks (Factory Act, OISD, PESO, environmental norms) creates gaps that can result in audit failures, fines, and safety incidents.</p></div>
  </div>
  <div class="warn"><p><strong>Core Insight:</strong> Knowledge fragmentation in industrial operations is not a file management problem. It is a safety problem, a quality problem, and an operational efficiency problem &mdash; and it compounds over time. The organisations that solve it first will have a structural advantage.</p></div>
  <h3>The Challenge Statement</h3>
  <p>Build an AI-powered Industrial Knowledge Intelligence platform that <strong>ingests heterogeneous documents</strong> &mdash; engineering drawings, maintenance records, safety procedures, inspection reports, operating instructions, project files &mdash; across structured and unstructured formats, and makes their collective intelligence <strong>queryable, actionable, and continuously updated</strong> at the point of need, across any device or function.</p>
</div>

<!-- SEC 2 -->
<div class="sec pb">
  <div class="sec-hd"><div class="sec-n">2</div><h2>Our Solution &mdash; OpsPilot AI</h2></div>
  <div class="info"><p>OpsPilot AI is an <strong>Enterprise Knowledge Intelligence Platform</strong> providing real-time operational insights, predictive maintenance intelligence, automated root-cause analysis, and compliance tracking &mdash; all powered by a Hybrid RAG Engine combining Vector Search and Knowledge Graphs.</p></div>
  <h3>What We Built &mdash; The Four Core Pillars</h3>
  <div class="fr">
    <div class="fi">&#129504;</div>
    <div class="fb"><h4>Universal Document Ingestion &amp; Knowledge Graph Agent</h4>
    <p>An AI pipeline that processes PDFs, scanned documents, DOCX, and XLSX files &mdash; extracting entities (equipment tags, process parameters, regulatory references, personnel, dates) and building a unified Neo4j knowledge graph that maintains relationships across document types and updates automatically as new records arrive.</p></div>
  </div>
  <div class="fr">
    <div class="fi">&#129302;</div>
    <div class="fb"><h4>Expert Knowledge Copilot (AI Chatbot)</h4>
    <p>A RAG-powered conversational AI (Groq Llama-3.3-70b) that answers operational, maintenance, and engineering queries across the full document corpus &mdash; with source citations and context-aware responses. Uses a Hybrid Retrieval system: Pinecone vector search + Neo4j graph traversal for maximum accuracy. Responses stream in real-time via SSE.</p></div>
  </div>
  <div class="fr">
    <div class="fi">&#128295;</div>
    <div class="fb"><h4>Maintenance Intelligence &amp; RCA Agent</h4>
    <p>An AI agent that fuses work order history, equipment failure records, inspection findings, and operating conditions to generate predictive maintenance recommendations and Root Cause Analysis (RCA) reports &mdash; reducing unplanned downtime by connecting the dots that no individual team member can connect alone.</p></div>
  </div>
  <div class="fr">
    <div class="fi">&#9989;</div>
    <div class="fb"><h4>Quality &amp; Regulatory Compliance Intelligence</h4>
    <p>An agentic system that maps regulatory requirements (Factory Act, OISD, PESO, environmental norms, quality standards) against current procedures, equipment states, and inspection records &mdash; identifying compliance gaps, auto-generating compliance evidence packages for audits, and flagging quality deviations before they escalate.</p></div>
  </div>
  <h3>Impact Metrics Targeted</h3>
  <div class="stats">
    <div class="stat"><div class="n">35%</div><div class="l">Reduction in search time</div></div>
    <div class="stat"><div class="n">&lt;2min</div><div class="l">AI response to any query</div></div>
    <div class="stat"><div class="n">100%</div><div class="l">Automated compliance detection</div></div>
    <div class="stat"><div class="n">24/7</div><div class="l">Knowledge on any device</div></div>
  </div>
</div>

<!-- SEC 3 -->
<div class="sec pb">
  <div class="sec-hd"><div class="sec-n">3</div><h2>System Architecture</h2></div>
  <h3>High-Level Architecture</h3>
  <div class="flow">
    <div class="fs">User Browser</div><div class="fa">&rarr;</div>
    <div class="fs a">React 19 Frontend (Vercel CDN)</div><div class="fa">&rarr;</div>
    <div class="fs">FastAPI Backend (Render)</div><div class="fa">&rarr;</div>
    <div class="fs a">AI Engine (LangChain + LangGraph)</div><div class="fa">&rarr;</div>
    <div class="fs">Polyglot Database Layer</div>
  </div>
  <h3>Component Architecture</h3>
  <div class="grid3">
    <div class="ab blue"><h4>&#127912; Frontend Layer</h4><p>React 19 + TypeScript + Vite. Vercel CDN. Zustand state. Real-time SSE streaming. Tailwind CSS dark-mode UI.</p></div>
    <div class="ab green"><h4>&#9881;&#65039; Backend API Layer</h4><p>FastAPI Python. RESTful + SSE endpoints. JWT auth. Role-based middleware. Pydantic v2 validation.</p></div>
    <div class="ab purple"><h4>&#129504; AI Engine</h4><p>LangChain + LangGraph multi-agent. Groq LLM + Gemini Embeddings. Hybrid RAG retrieval.</p></div>
    <div class="ab orange"><h4>&#128228; Document Pipeline</h4><p>Celery async workers. PDF/DOCX/XLSX parsing. PyMuPDF + pytesseract OCR. Entity extraction.</p></div>
    <div class="ab teal"><h4>&#128451;&#65039; Data Layer</h4><p>MongoDB (documents), Neo4j (graph), Pinecone (vectors), Redis (cache + broker).</p></div>
    <div class="ab slate"><h4>&#9729;&#65039; Deployment</h4><p>Vercel (frontend CI/CD), Render (backend), Upstash Redis, MongoDB Atlas, Pinecone Cloud.</p></div>
  </div>
  <h3>Document Ingestion Pipeline Flow</h3>
  <div class="flow">
    <div class="fs">Upload File (PDF/DOCX/XLSX)</div><div class="fa">&rarr;</div>
    <div class="fs a">Parse &amp; OCR (PyMuPDF + pytesseract)</div><div class="fa">&rarr;</div>
    <div class="fs">Chunk Text (LangChain)</div><div class="fa">&rarr;</div>
    <div class="fs a">Embed (Gemini 768-dim)</div><div class="fa">&rarr;</div>
    <div class="fs">Store in Pinecone + Neo4j</div>
  </div>
  <h3>AI Copilot Query Flow</h3>
  <div class="flow">
    <div class="fs">User Query</div><div class="fa">&rarr;</div>
    <div class="fs a">Embed Query (Gemini)</div><div class="fa">&rarr;</div>
    <div class="fs">Hybrid Retrieval (Pinecone + Neo4j)</div><div class="fa">&rarr;</div>
    <div class="fs a">LLM Synthesis (Groq Llama-3.3-70b)</div><div class="fa">&rarr;</div>
    <div class="fs">Stream via SSE</div>
  </div>
  <h3>Project Directory Structure</h3>
  <table>
    <thead><tr><th>Directory</th><th>Purpose</th><th>Key Files</th></tr></thead>
    <tbody>
      <tr><td><code>ai/agents/</code></td><td>Autonomous AI agents</td><td>copilot_agent.py, rca_agent.py, compliance_agent.py, report_agent.py</td></tr>
      <tr><td><code>ai/pipeline/</code></td><td>Document processing</td><td>chunkers.py, embedders.py, parsers.py</td></tr>
      <tr><td><code>ai/retrieval/</code></td><td>Hybrid search logic</td><td>vector_search.py, graph_search.py, hybrid.py</td></tr>
      <tr><td><code>ai/prompts/</code></td><td>LLM prompt templates</td><td>Centralized prompt management for all agents</td></tr>
      <tr><td><code>backend/app/api/v1/</code></td><td>FastAPI endpoints</td><td>auth, assets, documents, incidents, copilot, graph, compliance, rca, reports, maintenance, settings</td></tr>
      <tr><td><code>backend/app/models/</code></td><td>Beanie ODM models</td><td>User, Asset, Incident, Document, Maintenance, Report, AuditLog</td></tr>
      <tr><td><code>backend/app/services/</code></td><td>Business logic</td><td>auth_service.py, document_service.py, copilot_service.py</td></tr>
      <tr><td><code>frontend/src/pages/</code></td><td>Application views</td><td>Dashboard, Assets, Documents, Incidents, Maintenance, Compliance, KnowledgeGraph, Reports, Settings</td></tr>
      <tr><td><code>frontend/src/components/</code></td><td>Reusable UI</td><td>CopilotWidget.tsx, Layout.tsx, charts, cards</td></tr>
      <tr><td><code>worker/tasks/</code></td><td>Celery background jobs</td><td>document_tasks.py, report_tasks.py</td></tr>
    </tbody>
  </table>
</div>

<!-- SEC 4 -->
<div class="sec pb">
  <div class="sec-hd"><div class="sec-n">4</div><h2>AI Engine &mdash; Agents &amp; Core Intelligence</h2></div>
  <h3>Multi-Agent Architecture (LangGraph)</h3>
  <p>The AI engine uses <strong>LangGraph</strong> for complex multi-step agentic workflows with state management, conditional routing, and tool-use capabilities. Four specialized agents work together:</p>

  <h4>Agent 1: Expert Knowledge Copilot</h4>
  <div class="card" style="margin-bottom:10px;">
    <p><strong>Model:</strong> Groq Llama-3.3-70b-versatile (primary) &nbsp;|&nbsp; Google Gemini 2.5 Flash (fallback)</p>
    <p><strong>Retrieval:</strong> Hybrid RAG &mdash; Pinecone semantic search + Neo4j graph traversal for relationship-aware context</p>
    <p><strong>Output:</strong> Streamed via Server-Sent Events (SSE) for real-time token-by-token display</p>
    <p><strong>Capabilities:</strong> Source citation, multi-turn conversation, context-aware follow-ups, markdown-formatted answers</p>
  </div>

  <h4>Agent 2: Root Cause Analysis (RCA) Agent</h4>
  <div class="card" style="margin-bottom:10px;">
    <p><strong>Process:</strong> Ingests incident + asset history &rarr; retrieves similar past incidents from knowledge graph &rarr; synthesises probable root causes &rarr; generates structured RCA report.</p>
    <p><strong>Output:</strong> Structured report with timeline, causal chain, immediate corrective actions, preventive recommendations.</p>
  </div>

  <h4>Agent 3: Compliance Intelligence Agent</h4>
  <div class="card" style="margin-bottom:10px;">
    <p><strong>Frameworks:</strong> Factory Act, OISD standards, PESO regulations, environmental norms, ISO quality standards.</p>
    <p><strong>Output:</strong> Compliance gap report, audit evidence packages, automated deviations flagging.</p>
  </div>

  <h4>Agent 4: Report Generation Agent</h4>
  <div class="card" style="margin-bottom:10px;">
    <p><strong>Process:</strong> Runs asynchronously via Celery &rarr; pulls data from MongoDB &rarr; synthesises narrative + metrics &rarr; returns structured report document.</p>
    <p><strong>Supports:</strong> Maintenance summaries, operational digests, inspection reports, compliance evidence packages.</p>
  </div>

  <h3>Hybrid RAG Engine</h3>
  <table>
    <thead><tr><th>Strategy</th><th>Technology</th><th>Strength</th><th>Example Query</th></tr></thead>
    <tbody>
      <tr><td><strong>Vector Semantic Search</strong></td><td>Pinecone + Gemini Embeddings (768-dim)</td><td>Finds semantically similar content even with different phrasing</td><td>"What does the manual say about pump overheating?"</td></tr>
      <tr><td><strong>Knowledge Graph Traversal</strong></td><td>Neo4j + Cypher Queries</td><td>Follows entity relationships (Asset &rarr; Incidents &rarr; Root Causes)</td><td>"Show all failures linked to compressor C-202 in the last 6 months"</td></tr>
    </tbody>
  </table>

  <h3>LLM Provider Strategy (Provider-Agnostic Factory)</h3>
  <div class="grid3">
    <div class="ab blue"><h4>Primary: Groq</h4><p>Llama-3.3-70b-versatile. Ultra-fast inference via Groq custom silicon. Default for all copilot interactions.</p></div>
    <div class="ab green"><h4>Embeddings: Gemini</h4><p>models/gemini-embedding-001. 768-dimensional embeddings for semantic search and document indexing.</p></div>
    <div class="ab purple"><h4>Fallback: Gemini Flash</h4><p>gemini-2.5-flash. Auto-used if Groq rate limits are hit or for specific long-context tasks.</p></div>
  </div>

  <h3>Document Processing Pipeline (Celery Async)</h3>
  <table>
    <thead><tr><th>Format</th><th>Parser</th><th>Capabilities</th></tr></thead>
    <tbody>
      <tr><td><strong>PDF</strong></td><td>PyMuPDF</td><td>Text extraction, table extraction, image extraction, P&amp;ID parsing support</td></tr>
      <tr><td><strong>Scanned PDF / Images</strong></td><td>pytesseract (OCR)</td><td>Full optical character recognition, handwritten note extraction</td></tr>
      <tr><td><strong>DOCX / Word</strong></td><td>python-docx</td><td>Full text, tables, headers, styled content, metadata</td></tr>
      <tr><td><strong>XLSX / Excel</strong></td><td>openpyxl</td><td>Structured data extraction, table parsing, formula results</td></tr>
    </tbody>
  </table>
</div>

<!-- SEC 5 -->
<div class="sec pb">
  <div class="sec-hd"><div class="sec-n">5</div><h2>Backend &mdash; FastAPI Service &amp; API Reference</h2></div>
  <p>Production-ready <strong>FastAPI</strong> application with full async support, JWT authentication, RBAC, and 12+ API modules.</p>

  <h4>&#128272; Authentication &mdash; /api/v1/auth</h4>
  <div class="ep"><div class="m post">POST</div><div class="path">/auth/register</div><span style="color:#64748b"> &mdash; Register new user (email, password, role, full_name)</span></div>
  <div class="ep"><div class="m post">POST</div><div class="path">/auth/login</div><span style="color:#64748b"> &mdash; Login &amp; receive JWT access + refresh tokens</span></div>
  <div class="ep"><div class="m post">POST</div><div class="path">/auth/refresh</div><span style="color:#64748b"> &mdash; Refresh an expired access token</span></div>
  <div class="ep"><div class="m get">GET</div><div class="path">/auth/me</div><span style="color:#64748b"> &mdash; Get current authenticated user profile</span></div>
  <div class="ep"><div class="m post">POST</div><div class="path">/auth/forgot-password</div><span style="color:#64748b"> &mdash; Initiate password reset flow</span></div>
  <div class="ep"><div class="m post">POST</div><div class="path">/auth/reset-password</div><span style="color:#64748b"> &mdash; Complete reset with token</span></div>

  <h4>&#128230; Assets &mdash; /api/v1/assets</h4>
  <div class="ep"><div class="m get">GET</div><div class="path">/assets</div><span style="color:#64748b"> &mdash; List assets (paginated, filterable by status/type/location)</span></div>
  <div class="ep"><div class="m post">POST</div><div class="path">/assets</div><span style="color:#64748b"> &mdash; Create new asset record</span></div>
  <div class="ep"><div class="m get">GET</div><div class="path">/assets/{id}</div><span style="color:#64748b"> &mdash; Get single asset by ID</span></div>
  <div class="ep"><div class="m put">PUT</div><div class="path">/assets/{id}</div><span style="color:#64748b"> &mdash; Update asset details or status</span></div>
  <div class="ep"><div class="m del">DEL</div><div class="path">/assets/{id}</div><span style="color:#64748b"> &mdash; Delete asset record</span></div>

  <h4>&#128196; Documents &mdash; /api/v1/documents</h4>
  <div class="ep"><div class="m post">POST</div><div class="path">/documents/upload</div><span style="color:#64748b"> &mdash; Upload file and trigger async Celery processing pipeline</span></div>
  <div class="ep"><div class="m get">GET</div><div class="path">/documents</div><span style="color:#64748b"> &mdash; List all indexed documents</span></div>
  <div class="ep"><div class="m get">GET</div><div class="path">/documents/{id}</div><span style="color:#64748b"> &mdash; Get metadata and processing status</span></div>
  <div class="ep"><div class="m del">DEL</div><div class="path">/documents/{id}</div><span style="color:#64748b"> &mdash; Delete and remove from vector index</span></div>

  <h4>&#128680; Incidents &mdash; /api/v1/incidents</h4>
  <div class="ep"><div class="m post">POST</div><div class="path">/incidents</div><span style="color:#64748b"> &mdash; Create new incident report</span></div>
  <div class="ep"><div class="m get">GET</div><div class="path">/incidents</div><span style="color:#64748b"> &mdash; List incidents (filterable by severity, status, asset)</span></div>
  <div class="ep"><div class="m put">PUT</div><div class="path">/incidents/{id}</div><span style="color:#64748b"> &mdash; Update incident status or details</span></div>

  <h4>&#129302; AI Copilot &mdash; /api/v1/copilot</h4>
  <div class="ep"><div class="m post">POST</div><div class="path">/copilot/chat/stream</div><span style="color:#64748b"> &mdash; Stream AI response via SSE (real-time token-by-token output)</span></div>
  <div class="ep"><div class="m post">POST</div><div class="path">/copilot/chat</div><span style="color:#64748b"> &mdash; Standard non-streaming AI query endpoint</span></div>

  <h4>Additional API Modules</h4>
  <table>
    <thead><tr><th>Module</th><th>Prefix</th><th>Purpose</th></tr></thead>
    <tbody>
      <tr><td>Knowledge Graph</td><td>/api/v1/graph</td><td>Query Neo4j, get entity relationships, visualise graph data</td></tr>
      <tr><td>Compliance</td><td>/api/v1/compliance</td><td>Compliance status, gap analysis, regulatory mapping</td></tr>
      <tr><td>Root Cause Analysis</td><td>/api/v1/rca</td><td>Trigger RCA agent for an incident, retrieve structured reports</td></tr>
      <tr><td>Maintenance</td><td>/api/v1/maintenance</td><td>CRUD for maintenance schedules and work orders</td></tr>
      <tr><td>Reports</td><td>/api/v1/reports</td><td>Generate, list, and download AI-generated operational reports</td></tr>
      <tr><td>Dashboard</td><td>/api/v1/dashboard</td><td>Aggregated KPI data for role-specific dashboards</td></tr>
      <tr><td>Settings</td><td>/api/v1/settings</td><td>User profile, notification preferences, AI provider config</td></tr>
      <tr><td>Inspections</td><td>/api/v1/inspections</td><td>Inspection records, schedules, and findings</td></tr>
      <tr><td>Health</td><td>/health</td><td>Service health check for deployment monitoring</td></tr>
    </tbody>
  </table>

  <h3>Security &amp; Middleware Stack</h3>
  <ul>
    <li><strong>JWT Auth:</strong> Access tokens (30 min) + Refresh tokens (7 days) via python-jose / HS256</li>
    <li><strong>Password Security:</strong> bcrypt hashing via passlib</li>
    <li><strong>CORS Middleware:</strong> Configurable allowed origins for Vercel frontend</li>
    <li><strong>Role Guards:</strong> FastAPI Depends() pattern checks user role on every protected endpoint</li>
    <li><strong>Pydantic v2:</strong> All request/response bodies strictly validated and serialised</li>
    <li><strong>Structured Logging:</strong> structlog for production-grade, JSON-formatted audit logs</li>
  </ul>
</div>

<!-- SEC 6 -->
<div class="sec pb">
  <div class="sec-hd"><div class="sec-n">6</div><h2>Frontend &mdash; User Interface &amp; Dashboards</h2></div>
  <p>Premium React 19 single-page application with dark-mode glassmorphism, micro-animations, and role-adaptive views.</p>

  <h3>Application Pages</h3>
  <table>
    <thead><tr><th>Page</th><th>Route</th><th>Description</th></tr></thead>
    <tbody>
      <tr><td><strong>Auth</strong></td><td>/login, /signup</td><td>Sign In / Sign Up with email or Google demo. Role selector, forgot password, JWT session.</td></tr>
      <tr><td><strong>Dashboard</strong></td><td>/</td><td>Role-specific KPI overview with Recharts visualisations. Unique views per role.</td></tr>
      <tr><td><strong>Assets</strong></td><td>/assets</td><td>Equipment registry with status (Operational/Warning/Critical/Offline), filtering, CRUD.</td></tr>
      <tr><td><strong>Documents</strong></td><td>/documents</td><td>Drag-and-drop file upload, processing status tracker, indexed document browser.</td></tr>
      <tr><td><strong>Incidents</strong></td><td>/incidents</td><td>Log incidents, set severity, track resolution, trigger RCA from within the incident.</td></tr>
      <tr><td><strong>Maintenance</strong></td><td>/maintenance</td><td>Work order management, predictive scheduling, equipment health tracking.</td></tr>
      <tr><td><strong>Knowledge Graph</strong></td><td>/knowledge-graph</td><td>Interactive pannable/zoomable graph (ReactFlow) visualising Neo4j entity relationships.</td></tr>
      <tr><td><strong>Compliance</strong></td><td>/compliance</td><td>Regulatory compliance dashboard, gap analysis, audit evidence packages.</td></tr>
      <tr><td><strong>Reports</strong></td><td>/reports</td><td>AI-generated report library, generation triggers, download centre.</td></tr>
      <tr><td><strong>Settings</strong></td><td>/settings</td><td>User profile, notification preferences, AI provider configuration.</td></tr>
    </tbody>
  </table>

  <h3>AI Copilot Widget</h3>
  <p>Persistent, resizable chat panel available on <strong>every page</strong> without navigating away:</p>
  <ul>
    <li><strong>Always Available:</strong> Floating icon opens the panel from any page in the application</li>
    <li><strong>Resizable:</strong> Drag handle allows resizing between 300px and 80% of window width</li>
    <li><strong>Real-time Streaming:</strong> Token-by-token response via SSE for instant, interactive feel</li>
    <li><strong>Markdown Rendering:</strong> react-markdown with code blocks, tables, and lists</li>
    <li><strong>Auth-secured:</strong> Uses JWT access token from Zustand global auth store</li>
  </ul>

  <h3>Design System</h3>
  <div class="grid2">
    <div class="card"><h4>&#127912; Visual Design</h4><p>Dark-mode first with glassmorphism effects, gradient accents, premium slate/blue/orange palette. Tailwind CSS for utility-first styling.</p></div>
    <div class="card"><h4>&#9889; Micro-animations</h4><p>Hover effects, smooth transitions, loading skeletons, entrance animations on every interactive element for a premium feel.</p></div>
    <div class="card"><h4>&#128241; Responsive Layout</h4><p>Collapsible sidebar navigation, fluid grids, mobile-friendly layout for field technicians on tablets and phones.</p></div>
    <div class="card"><h4>&#128276; Real-time Feedback</h4><p>React-hot-toast notifications for all user actions. Axios interceptor auto-refreshes expired JWT tokens transparently.</p></div>
  </div>
</div>

<!-- SEC 7 -->
<div class="sec pb">
  <div class="sec-hd"><div class="sec-n">7</div><h2>Database Architecture (Polyglot Persistence)</h2></div>
  <p>Each database is chosen specifically for what it does best &mdash; a <strong>polyglot persistence</strong> strategy:</p>

  <h3>&#127823; MongoDB Atlas &mdash; Primary Document Store</h3>
  <div class="info"><p><strong>ODM:</strong> Beanie (async) built on Motor &nbsp;|&nbsp; <strong>Cloud:</strong> MongoDB Atlas M0 Free Tier</p></div>
  <table>
    <thead><tr><th>Collection</th><th>Contents</th></tr></thead>
    <tbody>
      <tr><td>users</td><td>User accounts, roles, preferences, bcrypt-hashed passwords</td></tr>
      <tr><td>assets</td><td>Equipment registry &mdash; tag, type, location, status, specifications, history</td></tr>
      <tr><td>documents</td><td>Uploaded file metadata, Celery task ID, processing status, extracted content summary</td></tr>
      <tr><td>incidents</td><td>Incident records &mdash; description, severity, affected assets, timeline, resolution</td></tr>
      <tr><td>maintenance</td><td>Work orders, maintenance schedules, equipment history</td></tr>
      <tr><td>reports</td><td>Generated report metadata, content, S3/storage links</td></tr>
      <tr><td>audit_logs</td><td>All user actions and system events for compliance audit trails</td></tr>
    </tbody>
  </table>

  <h3>&#128309; Neo4j AuraDB &mdash; Knowledge Graph</h3>
  <div class="info"><p><strong>Driver:</strong> neo4j-driver (Python) &nbsp;|&nbsp; <strong>Cloud:</strong> Neo4j AuraDB (Managed, TLS-encrypted)</p></div>
  <ul>
    <li><strong>Nodes:</strong> Equipment, Procedure, Regulation, Personnel, Document, Incident, Component</li>
    <li><strong>Relationships:</strong> MAINTAINS, REFERENCES, CAUSED_BY, AFFECTS, DEFINED_IN, OPERATED_BY</li>
    <li><strong>Power:</strong> "Find all regulations referenced in any procedure that applies to pump P-101" &mdash; a single Cypher query traverses 3 relationship levels instantly</li>
  </ul>

  <h3>&#128204; Pinecone Cloud &mdash; Vector Database</h3>
  <div class="info"><p><strong>Embeddings:</strong> Google Gemini (models/gemini-embedding-001) &mdash; 768 dimensions &nbsp;|&nbsp; <strong>Latency:</strong> &lt;100ms top-k retrieval</p></div>
  <ul>
    <li>Each chunk stored with metadata: document_id, page_number, asset_tag, document_type</li>
    <li>Namespace separation for different document types (manuals, incidents, procedures, regulations)</li>
  </ul>

  <h3>&#9889; Upstash Redis &mdash; Cache &amp; Message Broker</h3>
  <div class="info"><p><strong>Protocol:</strong> rediss:// (TLS-encrypted, serverless Redis) &nbsp;|&nbsp; <strong>Provider:</strong> Upstash</p></div>
  <ul>
    <li><strong>Celery Broker:</strong> Queues document processing and report generation tasks</li>
    <li><strong>Celery Backend:</strong> Stores task results and status for progress polling</li>
    <li><strong>Session Cache:</strong> Reduces MongoDB load for frequently-accessed data</li>
  </ul>
</div>

<!-- SEC 8 -->
<div class="sec pb">
  <div class="sec-hd"><div class="sec-n">8</div><h2>Role-Based Access Control (RBAC)</h2></div>
  <p>A <strong>4-tier role hierarchy</strong> with tailored dashboard experiences for different operational personas:</p>
  <div class="grid4">
    <div class="role-card admin"><div style="font-size:22px;margin-bottom:7px;">&#128081;</div><h4>Admin</h4><p>Full system access. User management, system config, compliance oversight, AI settings.</p></div>
    <div class="role-card eng"><div style="font-size:22px;margin-bottom:7px;">&#9881;&#65039;</div><h4>Engineer</h4><p>Technical ops. Asset management, document ingestion, RCA, maintenance planning, knowledge graph.</p></div>
    <div class="role-card op"><div style="font-size:22px;margin-bottom:7px;">&#128295;</div><h4>Operator</h4><p>Day-to-day ops. Incident reporting, work order execution, copilot queries, inspection records.</p></div>
    <div class="role-card view"><div style="font-size:22px;margin-bottom:7px;">&#128065;&#65039;</div><h4>Viewer</h4><p>Read-only. Dashboard KPIs, report viewing, copilot queries. No write permissions.</p></div>
  </div>

  <h3>Permission Matrix</h3>
  <table>
    <thead><tr><th>Feature</th><th>Admin</th><th>Engineer</th><th>Operator</th><th>Viewer</th></tr></thead>
    <tbody>
      <tr><td>View Dashboard &amp; KPIs</td><td>&#9989;</td><td>&#9989;</td><td>&#9989;</td><td>&#9989;</td></tr>
      <tr><td>AI Copilot Chat</td><td>&#9989;</td><td>&#9989;</td><td>&#9989;</td><td>&#9989;</td></tr>
      <tr><td>Log Incidents</td><td>&#9989;</td><td>&#9989;</td><td>&#9989;</td><td>&#10060;</td></tr>
      <tr><td>Upload Documents</td><td>&#9989;</td><td>&#9989;</td><td>&#10060;</td><td>&#10060;</td></tr>
      <tr><td>Asset Management (CRUD)</td><td>&#9989;</td><td>&#9989;</td><td>&#10060;</td><td>&#10060;</td></tr>
      <tr><td>Trigger RCA / AI Analysis</td><td>&#9989;</td><td>&#9989;</td><td>&#10060;</td><td>&#10060;</td></tr>
      <tr><td>Generate Reports</td><td>&#9989;</td><td>&#9989;</td><td>&#9989;</td><td>&#10060;</td></tr>
      <tr><td>Compliance Management</td><td>&#9989;</td><td>&#9989;</td><td>&#10060;</td><td>&#10060;</td></tr>
      <tr><td>User Management</td><td>&#9989;</td><td>&#10060;</td><td>&#10060;</td><td>&#10060;</td></tr>
      <tr><td>System Settings &amp; AI Config</td><td>&#9989;</td><td>&#10060;</td><td>&#10060;</td><td>&#10060;</td></tr>
    </tbody>
  </table>
</div>

<!-- SEC 9 -->
<div class="sec pb">
  <div class="sec-hd"><div class="sec-n">9</div><h2>Key Features Deep Dive</h2></div>

  <h3>1. Hybrid RAG &mdash; The Core Differentiator</h3>
  <p>When you ask "What caused the last major failure of compressor C-202?", the system simultaneously:</p>
  <ol>
    <li>Runs a <strong>vector search</strong> in Pinecone to find semantically similar documents (OEM manuals, inspection reports, maintenance records)</li>
    <li>Traverses the <strong>Neo4j knowledge graph</strong> starting from the C-202 node, following CAUSED_BY and AFFECTS relationships</li>
    <li>Fuses both result sets, ranks by relevance, feeds to Groq LLM for final synthesis</li>
  </ol>
  <p>This delivers dramatically more accurate, relationship-aware answers than either method alone.</p>

  <h3>2. Real-time AI Streaming via SSE</h3>
  <p>The AI Copilot uses <strong>Server-Sent Events (SSE)</strong> to stream responses token-by-token &mdash; identical to how ChatGPT works. Technical stack: FastAPI's <code>sse-starlette</code> + React's native <code>EventSource</code> API + immutable Zustand state updates to prevent React Strict Mode duplication.</p>

  <h3>3. Asynchronous Document Processing (Celery)</h3>
  <p>Document ingestion runs via <strong>Celery workers</strong> on Redis, enabling non-blocking uploads. OCR of large scanned PDFs (30&ndash;60 seconds) runs in the background without blocking the API server. The frontend polls the task status endpoint to show real-time progress indicators.</p>

  <h3>4. Interactive Knowledge Graph Visualisation</h3>
  <p>The Knowledge Graph page uses <strong>ReactFlow</strong> to render an interactive, pannable, zoomable graph of all entity relationships extracted from ingested documents. Engineers can visually explore how equipment, procedures, personnel, and regulations are interconnected.</p>

  <h3>5. Automated Root Cause Analysis</h3>
  <p>When an engineer clicks "Analyse" on an incident, the RCA Agent:</p>
  <ol>
    <li>Retrieves incident description and all associated asset metadata</li>
    <li>Searches knowledge graph for similar historical incidents on same/similar equipment</li>
    <li>Retrieves relevant OEM manual sections via vector search</li>
    <li>Synthesises structured report: Probable Root Causes (ranked by confidence), Contributing Factors, Immediate Corrective Actions, Long-term Preventive Recommendations</li>
  </ol>
</div>

<!-- SEC 10 -->
<div class="sec pb">
  <div class="sec-hd"><div class="sec-n">10</div><h2>Full Technology Stack</h2></div>
  <table>
    <thead><tr><th>Layer</th><th>Technology</th><th>Version</th><th>Purpose</th></tr></thead>
    <tbody>
      <tr><td rowspan="6"><strong>Frontend</strong></td><td>React</td><td>19.2.x</td><td>UI component library</td></tr>
      <tr><td>TypeScript</td><td>5.x</td><td>Type safety across the codebase</td></tr>
      <tr><td>Vite</td><td>6.x</td><td>Build tool and HMR dev server</td></tr>
      <tr><td>Tailwind CSS</td><td>3.x</td><td>Utility-first styling and dark mode</td></tr>
      <tr><td>Zustand</td><td>5.x</td><td>Lightweight global state management</td></tr>
      <tr><td>ReactFlow</td><td>11.x</td><td>Interactive knowledge graph visualisation</td></tr>
      <tr><td rowspan="6"><strong>Backend</strong></td><td>FastAPI</td><td>0.115+</td><td>Python async web framework</td></tr>
      <tr><td>Pydantic v2</td><td>2.7+</td><td>Data validation and serialisation</td></tr>
      <tr><td>Beanie</td><td>2.0+</td><td>MongoDB async ODM (built on Motor)</td></tr>
      <tr><td>python-jose</td><td>3.3+</td><td>JWT token creation and validation</td></tr>
      <tr><td>Celery</td><td>5.4+</td><td>Async task queue for background jobs</td></tr>
      <tr><td>uvicorn</td><td>0.30+</td><td>ASGI server for production deployment</td></tr>
      <tr><td rowspan="4"><strong>AI / LLM</strong></td><td>LangChain</td><td>0.3+</td><td>LLM orchestration framework</td></tr>
      <tr><td>LangGraph</td><td>0.2+</td><td>Multi-agent workflow state machine</td></tr>
      <tr><td>Groq (Llama-3.3-70b)</td><td>Latest</td><td>Primary LLM for generation and chat</td></tr>
      <tr><td>Google Gemini</td><td>gemini-2.5-flash</td><td>Embeddings (768-dim) + LLM fallback</td></tr>
      <tr><td rowspan="4"><strong>Databases</strong></td><td>MongoDB Atlas</td><td>7.x</td><td>Primary document store (cloud managed)</td></tr>
      <tr><td>Neo4j AuraDB</td><td>5.x</td><td>Knowledge graph (cloud managed)</td></tr>
      <tr><td>Pinecone</td><td>v3 API</td><td>Vector database for semantic search</td></tr>
      <tr><td>Redis (Upstash)</td><td>7.x</td><td>Cache and Celery message broker</td></tr>
      <tr><td rowspan="4"><strong>Doc Processing</strong></td><td>PyMuPDF</td><td>1.24+</td><td>PDF parsing and extraction</td></tr>
      <tr><td>pytesseract</td><td>0.3+</td><td>OCR for scanned documents and images</td></tr>
      <tr><td>python-docx</td><td>1.1+</td><td>Word document processing</td></tr>
      <tr><td>openpyxl</td><td>3.1+</td><td>Excel/spreadsheet file processing</td></tr>
      <tr><td rowspan="2"><strong>Deployment</strong></td><td>Vercel</td><td>&mdash;</td><td>Frontend hosting, CDN, auto-deploy from GitHub</td></tr>
      <tr><td>Render</td><td>&mdash;</td><td>Backend Python web service hosting</td></tr>
    </tbody>
  </table>
</div>

<!-- SEC 11 -->
<div class="sec pb">
  <div class="sec-hd"><div class="sec-n">11</div><h2>Deployment Architecture</h2></div>
  <div class="grid3">
    <div class="ab blue"><h4>&#127760; Vercel (Frontend)</h4><p>ops-pilot-hjur.vercel.app<br/>Auto-deploys on GitHub push. Global CDN. React SPA with vercel.json routing rewrites.</p></div>
    <div class="ab green"><h4>&#9881;&#65039; Render (Backend)</h4><p>opspilot-1-bwho.onrender.com<br/>Python web service. Uvicorn ASGI. Auto-deploys from GitHub main branch.</p></div>
    <div class="ab purple"><h4>&#127823; MongoDB Atlas</h4><p>Cloud-managed. M0 free tier. Replica sets, automatic backups, connection pooling.</p></div>
    <div class="ab orange"><h4>&#128309; Neo4j AuraDB</h4><p>Managed cloud Neo4j. TLS-encrypted bolt+s:// connection. Knowledge graph storage.</p></div>
    <div class="ab teal"><h4>&#128204; Pinecone Cloud</h4><p>Managed vector DB. opspilot index. Gemini 768-dim embeddings. Sub-100ms queries.</p></div>
    <div class="ab slate"><h4>&#9889; Upstash Redis</h4><p>Serverless Redis. TLS-encrypted rediss://. Celery broker + backend for async tasks.</p></div>
  </div>

  <h3>CI/CD Pipeline</h3>
  <div class="flow">
    <div class="fs">Git Push to GitHub</div><div class="fa">&rarr;</div>
    <div class="fs a">Vercel detects frontend change</div><div class="fa">&rarr;</div>
    <div class="fs">npm install + vite build</div><div class="fa">&rarr;</div>
    <div class="fs a">Deploy to Global CDN (~2 min)</div>
  </div>
  <div class="flow" style="margin-top:8px;">
    <div class="fs">Git Push to GitHub</div><div class="fa">&rarr;</div>
    <div class="fs a">Render detects backend change</div><div class="fa">&rarr;</div>
    <div class="fs">pip install + uvicorn start</div><div class="fa">&rarr;</div>
    <div class="fs a">Live in ~3-5 min</div>
  </div>

  <h3>Environment Variables Reference</h3>
  <table>
    <thead><tr><th>Service</th><th>Variable</th><th>Description</th></tr></thead>
    <tbody>
      <tr><td>Vercel</td><td>VITE_API_URL</td><td>Backend URL + /api/v1 (e.g., https://opspilot-1-bwho.onrender.com/api/v1)</td></tr>
      <tr><td>Render</td><td>MONGO_URI</td><td>MongoDB Atlas connection string with credentials</td></tr>
      <tr><td>Render</td><td>NEO4J_URI / NEO4J_USER / NEO4J_PASSWORD</td><td>Neo4j AuraDB connection credentials</td></tr>
      <tr><td>Render</td><td>PINECONE_API_KEY / PINECONE_INDEX_NAME</td><td>Pinecone cloud credentials</td></tr>
      <tr><td>Render</td><td>REDIS_URL</td><td>Upstash TLS Redis connection string (rediss://)</td></tr>
      <tr><td>Render</td><td>GROQ_API_KEY / GROQ_MODEL</td><td>Groq LLM API key and model name</td></tr>
      <tr><td>Render</td><td>GOOGLE_API_KEY / GEMINI_MODEL / GEMINI_EMBEDDING_MODEL</td><td>Google AI credentials for embeddings</td></tr>
      <tr><td>Render</td><td>SECRET_KEY</td><td>JWT signing secret (64-char random string)</td></tr>
      <tr><td>Render</td><td>CORS_ORIGINS</td><td>["https://your-vercel-url.vercel.app"] &mdash; JSON array of allowed origins</td></tr>
      <tr><td>Render</td><td>APP_ENV / DEBUG</td><td>Set to "production" / "false" for live deployment</td></tr>
    </tbody>
  </table>
</div>

<!-- SEC 12 -->
<div class="sec pb">
  <div class="sec-hd"><div class="sec-n">12</div><h2>Alignment with Hackathon Requirements</h2></div>

  <h3>Suggested Technologies &mdash; Implementation Status</h3>
  <table>
    <thead><tr><th>Requirement</th><th>Status</th><th>Implementation</th></tr></thead>
    <tbody>
      <tr><td>RAG over heterogeneous industrial document corpora</td><td><span class="tag g">&#9989; Implemented</span></td><td>Hybrid RAG: Pinecone vector search + Neo4j graph traversal + LangChain orchestration</td></tr>
      <tr><td>Knowledge Graphs &amp; Industrial Ontology Engineering</td><td><span class="tag g">&#9989; Implemented</span></td><td>Neo4j AuraDB with entity extraction pipeline. Equipment, Procedure, Regulation, Personnel nodes.</td></tr>
      <tr><td>OCR &amp; Document Intelligence (structured + unstructured)</td><td><span class="tag g">&#9989; Implemented</span></td><td>PyMuPDF + pytesseract OCR. Supports PDF, scanned images, DOCX, XLSX.</td></tr>
      <tr><td>Agentic AI for maintenance and compliance workflows</td><td><span class="tag g">&#9989; Implemented</span></td><td>LangGraph multi-agent: Copilot, RCA, Compliance, Report agents working in concert.</td></tr>
      <tr><td>Computer Vision (P&amp;ID parsing, drawing digitisation)</td><td><span class="tag o">&#128260; Partial</span></td><td>PDF image extraction + OCR layer in place. Full P&amp;ID-specific CV model is roadmap item.</td></tr>
      <tr><td>Quality Management System (QMS) Integration</td><td><span class="tag g">&#9989; Implemented</span></td><td>Compliance module with framework mapping, gap analysis, audit evidence generation.</td></tr>
    </tbody>
  </table>

  <h3>Expected Deliverables</h3>
  <table>
    <thead><tr><th>Deliverable</th><th>Status</th><th>Details</th></tr></thead>
    <tbody>
      <tr><td>Working Prototype</td><td><span class="tag g">&#9989; Live</span></td><td>Fully deployed on Vercel (frontend) + Render (backend). Real AI capabilities functional.</td></tr>
      <tr><td>Architecture Diagram</td><td><span class="tag g">&#9989; Included</span></td><td>Section 3 of this document covers full system architecture with flow diagrams.</td></tr>
      <tr><td>Presentation Deck</td><td><span class="tag g">&#9989; This Document</span></td><td>This comprehensive 12-section documentation serves as the detailed project write-up.</td></tr>
      <tr><td>Demo Video</td><td><span class="tag o">&#128249; Pending</span></td><td>Screen recording of the live application &mdash; to be submitted separately.</td></tr>
    </tbody>
  </table>

  <h3>What Makes OpsPilot Stand Out</h3>
  <div class="grid2">
    <div class="card"><h4>&#127981; True Industrial Focus</h4><p>Not a generic chatbot. Every feature is designed for industrial operations: asset lifecycle, work order management, regulatory compliance, P&amp;ID document support across the full operational domain.</p></div>
    <div class="card"><h4>&#128279; Hybrid Intelligence Engine</h4><p>The combination of vector semantic search AND knowledge graph relationship traversal delivers answers that neither method alone can provide &mdash; the true technical differentiator.</p></div>
    <div class="card"><h4>&#128101; Role-Aware Platform</h4><p>One platform serving 4 operational personas with tailored experiences &mdash; from the field operator on mobile to the compliance engineer to the plant administrator.</p></div>
    <div class="card"><h4>&#9729;&#65039; Production-Ready Deployment</h4><p>Fully deployed to cloud (not just a local demo) with CI/CD, environment management, JWT security, async task processing, structured logging, and CORS configuration.</p></div>
  </div>

  <div class="info" style="margin-top:24px;">
    <p>
      <strong>Repository:</strong> <a href="https://github.com/Arbind43/opsPilot" target="_blank">https://github.com/Arbind43/opsPilot</a><br/>
      <strong>Live Frontend:</strong> <a href="https://ops-pilot-hjur.vercel.app" target="_blank">https://ops-pilot-hjur.vercel.app</a><br/>
      <strong>Backend API:</strong> <a href="https://opspilot-1-bwho.onrender.com" target="_blank">https://opspilot-1-bwho.onrender.com</a><br/>
    <strong>Hackathon:</strong> ET AI Hackathon 2.0 &mdash; Problem Statement #8: AI for Industrial Knowledge Intelligence
    </p>
  </div>
</div>

</div><!-- /wrap -->

<footer>
  <div><strong>OpsPilot AI</strong> &mdash; Enterprise Knowledge Intelligence Platform<br/>ET AI Hackathon 2.0 &middot; Problem Statement #8 &middot; Team: Infinite Loop</div>
  <div style="text-align:right;"><strong><a href="https://github.com/Arbind43/opsPilot" target="_blank" style="color:inherit;">github.com/Arbind43/opsPilot</a></strong><br/>Confidential &middot; July 2026</div>
</footer>

<button class="fab" onclick="window.print()">&#128424;&#65039; Save as PDF</button>
</body>
</html>"""

with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    f.write(HTML)

print(f"Documentation generated successfully!")
print(f"File: {OUTPUT_PATH}")
print(f"Size: {len(HTML):,} bytes")
print(f"\nTo save as PDF: Open the file in Chrome and press Ctrl+P -> Save as PDF")
