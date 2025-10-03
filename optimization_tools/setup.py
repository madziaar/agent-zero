#!/usr/bin/env python
"""
Setup Script for Agent Zero Optimization Tools
----------------------------------------------
This script sets up the optimization tools directory structure
and moves existing optimization tools into the proper location.
"""

import os
import shutil


def setup_optimization_tools():
    """
    Set up the optimization tools directory and move existing tools.
    """
    # Get the current directory
    current_dir = os.getcwd()
    tools_dir = os.path.join(current_dir, "optimization_tools")

    # Create the optimization_tools directory if it doesn't exist
    if not os.path.exists(tools_dir):
        os.makedirs(tools_dir)
        print(f"Created directory: {tools_dir}")

    # List of tools to move
    tools = [
        "cleanup_caches.py",
        "organize_prompts.py",
        "analyze_agents.py"
    ]

    # Move each tool to the optimization_tools directory
    moved_files = []
    for tool in tools:
        source_path = os.path.join(current_dir, tool)
        dest_path = os.path.join(tools_dir, tool)

        if os.path.exists(source_path):
            if not os.path.exists(dest_path):
                shutil.copy2(source_path, dest_path)
                print(f"Copied {tool} to {tools_dir}")
                moved_files.append(tool)
            else:
                print(f"File already exists: {dest_path}")
        else:
            print(f"Source file not found: {source_path}")

    # Create __init__.py to make it a proper Python package
    init_path = os.path.join(tools_dir, "__init__.py")
    if not os.path.exists(init_path):
        with open(init_path, "w") as f:
            f.write('''"""
Agent Zero Optimization Tools Package
------------------------------------
Tools for analyzing, optimizing, and maintaining the Agent Zero codebase.
"""

__version__ = "0.1.0"
''')
        print(f"Created {init_path}")

    # Print summary
    if moved_files:
        print("\nSuccessfully set up the optimization tools:")
        for file in moved_files:
            print(f"- {file}")

        print("\nYou can now remove the original files from the root "
              "directory if desired.")
        print("Use the tools from the optimization_tools directory like this:")
        print("  python -m optimization_tools.cleanup_caches")
        print("  python -m optimization_tools.organize_prompts")
        print("  python -m optimization_tools.analyze_agents")
    else:
        print("\nNo files were moved. The tools might already be in place "
              "or not found.")


if __name__ == "__main__":
    setup_optimization_tools()
