import json
from pathlib import Path
from typing import Any, Generator, Literal, TypeAlias

import pydantic

BitwardenJsonItems: TypeAlias = dict[Literal["username"] | Literal["password"] | Literal["uris"], Any]
BitwardenJsonExportFormat: TypeAlias = list[dict[Literal["login"] | Any, BitwardenJsonItems | Any]]


class BitwardenItem(pydantic.BaseModel):
    username: str | None
    password: str | None
    uris: tuple[str, ...] | None

    def __str__(self) -> str:
        """Custom method for displaying class"""
        output_str = ""
        output_str += f"uris: {self.uris}" + "\n"
        output_str += f"username: {self.username}" + "\n"
        output_str += f"password: {self.password}" + "\n"
        return output_str


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


def parsed_bitwarden_item(item: BitwardenJsonItems) -> BitwardenItem:
    username = item["username"]
    password = item["password"]
    uris = item["uris"]

    if len(uris) == 0:
        return BitwardenItem(uris=None, username=username, password=password)

    only_uris: Generator[str, None, None] = (item["uri"] for item in uris)
    uris_tupled: tuple = tuple(sorted(only_uris))

    return BitwardenItem(uris=uris_tupled, username=username, password=password)


def get_unique_and_repeated(
    parsed_items: list[BitwardenItem],
) -> tuple[list[BitwardenItem], list[BitwardenItem]]:
    unique: list[BitwardenItem] = []
    repeated: list[BitwardenItem] = []

    for elem in parsed_items:
        if elem in unique:
            repeated.append(elem)
        else:
            unique.append(elem)

    return unique, repeated


def parse_raw_items(bw_export_items) -> list[BitwardenItem]:
    parsed_items: list[BitwardenItem] = []

    for it in bw_export_items:
        if "login" not in it:
            # Only process item elements, skip everything else
            continue

        login_item = it["login"]
        elem: BitwardenItem = parsed_bitwarden_item(login_item)

        parsed_items.append(elem)

    return parsed_items


def print_results(unique: list[BitwardenItem], repeated: list[BitwardenItem]) -> None:
    print(f"Found {len(unique)} unique elements.")
    print(f"Found {len(repeated)} repeated elements.")

    print("The repeated elements are:")
    for item in repeated:
        print(item)


def main() -> None:
    bw_export_file_items: BitwardenJsonExportFormat = get_latest_export_keys_from_bw_exports_folder()

    parsed_items: list[BitwardenItem] = parse_raw_items(bw_export_items=bw_export_file_items)
    unique: list[BitwardenItem]
    repeated: list[BitwardenItem]
    unique, repeated = get_unique_and_repeated(parsed_items=parsed_items)

    print_results(unique=unique, repeated=repeated)


if __name__ == "__main__":
    main()
