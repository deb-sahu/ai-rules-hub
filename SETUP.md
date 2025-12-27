# Automatic Setup Guide for AI Coding Rules

This guide provides step-by-step instructions for automatically integrating these AI coding standards with VS Code GitHub Copilot and Cursor IDE.

## Table of Contents

- [Prerequisites](#prerequisites)
- [VS Code with GitHub Copilot Setup](#vs-code-with-github-copilot-setup)
- [Cursor IDE Setup](#cursor-ide-setup)
- [Verification](#verification)
- [Troubleshooting](#troubleshooting)
- [Advanced Configuration](#advanced-configuration)

## Prerequisites

Before setting up automatic integration, ensure you have:

- Git installed on your system
- Access to this repository (clone or fork it)
- Active subscription to GitHub Copilot (for VS Code) or Cursor IDE

## VS Code with GitHub Copilot Setup

GitHub Copilot can automatically use coding rules from your repository through several methods:

### Method 1: Using `.github/copilot-instructions.md` (Recommended)

This is the simplest method for automatic integration with GitHub Copilot.

#### Step 1: Clone this repository to your project

```bash
# Navigate to your project root
cd /path/to/your/project

# Add this rules repository as a git submodule
git submodule add https://github.com/deb-sahu/ai-rules-hub .github/ai-rules

# Or clone it directly if you don't want to use submodules
git clone https://github.com/deb-sahu/ai-rules-hub .github/ai-rules
```

#### Step 2: Create a Copilot instructions file

Create a file named `.github/copilot-instructions.md` in your project root:

```bash
mkdir -p .github
touch .github/copilot-instructions.md
```

#### Step 3: Reference the rules in your instructions file

Add the following content to `.github/copilot-instructions.md`:

```markdown
# Copilot Instructions

Please follow the coding standards defined in our AI rules repository.

## General Guidelines

- Follow all coding standards from `.github/ai-rules/`
- Pay special attention to security and performance rules marked as "critical" or "high" priority

## Language-Specific Rules

### TypeScript/JavaScript
- Reference: `.github/ai-rules/typescript/rules.yml`
- Style Guide: `.github/ai-rules/typescript/styleguide.md`
- Use strict type checking
- Avoid `any` types

### React
- Reference: `.github/ai-rules/react/rules.yml`
- Style Guide: `.github/ai-rules/react/styleguide.md`
- Use functional components with hooks
- Follow accessibility guidelines

### Python
- Reference: `.github/ai-rules/python/rules.yml`
- Style Guide: `.github/ai-rules/python/styleguide.md`
- Follow PEP 8
- Use type hints

### C#/.NET
- Reference: `.github/ai-rules/csharp-dotnet/rules.yml`
- Style Guide: `.github/ai-rules/csharp-dotnet/styleguide.md`
- Use async/await patterns
- Follow SOLID principles

### SQL
- Reference: `.github/ai-rules/sql/rules.yml`
- Style Guide: `.github/ai-rules/sql/styleguide.md`
- Use parameterized queries
- Follow naming conventions

## Priority Levels

- **critical**: Must follow (security, correctness)
- **high**: Should follow (best practices)
- **medium**: Recommended (code quality)
- **low**: Optional (style preferences)
```

#### Step 4: Enable Copilot to read workspace files

1. Open VS Code Settings (Ctrl+, or Cmd+,)
2. Search for "Copilot"
3. Ensure the following settings are enabled:
   - `github.copilot.enable` - Enable GitHub Copilot
   - `github.copilot.advanced` - Enable advanced features

#### Step 5: Restart VS Code

Close and reopen VS Code to ensure Copilot picks up the new instructions.

### Method 2: Using Workspace-Specific Settings

You can configure Copilot to use specific context from your workspace:

#### Step 1: Create a `.vscode/settings.json` file

```bash
mkdir -p .vscode
touch .vscode/settings.json
```

#### Step 2: Add Copilot configuration

Add the following to `.vscode/settings.json`:

```json
{
  "github.copilot.enable": {
    "*": true
  },
  "github.copilot.advanced": {},
  "files.associations": {
    "**/ai-rules/**/*.yml": "yaml",
    "**/ai-rules/**/*.md": "markdown"
  },
  "files.watcherExclude": {
    "**/.git/objects/**": true,
    "**/.git/subtree-cache/**": true,
    "**/node_modules/**": true
  }
}
```

### Method 3: Repository-Level Integration (Organization)

For organization-wide deployment:

#### Step 1: Fork or clone this repository

```bash
git clone https://github.com/deb-sahu/ai-rules-hub
cd ai-rules-hub
```

#### Step 2: Add to your organization's GitHub

1. Create a new repository in your organization
2. Push the rules repository to your organization
3. Grant access to all developers

#### Step 3: Configure GitHub Copilot at organization level

1. Go to your GitHub Organization settings
2. Navigate to "Copilot" → "Policies"
3. Enable "Copilot" for your organization
4. Members will automatically get context from public repos in the org

### Method 4: Using VS Code Extension Settings

Configure Copilot through VS Code User or Workspace Settings:

1. **Open Command Palette** (Ctrl+Shift+P / Cmd+Shift+P)
2. Type: `Preferences: Open User Settings (JSON)`
3. Add:

```json
{
  "github.copilot.enable": {
    "*": true,
    "yaml": true,
    "markdown": true
  },
  "editor.inlineSuggest.enabled": true,
  "editor.suggest.preview": true
}
```

## Cursor IDE Setup

Cursor IDE has native support for custom AI rules and can automatically detect them in your workspace.

### Method 1: Using `.cursorrules` File (Recommended)

Cursor automatically reads a `.cursorrules` file in your project root.

#### Step 1: Clone the rules repository

```bash
# Navigate to your project root
cd /path/to/your/project

# Clone as a subdirectory
git clone https://github.com/deb-sahu/ai-rules-hub ai-rules

# Or add as submodule
git submodule add https://github.com/deb-sahu/ai-rules-hub ai-rules
```

#### Step 2: Create `.cursorrules` file

Create a `.cursorrules` file in your project root:

```bash
touch .cursorrules
```

#### Step 3: Configure rules in `.cursorrules`

Add the following content to `.cursorrules`:

```
# AI Coding Rules for Cursor

You are an expert developer following strict coding standards.

## Rules Repository
All coding standards are defined in the `ai-rules/` directory.

## Language-Specific Standards

### TypeScript
- Follow rules from: ai-rules/typescript/rules.yml
- Reference style guide: ai-rules/typescript/styleguide.md
- CRITICAL: No 'any' types, use explicit types
- HIGH: Strict null checks, handle undefined/null
- Use async/await for async operations

### React  
- Follow rules from: ai-rules/react/rules.yml
- Reference style guide: ai-rules/react/styleguide.md
- CRITICAL: Use functional components with hooks
- HIGH: Implement proper accessibility (ARIA labels)
- MEDIUM: Optimize with React.memo, useMemo, useCallback

### Python
- Follow rules from: ai-rules/python/rules.yml
- Reference style guide: ai-rules/python/styleguide.md
- CRITICAL: PEP 8 compliance
- HIGH: Type hints for all functions
- Use pathlib over os.path

### C#/.NET
- Follow rules from: ai-rules/csharp-dotnet/rules.yml
- Reference style guide: ai-rules/csharp-dotnet/styleguide.md
- CRITICAL: Async/await for I/O operations
- HIGH: Dependency injection pattern
- Follow SOLID principles

### SQL
- Follow rules from: ai-rules/sql/rules.yml
- Reference style guide: ai-rules/sql/styleguide.md
- CRITICAL: Always use parameterized queries (prevent SQL injection)
- HIGH: Proper indexing for performance
- Use consistent naming conventions

## Rule Priority System

When generating or modifying code:
- **CRITICAL**: Must always follow - security and correctness issues
- **HIGH**: Should follow - best practices and maintainability  
- **MEDIUM**: Recommended - code quality and readability
- **LOW**: Optional - style preferences

## Code Generation Guidelines

1. Always check ai-rules/ directory for language-specific rules before generating code
2. Reference styleguide.md files for examples of correct patterns
3. Use snippets from ai-rules/{language}/snippets/ when available
4. Prioritize security (CRITICAL) and best practices (HIGH) rules
5. When in doubt, ask for clarification rather than violating rules

## Context References

When I use @rules, @style, or @snippet shortcuts:
- @rules: Reference the rules.yml file for current language
- @style: Reference the styleguide.md file for current language  
- @snippet: Look in snippets/ directory for templates
```

#### Step 4: Configure Cursor Settings

1. Open Cursor IDE
2. Go to Settings (Ctrl+, or Cmd+,)
3. Navigate to "Cursor" → "General"
4. Enable "Rules File" option
5. Verify the path shows `.cursorrules` in your project root

#### Step 5: Restart Cursor

Close and reopen Cursor IDE to load the new rules.

### Method 2: Using Cursor's Built-in Rules Directory

Cursor can automatically detect rules from specific directories:

#### Step 1: Clone rules to `.cursor/` directory

```bash
mkdir -p .cursor
cd .cursor
git clone https://github.com/deb-sahu/ai-rules-hub rules
```

#### Step 2: Cursor will automatically detect the rules

Cursor scans `.cursor/` directory for AI rules and configuration files.

### Method 3: Global Rules Configuration

For rules that apply to all your projects:

#### Step 1: Clone to Cursor's global config directory

**macOS/Linux:**
```bash
mkdir -p ~/.cursor/rules
cd ~/.cursor/rules
git clone https://github.com/deb-sahu/ai-rules-hub .
```

**Windows:**
```cmd
mkdir %APPDATA%\.cursor\rules
cd %APPDATA%\.cursor\rules
git clone https://github.com/deb-sahu/ai-rules-hub .
```

#### Step 2: Configure global settings

Open Cursor Settings → Advanced → Global Rules Path and point to the cloned directory.

### Method 4: Using Cursor's AI Context

You can add rules as permanent context in Cursor:

1. Open Cursor IDE
2. Click on the AI Chat panel
3. Click the "+" icon to add context
4. Select "Add Directory" 
5. Choose the `ai-rules/` directory
6. The rules will now be available in all chat sessions

## Verification

### Testing VS Code Copilot Integration

1. **Create a test file** in your project:
   - For TypeScript: `test.ts`
   - For Python: `test.py`
   - For C#: `test.cs`

2. **Start typing** a function and check if Copilot suggestions follow the rules:

   **TypeScript Example:**
   ```typescript
   // Type: function getUserById
   // Expected suggestion should include:
   // - Explicit parameter types
   // - Return type (Promise<User | null>)
   // - Async/await if accessing database
   ```

3. **Check rule compliance**:
   - Suggestions should avoid `any` type
   - Should use proper naming conventions
   - Should include error handling

### Testing Cursor IDE Integration

1. **Open a file** in Cursor IDE

2. **Use the @ shortcuts**:
   - Type `@rules` in chat - should reference the rules files
   - Type `@style` in chat - should reference style guides
   - Type `@snippet` in chat - should access code snippets

3. **Ask Cursor to generate code**:
   ```
   "Generate a React component for a user profile card"
   ```
   
   Expected behavior:
   - Should follow React rules from `ai-rules/react/`
   - Use functional component with hooks
   - Include accessibility attributes
   - Follow naming conventions

4. **Verify in Chat**:
   - Open Cursor Chat (Ctrl+L or Cmd+L)
   - Ask: "What coding rules should I follow?"
   - Cursor should reference the `.cursorrules` file

## Troubleshooting

### VS Code Copilot Issues

#### Problem: Copilot not picking up rules

**Solutions:**
1. Ensure `.github/copilot-instructions.md` exists in project root
2. Check file permissions: `chmod 644 .github/copilot-instructions.md`
3. Restart VS Code
4. Check Copilot status: Click Copilot icon in status bar
5. Verify Copilot is enabled: Settings → Extensions → GitHub Copilot

#### Problem: Suggestions don't follow rules

**Solutions:**
1. Make sure rules are explicitly mentioned in `copilot-instructions.md`
2. Be more specific in your file comments about expected behavior
3. Use inline comments to guide Copilot: `// Must use explicit types, no 'any'`
4. Check if Copilot has access to workspace files

#### Problem: Copilot not reading submodule files

**Solutions:**
1. Initialize submodules: `git submodule update --init --recursive`
2. Clone directly instead of using submodules
3. Copy rules to `.github/ai-rules/` instead of linking

### Cursor IDE Issues

#### Problem: `.cursorrules` file not being loaded

**Solutions:**
1. Verify file is in project root directory
2. Check file has no extension: `.cursorrules` (not `.cursorrules.txt`)
3. Restart Cursor IDE
4. Check Cursor version (needs v0.8+): Help → About
5. Verify in Settings → Cursor → Rules File is enabled

#### Problem: Context not available in chat

**Solutions:**
1. Manually add context: Click "+" in chat → Add Directory → Select `ai-rules/`
2. Check directory permissions
3. Refresh Cursor: Ctrl+Shift+P → "Reload Window"
4. Clear Cursor cache: Settings → Advanced → Clear Cache

#### Problem: Rules not being followed

**Solutions:**
1. Be explicit in prompts: "Following the rules from ai-rules/typescript/rules.yml..."
2. Reference specific rules: "Use the HIGH priority rules for error handling"
3. Update `.cursorrules` to be more explicit about priorities
4. Check if rules file has syntax errors

### General Issues

#### Problem: Git submodule not updating

**Solutions:**
```bash
# Update submodule to latest version
git submodule update --remote ai-rules

# Or pull manually
cd ai-rules
git pull origin main
cd ..
```

#### Problem: Rules are outdated

**Solutions:**
```bash
# If using submodule
git submodule update --remote --merge

# If cloned directly  
cd ai-rules
git pull origin main
```

#### Problem: Conflicts between rules

**Solutions:**
1. Check priority levels in `rules.yml` files
2. Create project-specific overrides in `.cursorrules` or `copilot-instructions.md`
3. Document exceptions in your project's README

## Advanced Configuration

### Auto-Update Rules with Git Hooks

Create a git hook to automatically update rules:

**`.git/hooks/post-merge`:**
```bash
#!/bin/bash
# Auto-update ai-rules submodule after merge
git submodule update --init --recursive
echo "AI rules updated successfully"
```

Make it executable:
```bash
chmod +x .git/hooks/post-merge
```

### Custom Rule Priorities

Override priorities in your `.cursorrules` or `copilot-instructions.md`:

```markdown
## Custom Priority Overrides

For this project, we modify these rule priorities:

- SQL parameterized queries: CRITICAL → CRITICAL (keep)
- React accessibility: HIGH → CRITICAL (upgrade)
- TypeScript 'any' usage: HIGH → CRITICAL (upgrade)
- Python type hints: HIGH → MEDIUM (downgrade for legacy code)
```

### Language-Specific Configuration

Create separate instruction files per language:

```bash
.github/
├── copilot-instructions.md         # Main instructions
├── copilot-typescript.md           # TypeScript-specific
├── copilot-python.md               # Python-specific
└── copilot-csharp.md              # C#-specific
```

Reference in main instructions:
```markdown
For language-specific rules:
- TypeScript: See [copilot-typescript.md](.github/copilot-typescript.md)
- Python: See [copilot-python.md](.github/copilot-python.md)
```

### CI/CD Integration

Validate code against rules in your CI pipeline:

**GitHub Actions Example (`.github/workflows/validate-rules.yml`):**
```yaml
name: Validate Coding Rules

on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          submodules: recursive
      
      - name: Setup validation
        run: |
          # Add your rule validation scripts here
          echo "Checking code against ai-rules..."
          
      - name: Lint TypeScript
        if: contains(github.event.head_commit.modified, '.ts')
        run: npm run lint
      
      - name: Check Python style
        if: contains(github.event.head_commit.modified, '.py')
        run: |
          pip install flake8 mypy
          flake8 .
          mypy .
```

### Team Sharing via GitHub Packages

Share rules via your organization's GitHub:

1. Fork this repository to your organization
2. Customize rules for your team
3. Team members clone from your org's fork
4. Use GitHub's "Watch" feature to get notified of updates

### Multiple Projects Sync

Keep rules consistent across multiple projects:

```bash
# Create a central rules repository
mkdir ~/ai-coding-rules
cd ~/ai-coding-rules
git clone https://github.com/deb-sahu/ai-rules-hub .

# Symlink in each project
cd ~/project1
ln -s ~/ai-coding-rules .github/ai-rules

cd ~/project2  
ln -s ~/ai-coding-rules .github/ai-rules
```

Update once, reflects everywhere:
```bash
cd ~/ai-coding-rules
git pull origin main
# All projects now have updated rules
```

## Best Practices

1. **Keep rules updated**: Pull latest changes regularly
2. **Customize for your needs**: Fork and adjust priorities based on your team's needs
3. **Document exceptions**: If you need to deviate from rules, document why
4. **Review AI suggestions**: Don't blindly accept all suggestions, review for rule compliance
5. **Educate team**: Ensure all developers understand the rules and why they exist
6. **Iterate**: Continuously improve rules based on team feedback
7. **Version control**: Track changes to rules in git for accountability

## Support

If you encounter issues:

1. Check the [Troubleshooting](#troubleshooting) section
2. Review the main [README.md](README.md) for overview
3. Open an issue in the repository
4. Contact your development team lead

## Additional Resources

- [GitHub Copilot Documentation](https://docs.github.com/en/copilot)
- [Cursor IDE Documentation](https://cursor.sh/docs)
- [VS Code Settings Documentation](https://code.visualstudio.com/docs/getstarted/settings)
- Repository Rule Files: `{language}/rules.yml`
- Style Guides: `{language}/styleguide.md`
