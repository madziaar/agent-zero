# Agent Zero Optimization Tools

This directory contains a collection of tools designed to analyze, optimize, and maintain the Agent Zero codebase. These tools help identify inefficiencies, reorganize code, and provide ongoing maintenance capabilities.

## Tools Overview

### 1. `cleanup_caches.py`

**Purpose**: Removes Python cache files and other temporary artifacts that can accumulate over time.

**Features**:
- Cleans up `__pycache__` directories
- Removes `.pyc`, `.pyo`, and other Python cache files
- Cleans test artifacts (`.pytest_cache`, `.coverage`, etc.)
- Preserves Git directories and important project files

**Usage**:
```bash
python cleanup_caches.py
```

### 2. `organize_prompts.py`

**Purpose**: Analyzes and reorganizes the prompt files in the `prompts/` directory for better organization.

**Features**:
- Categorizes prompt files by type (system, framework, memory, etc.)
- Suggests a more logical directory structure
- Creates backups before making changes
- Interactive mode for user confirmation

**Usage**:
```bash
python organize_prompts.py
```

### 3. `analyze_agents.py`

**Purpose**: Analyzes agent profile directories to identify patterns, redundancies, and standardization opportunities.

**Features**:
- Compares file structures across agent profiles
- Identifies identical files that could be consolidated
- Detects divergent prompt files that might need standardization
- Suggests a standard template for new agent profiles
- Exports detailed analysis as JSON

**Usage**:
```bash
python analyze_agents.py
```

## Using the Tools Together

These tools are designed to be used as part of a comprehensive optimization strategy:

1. Start with `cleanup_caches.py` to remove temporary files and reduce clutter
2. Use `analyze_agents.py` to understand the current structure and identify opportunities for standardization
3. Apply `organize_prompts.py` to improve the organization of system prompts
4. Implement the recommendations from the analysis results
5. Run `cleanup_caches.py` regularly as part of ongoing maintenance

## Best Practices

- Run `cleanup_caches.py` before committing changes to avoid including cache files in version control
- Use `analyze_agents.py` when creating new agent profiles to ensure consistency
- After reorganizing prompts with `organize_prompts.py`, test thoroughly to ensure all systems function correctly
- Consider adding these tools to CI/CD pipelines or development workflows
- Refer to the main `OPTIMIZATION.md` document for broader optimization strategies

## Safety Considerations

- The tools create backups before making changes to important files
- Interactive confirmation is requested before applying structural changes
- Always test the system after reorganization to verify functionality
- Consider running tools in a development environment before applying to production

## Contributing

To enhance these optimization tools:

1. Add new cleanup patterns to `cleanup_caches.py` as needed
2. Improve categorization logic in `organize_prompts.py` for new prompt types
3. Extend analysis capabilities in `analyze_agents.py` for deeper insights
4. Consider adding new optimization tools for other aspects of the codebase

## See Also

- [OPTIMIZATION.md](../OPTIMIZATION.md) - Comprehensive optimization recommendations
- [docs/development.md](../docs/development.md) - General development guidelines