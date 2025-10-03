# Prompts Directory Organization

## Overview

This directory contains prompt files used by the Agent Zero framework. These prompts define agent behavior, system instructions, tool usage, and other aspects of the agent system.

The directory has been reorganized to improve maintainability, reduce redundancy, and make it easier to find and update prompt files.

## Directory Structure

```
prompts/
├── README.md                  # This file
├── system/                    # Core system prompts
│   ├── main/                  # Main system prompts defining agent behavior
│   ├── tools/                 # Tool-specific system prompts
│   ├── behaviour/             # Behaviour adjustment prompts
│   └── other/                 # Other system prompts
├── framework/                 # Internal framework messages
├── memory/                    # Memory-related prompts
├── tools/                     # Tool-related prompts
└── utilities/                 # Utility prompts
```

## Categories

### System Prompts

Located in the `system/` directory, these define the core behavior of the agent:

- `system/main/`: Core system prompts defining agent role, communication style, environment interaction, and problem-solving approach
- `system/tools/`: System prompts specific to individual tools
- `system/behaviour/`: Prompts related to behavior adjustment and personalization
- `system/other/`: Additional system prompts like datetime handling, memory management, etc.

### Framework Prompts

Located in the `framework/` directory, these are internal messages used by the framework:

- Error messages
- Warning templates
- Tool execution responses
- Message formatting templates

### Memory Prompts

Located in the `memory/` directory, these define memory-related operations:

- Memory consolidation
- Memory retrieval
- Memory filtering
- Solution storage and recall

### Tools Prompts

Located in the `tools/` directory, these define tool-specific prompts:

- Tool usage instructions
- Tool response formatting

### Utilities Prompts

Located in the `utilities/` directory, these are miscellaneous utility prompts:

- Context additions
- Agent information
- Special formatting instructions

## Naming Conventions

Files are named using the following conventions:

- `agent.system.main.*.md`: Core system prompts (now in system/main)
- `agent.system.tool.*.md`: Tool-specific prompts (now in system/tools)
- `agent.system.behaviour*.md`: Behaviour prompts (now in system/behaviour)
- `fw.*.md`: Framework messages (now in framework/)
- `memory.*.md`: Memory-related prompts (now in memory/)

## Adding New Prompt Files

When adding new prompt files:

1. Identify the appropriate category for your prompt
2. Place it in the corresponding directory
3. Follow the existing naming conventions for that category
4. Update documentation if adding a new type of prompt

## Benefits of This Organization

- Improved findability: Related prompts are grouped together
- Better maintainability: Easier to update all prompts of a specific type
- Reduced redundancy: Easier to identify similar prompts that could be consolidated
- Clearer structure: Helps new developers understand the prompt system

## Original Structure

The original structure had all prompt files in a flat directory, which made it difficult to find specific prompts and understand their purpose. The new structure organizes prompts by function and improves maintainability.