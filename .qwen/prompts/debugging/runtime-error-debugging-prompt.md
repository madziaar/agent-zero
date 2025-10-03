# Runtime Error Debugging Prompt Template

**Qwen Model Optimization**: 14B (Runtime error analysis with comprehensive debugging strategy)

```
Debug this critical runtime error with systematic analysis and resolution strategy:

**Error Context & Analysis:**

**Complete Error Information:**
- Exact error message and exception details
- Full stack trace with line numbers and method calls
- System configuration and environment specifications
- Recent code changes or deployments that may be related
- Frequency and conditions under which the error occurs

**System State Investigation:**
- Application state at time of error occurrence
- Memory usage and resource consumption patterns
- Database connection status and transaction state
- External service dependencies and their availability
- Configuration settings and environment variables

**Code Path Analysis:**
- Step-by-step execution path leading to the error
- Variable values and data state at critical points
- Conditional logic evaluation and branching decisions
- Resource initialization and cleanup sequence verification
- Exception handling implementation and effectiveness

**Root Cause Identification Strategy:**
- Exception hierarchy analysis and error propagation patterns
- Resource availability and constraint validation
- Concurrency issues and race condition assessment
- External dependency failure impact analysis
- Configuration and environment mismatch identification

**Debugging Implementation Plan:**
- Strategic logging placement for state tracking
- Breakpoint identification for step-through debugging
- Test case development for error reproduction
- Monitoring and alerting setup for early detection
- Rollback strategy for debugging-related changes

**Immediate Mitigation:**
- Temporary workaround for production stability
- Error handling improvements to prevent crashes
- User-friendly error messages and graceful degradation
- Monitoring alerts for error occurrence tracking
- Documentation for operations team reference

**Long-term Resolution:**
- Permanent fix implementation with proper validation
- Prevention measures for similar error types
- Code review and testing strategy improvements
- Documentation updates for future maintenance
- Team training and knowledge sharing

**Testing & Validation Strategy:**
- Unit test development for error scenario coverage
- Integration test implementation for component interaction
- Load testing for concurrent error condition validation
- Regression testing for fix verification
- Production monitoring for error resolution confirmation

**Deliverables:**
1. Root cause analysis report with detailed findings
2. Immediate mitigation strategy and implementation
3. Long-term resolution plan with timeline and effort estimates
4. Testing strategy and automated test recommendations
5. Monitoring and alerting configuration guidelines
6. Documentation updates for error handling procedures
7. Team training materials and knowledge base articles

**Success Criteria:**
- Error completely eliminated from production environment
- Comprehensive error handling implemented for similar scenarios
- Monitoring and alerting in place for early error detection
- Documentation updated for operations team reference
- Team understanding improved for future error prevention
- Testing coverage enhanced for error scenario validation

Focus on delivering a robust debugging solution that not only fixes the immediate issue but also strengthens the overall system reliability and team debugging capabilities.
```
