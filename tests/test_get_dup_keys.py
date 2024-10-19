from pathlib import Path

import pytest

from get_dup_keys import get_latest_jsonfile_from_folder


def test_get_latest_jsonfile_from_folder_no_files(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="Backup file not found"):
        get_latest_jsonfile_from_folder(tmp_path)


def test_get_latest_jsonfile_from_folder_single_file(tmp_path: Path) -> None:
    file = tmp_path / "file1.json"
    file.write_text("{}")
    assert get_latest_jsonfile_from_folder(tmp_path) == file


def test_get_latest_jsonfile_from_folder_multiple_files(tmp_path: Path) -> None:
    file1 = tmp_path / "file1.json"
    file2 = tmp_path / "file2.json"
    file1.write_text("{}")
    file2.write_text("{}")
    assert get_latest_jsonfile_from_folder(tmp_path) == file2


def test_get_latest_jsonfile_from_folder_sorted_by_name(tmp_path: Path) -> None:
    file1 = tmp_path / "a_file.json"
    file2 = tmp_path / "b_file.json"
    file1.write_text("{}")
    file2.write_text("{}")
    assert get_latest_jsonfile_from_folder(tmp_path) == file2
