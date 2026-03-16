# AI Coding Standards Repository

Centralized AI coding standards and style guides with automated sync across GitHub Copilot, Cursor, Claude Code, and other AI-powered development tools for consistent code completions.

**📚 [Setup Guide](SETUP.md)** - Step-by-step instructions for automatic integration with VS Code Copilot, Cursor IDE, and Claude Code.

## 📋 Overview

This repository contains comprehensive coding standards, style guides, and code snippets for multiple programming languages and frameworks. These standards are designed to be consumed by AI coding assistants to ensure consistent, high-quality code generation across your development team.

## 🗂️ Repository Structure

```
├── csharp-dotnet/
│   ├── rules.yml              # C#/.NET coding standards
│   ├── styleguide.md          # Examples and best practices
│   └── snippets/              # Code snippets and templates
├── typescript/
│   ├── rules.yml              # TypeScript coding standards
│   ├── styleguide.md          # Examples and best practices
│   └── snippets/              # Code snippets and templates
├── react/
│   ├── rules.yml              # React coding standards
│   ├── styleguide.md          # Examples and best practices
│   └── snippets/              # Code snippets and templates
├── sql/
│   ├── rules.yml              # SQL coding standards
│   ├── styleguide.md          # Examples and best practices
│   └── snippets/              # Code snippets and templates
├── python/
│   ├── rules.yml              # Python coding standards
│   ├── styleguide.md          # Examples and best practices
│   └── snippets/              # Code snippets and templates
├── java-spring-boot/
│   ├── rules.yml              # Java/Spring Boot coding standards
│   ├── styleguide.md          # Examples and best practices
│   └── snippets/              # Code snippets and templates
├── dart-flutter/
│   ├── rules.yml              # Dart/Flutter coding standards
│   ├── styleguide.md          # Examples and best practices
│   └── snippets/              # Code snippets and templates
├── .ai-rules-index.json       # Index file for AI tools
├── sync-config.json           # Configuration for syncing with AI tools
└── README.md                  # This file
```

## 🎯 Purpose

This repository serves several key purposes:

1. **Consistency**: Ensure all developers and AI assistants follow the same coding standards
2. **Quality**: Maintain high code quality through well-defined best practices
3. **Efficiency**: Speed up development with AI-powered code completion that follows your standards
4. **Education**: Provide clear examples and guidance for developers
5. **Integration**: Seamlessly integrate with popular AI coding tools

## 🚀 Supported Languages & Frameworks

### C#/.NET
- Naming conventions and code organization
- Dependency injection patterns
- Async/await best practices
- LINQ usage guidelines
- Testing with xUnit/NUnit
- Error handling and logging

### TypeScript
- Type safety and type annotations
- Modern JavaScript features
- Function and class patterns
- Error handling strategies
- Testing with Jest/Vitest

### React
- Component structure and organization
- Hooks usage and custom hooks
- State management patterns
- Performance optimization
- Accessibility guidelines
- Testing with React Testing Library

### SQL
- Schema design and normalization
- Query optimization
- Indexing strategies
- Security best practices
- Stored procedures and functions
- Transaction handling

### Python
- PEP 8 compliance
- Type hints and annotations
- Async/await patterns
- Data structures and algorithms
- Testing with pytest
- Error handling and context managers

## 🛠️ Integration with AI Tools

**→ For detailed setup instructions, see [SETUP.md](SETUP.md)**

### GitHub Copilot

GitHub Copilot can reference these standards through the `.ai-rules-index.json` file. To use:

1. Ensure this repository is accessible to your GitHub account
2. The `.ai-rules-index.json` file provides metadata about available rules
3. Copilot will automatically suggest code that follows these standards

**Quick Start:** See [VS Code Copilot Setup](SETUP.md#vs-code-with-github-copilot-setup) for automatic integration steps.

### Cursor IDE

Cursor can load these rules to provide context-aware suggestions:

1. Configure `sync-config.json` with your repository settings
2. Cursor will sync rules and provide completions based on your standards
3. Use `@rules` in Cursor to explicitly reference specific standards

**Quick Start:** See [Cursor IDE Setup](SETUP.md#cursor-ide-setup) for automatic integration steps.

### Claude Code

Claude Code uses `CLAUDE.md` files to load project-specific instructions:

1. Create a `CLAUDE.md` file in your project root referencing these standards
2. Claude Code automatically reads `CLAUDE.md` and follows the rules during coding sessions
3. Use `/init` in Claude Code to auto-generate a starter `CLAUDE.md`

**Quick Start:** See [Claude Code Setup](SETUP.md#claude-code-setup) for detailed integration steps.

### Other AI Tools

The standardized format (`rules.yml` + `styleguide.md`) can be consumed by:
- Tabnine
- Codeium
- Amazon CodeWhisperer
- Any tool supporting custom rule definitions

## 📖 Using the Standards

**→ New to setup? See [SETUP.md](SETUP.md) for automatic integration with VS Code Copilot, Cursor IDE, and Claude Code.**

### For Developers

Each language folder contains:

1. **rules.yml**: Machine-readable rules with priority levels and examples
2. **styleguide.md**: Human-readable guide with comprehensive examples showing ✅ good and ❌ bad practices
3. **snippets/**: Reusable code templates

### For AI Tools

The rules are structured to be easily parsed:

```yaml
rules:
  category_name:
    - rule: "Description of the rule"
      priority: "high|medium|low|critical"
      example: "Code example"
```

### Rule Priorities

- **critical**: Must follow (security, correctness)
- **high**: Should follow (best practices, maintainability)
- **medium**: Recommended (code quality, readability)
- **low**: Optional (style preferences)

## 🔄 Syncing with AI Tools

The `sync-config.json` file configures automatic syncing:

```json
{
  "sync_enabled": true,
  "tools": ["copilot", "cursor", "claude-code", "tabnine"],
  "update_frequency": "daily"
}
```

## 🤝 Contributing

To add or update standards:

1. Edit the appropriate `rules.yml` file
2. Update the corresponding `styleguide.md` with examples
3. Add any useful snippets to the `snippets/` folder
4. Update `.ai-rules-index.json` if adding new categories
5. Submit a pull request

### Guidelines for Contributors

- Keep rules concise and actionable
- Provide clear examples for each rule
- Specify priority levels appropriately
- Include both positive and negative examples in styleguides
- Test rules with AI tools before submitting

## 📚 Additional Resources

### Official Documentation
- [C#/.NET Documentation](https://docs.microsoft.com/en-us/dotnet/)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [React Documentation](https://react.dev/)
- [Python Documentation](https://docs.python.org/)
- [SQL Standards](https://www.iso.org/standard/63555.html)

### AI Tool Documentation
- [GitHub Copilot](https://github.com/features/copilot)
- [Cursor IDE](https://cursor.sh/)
- [Claude Code](https://docs.anthropic.com/en/docs/claude-code)
- [Tabnine](https://www.tabnine.com/)

## 🔐 Security

These rules include security best practices:
- Input validation and sanitization
- Secure authentication and authorization
- Protection against common vulnerabilities (SQL injection, XSS, etc.)
- Secure data storage and transmission

## 📞 Support

For questions or issues:
- Create an issue in this repository
- Contact your development team lead
- Refer to the styleguides for detailed examples

## 🔮 Future Enhancements

Planned additions:
- Java coding standards
- Go coding standards
- Kotlin coding standards
- GraphQL best practices
- Docker and container standards
- CI/CD pipeline configurations
- API design guidelines
- Microservices patterns

---

**Note**: These standards are living documents. Regular updates ensure they stay current with evolving best practices and new language features.
