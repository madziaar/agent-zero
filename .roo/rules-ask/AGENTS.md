# AGENTS.md

This file provides guidance to agents when working with code in this repository.

## Understanding the Organic, Learning Agent Framework Philosophy

The system implements an organic agent framework that learns and adapts through hierarchical delegation:

- **Multi-Agent Learning Patterns**: Agents can spawn subordinate agents with different profiles, creating learning hierarchies where specialized agents contribute to collective intelligence
- **Context Preservation**: Agent contexts maintain complete state isolation while enabling seamless delegation chains through superior/subordinate relationships
- **Adaptive Behavior**: The framework supports dynamic agent creation with inherited knowledge from parent agents while allowing specialized adaptations

## Model Provider Abstraction Complexity Explanation

The multi-layered model provider abstraction requires understanding complex interactions:

- **Provider Normalization Process**: Raw provider names are transformed through `_merge_provider_defaults()` with configuration merging from multiple sources including environment variables, settings files, and runtime parameters
- **API Key Rotation Strategy**: Supports both single API keys and comma-separated key rotation for load distribution and failover scenarios
- **Advanced Reasoning Detection**: Implements dual-mode reasoning extraction with native reasoning detection and fallback thinking tag parsing

## Multi-Protocol Architecture Conceptual Challenges

The WSGI/ASGI hybrid architecture presents conceptual challenges:

- **Synchronous/Asynchronous Boundary Management**: Traditional Flask WSGI endpoints coexist with async ASGI servers through DispatcherMiddleware routing
- **Dynamic Server Instantiation**: MCP and A2A servers are created dynamically at runtime rather than being static configurations
- **Path-Based Protocol Dispatch**: Request routing is determined by URL path prefixes (`/mcp`, `/a2a`) requiring understanding of protocol boundaries

## Agent Delegation System Conceptual Model

The hierarchical delegation system requires understanding sophisticated patterns:

- **Automatic Callback Chains**: When subordinate agents complete tasks, responses automatically propagate up through `_process_chain()` method
- **Context Inheritance**: Subordinate agents inherit configuration from their superiors while maintaining separate execution contexts
- **Delegation State Management**: The system tracks superior/subordinate relationships through embedded data structures enabling complex multi-agent workflows
