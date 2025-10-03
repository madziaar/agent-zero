# AGENTS.md

This file provides guidance to agents when working with code in this repository.

## Complex Runtime Isolation Debugging Challenges

The runtime ID-based session isolation creates unique debugging challenges:

- **Multi-Instance Session Collision**: Sessions are automatically isolated between instances using runtime ID embedding, making cross-instance debugging complex
- **Dynamic Session Cookie Names**: Session cookies include runtime IDs preventing collision but requiring awareness of current instance ID for debugging
- **Isolated Context Debugging**: Each AgentContext maintains separate state requiring careful tracking across multiple instances

## Multi-Protocol Debugging Complexity

The simultaneous WSGI/ASGI architecture creates sophisticated debugging scenarios:

- **Request Routing Complexity**: Requests are dynamically dispatched between WSGI and ASGI based on path prefixes (`/mcp`, `/a2a`)
- **Middleware Interaction Debugging**: DispatcherMiddleware and ASGIMiddleware interactions require understanding of both synchronous and asynchronous execution paths
- **Cross-Protocol State Management**: State must be carefully managed across WSGI/ASGI boundaries

## Session Collision Debugging in Multi-Instance Scenarios

Debugging session issues across multiple instances requires understanding:

- **Runtime ID Generation**: Each instance generates a unique 8-byte hex token used in session isolation
- **Session Cookie Isolation**: Session cookies include runtime ID preventing collision but requiring instance-specific debugging approaches
- **Cross-Instance State Tracking**: Context state is isolated between instances requiring separate debugging sessions for each

## Background Initialization Process Debugging

The complex async initialization sequence creates debugging challenges:

- **Event Loop Thread Management**: `EventLoopThread` instances are pooled by name requiring understanding of thread lifecycle management
- **Deferred Task Coordination**: Background tasks run in separate event loops with complex dependency chains
- **Initialization Order Dependencies**: Strict ordering requirements between chat persistence, MCP servers, job loops, and model preloading
