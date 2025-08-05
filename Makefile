.PHONY: help install install-dev test test-unit test-api test-cov test-watch lint format clean build docs

# Default target
help:
	@echo "Available commands:"
	@echo "  install      - Install the package in development mode"
	@echo "  install-dev  - Install the package with development dependencies"
	@echo "  test         - Run all tests"
	@echo "  test-unit    - Run unit tests only"
	@echo "  test-api     - Run API tests only"
	@echo "  test-cov     - Run tests with coverage report"
	@echo "  test-watch   - Run tests in watch mode"
	@echo "  lint         - Run linting checks"
	@echo "  format       - Format code with black"
	@echo "  clean        - Clean build artifacts"
	@echo "  build        - Build the package"
	@echo "  docs         - Generate documentation"

# Install the package in development mode
install:
	pip install -e .

# Install the package with development dependencies
install-dev:
	pip install -e ".[test]"

# Run all tests
test:
	pytest tests/ -v

# Run unit tests only
test-unit:
	pytest tests/ -v -m "unit"

# Run API tests only
test-api:
	pytest tests/ -v -m "api"

# Run tests with coverage report
test-cov:
	pytest tests/ -v --cov=src/notepy_online --cov-report=term-missing --cov-report=html

# Run tests in watch mode (requires pytest-watch)
test-watch:
	ptw tests/ -- -v

# Run linting checks
lint:
	flake8 src/ tests/
	black --check src/ tests/
	mypy src/

# Format code with black
format:
	black src/ tests/

# Clean build artifacts
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf .pytest_cache/
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete

# Build the package
build:
	python -m build

# Generate documentation
docs:
	# Add documentation generation commands here when needed
	@echo "Documentation generation not yet implemented"

# Run the server in development mode
serve:
	python -m notepy_online.server

# Run the CLI
cli:
	python -m notepy_online.cli

# Quick development setup
dev-setup: install-dev
	@echo "Development environment setup complete!"
	@echo "Run 'make test' to run tests"
	@echo "Run 'make serve' to start the development server" 