import subprocess

def capture_screenshot() -> bytes:
    result = subprocess.run(
        ["adb", "exec-out", "screencap", "-p"],
        capture_output=True,
        check=True,
    )
    return result.stdout