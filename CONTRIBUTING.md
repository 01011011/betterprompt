# Contributing to BetterPrompt

Thank you for your interest in contributing to BetterPrompt! This document provides guidelines for contributing to the project.

## Code of Conduct

By participating in this project, you agree to abide by our code of conduct:
- Be respectful and inclusive
- Use welcoming and inclusive language
- Focus on what is best for the community
- Show empathy towards other community members

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in the [Issues](../../issues) section
2. If not, create a new issue with:
   - Clear description of the bug
   - Steps to reproduce
   - Expected vs actual behavior
   - Environment details (OS, Python version, etc.)

### Suggesting Features

1. Check existing issues and discussions
2. Create a new issue with:
   - Clear description of the feature
   - Use cases and benefits
   - Possible implementation approach

### Contributing Code

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes**
4. **Add tests** for new functionality
5. **Run tests** to ensure nothing is broken
   ```bash
   pytest
   ```
6. **Update documentation** if needed
7. **Commit your changes**
   ```bash
   git commit -m "Add: brief description of changes"
   ```
8. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```
9. **Create a Pull Request**

## Development Setup

1. **Clone your fork**
   ```bash
   git clone https://github.com/yourusername/betterprompt.git
   cd betterprompt
   ```

2. **Set up virtual environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   copy .env.example .env
   # Edit .env with your Azure OpenAI credentials
   ```

## Coding Standards

- Follow PEP 8 style guidelines
- Use type hints where appropriate
- Write descriptive commit messages
- Add docstrings to functions and classes
- Keep functions small and focused
- Write tests for new features

## Testing

- Write unit tests for new functionality
- Ensure all tests pass before submitting PR
- Aim for good test coverage
- Test both success and error cases

## Documentation

- Update README.md if needed
- Add docstrings to new functions
- Update API documentation for new endpoints
- Include examples where helpful

## Pull Request Guidelines

- **One feature per PR** - Keep changes focused
- **Clear title and description** - Explain what and why
- **Reference related issues** - Use "Fixes #123" or "Relates to #123"
- **Include tests** - Don't forget to test your changes
- **Update documentation** - Keep docs current

## Getting Help

If you need help:
- Check the [README](README.md) for setup instructions
- Look at existing code for examples
- Ask questions in issue discussions
- Reach out to maintainers

## Recognition

Contributors will be recognized in:
- README.md acknowledgments
- Release notes for significant contributions
- GitHub contributors page

Thank you for contributing to BetterPrompt! 🚀
