# Agent Zero Integration Guide - Qwen Code Analyzer

This guide explains how to integrate the Qwen Code Analyzer into your Agent Zero workflow for enhanced code quality analysis and Qwen-specific optimization recommendations.

## Overview

The Qwen Code Analyzer provides comprehensive code analysis capabilities with optimizations specifically tailored for Qwen's coding strengths and patterns. It helps developers understand their codebase and get targeted suggestions for improvements that work well with Qwen's capabilities.

## Quick Integration

### Basic Setup

```python
# In your Agent Zero configuration or initialization
from tools.code_analyzer import CodeAnalyzer, AnalysisConfig

class QwenCodeAgent:
    def __init__(self):
        # Configure for Qwen integration
        config = AnalysisConfig(
            include_qwen_optimizations=True,
            focus_areas=['quality', 'performance', 'maintainability']
        )
        self.code_analyzer = CodeAnalyzer(config)

    def analyze_code_request(self, code: str, request_type: str = "general") -> dict:
        """Analyze code and prepare for Qwen processing."""
        # Analyze the code
        analysis = self.code_analyzer.analyze_code(code)

        # Get Qwen-specific recommendations
        qwen_recommendations = self.code_analyzer.get_qwen_recommendations(code)

        # Generate optimized prompt for Qwen
        qwen_prompt = self.code_analyzer.generate_qwen_prompt(analysis)

        return {
            "analysis": analysis,
            "qwen_prompt": qwen_prompt,
            "recommendations": qwen_recommendations,
            "quality_score": analysis.overall_score
        }
```

### Advanced Integration

```python
from tools.code_analyzer import CodeAnalyzer, AnalysisConfig, DetailLevel
from typing import Dict, List, Any

class AdvancedQwenCodeAgent:
    def __init__(self):
        # Advanced configuration
        config = AnalysisConfig(
            detail_level=DetailLevel.COMPREHENSIVE,
            include_qwen_optimizations=True,
            focus_areas=['performance', 'security', 'maintainability', 'quality'],
            performance_threshold=0.8,
            security_level='high',
            custom_rules={
                'max_function_length': 40,
                'require_type_hints': True,
                'preferred_patterns': ['list_comprehension', 'context_manager']
            }
        )
        self.code_analyzer = CodeAnalyzer(config)

    def process_codebase(self, directory: str) -> Dict[str, Any]:
        """Process entire codebase for comprehensive analysis."""
        project_analysis = self.code_analyzer.analyze_codebase(directory)

        # Generate prioritized improvement plan
        improvement_plan = self._create_improvement_plan(project_analysis)

        return {
            "project_analysis": project_analysis,
            "improvement_plan": improvement_plan,
            "qwen_integration_suggestions": project_analysis.qwen_integration_suggestions
        }

    def _create_improvement_plan(self, project_analysis) -> List[Dict[str, Any]]:
        """Create a prioritized plan for code improvements."""
        plan = []

        for file_analysis in project_analysis.files:
            if file_analysis.overall_score < 0.7:
                plan.append({
                    "file": file_analysis,  # This would need the filename
                    "priority": "high" if file_analysis.overall_score < 0.5 else "medium",
                    "focus_areas": self._identify_focus_areas(file_analysis),
                    "qwen_prompt": self.code_analyzer.generate_qwen_prompt(file_analysis)
                })

        return sorted(plan, key=lambda x: x["priority"])
```

## Integration Patterns

### Pattern 1: Pre-submission Analysis

```python
class PreSubmissionAnalyzer:
    def __init__(self):
        self.analyzer = CodeAnalyzer()

    def analyze_before_qwen(self, code: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze code before sending to Qwen."""
        # Get comprehensive analysis
        analysis = self.analyzer.analyze_code(code)

        # Check if code meets quality thresholds
        if analysis.overall_score < 0.5:
            return {
                "status": "needs_improvement",
                "analysis": analysis,
                "message": "Code quality is too low for effective Qwen processing",
                "suggestions": analysis.recommendations
            }

        # Generate optimized prompt for Qwen
        qwen_prompt = self.analyzer.generate_qwen_prompt(analysis)

        return {
            "status": "ready_for_qwen",
            "analysis": analysis,
            "qwen_prompt": qwen_prompt,
            "quality_score": analysis.overall_score
        }
```

### Pattern 2: Iterative Improvement

```python
class IterativeCodeImprover:
    def __init__(self):
        self.analyzer = CodeAnalyzer()
        self.improvement_history = []

    def improve_code_iteratively(self, initial_code: str, target_score: float = 0.8) -> Dict[str, Any]:
        """Iteratively improve code until target score is reached."""
        current_code = initial_code
        iterations = []

        while True:
            # Analyze current code
            analysis = self.analyzer.analyze_code(current_code)

            iterations.append({
                "iteration": len(iterations) + 1,
                "score": analysis.overall_score,
                "analysis": analysis
            })

            # Check if target reached
            if analysis.overall_score >= target_score:
                break

            # Generate Qwen prompt for improvement
            qwen_prompt = self.analyzer.generate_qwen_prompt(analysis)

            # Here you would send to Qwen and get improved code
            # improved_code = self.send_to_qwen(qwen_prompt)
            # current_code = improved_code

            # For demo, just break after first iteration
            break

        return {
            "iterations": iterations,
            "final_score": iterations[-1]["score"] if iterations else 0,
            "improvement_achieved": len(iterations) > 1
        }
```

### Pattern 3: Project-Wide Integration

```python
class ProjectCodeManager:
    def __init__(self):
        config = AnalysisConfig(detail_level=DetailLevel.STANDARD)
        self.analyzer = CodeAnalyzer(config)

    def manage_project_quality(self, project_directory: str) -> Dict[str, Any]:
        """Manage code quality across entire project."""
        # Analyze entire codebase
        project_analysis = self.analyzer.analyze_codebase(project_directory)

        # Generate project-wide insights
        insights = {
            "overall_health": project_analysis.average_quality_score,
            "total_files": project_analysis.total_files,
            "total_lines": project_analysis.total_lines,
            "recommendations": project_analysis.project_recommendations,
            "qwen_suggestions": project_analysis.qwen_integration_suggestions
        }

        # Create prioritized improvement backlog
        improvement_backlog = self._create_improvement_backlog(project_analysis)

        return {
            "insights": insights,
            "improvement_backlog": improvement_backlog,
            "qwen_ready_prompts": self._generate_qwen_prompts(project_analysis)
        }

    def _create_improvement_backlog(self, project_analysis) -> List[Dict[str, Any]]:
        """Create prioritized backlog of code improvements."""
        backlog = []

        for file_analysis in project_analysis.files:
            if file_analysis.overall_score < 0.8:  # Only include files needing improvement
                priority = self._calculate_priority(file_analysis)

                backlog.append({
                    "file": "unknown_filename",  # Would need to track filenames
                    "current_score": file_analysis.overall_score,
                    "priority": priority,
                    "focus_areas": self._identify_focus_areas(file_analysis),
                    "estimated_effort": self._estimate_effort(file_analysis)
                })

        return sorted(backlog, key=lambda x: x["priority"])
```

## Configuration for Agent Zero

### Basic Configuration

```json
{
  "qwen_tools": {
    "code_analyzer": {
      "enabled": true,
      "auto_analyze_threshold": 0.6,
      "focus_areas": ["quality", "performance"],
      "include_qwen_optimizations": true
    }
  }
}
```

### Advanced Configuration

```json
{
  "qwen_tools": {
    "code_analyzer": {
      "enabled": true,
      "detail_level": "comprehensive",
      "focus_areas": ["performance", "security", "maintainability", "quality"],
      "include_qwen_optimizations": true,
      "performance_threshold": 0.8,
      "security_level": "high",
      "custom_rules": {
        "max_function_length": 40,
        "require_type_hints": true,
        "preferred_patterns": ["list_comprehension", "context_manager"]
      },
      "project_analysis": {
        "enabled": true,
        "auto_analyze_on_save": true,
        "report_generation": true,
        "report_format": "markdown"
      }
    }
  }
}
```

## Usage Examples

### Example 1: Basic Code Analysis

```python
# Analyze code before sending to Qwen
code = """
def calculate_total(items):
    total = 0
    for item in items:
        total += item
    return total
"""

analysis = code_analyzer.analyze_code(code)
print(f"Quality Score: {analysis.quality_score:.2f}")

if analysis.overall_score < 0.7:
    # Generate Qwen prompt for improvement
    qwen_prompt = code_analyzer.generate_qwen_prompt(analysis)
    print(f"Qwen Prompt: {qwen_prompt}")
```

### Example 2: Performance-Focused Analysis

```python
# Configure for performance analysis
config = AnalysisConfig(
    focus_areas=['performance'],
    detail_level=DetailLevel.COMPREHENSIVE,
    performance_threshold=0.8
)

performance_analyzer = CodeAnalyzer(config)
perf_analysis = performance_analyzer.analyze_code(inefficient_code)

# Get performance-specific recommendations
perf_recommendations = [rec for rec in perf_analysis.recommendations
                       if 'performance' in rec.lower() or 'efficient' in rec.lower()]
```

### Example 3: Project-Wide Analysis

```python
# Analyze entire project
project_analysis = code_analyzer.analyze_codebase("/path/to/project")

print(f"Project Quality Score: {project_analysis.average_quality_score:.2f}")
print(f"Total Files: {project_analysis.total_files}")
print(f"Total Lines: {project_analysis.total_lines}")

# Get project-wide recommendations
for rec in project_analysis.project_recommendations:
    print(f"- {rec}")

# Get Qwen integration suggestions
for suggestion in project_analysis.qwen_integration_suggestions:
    print(f"Qwen: {suggestion}")
```

## Best Practices

### 1. Threshold-Based Processing

```python
def should_use_qwen(code_analysis) -> bool:
    """Determine if code should be sent to Qwen for improvement."""
    return (
        code_analysis.overall_score < 0.7 or  # Generally poor quality
        code_analysis.performance_score < 0.6 or  # Performance issues
        code_analysis.security_score < 0.8 or    # Security concerns
        len(code_analysis.issues) > 5  # Multiple issues
    )

def process_with_qwen_fallback(code: str) -> str:
    """Process code with Qwen fallback for poor quality code."""
    analysis = code_analyzer.analyze_code(code)

    if should_use_qwen(analysis):
        # Generate optimized prompt for Qwen
        qwen_prompt = code_analyzer.generate_qwen_prompt(analysis)

        # Send to Qwen for improvement
        # improved_code = send_to_qwen(qwen_prompt)
        return "improved_code_from_qwen"

    return code
```

### 2. Context-Aware Analysis

```python
def analyze_with_context(code: str, context: Dict[str, Any]) -> Dict[str, Any]:
    """Analyze code with additional context."""
    # Adjust analysis based on context
    config = AnalysisConfig()

    if context.get("framework") == "flask":
        config.custom_rules["flask_patterns"] = True
    if context.get("performance_critical"):
        config.focus_areas.insert(0, "performance")

    analyzer = CodeAnalyzer(config)
    return analyzer.analyze_code(code)
```

### 3. Batch Processing Optimization

```python
def batch_analyze_and_optimize(codes: List[str]) -> List[Dict[str, Any]]:
    """Batch analyze multiple code snippets efficiently."""
    results = []

    for code in codes:
        analysis = code_analyzer.analyze_code(code)

        result = {
            "code": code,
            "analysis": analysis,
            "needs_qwen": analysis.overall_score < 0.7,
            "qwen_prompt": code_analyzer.generate_qwen_prompt(analysis) if analysis.overall_score < 0.7 else None
        }

        results.append(result)

    return results
```

## Performance Considerations

- **Incremental Analysis**: Only re-analyze changed files in large projects
- **Caching**: Cache analysis results for frequently accessed code
- **Selective Focus**: Use focus areas to limit analysis scope when possible
- **Background Processing**: Run analysis in background for better user experience

## Troubleshooting

### Common Issues

1. **Slow Analysis**: Reduce detail level or focus areas for faster results
2. **Memory Usage**: Process large codebases in smaller chunks
3. **Language Detection**: Specify language explicitly if auto-detection fails
4. **Missing Context**: Provide project context for better recommendations

### Debugging

```python
def debug_analysis(code: str) -> Dict[str, Any]:
    """Debug analysis process step by step."""
    # Test language detection
    language = code_analyzer._detect_language(code)

    # Test analysis
    analysis = code_analyzer.analyze_code(code, language)

    # Test Qwen prompt generation
    qwen_prompt = code_analyzer.generate_qwen_prompt(analysis)

    return {
        "detected_language": language,
        "analysis": analysis,
        "qwen_prompt": qwen_prompt,
        "analysis_time": "measured_time",
        "prompt_quality": len(qwen_prompt.split()) > 10  # Simple quality check
    }
```

## Contributing

When extending the integration:

1. Follow existing configuration patterns
2. Maintain performance characteristics
3. Add appropriate error handling
4. Include comprehensive testing
5. Document new integration patterns

This integration provides a solid foundation for enhancing code quality analysis in Agent Zero while maintaining flexibility for customization and extension.