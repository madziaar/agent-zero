# Qwen Code Analyzer

A comprehensive toolkit for analyzing code and providing Qwen-specific optimization recommendations. This tool helps developers understand their codebase and get targeted suggestions for improvements that work well with Qwen's coding capabilities.

## Features

- **Code Quality Analysis**: Comprehensive analysis of code structure, patterns, and best practices
- **Qwen-Specific Recommendations**: Optimization suggestions tailored for Qwen's coding strengths
- **Performance Analysis**: Identify performance bottlenecks and optimization opportunities
- **Security Scanning**: Basic security vulnerability detection and recommendations
- **Complexity Metrics**: Measure code complexity and suggest refactoring opportunities
- **Language-Specific Analysis**: Support for multiple programming languages with language-specific insights

## Installation

```bash
pip install -r requirements.txt
```

## Quick Start

### Basic Usage

```python
from code_analyzer import CodeAnalyzer

analyzer = CodeAnalyzer()

# Analyze a code file
with open('example.py', 'r') as f:
    code = f.read()

analysis = analyzer.analyze_code(code, language='python')
print(f"Overall Quality Score: {analysis.quality_score}")
print(f"Complexity Score: {analysis.complexity_score}")

# Get Qwen-specific recommendations
recommendations = analyzer.get_qwen_recommendations(code)
for rec in recommendations:
    print(f"- {rec}")
```

### Advanced Usage

```python
from code_analyzer import CodeAnalyzer, AnalysisConfig

# Configure for specific analysis needs
config = AnalysisConfig(
    focus_areas=['performance', 'security', 'maintainability'],
    detail_level='comprehensive',
    include_qwen_optimizations=True
)

analyzer = CodeAnalyzer(config)

# Analyze with context
context = {
    'framework': 'Flask',
    'purpose': 'REST API',
    'team_size': 5
}

analysis = analyzer.analyze_code_with_context(code, context)
```

## Core Components

### CodeAnalyzer Class

Main class for code analysis and optimization recommendations.

**Methods:**

- `analyze_code(code: str, language: str = 'auto') -> CodeAnalysis`: Analyze code and return comprehensive results
- `get_qwen_recommendations(code: str) -> List[str]`: Get Qwen-specific optimization suggestions
- `analyze_codebase(directory: str) -> ProjectAnalysis`: Analyze entire codebase
- `compare_code_versions(old_code: str, new_code: str) -> ComparisonResult`: Compare code quality between versions

### AnalysisConfig Class

Configuration for customizing analysis behavior.

**Options:**

- `focus_areas`: List of analysis areas to prioritize
- `detail_level`: Level of detail in analysis ('basic', 'standard', 'comprehensive')
- `include_qwen_optimizations`: Whether to include Qwen-specific recommendations
- `performance_threshold`: Threshold for performance recommendations
- `security_level`: Security analysis sensitivity level

## Supported Languages

- **Python** (Primary focus - optimized for Qwen's Python strengths)
- **JavaScript/TypeScript**
- **Java**
- **C++**
- **Go**
- **Rust**

## Analysis Areas

### Code Quality

- Code structure and organization
- Naming conventions and readability
- Documentation completeness
- Error handling patterns

### Performance

- Algorithm efficiency analysis
- Resource usage patterns
- Bottleneck identification
- Optimization opportunities

### Security

- Common vulnerability patterns
- Input validation issues
- Authentication/authorization problems
- Data exposure risks

### Maintainability

- Code complexity metrics
- Duplication detection
- Testing coverage suggestions
- Refactoring opportunities

## Qwen-Specific Features

### Coding Pattern Optimization

The analyzer provides recommendations specifically tailored for Qwen's coding capabilities:

- **Function Structure**: Optimal function length and complexity for Qwen
- **Documentation Style**: Documentation patterns that work well with Qwen's understanding
- **Error Handling**: Patterns that help Qwen generate better error handling code
- **Algorithm Presentation**: Ways to structure algorithmic code for better Qwen comprehension

### Prompt Optimization Integration

Works seamlessly with the Prompt Optimizer to suggest better ways to ask Qwen for code improvements:

```python
# Get analysis
analysis = analyzer.analyze_code(problematic_code)

# Generate optimized prompt for Qwen
prompt_suggestion = analyzer.generate_qwen_prompt(analysis)
print(f"Suggested prompt: {prompt_suggestion}")
```

## Examples

### Example 1: Basic Code Analysis

```python
from code_analyzer import CodeAnalyzer

analyzer = CodeAnalyzer()
code = '''
def calculate_total(items):
    total = 0
    for item in items:
        total += item
    return total
'''

analysis = analyzer.analyze_code(code, language='python')
print(f"Quality Score: {analysis.quality_score:.2f}")
print(f"Issues Found: {len(analysis.issues)}")
print(f"Recommendations: {len(analysis.recommendations)}")
```

### Example 2: Qwen-Specific Recommendations

```python
# Get Qwen-tailored suggestions
qwen_recs = analyzer.get_qwen_recommendations(code)
print("Qwen Optimization Suggestions:")
for rec in qwen_recs:
    print(f"- {rec}")

# Generate optimal prompt for Qwen
optimal_prompt = analyzer.generate_optimal_qwen_prompt(code)
print(f"\nOptimal Qwen Prompt: {optimal_prompt}")
```

### Example 3: Performance Analysis

```python
# Analyze for performance issues
performance_analysis = analyzer.analyze_performance(code)
print(f"Performance Score: {performance_analysis.score}")
print("Performance Issues:")
for issue in performance_analysis.issues:
    print(f"- {issue.severity}: {issue.description}")
```

## Integration with Agent Zero

### Basic Integration

```python
# In your Agent Zero workflow
from code_analyzer import CodeAnalyzer

class QwenCodeAgent:
    def __init__(self):
        self.code_analyzer = CodeAnalyzer()

    def analyze_and_optimize(self, code: str, request_type: str = "general"):
        """Analyze code and prepare for Qwen optimization."""
        # Analyze the code
        analysis = self.code_analyzer.analyze_code(code)

        # Get Qwen-specific recommendations
```
