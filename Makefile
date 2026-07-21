# ──────────────────────────────────────────────────────
# OpsPilot — Makefile
# ──────────────────────────────────────────────────────
# Quick commands for development workflow.
# ──────────────────────────────────────────────────────

.PHONY: help dev up down build logs clean migrate seed

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# ── Docker ───────────────────────────────────────────
dev: ## Start all services in development mode
	docker compose -f docker-compose.yml -f docker-compose.dev.yml up --build

up: ## Start all services in production mode
	docker compose up -d --build

down: ## Stop all services
	docker compose down

build: ## Build all containers
	docker compose build

logs: ## Tail logs for all services
	docker compose logs -f

clean: ## Remove all containers, volumes, and images
	docker compose down -v --rmi all

# ── Backend ──────────────────────────────────────────
migrate: ## Run database migrations
	docker compose exec backend alembic upgrade head

migrate-new: ## Create a new migration (usage: make migrate-new MSG="add users table")
	docker compose exec backend alembic revision --autogenerate -m "$(MSG)"

seed: ## Seed database with sample data
	docker compose exec backend python -m infrastructure.scripts.seed_data

# ── Frontend ─────────────────────────────────────────
fe-install: ## Install frontend dependencies
	cd frontend && npm install

fe-dev: ## Start frontend dev server (no Docker)
	cd frontend && npm run dev

fe-build: ## Build frontend for production
	cd frontend && npm run build

# ── Backend (local) ──────────────────────────────────
be-install: ## Install backend dependencies
	cd backend && pip install -e ".[dev]"

be-dev: ## Start backend dev server (no Docker)
	cd backend && uvicorn app.main:app --reload --port 8000
