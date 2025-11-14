from ..utils.commands import run_cmd

def run_pytest() -> (int, str, str):
    print("[+] Running pytest...")
    return run_cmd(["pytest", "-q", "--maxfail=1"])
