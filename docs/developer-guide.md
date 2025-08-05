# 👨‍💻 Developer Guide

Complete guide for developers working with Notepy Online.

## 🚀 Overview

Notepy Online is built with modern Python technologies and follows best practices for maintainable, scalable code. This guide covers architecture, development setup, and contribution guidelines.

## 🏗️ Architecture

### Project Structure

```
notepy-online/
├── src/
│   └── notepy_online/
│       ├── __init__.py          # Package initialization
│       ├── cli.py               # Command-line interface
│       ├── core.py              # Core business logic
│       ├── resource.py          # Resource management
│       ├── server.py            # Web server implementation
│       ├── html.py              # HTML templates
│       ├── static_utils.py      # Static file utilities
│       └── static/              # Static assets
│           ├── css/             # Stylesheets
│           ├── js/              # JavaScript files
│           └── __init__.py
├── tests/                       # Test suite
├── docs/                        # Documentation
├── pyproject.toml              # Project configuration
├── Makefile                    # Development tasks
└── README.md                   # Project overview
```

### Core Components

#### ResourceManager (`resource.py`)
- **Purpose**: Manages application resources and configuration
- **Responsibilities**:
  - Cross-platform directory management
  - Configuration file handling
  - SSL certificate generation
  - Resource structure validation

#### NoteManager (`core.py`)
- **Purpose**: Core business logic for note management
- **Responsibilities**:
  - Note CRUD operations
  - Search and filtering
  - Tag management
  - Data persistence

#### NotepyOnlineServer (`server.py`)
- **Purpose**: Web server and RESTful API
- **Responsibilities**:
  - HTTP request handling
  - API endpoint implementation
  - Static file serving
  - SSL/TLS support

#### CLI (`cli.py`)
- **Purpose**: Command-line interface
- **Responsibilities**:
  - Command parsing and execution
  - User interaction
  - Output formatting
  - Error handling

## 🛠️ Development Setup

### Prerequisites

- **Python**: 3.12 or higher
- **Git**: For version control
- **Make**: For development tasks (optional)

### Environment Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-org/notepy-online.git
   cd notepy-online
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install in development mode**:
   ```bash
   pip install -e ".[test]"
   ```

4. **Verify installation**:
   ```bash
   notepy-online --version
   ```

### Development Dependencies

The project uses the following development tools:

- **pytest**: Testing framework
- **pytest-asyncio**: Async testing support
- **pytest-cov**: Coverage reporting
- **pytest-mock**: Mocking utilities
- **aioresponses**: Async HTTP mocking
- **httpx**: HTTP client for testing
- **black**: Code formatting
- **flake8**: Linting
- **mypy**: Type checking

## 🧪 Testing

### Running Tests

```bash
# Run all tests
make test

# Run specific test categories
make test-unit      # Unit tests only
make test-api       # API tests only

# Run with coverage
make test-cov

# Run in watch mode
make test-watch
```

### Test Structure

```
tests/
├── conftest.py          # Pytest configuration and fixtures
├── test_core.py         # Core functionality tests
├── test_cli.py          # CLI command tests
├── test_server.py       # Server functionality tests
├── test_api.py          # API endpoint tests
└── README.md            # Testing documentation
```

### Writing Tests

#### Unit Tests
```python
@pytest.mark.unit
def test_note_creation():
    """Test note creation functionality."""
    note_manager = NoteManager(mock_resource_manager)
    note = note_manager.create_note("Test Note", "Test content")
    
    assert note.title == "Test Note"
    assert note.content == "Test content"
    assert note.note_id is not None
```

#### API Tests
```python
@pytest.mark.asyncio
@pytest.mark.api
async def test_create_note_api(test_client):
    """Test note creation via API."""
    response = await test_client.post("/api/notes", json={
        "title": "API Test",
        "content": "Test content"
    })
    
    assert response.status == 201
    data = await response.json()
    assert data["success"] is True
    assert data["data"]["note"]["title"] == "API Test"
```

#### Integration Tests
```python
@pytest.mark.integration
def test_full_workflow():
    """Test complete note management workflow."""
    # Setup
    resource_mgr = ResourceManager()
    note_mgr = NoteManager(resource_mgr)
    
    # Create note
    note = note_mgr.create_note("Workflow Test", "Content")
    
    # Search note
    results = note_mgr.list_notes(search_query="Workflow")
    assert len(results) == 1
    assert results[0].note_id == note.note_id
    
    # Update note
    updated = note_mgr.update_note(note.note_id, title="Updated Title")
    assert updated.title == "Updated Title"
    
    # Delete note
    success = note_mgr.delete_note(note.note_id)
    assert success is True
```

### Test Fixtures

```python
@pytest.fixture
def sample_note_data():
    """Sample note data for testing."""
    return {
        "title": "Test Note",
        "content": "Test content",
        "tags": ["test", "sample"]
    }

@pytest.fixture
def populated_note_manager(note_manager, sample_note_data):
    """NoteManager with sample data."""
    note_manager.create_note(**sample_note_data)
    return note_manager
```

## 🔧 Code Quality

### Linting and Formatting

```bash
# Format code with black
make format

# Run linting checks
make lint

# Type checking with mypy
mypy src/
```

### Code Style

The project follows these style guidelines:

- **Black**: Code formatting (88 character line length)
- **PEP 8**: Python style guide
- **Type hints**: Use PEP 604 union syntax (`X | Y`)
- **Docstrings**: Google style, 88 character limit
- **Imports**: Organized with isort

### Pre-commit Hooks

```bash
# Install pre-commit hooks
pre-commit install

# Run hooks manually
pre-commit run --all-files
```

## 📦 Building and Distribution

### Building the Package

```bash
# Build wheel and source distribution
make build

# Clean build artifacts
make clean
```

### Development Installation

```bash
# Install in development mode
pip install -e .

# Install with test dependencies
pip install -e ".[test]"
```

## 🔍 Debugging

### Debug Mode

```bash
# Enable debug logging
export NOTEPY_LOG_LEVEL=DEBUG

# Run with debug output
notepy-online server --debug
```

### Debugging Tests

```bash
# Run tests with debugger
pytest tests/ --pdb

# Run specific test with maximum verbosity
pytest tests/test_core.py::test_note_creation -vvv -s
```

### Logging

```python
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Use in code
logger.debug("Debug message")
logger.info("Info message")
logger.warning("Warning message")
logger.error("Error message")
```

## 🚀 Performance Optimization

### Profiling

```bash
# Profile with cProfile
python -m cProfile -o profile.stats -m notepy_online.server

# Analyze profile
python -c "import pstats; pstats.Stats('profile.stats').sort_stats('cumulative').print_stats(10)"
```

### Memory Profiling

```bash
# Install memory profiler
pip install memory-profiler

# Profile memory usage
python -m memory_profiler src/notepy_online/core.py
```

### Async Performance

```python
import asyncio
import time

async def performance_test():
    """Test async performance."""
    start_time = time.time()
    
    # Run concurrent operations
    tasks = [async_operation() for _ in range(100)]
    results = await asyncio.gather(*tasks)
    
    end_time = time.time()
    print(f"Completed in {end_time - start_time:.2f} seconds")
```

## 🔒 Security Considerations

### Input Validation

```python
def validate_note_data(data: dict) -> bool:
    """Validate note input data."""
    if not isinstance(data.get("title"), str):
        return False
    
    if len(data["title"]) > 200:
        return False
    
    if "content" in data and len(data["content"]) > 100000:
        return False
    
    return True
```

### SSL/TLS Configuration

```python
def create_ssl_context(cert_file: Path, key_file: Path) -> ssl.SSLContext:
    """Create secure SSL context."""
    ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ssl_context.load_cert_chain(cert_file, key_file)
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    return ssl_context
```

### Rate Limiting

```python
from collections import defaultdict
import time

class RateLimiter:
    """Simple rate limiter implementation."""
    
    def __init__(self, max_requests: int, window: int):
        self.max_requests = max_requests
        self.window = window
        self.requests = defaultdict(list)
    
    def is_allowed(self, client_id: str) -> bool:
        now = time.time()
        client_requests = self.requests[client_id]
        
        # Remove old requests
        client_requests[:] = [req for req in client_requests if now - req < self.window]
        
        if len(client_requests) >= self.max_requests:
            return False
        
        client_requests.append(now)
        return True
```

## 📊 Monitoring and Metrics

### Health Checks

```python
async def health_check() -> dict:
    """System health check."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": __version__,
        "uptime": get_uptime(),
        "memory_usage": get_memory_usage(),
        "disk_usage": get_disk_usage()
    }
```

### Metrics Collection

```python
import time
from functools import wraps

def timing_decorator(func):
    """Decorator to measure function execution time."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        
        # Log or store metrics
        execution_time = end_time - start_time
        logger.info(f"{func.__name__} executed in {execution_time:.4f} seconds")
        
        return result
    return wrapper
```

## 🔄 Continuous Integration

### GitHub Actions Workflow

```yaml
name: CI/CD Pipeline

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.12, 3.13]
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -e ".[test]"
    
    - name: Run tests
      run: |
        make test-cov
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
```

### Pre-commit Configuration

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.3.0
    hooks:
      - id: black
        language_version: python3.12
  
  - repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
      - id: flake8
  
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.3.0
    hooks:
      - id: mypy
        additional_dependencies: [types-requests]
```

## 🤝 Contributing

### Development Workflow

1. **Fork the repository**
2. **Create a feature branch**:
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Make changes** and write tests
4. **Run tests** and ensure they pass
5. **Commit changes** with descriptive messages
6. **Push to your fork**
7. **Create a pull request**

### Commit Message Format

```
type(scope): description

[optional body]

[optional footer]
```

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Test changes
- `chore`: Maintenance tasks

**Examples**:
```
feat(api): add note search endpoint
fix(cli): resolve SSL certificate generation issue
docs(readme): update installation instructions
```

### Code Review Guidelines

- **Functionality**: Does the code work as intended?
- **Testing**: Are there adequate tests?
- **Documentation**: Is the code well-documented?
- **Style**: Does the code follow project conventions?
- **Performance**: Are there any performance implications?
- **Security**: Are there any security concerns?

## 📚 Additional Resources

### Documentation
- [Python Documentation](https://docs.python.org/)
- [aiohttp Documentation](https://docs.aiohttp.org/)
- [Click Documentation](https://click.palletsprojects.com/)
- [pytest Documentation](https://docs.pytest.org/)

### Tools
- [Black Code Formatter](https://black.readthedocs.io/)
- [Flake8 Linter](https://flake8.pycqa.org/)
- [MyPy Type Checker](https://mypy.readthedocs.io/)
- [Pre-commit Hooks](https://pre-commit.com/)

### Best Practices
- [PEP 8 Style Guide](https://www.python.org/dev/peps/pep-0008/)
- [PEP 484 Type Hints](https://www.python.org/dev/peps/pep-0484/)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)

---

**Related Documentation**:
- [API Reference](api-reference.md) - API documentation
- [CLI Reference](cli-reference.md) - Command-line interface
- [Configuration Guide](configuration.md) - Configuration options
- [Testing Guide](../tests/README.md) - Testing documentation 