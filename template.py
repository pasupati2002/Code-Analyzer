import os
from pathlib import Path

project_files = [
    "src/__init__.py",
    "src/analyzer.py",
    "src/prompts.py",
    "src/utils.py",
    "app.py",
    "README.md",
    ".env",
    ".gitignore",
    "requirements.txt",
    "tests/__init__.py",
]

for filepath in project_files:
    filepath = Path(filepath)
    filedir = filepath.parent

    if str(filedir) != ".":
        os.makedirs(filedir, exist_ok=True)

    if not filepath.exists() or filepath.stat().st_size == 0:
        filepath.touch()
        print(f"Created: {filepath}")
    else:
        print(f"Already exists: {filepath}")