# Contributing to Matrix System

First off, thank you for considering contributing to Matrix System! It's people like you that make Matrix System such a great tool.

## Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the existing issues as you might find out that you don't need to create one. When you are creating a bug report, please include as many details as possible:

* **Use a clear and descriptive title**
* **Describe the exact steps which reproduce the problem**
* **Provide specific examples to demonstrate the steps**
* **Describe the behavior you observed after following the steps**
* **Explain which behavior you expected to see instead and why**
* **Include logs and error messages**

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

* **Use a clear and descriptive title**
* **Provide a step-by-step description of the suggested enhancement**
* **Provide specific examples to demonstrate the steps**
* **Describe the current behavior and explain which behavior you expected to see instead**
* **Explain why this enhancement would be useful**

### Pull Requests

1. Fork the repo and create your branch from `main`
2. If you've added code that should be tested, add tests
3. If you've changed APIs, update the documentation
4. Ensure the test suite passes
5. Make sure your code lints
6. Issue that pull request!

## Development Process

### Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/matrix-system.git
cd matrix-system

# Install development dependencies
make dev-install

# Install pre-commit hooks
make pre-commit-install
```

### Development Workflow

1. Create a new branch for your feature or bugfix:
   ```bash
   git checkout -b feature/my-new-feature
   ```

2. Make your changes and ensure they follow our coding standards:
   ```bash
   make format    # Format code
   make lint      # Check linting
   make type-check # Check types
   ```

3. Write tests for your changes and ensure all tests pass:
   ```bash
   make test
   make test-cov  # Check coverage
   ```

4. Commit your changes with a clear commit message:
   ```bash
   git commit -m "Add feature: description of feature"
   ```

5. Push to your fork:
   ```bash
   git push origin feature/my-new-feature
   ```

6. Open a Pull Request

### Coding Standards

* Follow PEP 8 style guidelines
* Add type hints to all functions and methods
* Write comprehensive docstrings in Google style
* Maintain test coverage above 80%
* Use meaningful variable and function names
* Keep functions focused and small
* Write clear commit messages

### Type Hints

All code must include type hints:

```python
def my_function(param: str, count: int = 0) -> dict[str, Any]:
    """
    Brief description of function.

    Args:
        param: Description of param
        count: Description of count

    Returns:
        Description of return value

    Raises:
        ValueError: Description of when this is raised
    """
    return {"result": param * count}
```

### Documentation

* Update README.md if you change functionality
* Add docstrings to all public functions, classes, and modules
* Include examples in docstrings where appropriate
* Update type hints if you change function signatures

### Testing

* Write unit tests for all new functions
* Write integration tests for API interactions
* Ensure all tests pass before submitting PR
* Aim for 100% coverage of new code

```bash
# Run tests
make test

# Run with coverage
make test-cov

# Run specific test
uv run pytest tests/unit/test_myfeature.py -v
```

### Commit Messages

* Use the present tense ("Add feature" not "Added feature")
* Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
* Limit the first line to 72 characters or less
* Reference issues and pull requests liberally after the first line

Examples:
```
Add health check endpoint
Fix authentication error handling
Update documentation for new API
```

## Project Structure

```
matrix-system/
├── src/
│   └── matrix_system/
│       ├── api/          # API client code
│       ├── cli/          # CLI commands
│       ├── models/       # Pydantic models
│       └── utils/        # Utilities
├── tests/
│   ├── unit/            # Unit tests
│   └── integration/     # Integration tests
├── docs/                # Documentation
├── Makefile            # Development commands
├── pyproject.toml      # Project configuration
└── README.md           # Main documentation
```

## Questions?

Feel free to open an issue with your question or reach out to the maintainers.

## License

By contributing, you agree that your contributions will be licensed under the Apache License 2.0.
