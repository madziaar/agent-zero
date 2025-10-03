# Agent Zero Optimization Tools

This directory contains tools created to analyze, optimize, and maintain the Agent Zero codebase. These tools help identify inefficiencies, clean up redundancies, and maintain a well-organized project structure.

## Available Tools

### 1. cleanup_caches.py

**Purpose**: Removes Python cache files and other temporary artifacts that can accumulate during development.

**Usage**:
```bash
python optimization_tools/cleanup_caches.py
```

**Features**:
- Removes `__pycache__` directories
- Cleans `.pyc` and `.pyo` files
- Removes test artifacts
- Preserves important project files

### 2. organize_prompts.py

**Purpose**: Analyzes and reorganizes prompt files into a logical structure.

**Usage**:
```bash
python optimization_tools/organize_prompts.py
```

**Features**:
- Analyzes prompt files and categorizes them
- Suggests an improved directory structure
- Creates backups before moving files
- Interactive mode for selective implementation

### 3. analyze_agents.py

**Purpose**: Examines agent profile directories to identify redundancies and standardization opportunities.

**Usage**:
```bash
python optimization_tools/analyze_agents.py
```

**Features**:
- Analyzes agent profile structures
- Identifies common files across agents
- Detects unique customizations
- Suggests standardization improvements

## Using These Tools

### Regular Maintenance

We recommend running these tools periodically as part of your development workflow:

1. Run `cleanup_caches.py` before commits or when switching branches
2. Run `analyze_agents.py` when creating new agent profiles
3. Run `organize_prompts.py` when adding new prompt files

### Automation

Consider automating these tools as part of your CI/CD pipeline or git hooks:

```bash
# Example pre-commit hook
#!/bin/bash
python optimization_tools/cleanup_caches.py
```

### Best Practices

1. **Create Backups**: Always back up important files before running any optimization tool
2. **Review Changes**: Examine the changes suggested by the tools before applying them
3. **Test After Changes**: Verify that the system still functions correctly after optimization
4. **Document Updates**: Keep the optimization documentation up-to-date

## Adding New Tools

When adding new optimization tools:

1. Follow the existing naming and structure patterns
2. Document the tool's purpose and usage
3. Ensure the tool creates backups when modifying files
4. Add appropriate error handling
5. Update this README with the new tool's information

## Monitoring Project Health

The tools in this directory are designed to help maintain project health by:

1. **Reducing Clutter**: Removing unnecessary files
2. **Improving Organization**: Ensuring logical directory structures
3. **Promoting Consistency**: Standardizing patterns across the codebase
4. **Identifying Issues**: Highlighting potential problems

By regularly using these tools, you can help ensure that the Agent Zero codebase remains clean, well-organized, and maintainable as it continues to evolve.