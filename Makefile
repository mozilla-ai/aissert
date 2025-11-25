# Colors for output
GREEN  := \033[0;32m
YELLOW := \033[0;33m
NC     := \033[0m

.PHONY: help
help:
	@echo "Available targets:"
	@echo "  $(YELLOW)clean$(NC)                - Clean up build artifacts"
	@echo "  $(YELLOW)install$(NC)              - Install all workspace dependencies"
	@echo "  $(YELLOW)lint$(NC)                 - Run pre-commit checks on all files"
	@echo "  $(YELLOW)test$(NC)                 - Run tests for all packages"
	@echo "  $(YELLOW)test-aissert$(NC)         - Run tests for aissert package"
	@echo "  $(YELLOW)test-example-pkg$(NC)     - Run tests for example-pkg package"
	@echo "  $(YELLOW)test-pytest-aissert$(NC)  - Run tests for pytest-aissert package"
	@echo "  $(YELLOW)test-qa-bot$(NC)          - Run tests for qa_bot package"

.PHONY: install
install:
	@echo "$(GREEN)Installing workspace dependencies...$(NC)"
	uv sync --dev

.PHONY: test
test: install test-pytest-aissert test-qa-bot test-example-pkg
	@echo "$(GREEN)All tests completed$(NC)"

.PHONY: test-aissert
test-aissert:
	@echo "$(GREEN)Testing aissert...$(NC)"
	@echo "$(YELLOW)No tests directory found in aissert package$(NC)"

.PHONY: test-pytest-aissert
test-pytest-aissert:
	@echo "$(GREEN)Testing pytest-aissert...$(NC)"
	cd pytest-aissert && uv run pytest tests/ -v

.PHONY: test-qa-bot
test-qa-bot:
	@echo "$(GREEN)Testing qa_bot...$(NC)"
	cd qa_bot && uv run pytest tests/ -v

.PHONY: test-example-pkg
test-example-pkg:
	@echo "$(GREEN)Testing example-pkg...$(NC)"
	cd example-pkg && uv run pytest tests/ -v

.PHONY: lint
lint: install
	@echo "$(GREEN)Running pre-commit checks...$(NC)"
	uv run pre-commit run --all-files

.PHONY: clean
clean:
	@echo "$(GREEN)Cleaning build artifacts...$(NC)"
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .ruff_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name dist -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name build -exec rm -rf {} + 2>/dev/null || true
	@echo "$(GREEN)Clean complete$(NC)"
