import difflib
import filecmp
import shutil
from collections.abc import Generator
from pathlib import Path

import pytest
from _pytest.capture import CaptureFixture
from _pytest.fixtures import FixtureRequest

TEST_FOLDER = "test_cases"
BASELINE_FOLDER = "baseline"
TMP_FOLDER = "tmp"

def get_test_folder_path(test_case_path: str) -> str:
    # Traverse up until TEST_CASE_FOLDER is found
    current_dir = Path(test_case_path).parent
    while True:
        folder_name = current_dir.name
        if folder_name == TEST_FOLDER:
            return str(current_dir)
        parent_dir = current_dir.parent
        if parent_dir == current_dir:
            raise ValueError(f"Could not find the '{TEST_FOLDER}' directory in the path hierarchy.")
        current_dir = parent_dir

def get_file_paths(request: FixtureRequest) -> tuple[str, str]:
    test_case_path = str(request.path)

    test_folder_dir = get_test_folder_path(test_case_path)

    # Compute relative path from ROOT_DIR as before
    relative_path = Path(test_case_path).relative_to(Path(test_folder_dir))

    path_parts = list(relative_path.parts)

    new_path_parts = path_parts

    # We create a directory in the baseline & tmp folder for every test file
    new_path_parts[-1] = new_path_parts[-1].split(".")[0]

    # Then, we use the test function name as file name in that directory
    test_function_name = request.function.__name__
    if not test_function_name.startswith("test_"):
        raise ValueError("Test function does not follow naming convention")
    new_path_parts.append(test_function_name)

    # Get path of Baseline Dir and Tmp Dir
    parent_dir = Path(test_folder_dir).parent
    baseline_path = str(parent_dir / BASELINE_FOLDER / "/".join(new_path_parts)) + ".baseline"
    tmp_path = str(parent_dir / TMP_FOLDER / "/".join(new_path_parts)) + ".tmp"

    return baseline_path, tmp_path


# Saves std output to a file and compares it against our baseline
@pytest.fixture
def output_test(request: FixtureRequest, capsys: CaptureFixture[str]) -> Generator[None, None, None]:  # use "capfd" for fd-level
    baseline_path, tmp_path = get_file_paths(request)

    Path(tmp_path).parent.mkdir(parents=True, exist_ok=True)

    yield

    captured = capsys.readouterr()

    with Path(tmp_path).open("w") as file:
        file.write("Output:\n")
        file.write(captured.out)

        if captured.err:
            pytest.fail("Output test should only have positive test cases. This file contains an error")

    if not Path(baseline_path).exists():
        Path(baseline_path).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(tmp_path, baseline_path)
        print(f"Baseline file created: {baseline_path}")
    else:
        if not filecmp.cmp(tmp_path, baseline_path):
            with Path(tmp_path).open() as f:
                tmp_lines = f.readlines()

            with Path(baseline_path).open() as f:
                baseline_lines = f.readlines()

            diff = difflib.unified_diff(
                baseline_lines,
                tmp_lines,
                fromfile="baseline",
                tofile="tmp",
                lineterm=""
            )

            error_msg = "Tmp file and baseline file do not match:\n"
            error_msg += "\n".join(diff)

            pytest.fail(error_msg)
