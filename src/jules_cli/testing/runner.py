from ..utils.commands import run_cmd
from ..utils.logging import logger
import json
import tempfile
import os
from typing import Tuple

def run_tests(runner: str = "pytest") -> Tuple[int, str, str]:
    """
    Run tests using the specified runner.

    Args:
        runner: The test runner to use ('pytest', 'unittest', 'nose2').

    Returns:
        tuple: (exit_code, stdout, stderr)
    """
    if runner == "pytest":
        return _run_pytest()
    elif runner == "unittest":
        return _run_unittest()
    elif runner == "nose2":
        return _run_nose2()
    else:
        raise ValueError(f"Unknown runner: {runner}")

def _run_pytest() -> Tuple[int, str, str]:
    logger.info("Running pytest...")

    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tmp:
        report_path = tmp.name

    try:
        code, out, err = run_cmd(["pytest", "-q", "--maxfail=1", "--json-report", f"--json-report-file={report_path}"])

        try:
            with open(report_path) as f:
                report = json.load(f)
            summary = report.get("summary", {})
            logger.info(
                f"Test run summary: "
                f"{summary.get('passed', 0)} passed, "
                f"{summary.get('failed', 0)} failed, "
                f"{summary.get('skipped', 0)} skipped."
            )
        except (FileNotFoundError, json.JSONDecodeError):
            logger.warning("Could not read pytest report.")
    finally:
        if os.path.exists(report_path):
            os.remove(report_path)

    return code, out, err

def _run_unittest() -> Tuple[int, str, str]:
    logger.info("Running unittest...")
    # unittest prints output to stderr by default
    return run_cmd(["python", "-m", "unittest"])

def _run_nose2() -> Tuple[int, str, str]:
    logger.info("Running nose2...")
    return run_cmd(["python", "-m", "nose2"])
