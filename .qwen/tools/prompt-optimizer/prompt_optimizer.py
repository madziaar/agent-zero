#!/usr/bin/env python3
"""
Qwen Prompt Optimizer - Core functionality for analyzing and optimizing prompts for Qwen models.

This module provides tools to analyze prompt effectiveness, suggest improvements,
and optimize prompts specifically for Qwen's capabilities and coding focus.
"""

import re
import json
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class OptimizationLevel(Enum):
    """Optimization levels for prompt processing."""
    BASIC = "basic"
    STANDARD = "standard"
    ADVANCED = "advanced"


class ModelType(Enum):
    """Supported Qwen model types."""
    QWEN_CODER = "qwen-coder"
    QWEN_TURBO = "qwen-turbo"
    QWEN_PLUS = "qwen-plus"
    QWEN_MAX = "qwen-max"


@dataclass
class PromptAnalysis:
    """Results of prompt analysis."""
    clarity_score: float
    specificity_score: float
    structure_score: float
    context_adequacy: float
    token_efficiency: float
    qwen_compatibility: float
    overall_score: float
    issues: List[str]
    suggestions: List[str]
    strengths: List[str]


@dataclass
class ComparisonResult:
    """Results of prompt comparison."""
    prompt_scores: List[float]
    best_prompt_index: int
    improvements: List[str]
    recommendations: List[str]


@dataclass
class OptimizationConfig:
    """Configuration for prompt optimization."""
    model_type: ModelType = ModelType.QWEN_CODER
    optimization_level: OptimizationLevel = OptimizationLevel.STANDARD
    focus_areas: List[str] = None
    qwen_specific_features: Dict[str, bool] = None
    analysis_metrics: List[str] = None

    def __post_init__(self):
        if self.focus_areas is None:
            self.focus_areas = ["clarity", "specificity", "context"]
        if self.qwen_specific_features is None:
            self.qwen_specific_features = {
                "use_reasoning_tags": True,
                "context_window_optimization": True,
                "token_efficiency": True
            }
        if self.analysis_metrics is None:
            self.analysis_metrics = [
                "clarity_score", "specificity_score", "context_adequacy",
                "token_efficiency", "qwen_compatibility"
            ]


class QwenPromptTemplate:
    """Templates specifically designed for Qwen models."""

    @staticmethod
    def coding_task(task: str, language: str = "Python",
                    constraints: List[str] = None,
                    context: str = None) -> str:
        """Create an optimized prompt for coding tasks."""
        constraints = constraints or []
        context = context or ""

        template = f"""You are an expert {language} developer. {context}

Task: {task}

Requirements:
- Write clean, well-documented {language} code
- Follow best practices for {language}
- Include proper error handling"""

        if constraints:
            template += "\n- " + "\n- ".join(constraints)

        template += """

Please provide:
1. Complete, working code
2. Brief explanation of the implementation
3. Any important considerations or edge cases"""

        return template

    @staticmethod
    def code_review(code_snippet: str, focus_areas: List[str] = None) -> str:
        """Create an optimized prompt for code review."""
        focus_areas = focus_areas or [
            "performance", "readability", "maintainability"]

        template = f"""Please review this code snippet with focus on: {', '.join(focus_areas)}

Code to review:
```python
{code_snippet}
```

Please provide:
1. Overall assessment
2. Specific issues found
3. Suggested improvements
4. Best practices recommendations

Be constructive and provide specific examples for improvements."""

        return template

    @staticmethod
    def debugging_task(error_description: str, code_context: str = None,
                       environment: str = None) -> str:
        """Create an optimized prompt for debugging tasks."""
        context = f"\nCode context: {code_context}" if code_context else ""
        env_info = f"\nEnvironment: {environment}" if environment else ""

        template = f"""I need help debugging an issue. Here's what I know:

Error/Issue: {error_description}{context}{env_info}

Please help me:
1. Understand what might be causing this issue
2. Identify potential solutions
3. Provide step-by-step debugging guidance
4. Suggest preventive measures for similar issues in the future"""

        return template


class PromptOptimizer:
    """Main class for analyzing and optimizing prompts for Qwen models."""

    def __init__(self, config: OptimizationConfig = None):
        """Initialize the PromptOptimizer with configuration."""
        self.config = config or OptimizationConfig()
        self.qwen_patterns = self._initialize_qwen_patterns()

    def _initialize_qwen_patterns(self) -> Dict[str, Any]:
        """Initialize Qwen-specific patterns for analysis."""
        return {
            'reasoning_indicators': [
                r'\bthink\b', r'\breasoning\b', r'\banalyze\b', r'\bconsider\b',
                r'\blogic\b', r'\bapproach\b', r'\bstrategy\b'
            ],
            'coding_indicators': [
                r'\bfunction\b', r'\bclass\b', r'\bmethod\b', r'\bvariable\b',
                r'\balgorithm\b', r'\bimplementation\b', r'\bcode\b', r'\bprogramming\b'
            ],
            'structure_indicators': [
                r'\bstep[s]?\b', r'\bprocess\b', r'\bprocedure\b', r'\bguide\b',
                r'\binstruction[s]?\b', r'\btutorial\b', r'\bexample[s]?\b'
            ],
            'context_indicators': [
                r'\bcontext\b', r'\benvironment\b', r'\bbackground\b', r'\bscenario\b',
                r'\bproject\b', r'\bapplication\b', r'\buse.case\b'
            ]
        }

    def analyze_prompt(self, prompt: str) -> PromptAnalysis:
        """Analyze a prompt's effectiveness and provide scores."""
        if not prompt or not prompt.strip():
            return self._create_empty_analysis()

        # Calculate individual scores
        clarity_score = self._calculate_clarity_score(prompt)
        specificity_score = self._calculate_specificity_score(prompt)
        structure_score = self._calculate_structure_score(prompt)
        context_adequacy = self._calculate_context_adequacy(prompt)
        token_efficiency = self._calculate_token_efficiency(prompt)
        qwen_compatibility = self._calculate_qwen_compatibility(prompt)

        # Calculate overall score
        weights = {'clarity': 0.2, 'specificity': 0.25, 'structure': 0.15,
                   'context': 0.2, 'token_efficiency': 0.1, 'qwen_compatibility': 0.1}

        overall_score = (
            clarity_score * weights['clarity'] +
            specificity_score * weights['specificity'] +
            structure_score * weights['structure'] +
            context_adequacy * weights['context'] +
            token_efficiency * weights['token_efficiency'] +
            qwen_compatibility * weights['qwen_compatibility']
        )

        # Identify issues and suggestions
        issues = self._identify_issues(prompt)
        suggestions = self._generate_suggestions(prompt, issues)
        strengths = self._identify_strengths(prompt)

        return PromptAnalysis(
            clarity_score=clarity_score,
            specificity_score=specificity_score,
            structure_score=structure_score,
            context_adequacy=context_adequacy,
            token_efficiency=token_efficiency,
            qwen_compatibility=qwen_compatibility,
            overall_score=overall_score,
            issues=issues,
            suggestions=suggestions,
            strengths=strengths
        )

    def _calculate_clarity_score(self, prompt: str) -> float:
        """Calculate clarity score based on language clarity indicators."""
        # Simple heuristics for clarity
        sentences = re.split(r'[.!?]+', prompt)
        avg_words_per_sentence = sum(len(
            s.split()) for s in sentences if s.strip()) / len(sentences) if sentences else 0

        # Prefer moderate sentence length (10-25 words)
        if 10 <= avg_words_per_sentence <= 25:
            clarity_score = 0.9
        elif avg_words_per_sentence < 5:
            clarity_score = 0.5
        elif avg_words_per_sentence > 40:
            clarity_score = 0.4
        else:
            clarity_score = 0.7

        # Check for vague terms
        vague_terms = ['thing', 'stuff', 'something', 'it', 'they']
        vague_count = sum(prompt.lower().count(term) for term in vague_terms)
        clarity_penalty = min(vague_count * 0.05, 0.3)

        return max(0.1, clarity_score - clarity_penalty)

    def _calculate_specificity_score(self, prompt: str) -> float:
        """Calculate specificity score based on detail level."""
        # Check for specific technical terms and details
        technical_terms = len(re.findall(
            r'\b(function|class|variable|algorithm|implementation)\b', prompt, re.IGNORECASE))

        # Check for concrete requirements vs. vague requests
        concrete_indicators = len(re.findall(
            r'\b(must|should|need|require|specific|exactly|precisely)\b', prompt, re.IGNORECASE))
        vague_indicators = len(re.findall(
            r'\b(maybe|perhaps|somehow|somewhere)\b', prompt, re.IGNORECASE))

        # Base score from technical detail
        base_score = min(technical_terms * 0.1, 0.5)

        # Adjust for requirement specificity
        if concrete_indicators > vague_indicators:
            specificity_score = 0.7 + base_score
        elif vague_indicators > concrete_indicators:
            specificity_score = 0.3 + base_score
        else:
            specificity_score = 0.5 + base_score

        return min(1.0, specificity_score)

    def _calculate_structure_score(self, prompt: str) -> float:
        """Calculate structure score based on organization."""
        structure_indicators = 0

        # Check for numbered lists
        numbered_lists = len(re.findall(r'\b\d+\.', prompt))
        if numbered_lists > 0:
            structure_indicators += 0.3

        # Check for bullet points
        bullet_points = len(re.findall(r'[-*•]', prompt))
        if bullet_points > 0:
            structure_indicators += 0.2

        # Check for clear sections
        sections = len(re.findall(
            r'\b(step|phase|part|section|component)\b', prompt, re.IGNORECASE))
        if sections > 0:
            structure_indicators += 0.2

        # Check for logical flow indicators
        flow_indicators = len(re.findall(
            r'\b(first|then|next|after|finally|before)\b', prompt, re.IGNORECASE))
        if flow_indicators > 0:
            structure_indicators += 0.2

        # Penalty for very long unstructured blocks
        paragraphs = [p for p in prompt.split('\n\n') if p.strip()]
        if any(len(p.split()) > 100 for p in paragraphs):
            structure_indicators -= 0.2

        return max(0.1, min(1.0, 0.3 + structure_indicators))

    def _calculate_context_adequacy(self, prompt: str) -> float:
        """Calculate context adequacy score."""
        context_indicators = 0

        # Check for environment/project context
        context_words = ['project', 'environment', 'context',
                         'background', 'scenario', 'application']
        context_indicators += sum(prompt.lower().count(word)
                                  for word in context_words) * 0.1

        # Check for code snippets or examples
        has_code_snippet = '```' in prompt
        if has_code_snippet:
            context_indicators += 0.3

        # Check for specific constraints or requirements
        constraints = len(re.findall(
            r'\b(constraint|requirement|limitation|specific)\b', prompt, re.IGNORECASE))
        context_indicators += min(constraints * 0.1, 0.3)

        return min(1.0, 0.2 + context_indicators)

    def _calculate_token_efficiency(self, prompt: str) -> float:
        """Calculate token efficiency score."""
        word_count = len(prompt.split())

        # Optimal range is typically 50-200 words for most tasks
        if 50 <= word_count <= 200:
            efficiency_score = 0.9
        elif word_count < 20:
            efficiency_score = 0.4  # Too brief, might lack detail
        elif word_count > 400:
            efficiency_score = 0.3  # Too verbose, might exceed context window
        else:
            efficiency_score = 0.7

        # Bonus for clear, concise language
        avg_word_length = sum(len(word)
                              for word in prompt.split()) / word_count
        if 4 <= avg_word_length <= 8:  # Good balance of simplicity and precision
            efficiency_score += 0.1

        return min(1.0, efficiency_score)

    def _calculate_qwen_compatibility(self, prompt: str) -> float:
        """Calculate Qwen-specific compatibility score."""
        compatibility_score = 0.5  # Base score

        # Check for coding-related content
        coding_patterns = self.qwen_patterns['coding_indicators']
        coding_matches = sum(len(re.findall(pattern, prompt, re.IGNORECASE))
                             for pattern in coding_patterns)
        if coding_matches > 0:
            compatibility_score += 0.2

        # Check for reasoning indicators (good for Qwen)
        reasoning_patterns = self.qwen_patterns['reasoning_indicators']
        reasoning_matches = sum(len(re.findall(
            pattern, prompt, re.IGNORECASE)) for pattern in reasoning_patterns)
        if reasoning_matches > 0:
            compatibility_score += 0.2

        # Check for structured thinking
        structure_patterns = self.qwen_patterns['structure_indicators']
        structure_matches = sum(len(re.findall(
            pattern, prompt, re.IGNORECASE)) for pattern in structure_patterns)
        if structure_matches > 0:
            compatibility_score += 0.1

        return min(1.0, compatibility_score)

    def _identify_issues(self, prompt: str) -> List[str]:
        """Identify potential issues in the prompt."""
        issues = []

        # Check for vagueness
        vague_terms = ['thing', 'stuff', 'something', 'somehow']
        for term in vague_terms:
            if re.search(r'\b' + term + r'\b', prompt, re.IGNORECASE):
                issues.append(f"Contains vague term: '{term}'")

        # Check for unclear requirements
        if not re.search(r'\b(must|should|need|require|want|expect)\b', prompt, re.IGNORECASE):
            issues.append("Unclear requirements or expectations")

        # Check for missing context
        if len(prompt.split()) < 30 and '```' not in prompt:
            issues.append("Limited context provided")

        # Check for overly complex sentences
        sentences = [s.strip()
                     for s in re.split(r'[.!?]+', prompt) if s.strip()]
        long_sentences = [s for s in sentences if len(s.split()) > 35]
        if long_sentences:
            issues.append(
                f"Contains {len(long_sentences)} overly complex sentence(s)")

        return issues

    def _generate_suggestions(self, prompt: str, issues: List[str]) -> List[str]:
        """Generate improvement suggestions."""
        suggestions = []

        if not issues:
            return ["Prompt appears well-structured and clear"]

        for issue in issues:
            if "vague term" in issue:
                suggestions.append(
                    "Replace vague terms with specific, concrete language")
            elif "Unclear requirements" in issue:
                suggestions.append(
                    "Clearly specify what you want to achieve or expect as output")
            elif "Limited context" in issue:
                suggestions.append(
                    "Provide more context about your project, environment, or specific situation")
            elif "complex sentence" in issue:
                suggestions.append(
                    "Break down complex sentences into simpler, clearer statements")

        # General suggestions based on analysis
        if len(prompt.split()) > 300:
            suggestions.append(
                "Consider breaking this into multiple focused prompts")

        if not re.search(r'\bexample\b', prompt, re.IGNORECASE):
            suggestions.append(
                "Consider providing examples of expected input/output")

        return suggestions

    def _identify_strengths(self, prompt: str) -> List[str]:
        """Identify strengths of the prompt."""
        strengths = []

        # Check for good structure
        if re.search(r'\b\d+\.', prompt):
            strengths.append("Good use of numbered steps")

        # Check for specific technical details
        technical_terms = ['function', 'class', 'algorithm', 'implementation']
        if any(term in prompt.lower() for term in technical_terms):
            strengths.append("Includes specific technical requirements")

        # Check for clear expectations
        if re.search(r'\b(provide|return|output|result|show)\b', prompt, re.IGNORECASE):
            strengths.append("Clear output expectations specified")

        # Check for context
        if '```' in prompt:
            strengths.append("Includes code examples or snippets")

        if not strengths:
            strengths.append(
                "Has potential for improvement with more specific details")

        return strengths

    def _create_empty_analysis(self) -> PromptAnalysis:
        """Create an empty analysis for invalid prompts."""
        return PromptAnalysis(
            clarity_score=0.0,
            specificity_score=0.0,
            structure_score=0.0,
            context_adequacy=0.0,
            token_efficiency=0.0,
            qwen_compatibility=0.0,
            overall_score=0.0,
            issues=["Empty or invalid prompt"],
            suggestions=["Provide a valid, non-empty prompt"],
            strengths=[]
        )

    def optimize_prompt(self, prompt: str) -> str:
        """Optimize a prompt for better Qwen performance."""
        if not prompt or not prompt.strip():
            return prompt

        analysis = self.analyze_prompt(prompt)

        # Apply optimizations based on analysis
        optimized = prompt

        # Add structure if missing
        if analysis.structure_score < 0.6:
            optimized = self._add_structure(optimized)

        # Improve clarity if needed
        if analysis.clarity_score < 0.6:
            optimized = self._improve_clarity(optimized)

        # Enhance specificity if needed
        if analysis.specificity_score < 0.6:
            optimized = self._enhance_specificity(optimized)

        # Add Qwen-specific enhancements
        if self.config.optimization_level == OptimizationLevel.ADVANCED:
            optimized = self._add_qwen_enhancements(optimized)

        return optimized

    def _add_structure(self, prompt: str) -> str:
        """Add structure to improve prompt organization."""
        if '\n\n' not in prompt:
            # Add paragraph breaks for better readability
            sentences = re.split(r'([.!?]+)', prompt)
            structured = '\n\n'.join([
                sentences[i] + sentences[i+1]
                for i in range(0, len(sentences)-1, 2)
            ])
            return structured
        return prompt

    def _improve_clarity(self, prompt: str) -> str:
        """Improve prompt clarity."""
        # Replace vague terms with more specific alternatives
        replacements = {
            'thing': 'component',
            'stuff': 'elements',
            'something': 'specific item',
            'somehow': 'using an appropriate method'
        }

        for old, new in replacements.items():
            prompt = re.sub(r'\b' + old + r'\b', new,
                            prompt, flags=re.IGNORECASE)

        return prompt

    def _enhance_specificity(self, prompt: str) -> str:
        """Enhance prompt specificity."""
        # Add specificity indicators if missing
        if not re.search(r'\b(specifically|particularly|exactly)\b', prompt, re.IGNORECASE):
            # Insert specificity language
            sentences = prompt.split('. ')
            if sentences:
                sentences[0] += " Specifically, I need assistance with:"
                prompt = '. '.join(sentences)

        return prompt

    def _add_qwen_enhancements(self, prompt: str) -> str:
        """Add Qwen-specific enhancements."""
        enhanced = prompt

        # Add reasoning guidance for complex tasks
        if self.config.qwen_specific_features.get("use_reasoning_tags", False):
            if len(prompt.split()) > 100:  # Complex prompt
                enhanced = "<thinking>\nPlease think through this step by step.\n</thinking>\n\n" + enhanced

        # Add coding-specific guidance
        if "code" in prompt.lower() or "function" in prompt.lower():
            enhanced += "\n\nPlease ensure the code is well-documented, follows best practices, and includes proper error handling."

        return enhanced

    def get_optimization_suggestions(self, prompt: str) -> List[str]:
        """Get specific optimization suggestions for a prompt."""
        analysis = self.analyze_prompt(prompt)

        suggestions = []

        if analysis.clarity_score < 0.7:
            suggestions.append(
                "Improve clarity by using more specific language and avoiding vague terms")

        if analysis.specificity_score < 0.7:
            suggestions.append(
                "Add specific requirements, constraints, and expected outcomes")

        if analysis.structure_score < 0.7:
            suggestions.append(
                "Structure your prompt with clear sections, numbered steps, or bullet points")

        if analysis.context_adequacy < 0.7:
            suggestions.append(
                "Provide more context about your project, environment, or specific situation")

        if analysis.qwen_compatibility < 0.7:
            suggestions.append(
                "Add coding-specific details or technical requirements for better Qwen compatibility")

        if not suggestions:
            suggestions.append("Your prompt is well-optimized!")

        return suggestions

    def compare_prompts(self, prompts: List[str]) -> ComparisonResult:
        """Compare multiple prompt variations."""
        if not prompts:
            return ComparisonResult([], -1, [], [])

        analyses = [self.analyze_prompt(p) for p in prompts]
        scores = [a.overall_score for a in analyses]

        best_index = scores.index(max(scores))
        improvements = []
        recommendations = []

        # Generate comparison insights
        if len(prompts) > 1:
            best_prompt = prompts[best_index]
            worst_prompt = prompts[scores.index(min(scores))]

            if scores[best_index] > scores[scores.index(min(scores))] + 0.2:
                improvements.append(
                    f"Prompt {best_index + 1} is significantly better than prompt {scores.index(min(scores)) + 1}")

            recommendations.append(
                "Focus on clarity and specificity for best results")
            recommendations.append(
                "Structure complex requests with clear steps or sections")

        return ComparisonResult(
            prompt_scores=scores,
            best_prompt_index=best_index,
            improvements=improvements,
            recommendations=recommendations
        )


def main():
    """Example usage and testing."""
    optimizer = PromptOptimizer()

    # Test prompts
    test_prompts = [
        "Fix this code",  # Basic, unclear
        "Please help me debug this Python function that calculates fibonacci numbers",  # Better
        "I need a Python function to calculate fibonacci numbers with memoization, include error handling for invalid inputs, and provide clear documentation"  # Best
    ]

    print("=== Prompt Analysis Example ===\n")

    for i, prompt in enumerate(test_prompts, 1):
        print(f"Prompt {i}: {prompt}")
        analysis = optimizer.analyze_prompt(prompt)

        print(f"Overall Score: {analysis.overall_score:.2f}")
        print(f"Clarity: {analysis.clarity_score:.2f}")
        print(f"Specificity: {analysis.specificity_score:.2f}")
        print(f"Structure: {analysis.structure_score:.2f}")
        print()

    # Test optimization
    print("\n=== Prompt Optimization Example ===")
    basic_prompt = "Write code for sorting"
    optimized = optimizer.optimize_prompt(basic_prompt)

    print(f"Original: {basic_prompt}")
    print(f"Optimized: {optimized}")


if __name__ == "__main__":
    main()
