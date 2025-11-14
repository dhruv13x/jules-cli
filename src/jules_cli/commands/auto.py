from ..pytest.runner import run_pytest
from .task import run_task
from ..utils.logging import logger

def auto_fix_command(repo_dir_name="bot_platform"):
    # run pytest first
    code, out, err = run_pytest()
    if code == 0:
        logger.info("🎉 All tests passed. Nothing to do.")
        return {"status": "success", "message": "All tests passed."}
    failure_text = out + "\n" + err
    run_task(prompt_from_failure(failure_text), repo_dir_name=repo_dir_name, auto=True)
    return {"status": "running", "message": "Attempting to fix failed tests."}

def prompt_from_failure(failure_text: str) -> str:
    return (
        "You are Jules, an automated debugging assistant. I will paste pytest output. "
        "Produce a minimal, correct fix and include any new tests required. "
        "Return changes as changeSet.gitPatch.unidiffPatch or create a PR artifact. "
        "Pytest output:\n" + failure_text
    )
