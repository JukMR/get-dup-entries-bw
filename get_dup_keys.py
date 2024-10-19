import json
from pathlib import Path
from typing import Any, TypeAlias

BitwardenJsonItems: TypeAlias = dict[str, Any]
BitwardenJsonExportFormat: TypeAlias = dict[str, BitwardenJsonItems | Any]


def get_latest_jsonfile_from_folder(folder: Path) -> Path:
    """Return latest json file from sorting by name"""
    backup_file = list(folder.rglob("*.json"))

    if len(backup_file) == 0:
        raise ValueError("Backup file not found")

    if len(backup_file) > 1:
        # Sort array of file by date
        backup_file.sort(reverse=True)

    return backup_file[0]


def get_latest_export_keys_from_bw_exports_folder() -> BitwardenJsonExportFormat:
    bw_exports_folder: Path = Path("bw_exports")
    if not bw_exports_folder.exists():
        raise ValueError("Missing bw_exports folder")

    backup_file = get_latest_jsonfile_from_folder(folder=bw_exports_folder)

    with open(backup_file, "r", encoding="utf-8") as fd:
        loaded_keys = json.load(fd)

    items = loaded_keys["items"]
    return items


def get_unique_elements_for_item(item: BitwardenJsonItems) -> tuple | None:
    try:
        login_item = item["login"]
    except KeyError:
        # print(f"This item seems to be a card {item}. Skipping it")
        return None

    username = login_item["username"]
    password = login_item["password"]
    uris = login_item["uris"]
    if len(uris) == 0:
        # print(f"Empty uris in {item} object")
        return None, username, password

    only_uris = (item["uri"] for item in uris)
    uris_tupled: tuple = tuple(sorted(only_uris))

    return uris_tupled, username, password


def get_unique_and_repeated(
    parsed_items: list[tuple],
) -> tuple[list[tuple], list[tuple]]:
    unique: list[tuple] = []
    repeated: list[tuple] = []

    for elem in parsed_items:
        if elem in unique:
            repeated.append(elem)
        else:
            unique.append(elem)

    return unique, repeated


def main() -> None:
    bw_export_file_items: BitwardenJsonExportFormat = get_latest_export_keys_from_bw_exports_folder()
    parsed_items: list[tuple] = []
    for it in bw_export_file_items:
        elem = get_unique_elements_for_item(it)
        if elem is None:
            continue

        parsed_items.append(elem)

    unique, repeated = get_unique_and_repeated(parsed_items=parsed_items)
    print(f"Found {len(unique)} unique elements.")
    print(f"Found {len(repeated)} repeated elements.")

    print(f"The repeated elements are: {repeated}")

    for item in repeated:
        print(item)


if __name__ == "__main__":
    main()
