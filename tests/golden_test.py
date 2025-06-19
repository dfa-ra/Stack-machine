import subprocess
from pathlib import Path
import pytest
from pytest_golden.plugin import GoldenTestFixture
import sys

ROOT_PATH = (Path(__file__).parent / "../../").resolve()
if str(ROOT_PATH) not in sys.path:
    sys.path.insert(0, str(ROOT_PATH))

TEST_DIR = Path(__file__).parent
MAIN_EMULATOR_PATH = (TEST_DIR / "../main.py").resolve()

assert MAIN_EMULATOR_PATH.exists(), f"File {MAIN_EMULATOR_PATH} doesn't exist!"


def run_command(cmd: list[str]) -> str:
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        pytest.fail(f"Command failed: {result.stderr}")
    return result.stdout


def run_default(name: str) -> str:
    test_cases_path = Path("tests/golden/")
    input_forth = (test_cases_path / name / (name + ".forth")).resolve()
    input_conf = (test_cases_path / name / (name + ".yaml")).resolve()

    assert input_forth.exists(), f"ASM file missing: {input_forth}"
    assert input_conf.exists(), f"Config file missing: {input_conf}"

    out_emulator = run_command(
        ["python3", str(MAIN_EMULATOR_PATH), "-c", str(input_conf), str(input_forth)]
    )

    return out_emulator


@pytest.mark.golden_test("golden/cat/test_conf.yaml")
def test_cat(golden: GoldenTestFixture) -> None:
    name = "cat"
    out_emulator = run_default(name)

    assert out_emulator == golden.out["output"]

@pytest.mark.golden_test("golden/hello/test_conf.yaml")
def test_hello(golden: GoldenTestFixture) -> None:
    name = "hello"
    out_emulator = run_default(name)

    assert out_emulator == golden.out["output"]

@pytest.mark.golden_test("golden/hello_user_name/test_conf.yaml")
def test_hello_user_name(golden: GoldenTestFixture) -> None:
    name = "hello_user_name"
    out_emulator = run_default(name)

    assert out_emulator == golden.out["output"]

@pytest.mark.golden_test("golden/prob2/test_conf.yaml")
def test_prob2(golden: GoldenTestFixture) -> None:
    name = "prob2"
    out_emulator = run_default(name)

    assert out_emulator == golden.out["output"]

@pytest.mark.golden_test("golden/sort/test_conf.yaml")
def test_sort(golden: GoldenTestFixture) -> None:
    name = "sort"
    out_emulator = run_default(name)

    assert out_emulator == golden.out["output"]

@pytest.mark.golden_test("golden/ssm/test_conf.yaml")
def test_ssm(golden: GoldenTestFixture) -> None:
    name = "ssm"
    out_emulator = run_default(name)

    assert out_emulator == golden.out["output"]

@pytest.mark.golden_test("golden/vsm/test_conf.yaml")
def test_vsm(golden: GoldenTestFixture) -> None:
    name = "vsm"
    out_emulator = run_default(name)

    assert out_emulator == golden.out["output"]
