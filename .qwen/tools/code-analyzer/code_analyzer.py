#!/usr/bin/env python3
"""
Qwen Code Analyzer - Core functionality for analyzing code and providing Qwen-specific recommendations.

This module provides comprehensive code analysis capabilities with optimizations
specifically tailored for Qwen's coding strengths and patterns.
"""

import ast
import re
import json
import os
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Language(Enum):
    """Supported programming languages."""
    PYTHON = "python"
    JAVASCRIPT = "javascript"
    TYPESCRIPT = "typescript"
    JAVA = "java"
    CPP = "cpp"
    GO = "go"
    RUST = "rust"
    AUTO = "auto"


class DetailLevel(Enum):
    """Level of detail for analysis."""
    BASIC = "basic"
    STANDARD = "standard"
    COMPREHENSIVE = "comprehensive"


class Severity(Enum):
    """Severity levels for issues."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class CodeIssue:
    """Represents a code issue found during analysis."""
    line_number: int
    column: int
    severity: Severity
    category: str
    message: str
    suggestion: str
    qwen_impact: str  # How this affects Qwen's ability to work with the code


@dataclass
class CodeMetrics:
    """Code quality metrics."""
    lines_of_code: int
    cyclomatic_complexity: float
    maintainability_index: float
    code_duplication_ratio: float
    test_coverage_suggestion: float
    performance_score: float
    security_score: float


@dataclass
class CodeAnalysis:
    """Results of code analysis."""
    quality_score: float
    complexity_score: float
    maintainability_score: float
    performance_score: float
    security_score: float
    overall_score: float
    issues: List[CodeIssue]
    metrics: CodeMetrics
    recommendations: List[str]
    qwen_optimizations: List[str]
    language: str


@dataclass
class ProjectAnalysis:
    """Analysis results for entire project."""
    total_files: int
    total_lines: int
    average_quality_score: float
    files: List[CodeAnalysis]
    project_recommendations: List[str]
    qwen_integration_suggestions: List[str]


@dataclass
class AnalysisConfig:
    """Configuration for code analysis."""
    focus_areas: List[str] = None
    detail_level: DetailLevel = DetailLevel.STANDARD
    include_qwen_optimizations: bool = True
    performance_threshold: float = 0.7
    security_level: str = "standard"
    custom_rules: Dict[str, Any] = None

    def __post_init__(self):
        if self.focus_areas is None:
            self.focus_areas = ['quality', 'performance', 'security', 'maintainability']
        if self.custom_rules is None:
            self.custom_rules = {}


class PythonAnalyzer:
    """Specialized analyzer for Python code."""

    def __init__(self):
        self.qwen_patterns = {
            'pythonic_patterns': [
                'list_comprehension', 'dict_comprehension', 'generator_expression',
                'context_manager', 'decorator', 'descriptor'
            ],
            'performance_patterns': [
                'memoization', 'caching', 'lazy_evaluation', 'vectorization'
            ],
            'structure_patterns': [
                'class_organization', 'module_structure', 'import_optimization'
            ]
        }

    def analyze_python_file(self, code: str, filename: str = "") -> CodeAnalysis:
        """Analyze Python code comprehensively."""
        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            return self._create_syntax_error_analysis(e, filename)

        # Calculate metrics
        metrics = self._calculate_python_metrics(tree, code)

        # Find issues
        issues = self._find_python_issues(tree, code)

        # Calculate scores
        scores = self._calculate_python_scores(metrics, issues)

        # Generate recommendations
        recommendations = self._generate_python_recommendations(issues, metrics)

        # Generate Qwen-specific optimizations
        qwen_optimizations = self._generate_qwen_optimizations(tree, code)

        return CodeAnalysis(
            quality_score=scores['quality'],
            complexity_score=scores['complexity'],
            maintainability_score=scores['maintainability'],
            performance_score=scores['performance'],
            security_score=scores['security'],
            overall_score=scores['overall'],
            issues=issues,
            metrics=metrics,
            recommendations=recommendations,
            qwen_optimizations=qwen_optimizations,
            language='python'
        )

    def _calculate_python_metrics(self, tree: ast.AST, code: str) -> CodeMetrics:
        """Calculate comprehensive metrics for Python code."""
        lines = code.split('\n')

        # Basic metrics
        lines_of_code = len([line for line in lines if line.strip()])

        # Cyclomatic complexity (simplified calculation)
        complexity_nodes = len([node for node in ast.walk(tree)
                               if isinstance(node, (ast.If, ast.For, ast.While, ast.With, ast.Try, ast.FunctionDef))])
        cyclomatic_complexity = max(1, complexity_nodes / 10)  # Normalized

        # Maintainability index (simplified)
        avg_line_length = sum(len(line) for line in lines) / len(lines) if lines else 0
        maintainability_index = max(0, 100 - (avg_line_length * 0.1) - (complexity_nodes * 0.5))

        # Duplication ratio (simplified)
        code_duplication_ratio = self._calculate_duplication_ratio(code)

        # Test coverage suggestion
        test_coverage_suggestion = self._estimate_test_coverage(tree)

        # Performance score
        performance_score = self._calculate_performance_score(tree)

        # Security score
        security_score = self._calculate_security_score(tree, code)

        return CodeMetrics(
            lines_of_code=lines_of_code,
            cyclomatic_complexity=cyclomatic_complexity,
            maintainability_index=maintainability_index,
            code_duplication_ratio=code_duplication_ratio,
            test_coverage_suggestion=test_coverage_suggestion,
            performance_score=performance_score,
            security_score=security_score
        )

    def _find_python_issues(self, tree: ast.AST, code: str) -> List[CodeIssue]:
        """Find issues in Python code."""
        issues = []

        # Check for common issues
        issues.extend(self._check_naming_conventions(tree))
        issues.extend(self._check_code_structure(tree))
        issues.extend(self._check_error_handling(tree))
        issues.extend(self._check_performance_issues(tree, code))
        issues.extend(self._check_security_issues(tree, code))

        return sorted(issues, key=lambda x: (x.line_number, x.severity.value))

    def _check_naming_conventions(self, tree: ast.AST) -> List[CodeIssue]:
        """Check Python naming conventions."""
        issues = []

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if not node.name.islower() or '_' not in node.name:
                    issues.append(CodeIssue(
                        line_number=node.lineno,
                        column=node.col_offset,
                        severity=Severity.LOW,
                        category="naming",
                        message=f"Function '{node.name}' should use snake_case",
                        suggestion=f"Rename to: {node.name.lower().replace(' ', '_')}",
                        qwen_impact="Qwen works better with conventional Python naming"
                    ))

            elif isinstance(node, ast.ClassDef):
                if not node.name[0].isupper():
                    issues.append(CodeIssue(
                        line_number=node.lineno,
                        column=node.col_offset,
                        severity=Severity.LOW,
                        category="naming",
                        message=f"Class '{node.name}' should use PascalCase",
                        suggestion=f"Rename to: {node.name.capitalize()}",
                        qwen_impact="Qwen expects standard Python class naming"
                    ))

        return issues

    def _check_code_structure(self, tree: ast.AST) -> List[CodeIssue]:
        """Check code structure and organization."""
        issues = []

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # Check function length
                if hasattr(node, 'end_lineno') and node.end_lineno:
                    func_length = node.end_lineno - node.lineno
                    if func_length > 50:
                        issues.append(CodeIssue(
                            line_number=node.lineno,
                            column=node.col_offset,
                            severity=Severity.MEDIUM,
                            category="structure",
                            message=f"Function '{node.name}' is too long ({func_length} lines)",
                            suggestion="Break into smaller, focused functions",
                            qwen_impact="Qwen works better with smaller, focused functions"
                        ))

                # Check for missing docstrings
                if not ast.get_docstring(node):
                    issues.append(CodeIssue(
                        line_number=node.lineno,
                        column=node.col_offset,
                        severity=Severity.LOW,
                        category="documentation",
                        message=f"Function '{node.name}' missing docstring",
                        suggestion="Add a docstring explaining the function's purpose",
                        qwen_impact="Qwen understands documented code better"
                    ))

        return issues

    def _check_error_handling(self, tree: ast.AST) -> List[CodeIssue]:
        """Check error handling patterns."""
        issues = []

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # Check if function handles potential exceptions
                has_try = False
                has_return = False

                for child in ast.walk(node):
                    if isinstance(child, ast.Try):
                        has_try = True
                    elif isinstance(child, ast.Return):
                        has_return = True

                if has_return and not has_try:
                    issues.append(CodeIssue(
                        line_number=node.lineno,
                        column=node.col_offset,
                        severity=Severity.MEDIUM,
                        category="error_handling",
                        message=f"Function '{node.name}' returns values but lacks error handling",
                        suggestion="Consider adding try-catch blocks for robust error handling",
                        qwen_impact="Qwen can help implement better error handling patterns"
                    ))

        return issues

    def _check_performance_issues(self, tree: ast.AST, code: str) -> List[CodeIssue]:
        """Check for performance issues."""
        issues = []

        # Check for inefficient loops
        lines = code.split('\n')
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            if ('for' in stripped and 'append' in stripped and
                stripped.endswith(')')):
                issues.append(CodeIssue(
                    line_number=i,
                    column=0,
                    severity=Severity.MEDIUM,
                    category="performance",
                    message="Potential inefficient list building pattern",
                    suggestion="Consider using list comprehension",
                    qwen_impact="Qwen excels at optimizing list comprehensions"
                ))

        return issues

    def _check_security_issues(self, tree: ast.AST, code: str) -> List[CodeIssue]:
        """Check for security issues."""
        issues = []

        # Check for use of eval (security risk)
        if 'eval(' in code:
            lines = code.split('\n')
            for i, line in enumerate(lines, 1):
                if 'eval(' in line:
                    issues.append(CodeIssue(
                        line_number=i,
                        column=line.find('eval('),
                        severity=Severity.HIGH,
                        category="security",
                        message="Use of eval() is a security risk",
                        suggestion="Avoid eval() or use ast.literal_eval() for safe evaluation",
                        qwen_impact="Qwen can help implement safer alternatives"
                    ))

        # Check for input validation
        input_functions = ['input(', 'raw_input(']
        for func in input_functions:
            if func in code:
                lines = code.split('\n')
                for i, line in enumerate(lines, 1):
                    if func in line:
                        issues.append(CodeIssue(
                            line_number=i,
                            column=line.find(func),
                            severity=Severity.MEDIUM,
                            category="security",
                            message="Input function without validation",
                            suggestion="Add input validation and sanitization",
                            qwen_impact="Qwen can help implement proper input validation"
                        ))

        return issues

    def _calculate_duplication_ratio(self, code: str) -> float:
        """Calculate code duplication ratio."""
        lines = [line.strip() for line in code.split('\n') if line.strip()]

        if len(lines) < 10:
            return 0.0

        # Simple duplication detection
        duplicates = 0
        seen = set()

        for line in lines:
            if line in seen:
                duplicates += 1
            else:
                seen.add(line)

        return duplicates / len(lines)

    def _estimate_test_coverage(self, tree: ast.AST) -> float:
        """Estimate suggested test coverage."""
        functions = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]

        if not functions:
            return 1.0  # No functions to test

        # Simple heuristic: suggest 80% coverage for complex functions
        complex_functions = [f for f in functions if self._calculate_function_complexity(f) > 3]
        return max(0.5, 1.0 - (len(complex_functions) * 0.1))

    def _calculate_function_complexity(self, func: ast.FunctionDef) -> int:
        """Calculate function complexity."""
        complexity = 1  # Base complexity

        for node in ast.walk(func):
            if isinstance(node, (ast.If, ast.For, ast.While, ast.With, ast.Try)):
                complexity += 1

        return complexity

    def _calculate_performance_score(self, tree: ast.AST) -> float:
        """Calculate performance score."""
        # Simple heuristic based on code patterns
        performance_indicators = 0

        for node in ast.walk(tree):
            if isinstance(node, ast.ListComp):
                performance_indicators += 0.2
            elif isinstance(node, ast.GeneratorExp):
                performance_indicators += 0.3
            elif isinstance(node, ast.With):  # Context managers
                performance_indicators += 0.1

        return min(1.0, 0.5 + performance_indicators)

    def _calculate_security_score(self, tree: ast.AST, code: str) -> float:
        """Calculate security score."""
        # Start with perfect score
        security_score = 1.0

        # Deduct for security issues
        if 'eval(' in code:
            security_score -= 0.3

        if 'input(' in code and 'validate' not in code.lower():
            security_score -= 0.2

        if 'exec(' in code:
            security_score -= 0.4

        return max(0.0, security_score)

    def _calculate_python_scores(self, metrics: CodeMetrics, issues: List[CodeIssue]) -> Dict[str, float]:
        """Calculate overall scores from metrics and issues."""
        # Quality score based on issues and metrics
        critical_issues = len([i for i in issues if i.severity == Severity.CRITICAL])
        high_issues = len([i for i in issues if i.severity == Severity.HIGH])
        medium_issues = len([i for i in issues if i.severity == Severity.MEDIUM])

        issue_penalty = (critical_issues * 0.3 + high_issues * 0.2 + medium_issues * 0.1)
        quality_score = max(0.1, metrics.maintainability_index / 100 - issue_penalty)

        # Complexity score (inverse of cyclomatic complexity)
        complexity_score = max(0.1, 1.0 - (metrics.cyclomatic_complexity / 10))

        # Maintainability score (based on maintainability index)
        maintainability_score = max(0.1, metrics.maintainability_index / 100)

        # Performance score (from metrics)
        performance_score = metrics.performance_score

        # Security score (from metrics)
        security_score = metrics.security_score

        # Overall score (weighted average)
        overall_score = (
            quality_score * 0.3 +
            complexity_score * 0.2 +
            maintainability_score * 0.2 +
            performance_score * 0.15 +
            security_score * 0.15
        )

        return {
            'quality': quality_score,
            'complexity': complexity_score,
            'maintainability': maintainability_score,
            'performance': performance_score,
            'security': security_score,
            'overall': overall_score
        }

    def _generate_python_recommendations(self, issues: List[CodeIssue], metrics: CodeMetrics) -> List[str]:
        """Generate improvement recommendations."""
        recommendations = []

        # Based on metrics
        if metrics.cyclomatic_complexity > 5:
            recommendations.append("Consider breaking down complex functions into smaller, more focused ones")

        if metrics.code_duplication_ratio > 0.1:
            recommendations.append("Remove code duplication using functions or classes")

        if metrics.maintainability_index < 70:
            recommendations.append("Improve code maintainability by adding documentation and simplifying logic")

        # Based on issues
        categories = {}
        for issue in issues:
            if issue.category not in categories:
                categories[issue.category] = 0
            categories[issue.category] += 1

        if categories.get('naming', 0) > 2:
            recommendations.append("Fix naming convention issues for better code readability")

        if categories.get('performance', 0) > 0:
            recommendations.append("Address performance issues to improve code efficiency")

        if categories.get('security', 0) > 0:
            recommendations.append("Fix security issues to make code more robust")

        return recommendations

    def _generate_qwen_optimizations(self, tree: ast.AST, code: str) -> List[str]:
        """Generate Qwen-specific optimizations."""
        optimizations = []

        # Check for patterns that Qwen can optimize well
        has_list_comprehensions = any(isinstance(node, ast.ListComp) for node in ast.walk(tree))
        if not has_list_comprehensions:
            optimizations.append("Consider using list comprehensions for better readability and performance")

        # Check for error handling patterns
        has_error_handling = any(isinstance(node, ast.Try) for node in ast.walk(tree))
        if not has_error_handling:
            optimizations.append("Add proper error handling patterns that Qwen can help implement")

        # Check for function organization
        functions = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
        if len(functions) > 10:
            optimizations.append("Consider organizing functions into classes or modules for better structure")

        # Check for documentation patterns
        documented_functions = [f for f in functions if ast.get_docstring(f)]
        if len(documented_functions) / len(functions) < 0.5:
            optimizations.append("Add docstrings using patterns that Qwen understands well")

        return optimizations

    def _create_syntax_error_analysis(self, error: SyntaxError, filename: str) -> CodeAnalysis:
        """Create analysis for code with syntax errors."""
        return CodeAnalysis(
            quality_score=0.1,
            complexity_score=0.1,
            maintainability_score=0.1,
            performance_score=0.1,
            security_score=0.5,  # Neutral security score
            overall_score=0.1,
            issues=[CodeIssue(
                line_number=error.lineno or 1,
                column=error.offset or 0,
                severity=Severity.CRITICAL,
                category="syntax",
                message=f"Syntax error: {error.msg}",
                suggestion="Fix syntax errors before analysis",
                qwen_impact="Qwen cannot work with code that has syntax errors"
            )],
            metrics=CodeMetrics(0, 0, 0, 0, 0, 0, 0),
            recommendations=["Fix syntax errors", "Ensure code is valid Python"],
            qwen_optimizations=["Fix syntax errors before asking Qwen for help"],
            language='python'
        )


class CodeAnalyzer:
    """Main code analyzer class."""

    def __init__(self, config: AnalysisConfig = None):
        """Initialize the CodeAnalyzer."""
        self.config = config or AnalysisConfig()
        self.python_analyzer = PythonAnalyzer()

    def analyze_code(self, code: str, language: str = 'auto') -> CodeAnalysis:
        """Analyze code and return comprehensive results."""
        if language == 'auto':
            language = self._detect_language(code)

        if language == 'python':
            return self.python_analyzer.analyze_python_file(code)
        else:
            return self._analyze_generic_code(code, language)

    def _detect_language(self, code: str) -> str:
        """Detect programming language from code."""
        # Simple language detection based on common patterns
        if 'def ' in code and ('.py' in code[:100] or 'import ' in code):
            return 'python'
        elif 'function ' in code or 'const ' in code or 'let ' in code:
            return 'javascript'
        elif 'public class ' in code or 'private ' in code:
            return 'java'
        elif 'package main' in code or 'func ' in code:
            return 'go'
        else:
            return 'unknown'

    def _analyze_generic_code(self, code: str, language: str) -> CodeAnalysis:
        """Generic analysis for unsupported languages."""
        lines = code.split('\n')
        lines_of_code = len([line for line in lines if line.strip()])

        # Basic metrics
        avg_line_length = sum(len(line) for line in lines) / len(lines) if lines else 0
        maintainability_index = max(0, 100 - (avg_line_length * 0.1))

        return CodeAnalysis(
            quality_score=min(1.0, maintainability_index / 100),
            complexity_score=0.5,  # Neutral complexity
            maintainability_score=min(1.0, maintainability_index / 100),
            performance_score=0.5,  # Neutral performance
            security_score=0.7,  # Slightly positive security
            overall_score=min(1.0, maintainability_index / 100),
            issues=[],
            metrics=CodeMetrics(
                lines_of_code=lines_of_code,
                cyclomatic_complexity=1.0,
                maintainability_index=maintainability_index,
                code_duplication_ratio=0.0,
                test_coverage_suggestion=0.8,
                performance_score=0.5,
                security_score=0.7
            ),
            recommendations=[f"Language '{language}' support is limited", "Consider contributing language-specific analyzers"],
            qwen_optimizations=["Qwen works best with Python code"],
            language=language
        )

    def get_qwen_recommendations(self, code: str) -> List[str]:
        """Get Qwen-specific optimization recommendations."""
        analysis = self.analyze_code(code)

        recommendations = []
        recommendations.extend(analysis.qwen_optimizations)

        # Add general Qwen recommendations
        if analysis.language != 'python':
            recommendations.append("Consider converting to Python for better Qwen compatibility")

        if analysis.overall_score < 0.6:
            recommendations.append("Qwen can help refactor this code for better structure and performance")

        if len(analysis.issues) > 5:
            recommendations.append("Qwen excels at fixing multiple code issues systematically")

        return recommendations

    def generate_qwen_prompt(self, analysis: CodeAnalysis) -> str:
        """Generate an optimized prompt for Qwen based on analysis."""
        prompt_parts = []

        # Main request based on analysis
        if analysis.overall_score < 0.5:
            prompt_parts.append("Please help me completely refactor this code to improve its quality, performance, and maintainability.")
        elif analysis.overall_score < 0.7:
            prompt_parts.append("Please help me improve this code by addressing the identified issues and implementing best practices.")
        else:
            prompt_parts.append("Please help me optimize this already good code for even better performance and maintainability.")

        # Add specific focus areas
        focus_areas = []
        if analysis.quality_score < 0.7:
            focus_areas.append("code quality")
        if analysis.performance_score < 0.7:
            focus_areas.append("performance")
        if analysis.security_score < 0.8:
            focus_areas.append("security")
        if analysis.maintainability_score < 0.7:
            focus_areas.append("maintainability")

        if focus_areas:
            prompt_parts.append(f"Focus on: {', '.join(focus_areas)}")

        # Add specific recommendations
        if analysis.recommendations:
            prompt_parts.append("Specific improvements needed:")
            for rec in analysis.recommendations[:3]:  # Limit to top 3
                prompt_parts.append(f"- {rec}")

        # Add Qwen-specific guidance
        prompt_parts.append("Please provide:")
        prompt_parts.append("1. Improved code with explanations")
        prompt_parts.append("2. Key changes made and why")
        prompt_parts.append("3. Any additional best practices to consider")

        return "\n".join(prompt_parts)

    def analyze_codebase(self, directory: str) -> ProjectAnalysis:
        """Analyze entire codebase."""
        project_files = []
        total_lines = 0

        for root, dirs, files in os.walk(directory):
            # Skip common directories to avoid noise
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['__pycache__', 'node_modules', 'venv']]

            for file in files:
                if file.endswith(('.py', '.js', '.ts', '.java', '.cpp', '.go', '.rs')):
                    filepath = os.path.join(root, file)
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            code = f.read()

                        analysis = self.analyze_code(code, self._detect_language(code))
                        project_files.append(analysis)
                        total_lines += analysis.metrics.lines_of_code

                    except Exception as e:
                        logger.warning(f"Could not analyze {filepath}: {e}")

        if not project_files:
            return ProjectAnalysis(0, 0, 0.0, [], [], [])

        # Calculate project-wide metrics
        average_quality = sum(f.quality_score for f in project_files) / len(project_files)

        # Generate project recommendations
        project_recommendations = self._generate_project_recommendations(project_files)

        # Generate Qwen integration suggestions
        qwen_suggestions = self._generate_qwen_integration_suggestions(project_files)

        return ProjectAnalysis(
            total_files=len(project_files),
            total_lines=total_lines,
            average_quality_score=average_quality,
            files=project_files,
            project_recommendations=project_recommendations,
            qwen_integration_suggestions=qwen_suggestions
        )

    def _generate_project_recommendations(self, files: List[CodeAnalysis]) -> List[str]:
        """Generate project-wide recommendations."""
        recommendations = []

        # Overall quality assessment
        avg_score = sum(f.overall_score for f in files) / len(files)
        if avg_score < 0.6:
            recommendations.append("Project needs significant refactoring for better code quality")
        elif avg_score < 0.8:
            recommendations.append("Project has good quality but could benefit from targeted improvements")

        # Common issues across files
        all_issues = [issue for file in files for issue in file.issues]
        issue_categories = {}
        for issue in all_issues:
            issue_categories[issue.category] = issue_categories.get(issue.category, 0) + 1

        for category, count in issue_categories.items():
            if count > len(files) * 0.3:  # Issues in more than 30% of files
                recommendations.append(f"Address {category} issues across {count} files")

        return recommendations

    def _generate_qwen_integration_suggestions(self, files: List[CodeAnalysis]) -> List[str]:
        """Generate Qwen integration suggestions for the project."""
        suggestions = []

        # Language distribution
        languages = {}
        for file in files:
            languages[file.language] = languages.get(file.language, 0) + 1

        if languages.get('python', 0) < len(files) * 0.5:
            suggestions.append("Consider migrating more code to Python for better Qwen compatibility")

        # Improvement opportunities
        needs_improvement = [f for f in files if f.overall_score < 0.7]
        if needs_improvement:
            suggestions.append(f"Qwen can help improve {len(needs_improvement)} files with low quality scores")

        # Best practices
        if len(files) > 5:
            suggestions.append("Use Qwen's batch processing capabilities for large-scale refactoring")

        return suggestions


def main():
    """Example usage and testing."""
    analyzer = CodeAnalyzer()

    # Example code for testing
    test_code = '''
def calculate_total(items):
    total = 0
    for item in items:
        total += item
    return total

def process_data(data):
    result = []
    for d in data:
        result.append(d * 2)
    return result
'''

    print("=== Code Analysis Example ===\n")

    # Analyze the code
    analysis = analyzer.analyze_code(test_code, language='python')

    print(f"Overall Score: {analysis.overall_score:.3f}")
    print(f"Quality Score: {analysis.quality_score".3f"}")
    print(f"Complexity Score: {analysis.complexity_score".3f"}")
    print(f"Performance Score: {analysis.performance_score".3f"}")
    print(f"Security Score: {analysis.security_score".3f"}")
    print()

    print(f"Issues Found: {len(analysis.issues)}")
    for issue in analysis.issues[:3]:  # Show top 3 issues
        print(f"- {issue.category.title()}: {issue.message}")
    print()

    print("Qwen Recommendations:")
    for rec in analysis.qwen_optimizations[:3]:
        print(f"- {rec}")
    print()

    # Generate Qwen prompt
    qwen_prompt = analyzer.generate_qwen_prompt(analysis)
    print("Generated Qwen Prompt:")
    print(qwen_prompt)


if __name__ == "__main__":
    main()