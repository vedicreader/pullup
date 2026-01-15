# Contributing to Pullup

Thank you for your interest in contributing to Pullup! This guide will help you get started.

## Development Setup

1. Clone the repository:
```bash
git clone https://github.com/Karthik777/pullup.git
cd pullup
```

2. Install in development mode:
```bash
pip install -e .
```

3. Install development dependencies:
```bash
pip install nbdev pytest
```

## Project Structure

Pullup uses [nbdev](https://nbdev.fast.ai/) for development, which means all code is written in Jupyter notebooks:

```
pullup/
├── nbs/                    # Jupyter notebooks (source of truth)
│   ├── index.ipynb        # Main documentation
│   ├── 00_core.ipynb      # Core utilities
│   ├── 01_aws.ipynb       # AWS module
│   ├── 02_azure.ipynb     # Azure module
│   ├── 03_gcp.ipynb       # GCP module
│   └── 04_hetzner.ipynb   # Hetzner module
├── pullup/                 # Auto-generated Python modules
├── tests/                  # Test files
└── examples/              # Example Pulumi programs
```

## Making Changes

### 1. Edit Notebooks

All code changes should be made in the notebooks under `nbs/`:

- Open the relevant notebook in Jupyter
- Make your changes
- Document your changes with markdown cells
- Add examples where appropriate

### 2. Export to Python

After editing notebooks, export them to Python modules:

```bash
nbdev_export
```

This generates the Python files in `pullup/` directory.

### 3. Run Tests

Before submitting, make sure all tests pass:

```bash
pytest tests/
```

### 4. Update Documentation

If you've added new features:

```bash
nbdev_readme  # Update README
nbdev_prepare # Full preparation (export, test, readme, etc.)
```

## Coding Standards

Pullup follows the [fastai style guide](https://docs.fast.ai/dev/style.html):

- **Functional**: Prefer functions over classes when possible
- **Composable**: Functions should be easy to combine
- **Documented**: Use docstrings and type hints
- **Tested**: Add tests for new functionality
- **Minimal**: Keep code simple and focused

### Type Hints

Use type hints for function parameters:

```python
def storage(name:str=None,        # Bucket name
            versioning:bool=True, # Enable versioning
            **kwargs):
    ...
```

### Documentation

- Use markdown cells to explain concepts
- Add code examples that can be run
- Document security implications
- Explain default behavior

### Security

All new infrastructure functions should:

1. Have security enabled by default
2. Document security features
3. Provide clear ways to customize security
4. Follow cloud provider best practices

## Adding New Features

### Adding a New Cloud Provider

1. Create a new notebook: `nbs/05_newprovider.ipynb`
2. Set the default export: `#| default_exp newprovider`
3. Import required packages
4. Implement core functions (storage, network, compute)
5. Export and test

### Adding Functions to Existing Modules

1. Open the relevant notebook (e.g., `01_aws.ipynb`)
2. Add a new cell with `#| export` directive
3. Implement your function
4. Add documentation and examples
5. Export with `nbdev_export`

## Testing

### Writing Tests

Add tests to `tests/test_*.py`:

```python
def test_new_feature():
    """Test description"""
    from pullup import aws
    # Test implementation
    assert result == expected
```

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_basic.py

# Run with verbose output
pytest -v

# Run with coverage
pytest --cov=pullup
```

## Pull Request Process

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Make your changes in the notebooks
4. Export: `nbdev_export`
5. Test: `pytest`
6. Commit with clear messages
7. Push to your fork
8. Create a Pull Request

### PR Checklist

- [ ] Code changes made in notebooks (not directly in Python files)
- [ ] Tests added for new functionality
- [ ] All tests passing
- [ ] Documentation updated
- [ ] Examples added if applicable
- [ ] Security best practices followed
- [ ] Code follows fastai style guide

## Questions?

- Open an issue for bugs or feature requests
- Discussions for questions and ideas
- Check existing issues before creating new ones

## License

By contributing, you agree that your contributions will be licensed under the Apache 2.0 License.
