# Agent Profile Template and Standards

## Overview

This document defines the standard structure and organization for Agent Zero agent profiles. Following these standards ensures consistency across different agent types and makes maintenance and extension easier.

## Standard Directory Structure

```
agent-name/
├── _context.md                # Agent context and description
├── prompts/                   # Agent-specific prompt overrides
│   ├── agent.system.main.role.md             # Core role definition
│   ├── agent.system.main.communication.md    # Communication style
│   ├── agent.system.main.solving.md          # Problem-solving approach
│   ├── agent.system.main.tips.md             # Agent-specific tips
│   └── agent.system.tools.md                 # Tool specializations
├── extensions/                # Agent-specific extensions (if needed)
│   └── agent_init/
│       └── _10_agent_specific_extension.py
└── tools/                     # Agent-specific tools (if needed)
    └── agent_specific_tool.py
```

## File Naming and Organization

### Core Files

- **_context.md**: Provides a high-level description of the agent, its purpose, and key characteristics. This file should be present in all agent profiles.

### Prompt Files

Agent-specific prompts should follow the naming conventions established in the main prompts directory:

- **agent.system.main.role.md**: Defines the agent's core identity and purpose
- **agent.system.main.communication.md**: Defines the agent's communication style
- **agent.system.main.solving.md**: Defines the agent's approach to problem-solving
- **agent.system.main.tips.md**: Provides agent-specific tips and guidance
- **agent.system.tools.md**: Customizes how the agent uses tools

Only include files that need to override the default behavior. If the agent should use the default prompt for a specific aspect, do not include that file.

### Extensions

If the agent requires custom extensions:

- Place them in an `extensions/` directory
- Follow the extension naming convention with a prefix (_XX_) to control execution order
- Document the purpose and behavior of each extension

### Tools

If the agent requires custom tools:

- Place them in a `tools/` directory
- Follow the standard tool implementation pattern
- Document the tool's purpose, parameters, and usage

## Common Agent Types

The repository includes several standard agent types:

1. **default**: Base agent with balanced capabilities
2. **developer**: Specialized for software development
3. **researcher**: Specialized for research and information gathering
4. **agent0**: Experimental agent with unique capabilities
5. **hacker**: Security-focused agent
6. **qwen-coder**: Coding specialist agent

When creating a new agent, consider whether it could be a specialized version of an existing agent type rather than creating an entirely new profile.

## Guidelines for Creating New Agents

When creating a new agent profile:

1. Start with the _example template or copy an existing agent that's closest to your target behavior
2. Modify only the files necessary to establish the unique aspects of the agent
3. Maintain consistency with the established naming conventions
4. Document the agent's purpose and special capabilities in the _context.md file
5. Test the agent with typical use cases to verify that the customizations have the intended effect

## Optimizing Existing Agents

For existing agent profiles:

1. Ensure they follow the standard directory structure
2. Remove any unused or duplicate files
3. Consolidate similar functionality when possible
4. Update documentation to reflect current behavior
5. Consider moving common behavior into the default agent profile

## Benefits of Standardization

- **Consistency**: Makes it easier to understand and modify agent profiles
- **Maintainability**: Reduces effort required to update agent behavior
- **Extendability**: Provides a clear path for creating new agents
- **Documentation**: Ensures all agents are well-documented
- **Reduced Redundancy**: Minimizes duplicate code and prompt text

## Best Practices

1. **Minimal Overrides**: Only override prompts when necessary
2. **Clear Documentation**: Document what makes the agent unique
3. **Test Thoroughly**: Validate that customizations have the intended effect
4. **Maintain Consistency**: Follow the established naming conventions
5. **Regular Review**: Periodically review agent profiles for optimization opportunities