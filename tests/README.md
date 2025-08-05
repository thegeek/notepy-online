# Notepy Online Testing Guide

This directory contains comprehensive tests for the Notepy Online application using pytest, the best testing framework for Python.

## 🧪 Testing Framework

We use **pytest** as our primary testing framework because it offers:

- **Simple and powerful**: Easy to write and understand tests
- **Rich ecosystem**: Extensive plugins and fixtures
- **Excellent async support**: Built-in support for testing async code
- **Great reporting**: Detailed test reports and coverage analysis
- **Flexible**: Supports various test types and configurations

## 📁 Test Structure

```
tests/
├── __init__.py              # Test package initialization
├── conftest.py             # Pytest configuration and shared fixtures
├── test_core.py            # Unit tests for core functionality
├── test_api.py             # API integration tests
├── test_server.py          # Server functionality tests
├── test_cli.py             # CLI command tests
└── README.md               # This file
```

## 🚀 Quick Start

### 1. Install Development Dependencies

```bash
# Install the package with test dependencies
make install-dev

# Or manually
pip install -e ".[test]"
```

### 2. Run All Tests

```bash
# Run all tests
make test

# Or manually
pytest tests/ -v
```

### 3. Run Specific Test Types

```bash
# Unit tests only
make test-unit

# API tests only
make test-api

# Tests with coverage report
make test-cov
```

## 🏷️ Test Categories

### Unit Tests (`@pytest.mark.unit`)
- Test individual functions and classes in isolation
- Fast execution, no external dependencies
- Located in `test_core.py` and `test_cli.py`

### API Tests (`@pytest.mark.api`)
- Test the web API endpoints
- Use aiohttp test client for HTTP requests
- Located in `test_api.py` and `test_server.py`

### Integration Tests (`@pytest.mark.integration`)
- Test complete workflows and system integration
- May involve multiple components working together

### Slow Tests (`@pytest.mark.slow`)
- Tests that take longer to execute
- Can be skipped with `-m "not slow"`

## 🔧 Test Configuration

### Pytest Configuration (`pyproject.toml`)

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py", "*_test.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = [
    "--strict-markers",
    "--strict-config",
    "--cov=src/notepy_online",
    "--cov-report=term-missing",
    "--cov-report=html:htmlcov",
    "--cov-report=xml",
    "--cov-fail-under=80"
]
markers = [
    "slow: marks tests as slow (deselect with '-m \"not slow\"')",
    "integration: marks tests as integration tests",
    "unit: marks tests as unit tests",
    "api: marks tests as API tests"
]
asyncio_mode = "auto"
```

### Coverage Configuration

- **Minimum coverage**: 80%
- **Coverage reports**: Terminal, HTML, and XML formats
- **Excluded files**: Tests, migrations, cache files

## 🛠️ Test Fixtures

### Core Fixtures (`conftest.py`)

- `temp_dir`: Temporary directory for test data
- `resource_manager`: ResourceManager with temporary directory
- `note_manager`: NoteManager for testing
- `sample_note`: Sample Note instance
- `sample_notes`: List of sample notes
- `populated_note_manager`: NoteManager with sample data
- `test_server`: NotepyOnlineServer instance
- `test_client`: aiohttp TestClient for API testing

### Usage Example

```python
def test_create_note(note_manager, sample_note_data):
    """Test note creation using fixtures."""
    note = note_manager.create_note(**sample_note_data)
    assert note.title == sample_note_data["title"]
```

## 📊 Test Coverage

### Running Coverage Reports

```bash
# Generate coverage report
make test-cov

# View HTML coverage report
open htmlcov/index.html
```

### Coverage Targets

- **Overall coverage**: ≥80%
- **Core modules**: ≥90%
- **API endpoints**: ≥95%

## 🔄 Continuous Integration

### GitHub Actions Workflow

```yaml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.12'
      - run: make install-dev
      - run: make test-cov
      - run: make lint
```

## 🧪 Writing Tests

### Test Naming Convention

- **Files**: `test_*.py`
- **Classes**: `Test*`
- **Functions**: `test_*`

### Example Test Structure

```python
@pytest.mark.unit
class TestNoteManager:
    """Test cases for the NoteManager class."""

    def test_create_note(self, note_manager):
        """Test creating a new note."""
        note = note_manager.create_note("Test Note", "Test content")
        assert note.title == "Test Note"
        assert note.content == "Test content"

    @pytest.mark.asyncio
    async def test_async_operation(self, test_client):
        """Test async API operations."""
        response = await test_client.get("/api/notes")
        assert response.status == 200
```

### Async Testing

```python
@pytest.mark.asyncio
async def test_api_endpoint(test_client):
    """Test API endpoint with async client."""
    response = await test_client.post("/api/notes", json={
        "title": "Test Note",
        "content": "Test content"
    })
    assert response.status == 201
```

### Mocking

```python
@patch('notepy_online.core.ResourceManager')
def test_with_mock(mock_resource_manager):
    """Test with mocked dependencies."""
    mock_resource_manager.return_value.get_data.return_value = "mocked_data"
    # Test implementation
```

## 🐛 Debugging Tests

### Verbose Output

```bash
# Run tests with verbose output
pytest tests/ -v -s

# Run specific test with maximum verbosity
pytest tests/test_core.py::TestNote::test_note_creation -vvv -s
```

### Debugging Failed Tests

```bash
# Run only failed tests
pytest tests/ --lf

# Run tests and stop on first failure
pytest tests/ -x

# Run tests with debugger on failure
pytest tests/ --pdb
```

### Test Discovery

```bash
# List all tests without running them
pytest tests/ --collect-only

# Show test names
pytest tests/ --collect-only -q
```

## 📈 Performance Testing

### Benchmark Tests

```python
@pytest.mark.benchmark
def test_note_creation_performance(benchmark, note_manager):
    """Benchmark note creation performance."""
    def create_note():
        return note_manager.create_note("Test", "Content")
    
    result = benchmark(create_note)
    assert result.stats.mean < 0.001  # Should complete in <1ms
```

### Load Testing

```python
@pytest.mark.asyncio
async def test_concurrent_requests(test_client):
    """Test handling of concurrent requests."""
    tasks = [
        test_client.get("/api/notes")
        for _ in range(10)
    ]
    responses = await asyncio.gather(*tasks)
    assert all(r.status == 200 for r in responses)
```

## 🔍 Test Data Management

### Temporary Test Data

```python
@pytest.fixture
def test_notes_file(temp_dir):
    """Create temporary notes file for testing."""
    notes_file = temp_dir / "notes.json"
    notes_file.write_text('{"test": {"title": "Test"}}')
    return notes_file
```

### Database Testing

```python
@pytest.fixture
def test_database():
    """Create temporary database for testing."""
    # Setup test database
    yield test_db
    # Cleanup after tests
```

## 🚨 Common Issues

### Import Errors

```bash
# Ensure package is installed in development mode
pip install -e .

# Check Python path
python -c "import notepy_online; print(notepy_online.__file__)"
```

### Async Test Issues

```python
# Use pytest-asyncio for async tests
@pytest.mark.asyncio
async def test_async_function():
    result = await async_function()
    assert result == expected
```

### Fixture Scope Issues

```python
# Use appropriate fixture scope
@pytest.fixture(scope="session")  # Shared across test session
def expensive_fixture():
    return expensive_setup()

@pytest.fixture(scope="function")  # New instance per test
def fresh_fixture():
    return fresh_setup()
```

## 📚 Additional Resources

- [pytest Documentation](https://docs.pytest.org/)
- [pytest-asyncio Documentation](https://pytest-asyncio.readthedocs.io/)
- [aiohttp Testing Guide](https://docs.aiohttp.org/en/stable/testing.html)
- [Click Testing Guide](https://click.palletsprojects.com/en/8.1.x/testing/)

## 🤝 Contributing

When adding new tests:

1. **Follow naming conventions**
2. **Use appropriate markers**
3. **Add docstrings to test functions**
4. **Ensure good coverage**
5. **Run tests locally before committing**
6. **Update this README if needed**

## 📊 Test Statistics

- **Total tests**: 100+
- **Unit tests**: 60+
- **API tests**: 40+
- **Coverage target**: 80%+
- **Test execution time**: <30 seconds

Run `make test-cov` to see current statistics and coverage reports. 