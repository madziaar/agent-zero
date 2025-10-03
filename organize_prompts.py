#!/usr/bin/env python
"""
Organize Prompts Script for Agent Zero
-------------------------------------
This script analyzes the prompts directory and suggests a better 
organization structure.
It can also implement the suggested changes if requested.
"""

import os
import re
import shutil
from pathlib import Path
from collections import defaultdict


def analyze_prompts(prompts_dir="prompts"):
    """
    Analyze the prompts directory and group files by category.
    """
    print(f"Analyzing prompts directory: {prompts_dir}")

    if not os.path.isdir(prompts_dir):
        print(f"Error: {prompts_dir} is not a directory or does not exist.")
        return None

    # Group patterns to identify
    patterns = {
        "system": r"agent\.system\.",
        "framework": r"fw\.",
        "memory": r"memory\.",
        "behaviour": r"behaviour\.",
        "tool": r"tool\.",
        "utilities": r"^(?!agent|fw|memory|behaviour).*\.(?:sys|msg)\.md$"
    }

    categories = defaultdict(list)
    unclassified = []

    # Analyze each file
    for file_path in Path(prompts_dir).glob("*.md"):
        filename = file_path.name
        classified = False

        for category, pattern in patterns.items():
            if re.search(pattern, filename):
                categories[category].append(str(file_path))
                classified = True
                break

        if not classified:
            unclassified.append(str(file_path))

    # Further categorize system files
    if categories["system"]:
        system_subcategories = defaultdict(list)
        for file_path in categories["system"]:
            filename = os.path.basename(file_path)
            if "main" in filename:
                system_subcategories["main"].append(file_path)
            elif "tool" in filename:
                system_subcategories["tools"].append(file_path)
            elif "behaviour" in filename:
                system_subcategories["behaviour"].append(file_path)
            else:
                system_subcategories["other"].append(file_path)

        # Replace the system category with subcategories
        del categories["system"]
        for subcategory, files in system_subcategories.items():
            categories[f"system_{subcategory}"] = files

    # Add unclassified files
    if unclassified:
        categories["unclassified"] = unclassified

    return categories


def suggest_structure(categories):
    """
    Suggest a new directory structure based on the analysis.
    """
    if not categories:
        return None

    suggested_structure = {
        "prompts/": {
            "system/": {
                "main/": "Core system prompts defining agent behavior",
                "tools/": "Tool-specific system prompts",
                "behaviour/": "Behaviour adjustment prompts",
                "other/": "Other system prompts"
            },
            "framework/": "Internal framework messages",
            "memory/": "Memory-related prompts",
            "tools/": "Tool-related prompts",
            "utilities/": "Utility prompts for various functions"
        }
    }

    return suggested_structure


def print_analysis(categories, suggested_structure):
    """
    Print the analysis results and suggested structure.
    """
    print("\n=== PROMPT FILES ANALYSIS ===\n")

    total_files = sum(len(files) for files in categories.values())
    print(f"Total prompt files: {total_files}\n")

    for category, files in categories.items():
        print(f"{category}: {len(files)} files")
        for file in files[:3]:  # Show first 3 examples
            print(f"  - {os.path.basename(file)}")
        if len(files) > 3:
            print(f"  - ... and {len(files) - 3} more files")
        print()

    print("\n=== SUGGESTED DIRECTORY STRUCTURE ===\n")

    def print_tree(structure, indent=0):
        for key, value in structure.items():
            print("  " * indent + key)
            if isinstance(value, dict):
                print_tree(value, indent + 1)
            else:
                print("  " * (indent + 1) + f"- {value}")

    print_tree(suggested_structure)


def implement_reorganization(categories, prompts_dir="prompts", backup=True):
    """
    Implement the suggested reorganization.
    """
    if not categories:
        return False

    # Create backup
    if backup:
        backup_dir = f"{prompts_dir}_backup"
        print(f"Creating backup at {backup_dir}...")
        if os.path.exists(backup_dir):
            shutil.rmtree(backup_dir)
        shutil.copytree(prompts_dir, backup_dir)

    # Create new directory structure
    new_structure = {
        "system": {
            "main": [f for f in categories.get("system_main", [])],
            "tools": [f for f in categories.get("system_tools", [])],
            "behaviour": [f for f in categories.get("system_behaviour", [])],
            "other": [f for f in categories.get("system_other", [])]
        },
        "framework": [f for f in categories.get("framework", [])],
        "memory": [f for f in categories.get("memory", [])],
        "tools": [f for f in categories.get("tool", [])],
        "utilities": [f for f in categories.get("utilities", [])],
        "unclassified": [f for f in categories.get("unclassified", [])]
    }

    # Create directories and move files
    for category, content in new_structure.items():
        if isinstance(content, dict):
            # Handle subcategories
            for subcategory, files in content.items():
                if not files:
                    continue

                subdir = os.path.join(prompts_dir, category, subcategory)
                os.makedirs(subdir, exist_ok=True)

                for file_path in files:
                    filename = os.path.basename(file_path)
                    dest_path = os.path.join(subdir, filename)
                    shutil.move(file_path, dest_path)
                    print(f"Moved {filename} to {subdir}")
        else:
            # Handle top-level categories
            if not content:
                continue

            category_dir = os.path.join(prompts_dir, category)
            os.makedirs(category_dir, exist_ok=True)

            for file_path in content:
                filename = os.path.basename(file_path)
                dest_path = os.path.join(category_dir, filename)
                shutil.move(file_path, dest_path)
                print(f"Moved {filename} to {category_dir}")

    print("\nReorganization complete!")
    return True


def main():
    """
    Main function to run the script.
    """
    prompts_dir = "prompts"

    print("=== AGENT ZERO PROMPT ORGANIZATION TOOL ===")
    print("This tool analyzes and reorganizes the prompt files "
          "for better organization.\n")

    categories = analyze_prompts(prompts_dir)

    if not categories:
        print("No analysis could be performed. Exiting.")
        return

    suggested_structure = suggest_structure(categories)
    print_analysis(categories, suggested_structure)

    choice = input("\nWould you like to implement this reorganization? "
                   "(y/n): ")

    if choice.lower() == 'y':
        implement_reorganization(categories, prompts_dir)
        print("\nRecommended Next Steps:")
        print("1. Update any scripts or code that reference specific "
              "prompt files")
        print("2. Review the reorganized structure to ensure it meets "
              "your needs")
        print("3. Run tests to verify functionality is preserved")
    else:
        print("\nNo changes were made. You can run this script again later "
              "to implement the changes.")


if __name__ == "__main__":
    main()
