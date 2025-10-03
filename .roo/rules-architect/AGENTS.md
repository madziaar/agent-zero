# AGENTS.md

This file provides guidance to agents when working with code in this repository.

## Architectural Constraints of Simultaneous WSGI/ASGI Deployment

The hybrid WSGI/ASGI architecture imposes specific architectural constraints:

- **Protocol Boundary Management**: Synchronous WSGI and asynchronous ASGI servers must coexist without blocking each other, requiring careful middleware design
- **Request Routing Architecture**: Path-based dispatching (`/mcp`, `/a2a`) determines protocol handling, affecting overall system design
- **State Synchronization**: Shared state must be carefully managed across synchronous/asynchronous boundaries

## Scalability Implications of Runtime ID Session Isolation

The runtime ID-based session isolation has significant scalability implications:

- **Instance Isolation Strategy**: Each runtime instance maintains complete session isolation through unique 8-byte hex IDs embedded in cookie names
- **Multi-Instance Deployment**: The architecture supports multiple instances on the same host without session collision
- **Horizontal Scaling**: Runtime ID isolation enables horizontal scaling strategies while maintaining session integrity

## Complex Initialization Sequence Architectural Requirements

The background initialization sequence imposes strict architectural requirements:

- **Dependency Chain Management**: Chat persistence must precede MCP server initialization, followed by job loops, then model preloading
- **Event Loop Architecture**: `EventLoopThread` pooling and `DeferredTask` management require sophisticated background processing architecture
- **Failure Recovery**: Background process failures must not block main thread initialization

## Multi-Layer Authentication Architectural Patterns

The coordinated authentication system requires understanding complex architectural patterns:

- **Layered Security Architecture**: Network-level (loopback validation), transport-level (API keys), application-level (basic auth), and session-level (CSRF) security
- **Runtime ID Integration**: Session cookies include runtime IDs for complete instance isolation
- **Context-Aware Security**: Different endpoints (`/`, `/mcp`, `/a2a`) require different authentication mechanisms based on access patterns

## Hierarchical Agent Delegation Architectural Patterns

The multi-agent delegation system requires sophisticated architectural understanding:

- **Agent Context Architecture**: Each agent maintains isolated context while supporting delegation chains through superior/subordinate relationships
- **Message Propagation Architecture**: The `_process_chain()` method enables automatic response propagation through delegation hierarchies
- **Resource Management**: Agent lifecycle management includes proper cleanup of subordinate agents and their associated resources
