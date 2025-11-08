# AI Rules Hub

Centralized, provider-agnostic source of coding rules and standards for different languages and frameworks.

## Overview

This repository provides a comprehensive collection of AI coding standards, style guides, and code snippets for various programming languages and frameworks. It's designed to work seamlessly with AI-powered development tools like GitHub Copilot, Cursor, AWS CodeWhisperer, and Tabnine to ensure consistent, high-quality code completions.

## Supported Languages & Frameworks

- **C#/.NET** - Enterprise .NET applications
- **TypeScript** - Type-safe JavaScript development
- **React** - Modern React applications with hooks and best practices
- **SQL** - Database queries and schema design
- **Python** - Python 3.x with PEP 8 standards
- **Java/Spring Boot** - Enterprise Java applications
- **Dart/Flutter** - Cross-platform mobile development

## Repository Structure

```
ai-rules-hub/
├── README.md                    # This file
├── .ai-rules-index.json         # Index for AI tools integration
├── sync-config.json             # Sync configuration for AI tools
├── csharp-dotnet/
│   ├── rules.yml               # C#/.NET coding standards
│   ├── styleguide.md           # Style guide with examples
│   └── snippets/               # Code snippets
├── typescript/
│   ├── rules.yml               # TypeScript coding standards
│   ├── styleguide.md           # Style guide with examples
│   └── snippets/               # Code snippets
├── react/
│   ├── rules.yml               # React coding standards
│   ├── styleguide.md           # Style guide with examples
│   └── snippets/               # Code snippets
├── sql/
│   ├── rules.yml               # SQL coding standards
│   ├── styleguide.md           # Style guide with examples
│   └── snippets/               # Code snippets
├── python/
│   ├── rules.yml               # Python coding standards
│   ├── styleguide.md           # Style guide with examples
│   └── snippets/               # Code snippets
├── java-spring-boot/
│   ├── rules.yml               # Java/Spring Boot coding standards
│   ├── styleguide.md           # Style guide with examples
│   └── snippets/               # Code snippets
└── dart-flutter/
    ├── rules.yml               # Dart/Flutter coding standards
    ├── styleguide.md           # Style guide with examples
    └── snippets/               # Code snippets
```

## Usage

### For AI Tools

This repository is designed to be consumed by AI-powered development tools. The `.ai-rules-index.json` file provides a standardized way for tools to discover and load coding standards.

### For Developers

1. Browse the language-specific folders to find coding standards
2. Review the `rules.yml` files for AI-specific coding rules
3. Check the `styleguide.md` files for detailed examples and best practices
4. Use code snippets from the `snippets/` folders as templates

## Integration with AI Tools

### GitHub Copilot

GitHub Copilot automatically reads the `.ai-rules-index.json` file to understand your coding standards and provide better suggestions.

### Cursor

Cursor uses the `sync-config.json` file to synchronize coding standards and provide context-aware completions.

### AWS CodeWhisperer

CodeWhisperer can be configured to reference the rules files for language-specific recommendations.

### Tabnine

Tabnine can learn from the style guides and snippets to provide more accurate completions.

## Contributing

To add a new language or framework:

1. Create a new folder with a descriptive name (e.g., `kotlin`)
2. Add `rules.yml` with AI coding standards
3. Add `styleguide.md` with examples and best practices
4. Optionally add a `snippets/` folder with code templates
5. Update `.ai-rules-index.json` to include the new language
6. Update `sync-config.json` to add the folder to the paths list

## File Formats

### rules.yml

Contains AI-specific coding rules in YAML format:
- Naming conventions
- Code organization patterns
- Security best practices
- Performance guidelines
- Framework-specific rules

### styleguide.md

Markdown document with:
- Detailed explanations of coding standards
- Code examples (good and bad)
- Best practices
- Common pitfalls to avoid

### snippets/

Directory containing reusable code templates that AI tools can reference.

## License

This repository is open-source and available for use with any AI-powered development tool.

## Maintenance

This repository is actively maintained to keep up with:
- Language and framework updates
- New AI tool capabilities
- Community feedback and contributions
- Evolving best practices
