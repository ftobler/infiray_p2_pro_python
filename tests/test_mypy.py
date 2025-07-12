import subprocess
import pytest


def test_mypy_passes():
    try:
        subprocess.run(["mypy", "infiray_show/", "tests/"], capture_output=True, check=True, text=True)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"""mypy failed: {e.stdout}
{e.stderr}""")
