#!/usr/bin/env python3
"""
Stack Overflow Answer Validator - Because 2015 code shouldn't run your 2024 project.
"""

import re
import sys
import warnings
from datetime import datetime
from typing import Optional


def extract_code_blocks(text: str) -> list[str]:
    """Extracts code from those beautiful ``` blocks. Returns empty list if you're unlucky."""
    return re.findall(r'```(?:python)?\n(.*?)```', text, re.DOTALL)


def check_imports(code: str) -> list[str]:
    """Finds imports that might be deprecated, like your ex's promises."""
    deprecated_patterns = [
        (r'from tkinter import ttk', 'ttk is still fine, but are YOU?'),
        (r'import urllib2', 'Python 2 called, it wants its imports back'),
        (r'from StringIO import', 'This import is so old it has a pension'),
        (r'import md5', 'MD5? More like M-Deprecated'),
        (r'print \w+', 'Missing parentheses - the classic sign of vintage code')
    ]
    
    issues = []
    for pattern, message in deprecated_patterns:
        if re.search(pattern, code):
            issues.append(message)
    return issues


def check_for_magic_numbers(code: str) -> list[str]:
    """Because 42 might be the answer, but not a good timeout value."""
    magic_numbers = re.findall(r'\b\d{3,}\b', code)
    if magic_numbers:
        return [f"Magic number(s) found: {', '.join(magic_numbers)} - hope they're not port numbers"]
    return []


def validate_stackoverflow_answer(answer_text: str, url: Optional[str] = None) -> dict:
    """
    Validates a Stack Overflow answer.
    Returns a verdict that's probably more accurate than the answer itself.
    """
    code_blocks = extract_code_blocks(answer_text)
    
    if not code_blocks:
        return {
            "status": "SUSPICIOUS",
            "message": "No code blocks found. Probably just philosophical advice about programming."
        }
    
    all_issues = []
    for i, code in enumerate(code_blocks, 1):
        issues = check_imports(code) + check_for_magic_numbers(code)
        if issues:
            all_issues.append(f"Block {i}: {' | '.join(issues)}")
    
    current_year = datetime.now().year
    if url and re.search(r'stackoverflow\.com/questions/\d+/', url):
        # Extract question ID and make a wild guess about age
        match = re.search(r'questions/(\d+)/', url)
        if match:
            qid = int(match.group(1))
            # Early SO questions have lower IDs (started 2008)
            if qid < 1000000:  # Rough heuristic
                all_issues.append(f"Question ID {qid} looks ancient (like before {current_year-5})")
    
    if all_issues:
        return {
            "status": "PROBABLY_OUTDATED",
            "message": "Potential issues found:" + "\n- ".join([''] + all_issues),
            "advice": "Check library docs instead. Or just rewrite it yourself like a real developer."
        }
    
    return {
        "status": "MAYBE_OK",
        "message": "No obvious red flags. But remember: Stack Overflow answers age like milk.",
        "advice": "Test thoroughly before production. Or better yet, write your own solution."
    }


def main():
    """Main function because every script needs one, like every developer needs coffee."""
    print("Stack Overflow Answer Validator")
    print("=" * 40)
    
    if len(sys.argv) > 1:
        # Read from file
        with open(sys.argv[1], 'r') as f:
            content = f.read()
    else:
        # Or from stdin
        print("Paste Stack Overflow answer (Ctrl+D when done):")
        content = sys.stdin.read()
    
    url = sys.argv[2] if len(sys.argv) > 2 else None
    result = validate_stackoverflow_answer(content, url)
    
    print(f"\nVerdict: {result['status']}")
    print(result['message'])
    if 'advice' in result:
        print(f"\nAdvice: {result['advice']}")


if __name__ == "__main__":
    main()
