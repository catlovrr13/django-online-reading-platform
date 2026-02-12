#!/usr/bin/env python3
"""
Clear Django migrations + pycache + other junk
Use with caution - irreversible!
"""

import os
import shutil
import sys
from pathlib import Path

def remove_tree(path: Path) -> None:
    if path.exists():
        print(f"Removing: {path}")
        if path.is_dir():
            shutil.rmtree(path, ignore_errors=True)
        else:
            path.unlink(missing_ok=True)

def main():
    project_root = Path.cwd().resolve()
    print(f"Cleaning project: {project_root}\n")

    patterns_to_delete = [
        # Python cache
        "**/__pycache__",
        "**/*.pyc",
        "**/*.pyo",
        "**/*.pyd",
        
        # Django migrations (except __init__.py)
        "**/migrations/*.py",
        "**/migrations/*.pyc",
        "!**/migrations/__init__.py",
        
        # Common junk
        "**/.pytest_cache",
        "**/.coverage",
        "**/coverage.xml",
        "**/htmlcov",
        "**/*.log",
    ]

    deleted_count = 0

    for pattern in patterns_to_delete:
        if pattern.startswith("!"):
            # Skip negation patterns for now (we'll handle __init__.py separately)
            continue
            
        for item in project_root.glob(pattern):
            if item.is_file() and item.name == "__init__.py" and "migrations" in item.parts:
                continue  # protect migrations/__init__.py
                
            remove_tree(item)
            deleted_count += 1

    # Special handling: remove empty migrations folders
    for migrations_dir in project_root.glob("**/migrations"):
        if migrations_dir.is_dir():
            remaining = list(migrations_dir.glob("*"))
            if len(remaining) == 1 and remaining[0].name == "__init__.py":
                print(f"Removing empty migrations folder: {migrations_dir}")
                remove_tree(migrations_dir)
                deleted_count += 1

    print(f"\nFinished. Removed {deleted_count} items.")
    print("\nNext steps usually are:")
    print("1. python manage.py makemigrations")
    print("2. python manage.py migrate --fake-initial  # or just migrate")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] in ("--help", "-h"):
        print(__doc__)
        sys.exit(0)

    answer = input("This will DELETE migrations and pycache. Continue? [y/N] ").strip().lower()
    if answer not in ("y", "yes"):
        print("Aborted.")
        sys.exit(1)

    main()