# src/jules_cli/commands/suggest.py

import typer
from typing import Optional
from ..commands.task import run_task
from ..utils.logging import logger

MASTER_SUGGEST_PROMPT = """
You are a Senior Staff Engineer auditing this repository.
Your goal is to suggest high-impact improvements.

Please scan the codebase and identify:
1. Critical technical debt or anti-patterns.
2. Missing edge-case handling or error handling.
3. Areas with low test coverage or brittle tests.
4. Performance bottlenecks.
5. Opportunities to modernize the stack (e.g., new language features).

Output a detailed plan with specific, actionable steps to address the top 3 most important findings.
Do not execute code yet; wait for approval.
"""

def cmd_suggest(
    focus: Optional[str] = typer.Option(None, "--focus", "-f", help="Focus area (e.g., security, tests, performance)."),
):
    """
    Ask Jules to proactively scan the repo and suggest improvements.
    """
    prompt = MASTER_SUGGEST_PROMPT
    
    if focus:
        prompt += f"\n\nPlease prioritize your analysis on: {focus.upper()}."

    logger.info("🧠 Starting proactive code analysis...")
    logger.info("This may take a moment as Jules reads the repository context...")
    
    # We reuse run_task because it handles session creation, polling, and result display perfectly.
    return run_task(prompt)