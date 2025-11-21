# Contributing to MCP Clarify

Thank you for your interest in contributing to MCP Clarify! This document provides guidelines for contributing to the project.

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/mcp-clarify.git
   cd mcp-clarify
   ```
3. **Set up the development environment**:
   ```bash
   uv venv
   source .venv/bin/activate  # On Linux/macOS
   uv pip install fastmcp pydantic pytest pytest-asyncio
   ```

## Development Workflow

1. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**:
   - Write clear, self-documenting code
   - Follow PEP 8 style guidelines
   - Add comments for complex logic

3. **Test your changes**:
   ```bash
   # Run the server locally
   python hitl_server.py
   
   # Test with an MCP client (Cursor, Claude Desktop, etc.)
   ```

4. **Commit your changes**:
   ```bash
   git add .
   git commit -m "Brief description of your changes"
   ```

5. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Open a Pull Request** on GitHub

## Code Style

- Follow [PEP 8](https://pep8.org/) style guidelines
- Use type hints where appropriate
- Keep functions focused and single-purpose
- Write descriptive variable names

## Testing

When adding new features:

- Test with multiple MCP clients (Cursor, Claude Desktop, VS Code)
- Verify compatibility with both Pydantic v1 and v2
- Test edge cases (empty answers, invalid choices, etc.)
- Ensure backward compatibility

## Documentation

- Update the README.md if you add new features
- Add docstrings to new functions
- Include usage examples for new capabilities

## Pull Request Guidelines

- **Title**: Use a clear, descriptive title
- **Description**: Explain what changes you made and why
- **Testing**: Describe how you tested your changes
- **Breaking Changes**: Clearly note any breaking changes

## Questions?

If you have questions or need help:

- Open an issue on GitHub
- Check existing issues and PRs for similar discussions

## Code of Conduct

Please read and follow our [Code of Conduct](CODE_OF_CONDUCT.md) to ensure a welcoming environment for everyone.

## Security

If you discover a security vulnerability, please follow the guidelines in our [Security Policy](SECURITY.md) instead of opening a public issue.

## License

By contributing to MCP Clarify, you agree that your contributions will be licensed under the MIT License.

