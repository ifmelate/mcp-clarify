# Security Policy

## Supported Versions

We release patches for security vulnerabilities. Which versions are eligible for receiving such patches depends on the CVSS v3.0 Rating:

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |

## Reporting a Vulnerability

We take the security of MCP Clarify seriously. If you believe you have found a security vulnerability, please report it to us as described below.

**Please do not report security vulnerabilities through public GitHub issues.**

Instead, please report them via email to [ifmelate@users.noreply.github.com](mailto:ifmelate@users.noreply.github.com).

You should receive a response within 48 hours. If for some reason you do not, please follow up via email to ensure we received your original message.

Please include the following information (as much as you can provide) to help us better understand the nature and scope of the possible issue:

* Type of issue (e.g. buffer overflow, SQL injection, cross-site scripting, etc.)
* Full paths of source file(s) related to the manifestation of the issue
* The location of the affected source code (tag/branch/commit or direct URL)
* Any special configuration required to reproduce the issue
* Step-by-step instructions to reproduce the issue
* Proof-of-concept or exploit code (if possible)
* Impact of the issue, including how an attacker might exploit the issue

This information will help us triage your report more quickly.

## Preferred Languages

We prefer all communications to be in English.

## Policy

We follow the principle of [Coordinated Vulnerability Disclosure](https://vuls.cert.org/confluence/display/Wiki/Coordinated+Vulnerability+Disclosure+Guidance).

## Security Best Practices

When using MCP Clarify:

1. **Run in Isolated Environments**: Always run MCP servers in isolated environments with appropriate permissions
2. **Validate Input**: Be cautious about the data you provide when answering clarification questions
3. **Keep Dependencies Updated**: Regularly update `fastmcp` and `pydantic` to their latest secure versions
4. **Use Virtual Environments**: Always use Python virtual environments to isolate dependencies
5. **Review Configurations**: Ensure your MCP client configurations use absolute paths and appropriate permissions

## Known Security Considerations

* **Local Execution Only**: This server is designed for local stdio transport only. Do not expose it over network connections without proper authentication and encryption
* **User Input**: The server elicits user input, which should be treated as untrusted data by AI agents
* **Dependencies**: Security depends on the underlying FastMCP and Pydantic libraries

## Updates and Announcements

Security updates will be announced through:
- GitHub Security Advisories
- Repository releases with security tags
- The CHANGELOG.md file with `[SECURITY]` markers

## Acknowledgments

We appreciate the security research community and will acknowledge researchers who responsibly disclose vulnerabilities (unless they prefer to remain anonymous).

