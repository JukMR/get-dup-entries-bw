from pytest import fixture

from get_dup_keys import BitwardenItem, get_unique_and_repeated, parse_raw_items


@fixture
def item_mock() -> list[dict]:
    items = [
        {
            "passwordHistory": None,
            "revisionDate": "2022-08-15T00:18:49.546Z",
            "creationDate": "2022-08-15T00:18:49.546Z",
            "deletedDate": None,
            "id": "abcdefg1-1234-5678-1234-123412341234",
            "organizationId": None,
            "folderId": None,
            "type": 1,
            "reprompt": 0,
            "name": "--",
            "notes": None,
            "favorite": False,
            "login": {
                "fido2Credentials": [],
                "uris": [
                    {
                        "match": None,
                        "uri": "www.url.com",
                    }
                ],
                "username": "user",
                "password": "pass",
                "totp": None,
            },
            "collectionIds": None,
        },
        {
            "passwordHistory": None,
            "revisionDate": "2022-08-15T00:18:49.546Z",
            "creationDate": "2022-08-15T00:18:49.546Z",
            "deletedDate": None,
            "id": "abcdefg1-5678-5678-1234-123412341234",
            "organizationId": None,
            "folderId": None,
            "type": 1,
            "reprompt": 0,
            "name": "--",
            "notes": None,
            "favorite": False,
            "login": {
                "fido2Credentials": [],
                "uris": [
                    {
                        "match": None,
                        "uri": "www.url.com",
                    }
                ],
                "username": "user",
                "password": "pass",
                "totp": None,
            },
            "collectionIds": None,
        },
    ]
    return items


def test_parsing_from_raw_item(item_mock) -> None:
    items_parsed = parse_raw_items(item_mock)

    assert items_parsed == [
        BitwardenItem(
            username="user",
            password="pass",
            uris=("www.url.com",),
        ),
        BitwardenItem(
            username="user",
            password="pass",
            uris=("www.url.com",),
        ),
    ]


def test_full_cycle(item_mock) -> None:
    items_parsed = parse_raw_items(item_mock)
    unique, repeated = get_unique_and_repeated(items_parsed)
    assert repeated == [
        BitwardenItem(
            username="user",
            password="pass",
            uris=("www.url.com",),
        ),
    ]
