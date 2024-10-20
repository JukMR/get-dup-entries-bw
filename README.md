# Bitwarden duplicated keys

This repository has a script which gets the entries which seems to be duplicated in a bitwarden export. This is useful
if you accidently duplicated you vault while doing exports and imports and have many entries duplicated in your db.

NOTE: this script only show you which entries are duplicated but doesn't delete anything. You will still need to delete
them in your bitwarden vault.

## Usage

To use it, generate a plain json export from the bitwarden client. Put this json file in the `bw_exports` folder.
Execute `get_dup_keys.py` by doing:

```bash
poetry install
poetry shell
python3 get_dup_keys.py

```

or simply

```bash
poetry run python3 get_dup_keys.py
```

