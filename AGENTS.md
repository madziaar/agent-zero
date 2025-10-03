# AGENTS.md

This file provides guidance to agents when working with code in this repository.

## Multi-Protocol WSGI/ASGI Architecture Pattern

The system runs both WSGI (Flask) and ASGI (MCP/A2A) servers simultaneously using DispatcherMiddleware and ASGIMiddleware. This hybrid architecture allows traditional synchronous web endpoints to coexist with async-capable MCP and A2A servers on the same port, with routes dynamically dispatched based on path prefixes (`/mcp` and `/a2a`).

## Dynamic ASGI Application Instantiation

MCP and A2A servers are instantiated dynamically at runtime rather than being static WSGI applications. This pattern enables runtime configuration of server capabilities and allows for hot-swapping of server implementations without restarting the main web application.

## Runtime ID-Based Session Isolation

Each runtime instance generates a unique 8-byte hex token (`secrets.token_hex(8)`) that gets embedded in session cookie names. This prevents session collision when multiple Agent Zero instances run on the same host, ensuring complete isolation between different deployments or development environments.

## Complex Async Initialization Sequence

The system uses a sophisticated background initialization pattern with `DeferredTask` and `EventLoopThread` management. Initialization processes (MCP servers, chat persistence, job loops, preloading) run in separate event loops to prevent blocking the main thread, with careful coordination to ensure proper startup sequencing.

## Hierarchical Agent Delegation System

Agents implement true multi-agent cooperation through a superior/subordinate relationship pattern. When a subordinate agent completes its monologue, the response automatically propagates back up the delegation chain through the `_process_chain` method, enabling seamless task delegation and result aggregation across multiple specialized agents.

## Model Provider Abstraction Complexity

The system implements multiple layers of model provider abstraction that would surprise experienced developers:

- **Provider Normalization**: Raw provider names are normalized through `_merge_provider_defaults()` with configuration merging from multiple sources
- **Multi-Format API Key Handling**: API keys support both single keys and comma-separated round-robin rotation
- **Advanced Reasoning Detection**: Native reasoning content is automatically detected and separated from regular responses, with fallback to manual thinking tag parsing
- **Rate Limiting Integration**: Per-provider rate limiters are applied at the model wrapper level, not just at the API client level

## Background Task Coordination

The system maintains multiple concurrent background processes with sophisticated lifecycle management:

- **Event Loop Thread Pooling**: `EventLoopThread` instances are pooled by thread name to prevent resource leaks
- **Deferred Task Chaining**: Tasks can have child tasks with automatic cleanup coordination
- **Cross-Thread Execution**: The `execute_inside` method allows synchronous functions to run within async task contexts
- **Graceful Termination**: Background tasks support both soft cancellation and thread termination with proper cleanup sequencing

## Multi-Layer Authentication Coordination

The authentication system implements multiple overlapping security mechanisms that coordinate seamlessly:

- **Network-Level Filtering**: Loopback address validation prevents external access
- **API Key Authentication**: Token-based auth for programmatic access
- **HTTP Basic Authentication**: Username/password protection for web interface
- **CSRF Protection**: Session-based token validation for form submissions
- **Runtime ID Integration**: Session cookies include runtime ID for instance isolation

This multi-layered approach ensures security at every level while maintaining usability for different access patterns.
