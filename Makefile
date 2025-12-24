.PHONY: help install dev-install clean lint format type-check test test-cov test-unit test-integration build publish run docs serve-docs pre-commit frontend-install frontend-dev frontend-build frontend-clean serve install-all

# Colors for terminal output
BLUE := \033[0;34m
GREEN := \033[0;32m
YELLOW := \033[0;33m
RED := \033[0;31m
NC := \033[0m # No Color

# Python and UV configuration
PYTHON := python3
UV := uv
PROJECT_NAME := matrix-system
SRC_DIR := src/matrix_system
TEST_DIR := tests

# Frontend configuration
FRONTEND_DIR := frontend
NODE := node
NPM := npm

##@ General

help: ## Display this help message
	@echo "$(BLUE)Matrix System - Makefile Help$(NC)"
	@echo "$(GREEN)==============================$(NC)"
	@echo ""
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make $(YELLOW)<target>$(NC)\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  $(YELLOW)%-20s$(NC) %s\n", $$1, $$2 } /^##@/ { printf "\n$(BLUE)%s$(NC)\n", substr($$0, 5) } ' $(MAKEFILE_LIST)
	@echo ""

##@ Installation

install: ## Install backend production dependencies
	@echo "$(GREEN)Installing backend production dependencies...$(NC)"
	$(UV) pip install -e .
	@echo "$(GREEN)✓ Backend installation complete!$(NC)"

dev-install: ## Install backend development dependencies
	@echo "$(GREEN)Installing backend development dependencies...$(NC)"
	$(UV) pip install -e ".[dev]"
	@echo "$(GREEN)✓ Backend development installation complete!$(NC)"

install-all: install frontend-install ## Install both backend and frontend dependencies
	@echo "$(GREEN)✓ Full installation complete!$(NC)"

sync: ## Sync all dependencies using uv
	@echo "$(GREEN)Syncing dependencies with uv...$(NC)"
	$(UV) pip compile pyproject.toml -o requirements.txt
	$(UV) pip sync requirements.txt
	@echo "$(GREEN)✓ Sync complete!$(NC)"

##@ Code Quality

lint: ## Run linting checks with ruff
	@echo "$(GREEN)Running linting checks...$(NC)"
	$(UV) run ruff check $(SRC_DIR) $(TEST_DIR)
	@echo "$(GREEN)✓ Linting complete!$(NC)"

lint-fix: ## Run linting checks and auto-fix issues
	@echo "$(GREEN)Running linting with auto-fix...$(NC)"
	$(UV) run ruff check --fix $(SRC_DIR) $(TEST_DIR)
	@echo "$(GREEN)✓ Linting with fix complete!$(NC)"

format: ## Format code with black and ruff
	@echo "$(GREEN)Formatting code...$(NC)"
	$(UV) run black $(SRC_DIR) $(TEST_DIR)
	$(UV) run ruff format $(SRC_DIR) $(TEST_DIR)
	$(UV) run isort $(SRC_DIR) $(TEST_DIR)
	@echo "$(GREEN)✓ Formatting complete!$(NC)"

format-check: ## Check code formatting without making changes
	@echo "$(GREEN)Checking code formatting...$(NC)"
	$(UV) run black --check $(SRC_DIR) $(TEST_DIR)
	$(UV) run ruff format --check $(SRC_DIR) $(TEST_DIR)
	$(UV) run isort --check-only $(SRC_DIR) $(TEST_DIR)
	@echo "$(GREEN)✓ Format check complete!$(NC)"

type-check: ## Run type checking with mypy
	@echo "$(GREEN)Running type checks...$(NC)"
	$(UV) run mypy $(SRC_DIR)
	@echo "$(GREEN)✓ Type checking complete!$(NC)"

check: lint type-check format-check ## Run all code quality checks

##@ Testing

test: ## Run all tests
	@echo "$(GREEN)Running tests...$(NC)"
	$(UV) run pytest $(TEST_DIR) -v
	@echo "$(GREEN)✓ Tests complete!$(NC)"

test-cov: ## Run tests with coverage report
	@echo "$(GREEN)Running tests with coverage...$(NC)"
	$(UV) run pytest $(TEST_DIR) -v --cov=$(SRC_DIR) --cov-report=term-missing --cov-report=html
	@echo "$(GREEN)✓ Coverage report generated in htmlcov/$(NC)"

test-unit: ## Run unit tests only
	@echo "$(GREEN)Running unit tests...$(NC)"
	$(UV) run pytest $(TEST_DIR)/unit -v
	@echo "$(GREEN)✓ Unit tests complete!$(NC)"

test-integration: ## Run integration tests only
	@echo "$(GREEN)Running integration tests...$(NC)"
	$(UV) run pytest $(TEST_DIR)/integration -v
	@echo "$(GREEN)✓ Integration tests complete!$(NC)"

test-watch: ## Run tests in watch mode
	@echo "$(GREEN)Running tests in watch mode...$(NC)"
	$(UV) run pytest-watch $(TEST_DIR) -v

##@ Build & Publish

build: clean ## Build distribution packages
	@echo "$(GREEN)Building distribution packages...$(NC)"
	$(UV) build
	@echo "$(GREEN)✓ Build complete! Packages in dist/$(NC)"

publish-test: build ## Publish to TestPyPI
	@echo "$(YELLOW)Publishing to TestPyPI...$(NC)"
	$(UV) publish --repository testpypi
	@echo "$(GREEN)✓ Published to TestPyPI!$(NC)"

publish: build ## Publish to PyPI
	@echo "$(RED)Publishing to PyPI...$(NC)"
	@read -p "Are you sure you want to publish to PyPI? [y/N] " -n 1 -r; \
	echo; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		$(UV) publish; \
		echo "$(GREEN)✓ Published to PyPI!$(NC)"; \
	else \
		echo "$(YELLOW)Publication cancelled.$(NC)"; \
	fi

##@ Development

run: ## Run the CLI application
	@echo "$(GREEN)Running Matrix System CLI...$(NC)"
	$(UV) run matrix --help

run-dev: ## Run the CLI in development mode
	@echo "$(GREEN)Running Matrix System CLI in dev mode...$(NC)"
	$(UV) run python -m matrix_system.cli.main --help

serve: frontend-dev ## Start the frontend development server
	@echo "$(GREEN)Frontend server running at http://localhost:3000$(NC)"

##@ Documentation

docs: ## Build documentation
	@echo "$(GREEN)Building documentation...$(NC)"
	$(UV) run mkdocs build
	@echo "$(GREEN)✓ Documentation built in site/$(NC)"

serve-docs: ## Serve documentation locally
	@echo "$(GREEN)Serving documentation at http://127.0.0.1:8000$(NC)"
	$(UV) run mkdocs serve

##@ Maintenance

clean: ## Clean build artifacts and cache files
	@echo "$(YELLOW)Cleaning build artifacts...$(NC)"
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .eggs/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf .ruff_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf coverage.xml
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.py,cover" -delete
	@echo "$(GREEN)✓ Cleanup complete!$(NC)"

clean-all: clean frontend-clean ## Deep clean including virtual environments and frontend
	@echo "$(YELLOW)Deep cleaning...$(NC)"
	rm -rf .venv/
	rm -rf venv/
	rm -rf env/
	@echo "$(GREEN)✓ Deep cleanup complete!$(NC)"

##@ Pre-commit

pre-commit-install: ## Install pre-commit hooks
	@echo "$(GREEN)Installing pre-commit hooks...$(NC)"
	$(UV) run pre-commit install
	@echo "$(GREEN)✓ Pre-commit hooks installed!$(NC)"

pre-commit: ## Run pre-commit on all files
	@echo "$(GREEN)Running pre-commit checks...$(NC)"
	$(UV) run pre-commit run --all-files
	@echo "$(GREEN)✓ Pre-commit checks complete!$(NC)"

##@ CI/CD

ci: check test-cov ## Run all CI checks
	@echo "$(GREEN)✓ All CI checks passed!$(NC)"

##@ Information

version: ## Show project version
	@echo "$(BLUE)Matrix System Version:$(NC)"
	@grep -m1 version pyproject.toml | cut -d'"' -f2

info: ## Show project information
	@echo "$(BLUE)Project Information:$(NC)"
	@echo "$(GREEN)Name:$(NC) $(PROJECT_NAME)"
	@echo "$(GREEN)Source:$(NC) $(SRC_DIR)"
	@echo "$(GREEN)Tests:$(NC) $(TEST_DIR)"
	@echo "$(GREEN)Python:$(NC) $$($(PYTHON) --version)"
	@echo "$(GREEN)UV:$(NC) $$($(UV) --version 2>/dev/null || echo 'not installed')"
	@echo "$(GREEN)Node:$(NC) $$($(NODE) --version 2>/dev/null || echo 'not installed')"
	@echo "$(GREEN)NPM:$(NC) $$($(NPM) --version 2>/dev/null || echo 'not installed')"

##@ Frontend

frontend-install: ## Install frontend dependencies
	@echo "$(GREEN)Installing frontend dependencies...$(NC)"
	@if [ ! -d "$(FRONTEND_DIR)" ]; then \
		echo "$(RED)Error: Frontend directory not found!$(NC)"; \
		exit 1; \
	fi
	cd $(FRONTEND_DIR) && $(NPM) install
	@echo "$(GREEN)✓ Frontend installation complete!$(NC)"

frontend-dev: ## Start frontend development server
	@echo "$(GREEN)Starting frontend development server...$(NC)"
	@echo "$(BLUE)Dashboard will be available at http://localhost:3000$(NC)"
	cd $(FRONTEND_DIR) && $(NPM) run dev

frontend-build: ## Build frontend for production
	@echo "$(GREEN)Building frontend for production...$(NC)"
	cd $(FRONTEND_DIR) && $(NPM) run build
	@echo "$(GREEN)✓ Frontend build complete!$(NC)"

frontend-start: frontend-build ## Start frontend production server
	@echo "$(GREEN)Starting frontend production server...$(NC)"
	cd $(FRONTEND_DIR) && $(NPM) start

frontend-lint: ## Lint frontend code
	@echo "$(GREEN)Linting frontend code...$(NC)"
	cd $(FRONTEND_DIR) && $(NPM) run lint
	@echo "$(GREEN)✓ Frontend linting complete!$(NC)"

frontend-type-check: ## Type check frontend code
	@echo "$(GREEN)Type checking frontend code...$(NC)"
	cd $(FRONTEND_DIR) && $(NPM) run type-check
	@echo "$(GREEN)✓ Frontend type checking complete!$(NC)"

frontend-clean: ## Clean frontend build artifacts
	@echo "$(YELLOW)Cleaning frontend artifacts...$(NC)"
	@if [ -d "$(FRONTEND_DIR)" ]; then \
		rm -rf $(FRONTEND_DIR)/node_modules; \
		rm -rf $(FRONTEND_DIR)/.next; \
		rm -rf $(FRONTEND_DIR)/out; \
		rm -rf $(FRONTEND_DIR)/.vercel; \
		echo "$(GREEN)✓ Frontend cleanup complete!$(NC)"; \
	else \
		echo "$(YELLOW)Frontend directory not found, skipping...$(NC)"; \
	fi
