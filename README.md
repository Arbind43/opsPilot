# OpsPilot AI 🧠

**Enterprise Knowledge Intelligence Platform**

OpsPilot AI is an advanced, AI-powered knowledge management and operational intelligence platform designed for modern enterprises. It provides real-time insights, predictive resource management, and automated root-cause analysis (RCA) by leveraging a Hybrid RAG Engine (Vector Database + Knowledge Graph).

## 🌟 Key Features
- **Hybrid RAG Engine**: Combines the semantic search capabilities of ChromaDB with the relationship mapping of Neo4j Knowledge Graphs for highly accurate AI responses.
- **Automated Root Cause Analysis (RCA)**: Instantly diagnose operational incidents and anomalies using LLM-driven forensic analysis.
- **Compliance Intelligence**: Automated regulatory tracking and auditing workflows to ensure continuous compliance.
- **Predictive Resource Intelligence**: Anticipate maintenance needs and optimize resource allocation across your domain.
- **Role-Based Access Control (RBAC)**: Tailored dashboard experiences for Admins, Engineers, Operators, and Viewers.
- **Sleek, Modern UI**: A premium, responsive interface featuring glassmorphism and micro-animations for an unparalleled user experience.

## 🏗️ Architecture Stack
- **Frontend**: React 18, TypeScript, Vite, Tailwind CSS, Lucide Icons, Zustand (State Management).
- **Backend**: FastAPI (Python), SQLAlchemy (ORM), Celery (Background Workers).
- **Databases**: 
  - PostgreSQL (Relational Data)
  - Neo4j (Knowledge Graph)
  - ChromaDB (Vector Database)
  - Redis (Caching & Celery Broker)

## 🚀 Getting Started

### Prerequisites
Make sure you have the following installed on your machine:
- Node.js (v18+)
- Python (3.10+)
- Docker & Docker Compose (for spinning up databases)

### 1. Start the Infrastructure (Databases)
OpsPilot relies on several databases. You can spin them all up instantly using the provided Docker Compose file:
```bash
docker-compose -f docker-compose.dev.yml up -d
```
*This starts PostgreSQL, Neo4j, ChromaDB, and Redis.*

### 2. Start the Backend (FastAPI)
Navigate to the `backend` directory, install dependencies, and start the server:
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # On Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
```
*(Alternatively, you can run the `run_local.ps1` script if on Windows)*

### 3. Start the Frontend (React)
Open a new terminal, navigate to the `frontend` directory, install dependencies, and start the Vite dev server:
```bash
cd frontend
npm install
npm run dev
```

### 4. Access the Application
- **Web App**: http://localhost:5173
- **Backend API Docs (Swagger)**: http://localhost:8000/docs

## 🔐 Authentication
OpsPilot supports a seamless authentication experience. You can:
1. **Sign up with Email/Password** and select a specific role (Admin, Engineer, Operator, Viewer).
2. **Sign in with Google** for a frictionless login that automatically provisions an admin demo account.

---
*Built for the ET AI Hackathon.*
