# Agent Zero Integration Guide - Qwen Prompt Optimizer

This guide explains how to integrate the Qwen Prompt Optimizer into your Agent Zero workflow for enhanced prompt quality and Qwen-specific optimizations.

## Overview

The Qwen Prompt Optimizer provides tools to analyze, optimize, and enhance prompts specifically for Qwen models, improving response quality and coding effectiveness in Agent Zero.

## Quick Integration

### Basic Setup

```python
# In your Agent Zero configuration or initialization
from tools.prompt_optimizer import PromptOptimizer, OptimizationConfig, ModelType

class QwenAgent:
    def __init__(self):
        # Configure for Qwen Coder
        config = OptimizationConfig(
            model_type=ModelType.QWEN_CODER,
            optimization_level="standard"
        )
        self.prompt_optimizer = PromptOptimizer(config)

    def process_request(self, user_prompt: str) -> str:
        """Process user requests with prompt optimization."""
        # Analyze current prompt
        analysis = self.prompt_optimizer.analyze_prompt(user_prompt)

        # Optimize for Qwen if score is below threshold
        if analysis.overall_score < 0.7:
            optimized_prompt = self.prompt_optimizer.optimize_prompt(user_prompt)
            print(f"Prompt optimized: {analysis.overall_score:.2f} -> {self.prompt_optimizer.analyze_prompt(optimized_prompt).overall_score:.2f}")
            return optimized_prompt

        return user_prompt
```

### Advanced Integration

```python
from tools.prompt_optimizer import QwenPromptTemplate
from typing import Dict, Any

class AdvancedQwenAgent:
    def __init__(self):
        config = OptimizationConfig(
            model_type=ModelType.QWEN_CODER,
            optimization_level="advanced",
            qwen_specific_features={
                "use_reasoning_tags": True,
                "context_window_optimization": True,
                "token_efficiency": True
            }
        )
        self.prompt_optimizer = PromptOptimizer(config)

    def optimize_coding_request(self, task: str, language: str = "Python",
                              constraints: List[str] = None) -> str:
        """Optimize coding-specific requests."""
        # Create template for coding task
        template = QwenPromptTemplate.coding_task(
            task=task,
            language=language,
            constraints=constraints or []
        )

        # Optimize the template
        return self.prompt_optimizer.optimize_prompt(template)

    def optimize_debugging_request(self, error: str, context: str = None) -> str:
        """Optimize debugging requests."""
        template = QwenPromptTemplate.debugging_task(
            error_description=error,
            code_context=context
        )

        return self.prompt_optimizer.optimize_prompt(template)

    def batch_optimize(self, prompts: List[str]) -> List[str]:
        """Batch optimize multiple prompts."""
        return [self.prompt_optimizer.optimize_prompt(p) for p in prompts]
```

## Integration Patterns

### Pattern 1: Pre-processing Middleware

```python
class PromptOptimizationMiddleware:
    def __init__(self):
        self.optimizer = PromptOptimizer()

    def process(self, messages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Process messages before sending to Qwen."""
        for message in messages:
            if message.get("role") == "user":
                original_content = message.get("content", "")
                optimized_content = self.optimizer.optimize_prompt(original_content)
                message["content"] = optimized_content

        return messages
```

### Pattern 2: Context-Aware Optimization

```python
class ContextAwareOptimizer:
    def __init__(self):
        self.optimizer = PromptOptimizer()

    def optimize_with_context(self, prompt: str, context: Dict[str, Any]) -> str:
        """Optimize prompt based on conversation context."""
        # Analyze context to determine optimization strategy
        if context.get("last_error"):
            # Use debugging template for error scenarios
            template = QwenPromptTemplate.debugging_task(
                error_description=context["last_error"],
                code_context=context.get("code_snippet")
            )
            return self.optimizer.optimize_prompt(template)

        elif context.get("task_type") == "coding":
            # Use coding template for coding tasks
            template = QwenPromptTemplate.coding_task(
                task=prompt,
                language=context.get("preferred_language", "Python")
            )
            return self.optimizer.optimize_prompt(template)

        else:
            # Standard optimization
            return self.optimizer.optimize_prompt(prompt)
```

### Pattern 3: Performance Monitoring

```python
class OptimizationMonitor:
    def __init__(self):
        self.optimizer = PromptOptimizer()
        self.metrics = []

    def process_and_monitor(self, prompt: str) -> Tuple[str, Dict[str, Any]]:
        """Process prompt and collect metrics."""
        # Original analysis
        original_analysis = self.optimizer.analyze_prompt(prompt)

        # Optimization
        optimized_prompt = self.optimizer.optimize_prompt(prompt)

        # Optimized analysis
        optimized_analysis = self.optimizer.analyze_prompt(optimized_prompt)

        # Collect metrics
        metrics = {
            "original_score": original_analysis.overall_score,
            "optimized_score": optimized_analysis.overall_score,
            "improvement": optimized_analysis.overall_score - original_analysis.overall_score,
            "issues_resolved": len(original_analysis.issues) - len(optimized_analysis.issues)
        }

        self.metrics.append(metrics)
        return optimized_prompt, metrics

    def get_average_improvement(self) -> float:
        """Get average improvement across all optimizations."""
        if not self.metrics:
            return 0.0
        return sum(m["improvement"] for m in self.metrics) / len(self.metrics)
```

## Configuration for Agent Zero

### Basic Configuration

Add to your Agent Zero configuration:

```json
{
  "qwen_tools": {
    "prompt_optimizer": {
      "enabled": true,
      "model_type": "qwen-coder",
      "optimization_level": "standard",
      "auto_optimize_threshold": 0.7
    }
  }
}
```

### Advanced Configuration

```json
{
  "qwen_tools": {
    "prompt_optimizer": {
      "enabled": true,
      "model_type": "qwen-coder",
      "optimization_level": "advanced",
      "qwen_specific_features": {
        "use_reasoning_tags": true,
        "context_window_optimization": true,
        "token_efficiency": true
      },
      "custom_templates": {
        "coding_task": {
          "include_error_handling": true,
          "include_documentation": true,
          "language_preference": "Python"
        }
      },
      "performance_monitoring": {
        "enabled": true,
        "log_metrics": true,
        "metrics_file": "optimization_metrics.json"
      }
    }
  }
}
```

## Usage Examples

### Example 1: Coding Task Optimization

```python
# User request
user_request = "Write a function to calculate fibonacci numbers"

# Create optimized coding prompt
template = QwenPromptTemplate.coding_task(
    task=user_request,
    language="Python",
    constraints=["use memoization", "include error handling", "add documentation"]
)

optimized_prompt = optimizer.optimize_prompt(template)
# Result: Well-structured prompt with specific requirements and constraints
```

### Example 2: Debugging Integration

```python
# Error scenario
error_context = {
    "error_message": "TypeError: 'int' object is not iterable",
    "code_snippet": "for item in items: process(item)",
    "environment": "Python 3.9, Flask application"
}

# Create debugging prompt
debug_template = QwenPromptTemplate.debugging_task(
    error_description=error_context["error_message"],
    code_context=error_context["code_snippet"]
)

optimized_debug_prompt = optimizer.optimize_prompt(debug_template)
```

### Example 3: Batch Processing

```python
# Multiple requests
requests = [
    "Help me write Python code",
    "Debug this error",
    "Review my code",
    "Optimize this algorithm"
]

# Batch optimize all requests
optimized_requests = optimizer.compare_prompts(requests)
# Returns analysis and recommendations for all prompts
```

## Best Practices

### 1. Threshold-Based Optimization

```python
def should_optimize(analysis) -> bool:
    """Determine if prompt should be optimized."""
    return (
        analysis.overall_score < 0.7 or  # Low overall score
        analysis.clarity_score < 0.6 or   # Unclear prompt
        analysis.specificity_score < 0.6 or  # Too vague
        len(analysis.issues) > 2  # Multiple issues
    )
```

### 2. Context Preservation

````python
def optimize_with_context(prompt: str, context: Dict[str, Any]) -> str:
    """Optimize while preserving important context."""
    # Don't optimize if prompt already has good structure
    analysis = optimizer.analyze_prompt(prompt)
    if analysis.structure_score > 0.8:
        return prompt

    # Optimize but preserve code snippets and specific requirements
    optimized = optimizer.optimize_prompt(prompt)

    # Ensure important context is maintained
    if "```" in prompt and "```" not in optimized:
        optimized += "\n\n" + prompt[prompt.find("```"):]

    return optimized
````

### 3. Performance Optimization

```python
import functools

@functools.lru_cache(maxsize=1000)
def cached_optimize(prompt: str) -> str:
    """Cache optimization results for similar prompts."""
    return optimizer.optimize_prompt(prompt)

# Use in high-frequency scenarios
optimized = cached_optimize(user_prompt)
```

## Troubleshooting

### Common Issues

1. **Over-optimization**: If prompts become too verbose, adjust optimization level to "basic"
2. **Context Loss**: Ensure important code snippets and requirements are preserved
3. **Performance Impact**: Use caching for high-frequency optimization scenarios

### Debugging

```python
def debug_optimization(prompt: str) -> Dict[str, Any]:
    """Debug optimization process."""
    original_analysis = optimizer.analyze_prompt(prompt)
    optimized_prompt = optimizer.optimize_prompt(prompt)
    optimized_analysis = optimizer.analyze_prompt(optimized_prompt)

    return {
        "original": {
            "prompt": prompt,
            "analysis": original_analysis
        },
        "optimized": {
            "prompt": optimized_prompt,
            "analysis": optimized_analysis
        },
        "improvement": {
            "score_delta": optimized_analysis.overall_score - original_analysis.overall_score,
            "issues_resolved": len(original_analysis.issues) - len(optimized_analysis.issues)
        }
    }
```

## Performance Considerations

- **Lightweight**: No external dependencies for basic functionality
- **Fast Analysis**: Prompt analysis typically takes <100ms
- **Memory Efficient**: Minimal memory footprint for optimization operations
- **Scalable**: Suitable for batch processing and high-frequency scenarios

## Contributing

When extending the integration:

1. Follow the existing configuration patterns
2. Maintain backward compatibility
3. Add appropriate error handling
4. Include performance considerations
5. Document new integration patterns

This integration provides a solid foundation for enhancing prompt quality in Agent Zero while maintaining flexibility for customization and extension.
