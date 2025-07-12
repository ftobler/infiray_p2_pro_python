import subprocess
import pytest


def test_flake8_passes():
    try:
        subprocess.run(["flake8", "infiray_show/", "tests/"], capture_output=True, check=True, text=True)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"flake8 failed: {e.stdout}\n{e.stderr}")
