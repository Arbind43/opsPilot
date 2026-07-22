# OpsPilot AI 🧠

**Enterprise Knowledge Intelligence Platform**

OpsPilot AI is an advanced, AI-powered knowledge management and operational intelligence platform designed for modern enterprises. It provides real-time insights, predictive resource management, and automated root-cause analysis (RCA) by leveraging a Hybrid RAG Engine (Vector Database + Knowledge Graph).

## 🌟 Key Features
- **Hybrid RAG Engine**: Combines the semantic search capabilities of Pinecone with the relationship mapping of Neo4j Knowledge Graphs for highly accurate AI responses.
- **Automated Root Cause Analysis (RCA)**: Instantly diagnose operational incidents and anomalies using LLM-driven forensic analysis.
- **Compliance Intelligence**: Automated regulatory tracking and auditing workflows to ensure continuous compliance.
- **Predictive Resource Intelligence**: Anticipate maintenance needs and optimize resource allocation across your domain.
- **Role-Based Access Control (RBAC)**: Tailored dashboard experiences for Admins, Engineers, Operators, and Viewers.
- **Sleek, Modern UI**: A premium, responsive interface featuring glassmorphism and micro-animations for an unparalleled user experience.

## 🏗️ Architecture Stack
- **Frontend**: React 18, TypeScript, Vite, Tailwind CSS, Lucide Icons, Zustand (State Management).
- **Backend**: FastAPI (Python), Beanie (ODM), Celery (Background Workers).
- **AI Core**: LangChain, OpenAI/Google APIs, custom multi-agent architecture.
- **Databases**: 
  - MongoDB (Document Store)
  - Neo4j (Knowledge Graph)
  - Pinecone (Vector Database)
  - Redis (Caching & Celery Broker)

## 📁 Project Structure

The repository is modularized into distinct domains to ensure scalability and separation of concerns:

```text
opspilot/
├── ai/                     # Core AI Engine
│   ├── agents/             # Autonomous AI agents (RCA, Compliance, Reports)
│   ├── pipeline/           # Data processing (Chunkers, Embedders, Parsers)
│   ├── retrieval/          # Hybrid search logic (Vector Search + Graph Search)
│   └── prompts/            # Centralized LLM prompt templates
├── backend/                # FastAPI Backend Service
│   ├── app/
│   │   ├── api/v1/         # API endpoints (Auth, Incidents, Copilot, etc.)
│   │   ├── core/           # Security, middleware, and config
│   │   ├── db/             # Database session and clients (Mongo, Neo4j, Pinecone)
│   │   ├── models/         # Beanie ODM database models
│   │   ├── schemas/        # Pydantic validation schemas
│   │   └── services/       # Core business logic
├── frontend/               # React + Vite Frontend
│   ├── src/
│   │   ├── assets/         # Images, fonts, and static SVGs
│   │   ├── components/     # Reusable UI components (Buttons, Inputs, Cards)
│   │   ├── pages/          # Application views (Dashboard, Incidents, Settings, etc.)
│   │   ├── store/          # Zustand global state management
│   │   └── lib/            # Utilities, API client configuration, RBAC helpers
└── worker/                 # Celery Background Workers
    └── tasks/              # Long-running tasks (Document processing, Report gen)
```

## 🚀 Getting Started

### Prerequisites
Make sure you have the following installed on your machine:
- Node.js (v18+)
- Python (3.10+)

Before running locally, ensure you have set up your `.env` file with connections to MongoDB, Neo4j, Pinecone, and Redis instances.

### 1. Start the Backend (FastAPI)
Navigate to the `backend` directory, install dependencies, and start the server:
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # On Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### 2. Start the Frontend (React)
Open a new terminal, navigate to the `frontend` directory, install dependencies, and start the Vite dev server:
```bash
cd frontend
npm install
npm run dev
```

### 3. Access the Application
- **Web App**:  https://ops-pilot-hjur.vercel.app
- **Backend API Docs (Swagger)**: https://opspilot-1-bwho.onrender.com

## 🔐 Authentication
OpsPilot supports a seamless authentication experience. You can:
1. **Sign up with Email/Password** and select a specific role (Admin, Engineer, Operator, Viewer).
2. **Sign in with Google** for a frictionless login that automatically provisions an admin demo account.

## 🛠️ Development & Contribution
- Follow standard Git workflow (branch, commit, push, PR).
- The `ai` directory contains modular components; to add a new AI skill, add an agent to `ai/agents`.
- Frontend styling heavily relies on `tailwind.config.js` for design tokens.

---
*Built for the ET AI Hackathon.*
