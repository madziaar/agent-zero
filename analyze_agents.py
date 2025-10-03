#!/usr/bin/env python
"""
Agent Profiles Analysis Script for Agent Zero
--------------------------------------------
This script analyzes the agent profile directories to identify
patterns, redundancies, and standardization opportunities.
"""

import os
import json
import difflib
import hashlib
from collections import defaultdict


def analyze_agents(agents_dir="agents"):
    """
    Analyze the agent profile directories.
    """
    print(f"Analyzing agent profiles in: {agents_dir}")

    if not os.path.isdir(agents_dir):
        print(f"Error: {agents_dir} is not a directory or does not exist.")
        return None

    # Get all agent directories
    agent_dirs = [
        d for d in os.listdir(agents_dir)
        if os.path.isdir(os.path.join(agents_dir, d)) and not d.startswith('.')
    ]

    if not agent_dirs:
        print("No agent profiles found.")
        return None

    print(f"Found {len(agent_dirs)} agent profiles: {', '.join(agent_dirs)}")

    # Analyze structure
    structure_analysis = analyze_directory_structure(agents_dir, agent_dirs)

    # Analyze prompt content patterns
    prompt_analysis = analyze_prompt_content(agents_dir, agent_dirs)

    # Analyze file similarities
    similarity_analysis = analyze_file_similarities(agents_dir, agent_dirs)

    # Combine analyses
    analysis = {
        "agent_profiles": agent_dirs,
        "structure_analysis": structure_analysis,
        "prompt_analysis": prompt_analysis,
        "similarity_analysis": similarity_analysis
    }

    return analysis


def analyze_directory_structure(agents_dir, agent_dirs):
    """Analyze the directory structure of each agent profile."""
    structure = {}
    all_paths = set()

    for agent in agent_dirs:
        agent_path = os.path.join(agents_dir, agent)
        structure[agent] = {}

        # Get all files and directories
        for root, dirs, files in os.walk(agent_path):
            rel_root = os.path.relpath(root, agent_path)
            if rel_root == ".":
                rel_root = ""

            # Track directories
            for d in dirs:
                rel_path = os.path.join(rel_root, d).replace("\\", "/")
                if rel_path not in structure[agent]:
                    structure[agent][rel_path] = {
                        "type": "directory", "files": []}
                all_paths.add(rel_path)

            # Track files
            for f in files:
                # Create file path and add to structure
                parent_dir = rel_root.replace("\\", "/")

                if parent_dir not in structure[agent]:
                    structure[agent][parent_dir] = {
                        "type": "directory", "files": []}

                structure[agent][parent_dir]["files"].append(f)
                all_paths.add(os.path.join(parent_dir, f).replace("\\", "/"))

    # Calculate stats
    common_paths = set.intersection(*(
        {path for path in all_paths if path in structure[agent] or any(
            path == os.path.join(parent, file).replace("\\", "/")
            for parent in structure[agent]
            for file in structure[agent][parent].get("files", [])
        )}
        for agent in agent_dirs
    ))

    unique_paths = {
        agent: {
            path for path in all_paths
            if (path in structure[agent] or any(
                path == os.path.join(parent, file).replace("\\", "/")
                for parent in structure[agent]
                for file in structure[agent][parent].get("files", [])
            )) and path not in common_paths
        }
        for agent in agent_dirs
    }

    return {
        "detailed_structure": structure,
        "common_paths": sorted(list(common_paths)),
        "unique_paths": {agent: sorted(list(paths)) for agent, paths in unique_paths.items()},
        "stats": {
            "total_unique_paths": len(all_paths),
            "common_paths_count": len(common_paths),
            "unique_paths_per_agent": {agent: len(paths) for agent, paths in unique_paths.items()}
        }
    }


def analyze_prompt_content(agents_dir, agent_dirs):
    """Analyze the content of prompt files across agent profiles."""
    prompt_stats = {}
    prompt_file_patterns = defaultdict(list)

    # Find all prompt files
    for agent in agent_dirs:
        agent_path = os.path.join(agents_dir, agent)
        prompts_dir = os.path.join(agent_path, "prompts")

        if not os.path.isdir(prompts_dir):
            continue

        prompt_files = []
        for root, _, files in os.walk(prompts_dir):
            for file in files:
                if file.endswith(".md"):
                    full_path = os.path.join(root, file)
                    rel_path = os.path.relpath(full_path, agent_path)
                    prompt_files.append((rel_path, full_path))

        prompt_stats[agent] = {
            "prompt_file_count": len(prompt_files),
            "prompt_files": [rel_path for rel_path, _ in prompt_files]
        }

        # Analyze content patterns
        for rel_path, full_path in prompt_files:
            try:
                with open(full_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    content_hash = hashlib.md5(content.encode()).hexdigest()
                    prompt_file_patterns[rel_path].append({
                        "agent": agent,
                        "content_hash": content_hash,
                        "content_length": len(content),
                        "line_count": content.count('\n') + 1
                    })
            except Exception as e:
                print(f"Error reading {full_path}: {e}")

    # Find common patterns
    common_prompt_files = []
    divergent_prompt_files = []

    for rel_path, instances in prompt_file_patterns.items():
        if len(instances) > 1:  # File exists in multiple agents
            hashes = [instance["content_hash"] for instance in instances]
            if len(set(hashes)) == 1:
                # Same content across all instances
                common_prompt_files.append({
                    "file": rel_path,
                    "agents": [instance["agent"] for instance in instances],
                    "content_length": instances[0]["content_length"],
                    "line_count": instances[0]["line_count"],
                    "identical": True
                })
            else:
                # Different content
                divergent_prompt_files.append({
                    "file": rel_path,
                    "agents": [instance["agent"] for instance in instances],
                    "content_differences": True,
                    "instances": instances
                })

    return {
        "prompt_stats": prompt_stats,
        "common_prompt_files": common_prompt_files,
        "divergent_prompt_files": divergent_prompt_files
    }


def analyze_file_similarities(agents_dir, agent_dirs):
    """Analyze similarities between files with the same name across agent profiles."""
    similarities = []

    # Get all unique file paths across all agents
    all_file_paths = defaultdict(dict)

    for agent in agent_dirs:
        agent_path = os.path.join(agents_dir, agent)

        for root, _, files in os.walk(agent_path):
            for file in files:
                if file.endswith(('.md', '.py')):
                    full_path = os.path.join(root, file)
                    rel_path = os.path.relpath(full_path, agent_path)
                    all_file_paths[rel_path][agent] = full_path

    # Analyze files that appear in multiple agents
    for rel_path, agent_files in all_file_paths.items():
        if len(agent_files) > 1:
            file_similarities = []

            # Compare each pair of files
            agents = list(agent_files.keys())
            for i, agent1 in enumerate(agents):
                for agent2 in agents[i+1:]:
                    try:
                        with open(agent_files[agent1], 'r', encoding='utf-8') as f1:
                            content1 = f1.read().splitlines()
                        with open(agent_files[agent2], 'r', encoding='utf-8') as f2:
                            content2 = f2.read().splitlines()

                        # Calculate similarity ratio
                        matcher = difflib.SequenceMatcher(
                            None, content1, content2)
                        ratio = matcher.ratio()

                        file_similarities.append({
                            "agents": [agent1, agent2],
                            "similarity_ratio": ratio,
                            "identical": ratio > 0.99
                        })
                    except Exception as e:
                        print(
                            f"Error comparing {rel_path} between {agent1} and {agent2}: {e}")

            if file_similarities:
                similarities.append({
                    "file": rel_path,
                    "comparisons": file_similarities,
                    "average_similarity": sum(c["similarity_ratio"] for c in file_similarities) / len(file_similarities)
                })

    return {
        "file_similarities": similarities
    }


def suggest_optimizations(analysis):
    """Suggest optimizations based on the analysis."""
    suggestions = []

    # Check for completely identical files that could be moved to a common location
    if analysis.get("similarity_analysis", {}).get("file_similarities"):
        identical_files = []
        for file_data in analysis["similarity_analysis"]["file_similarities"]:
            if all(comp["identical"] for comp in file_data["comparisons"]):
                identical_files.append(file_data["file"])

        if identical_files:
            suggestions.append({
                "type": "identical_files",
                "description": "These files are identical across multiple agent profiles and could be moved to a common location:",
                "files": identical_files,
                "recommendation": "Create a 'common' directory and reference these files from there."
            })

    # Check for standardization opportunities in directory structure
    if analysis.get("structure_analysis", {}).get("common_paths"):
        missing_common_paths = {}
        common_paths = set(analysis["structure_analysis"]["common_paths"])

        for agent in analysis["agent_profiles"]:
            agent_paths = set()
            for path in analysis["structure_analysis"]["detailed_structure"].get(agent, {}):
                agent_paths.add(path)
                for file in analysis["structure_analysis"]["detailed_structure"][agent][path].get("files", []):
                    agent_paths.add(os.path.join(
                        path, file).replace("\\", "/"))

            missing = common_paths - agent_paths
            if missing:
                missing_common_paths[agent] = sorted(list(missing))

        if missing_common_paths:
            suggestions.append({
                "type": "missing_common_files",
                "description": "These agents are missing files that are common across other profiles:",
                "missing_files": missing_common_paths,
                "recommendation": "Standardize agent profiles by adding these common files."
            })

    # Check for divergent prompt files that might need standardization
    if analysis.get("prompt_analysis", {}).get("divergent_prompt_files"):
        divergent_files = analysis["prompt_analysis"]["divergent_prompt_files"]
        if divergent_files:
            suggestions.append({
                "type": "divergent_prompts",
                "description": "These prompt files exist across multiple agents but have different content:",
                "files": [file_data["file"] for file_data in divergent_files],
                "recommendation": "Review these files to determine if the differences are intentional or if they could be standardized."
            })

    # Suggest a template for new agent profiles
    common_files = analysis.get(
        "structure_analysis", {}).get("common_paths", [])
    if common_files:
        template_structure = {}
        for path in common_files:
            if "/" in path:
                dir_path, file = os.path.split(path)
                if dir_path not in template_structure:
                    template_structure[dir_path] = []
                template_structure[dir_path].append(file)
            else:
                if "" not in template_structure:
                    template_structure[""] = []
                template_structure[""].append(path)

        suggestions.append({
            "type": "agent_template",
            "description": "Suggested standard template for agent profiles:",
            "template": template_structure,
            "recommendation": "Create a '_template' directory with this structure for new agent profiles."
        })

    return suggestions


def print_analysis_results(analysis, suggestions):
    """Print the analysis results and optimization suggestions."""
    print("\n=== AGENT PROFILES ANALYSIS ===\n")

    # Print basic stats
    print(f"Total agent profiles: {len(analysis['agent_profiles'])}")
    for agent in analysis['agent_profiles']:
        prompt_count = analysis.get('prompt_analysis', {}).get(
            'prompt_stats', {}).get(agent, {}).get('prompt_file_count', 0)
        unique_paths = analysis.get('structure_analysis', {}).get(
            'stats', {}).get('unique_paths_per_agent', {}).get(agent, 0)
        print(
            f"  - {agent}: {prompt_count} prompt files, {unique_paths} unique files/directories")

    # Print common files
    common_paths = analysis.get(
        'structure_analysis', {}).get('common_paths', [])
    print(
        f"\nCommon files/directories across all profiles: {len(common_paths)}")
    for path in common_paths[:5]:  # Show just a few examples
        print(f"  - {path}")
    if len(common_paths) > 5:
        print(f"  - ... and {len(common_paths) - 5} more")

    # Print divergent prompt files
    divergent_files = analysis.get('prompt_analysis', {}).get(
        'divergent_prompt_files', [])
    print(
        f"\nPrompt files with different content across profiles: {len(divergent_files)}")
    for file_data in divergent_files[:3]:  # Show just a few examples
        print(
            f"  - {file_data['file']} (used in {', '.join(file_data['agents'])})")
    if len(divergent_files) > 3:
        print(f"  - ... and {len(divergent_files) - 3} more")

    # Print similar files
    similar_files = analysis.get(
        'similarity_analysis', {}).get('file_similarities', [])
    print(
        f"\nFiles with high similarity across profiles: {len(similar_files)}")
    for file_data in sorted(similar_files, key=lambda x: x['average_similarity'], reverse=True)[:3]:
        print(
            f"  - {file_data['file']} (avg. similarity: {file_data['average_similarity']:.2f})")
    if len(similar_files) > 3:
        print(f"  - ... and {len(similar_files) - 3} more")

    # Print suggestions
    print("\n=== OPTIMIZATION SUGGESTIONS ===\n")

    for i, suggestion in enumerate(suggestions, 1):
        print(f"{i}. {suggestion['description']}")

        if suggestion['type'] == 'identical_files':
            for file in suggestion['files'][:5]:  # Show just a few examples
                print(f"  - {file}")
            if len(suggestion['files']) > 5:
                print(f"  - ... and {len(suggestion['files']) - 5} more")

        elif suggestion['type'] == 'missing_common_files':
            for agent, files in suggestion['missing_files'].items():
                if files:
                    print(f"  - {agent} is missing:")
                    for file in files[:3]:
                        print(f"    * {file}")
                    if len(files) > 3:
                        print(f"    * ... and {len(files) - 3} more")

        elif suggestion['type'] == 'agent_template':
            print("  Suggested template structure:")
            for dir_path, files in suggestion['template'].items():
                if dir_path:
                    print(f"  - {dir_path}/")
                else:
                    print("  - [root]")
                for file in files[:3]:
                    print(f"    * {file}")
                if len(files) > 3:
                    print(f"    * ... and {len(files) - 3} more")

        print(f"  Recommendation: {suggestion['recommendation']}\n")


def save_analysis(analysis, suggestions, output_file="agent_analysis.json"):
    """Save the analysis results to a JSON file."""
    combined_data = {
        "analysis": analysis,
        "suggestions": suggestions
    }

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(combined_data, f, indent=2)

    print(f"\nAnalysis saved to {output_file}")


def main():
    """Main function to run the script."""
    agents_dir = "agents"

    print("=== AGENT ZERO PROFILE ANALYSIS TOOL ===")
    print("This tool analyzes agent profile directories to identify "
          "patterns, redundancies, and standardization opportunities.\n")

    analysis = analyze_agents(agents_dir)

    if not analysis:
        print("No analysis could be performed. Exiting.")
        return

    suggestions = suggest_optimizations(analysis)
    print_analysis_results(analysis, suggestions)

    choice = input(
        "\nWould you like to save the detailed analysis to a JSON file? (y/n): ")

    if choice.lower() == 'y':
        output_file = input(
            "Enter output filename (default: agent_analysis.json): ")
        if not output_file:
            output_file = "agent_analysis.json"
        save_analysis(analysis, suggestions, output_file)

        print("\nRecommended Next Steps:")
        print("1. Review the analysis and suggestions in detail")
        print("2. Create a standardized agent profile template")
        print("3. Consolidate identical files into a common location")
        print("4. Document the standard agent profile structure")
    else:
        print("\nAnalysis complete. No file was saved.")


if __name__ == "__main__":
    main()
