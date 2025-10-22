# A.U.R.A (Adaptive User Retention Assistant) - Makefile
# This Makefile provides convenient commands for Docker operations,
# development workflow, and deployment tasks

.PHONY: help build up down dev logs clean test lint format install

# Default target
help: ## Show this help message
	@echo "A.U.R.A (Adaptive User Retention Assistant) - Available Commands:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# Docker Operations
build: ## Build all Docker images
	@echo "Building A.U.R.A Docker images..."
	docker-compose build

build-dev: ## Build development Docker images
	@echo "Building A.U.R.A development Docker images..."
	docker-compose -f docker-compose.dev.yml build

up: ## Start all services in production mode
	@echo "Starting A.U.R.A in production mode..."
	docker-compose up -d

up-dev: ## Start all services in development mode
	@echo "Starting A.U.R.A in development mode..."
	docker-compose -f docker-compose.dev.yml up -d

down: ## Stop all services
	@echo "Stopping A.U.R.A services..."
	docker-compose down
	docker-compose -f docker-compose.dev.yml down

restart: ## Restart all services
	@echo "Restarting A.U.R.A services..."
	docker-compose restart

restart-dev: ## Restart development services
	@echo "Restarting A.U.R.A development services..."
	docker-compose -f docker-compose.dev.yml restart

# Development Operations
dev: ## Start development environment with all tools
	@echo "Starting A.U.R.A development environment..."
	docker-compose -f docker-compose.dev.yml up -d
	@echo ""
	@echo "Development services started:"
	@echo "  - Streamlit Dashboard: http://localhost:8501"
	@echo "  - Jupyter Lab: http://localhost:8888 (token: aura-dev-token)"
	@echo "  - Redis: localhost:6379"
	@echo "  - PostgreSQL: localhost:5432"
	@echo ""
	@echo "To view logs: make logs-dev"

logs: ## Show logs for all services
	docker-compose logs -f

logs-dev: ## Show logs for development services
	docker-compose -f docker-compose.dev.yml logs -f

logs-app: ## Show logs for main application only
	docker-compose logs -f aura-app

logs-app-dev: ## Show logs for development application only
	docker-compose -f docker-compose.dev.yml logs -f aura-app-dev

# Database Operations
db-init: ## Initialize database with sample data
	@echo "Initializing database with sample data..."
	docker-compose -f docker-compose.dev.yml exec postgres-dev psql -U aura_dev_user -d aura_dev_db -f /docker-entrypoint-initdb.d/init-dev.sql
	docker-compose -f docker-compose.dev.yml exec postgres-dev psql -U aura_dev_user -d aura_dev_db -f /docker-entrypoint-initdb.d/sample-data.sql

db-reset: ## Reset database (WARNING: This will delete all data)
	@echo "Resetting database..."
	docker-compose -f docker-compose.dev.yml down -v
	docker-compose -f docker-compose.dev.yml up -d postgres-dev
	sleep 10
	$(MAKE) db-init

db-shell: ## Connect to database shell
	docker-compose -f docker-compose.dev.yml exec postgres-dev psql -U aura_dev_user -d aura_dev_db

# Testing and Quality Assurance
test: ## Run all tests
	@echo "Running A.U.R.A tests..."
	docker-compose -f docker-compose.dev.yml exec aura-app-dev python -m pytest src/tests/ -v

test-unit: ## Run unit tests only
	@echo "Running unit tests..."
	docker-compose -f docker-compose.dev.yml exec aura-app-dev python -m pytest src/tests/unit/ -v

test-integration: ## Run integration tests only
	@echo "Running integration tests..."
	docker-compose -f docker-compose.dev.yml exec aura-app-dev python -m pytest src/tests/integration/ -v

lint: ## Run linting checks
	@echo "Running linting checks..."
	docker-compose -f docker-compose.dev.yml exec aura-app-dev flake8 src/
	docker-compose -f docker-compose.dev.yml exec aura-app-dev black --check src/
	docker-compose -f docker-compose.dev.yml exec aura-app-dev mypy src/

format: ## Format code
	@echo "Formatting code..."
	docker-compose -f docker-compose.dev.yml exec aura-app-dev black src/
	docker-compose -f docker-compose.dev.yml exec aura-app-dev isort src/

# Data Pipeline Operations
data-pipeline: ## Run data pipeline processing
	@echo "Running data pipeline..."
	docker-compose -f docker-compose.dev.yml exec data-worker-dev python src/data_pipeline/orchestrator.py

data-reset: ## Reset all data (WARNING: This will delete all data)
	@echo "Resetting all data..."
	docker-compose -f docker-compose.dev.yml exec aura-app-dev rm -rf data/bronze/* data/silver/* data/gold/* data/temp/*
	docker-compose -f docker-compose.dev.yml exec aura-app-dev rm -rf models/* uploads/* logs/*

# Monitoring and Debugging
monitor: ## Start monitoring services (Prometheus + Grafana)
	@echo "Starting monitoring services..."
	docker-compose --profile monitoring up -d

monitor-stop: ## Stop monitoring services
	@echo "Stopping monitoring services..."
	docker-compose --profile monitoring down

shell: ## Open shell in main application container
	docker-compose -f docker-compose.dev.yml exec aura-app-dev bash

shell-jupyter: ## Open shell in Jupyter container
	docker-compose -f docker-compose.dev.yml exec jupyter-dev bash

# Cleanup Operations
clean: ## Clean up Docker resources
	@echo "Cleaning up Docker resources..."
	docker-compose down -v
	docker-compose -f docker-compose.dev.yml down -v
	docker system prune -f

clean-all: ## Clean up all Docker resources (WARNING: This will remove all containers, images, and volumes)
	@echo "Cleaning up all Docker resources..."
	docker-compose down -v --rmi all
	docker-compose -f docker-compose.dev.yml down -v --rmi all
	docker system prune -af
	docker volume prune -f

# Installation and Setup
install: ## Install Python dependencies
	@echo "Installing Python dependencies..."
	pip install -r requirements.txt

install-dev: ## Install development dependencies
	@echo "Installing development dependencies..."
	pip install -r requirements.txt
	pip install pre-commit
	pre-commit install

# Quick Start Commands
start: dev ## Quick start development environment
	@echo "A.U.R.A development environment is ready!"
	@echo "Dashboard: http://localhost:8501"
	@echo "Jupyter: http://localhost:8888"

stop: down ## Stop all services

status: ## Show status of all services
	@echo "A.U.R.A Services Status:"
	@echo ""
	@echo "Production Services:"
	@docker-compose ps
	@echo ""
	@echo "Development Services:"
	@docker-compose -f docker-compose.dev.yml ps

# Production Deployment
deploy: build up ## Deploy to production
	@echo "A.U.R.A deployed to production!"

deploy-dev: build-dev up-dev ## Deploy development environment
	@echo "A.U.R.A development environment deployed!"
