import json

import requests
from django.test import TestCase

CORRECT_IMPORT_BATCHES = [
    # Creating
    {
        "items": [
            {
                "type": "CATEGORY",
                "name": "Товары",
                "id": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
                "parentId": None
            }
        ],
        "updateDate": "2022-02-01T12:00:00.000Z"
    },
    {
        "items": [
            {
                "type": "CATEGORY",
                "name": "Смартфоны",
                "id": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
                "parentId": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1"
            },
            {
                "type": "OFFER",
                "name": "jPhone 13",
                "id": "863e1a7a-1304-42ae-943b-179184c077e3",
                "parentId": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
                "price": 79999
            },
            {
                "type": "OFFER",
                "name": "Xomiа Readme 10",
                "id": "b1d8fd7d-2ae3-47d5-b2f9-0f094af800d4",
                "parentId": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
                "price": 59999
            }
        ],
        "updateDate": "2022-02-02T12:00:00.000Z"
    },
    {
        "items": [
            {
                "type": "CATEGORY",
                "name": "Телевизоры",
                "id": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                "parentId": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1"
            },
            {
                "type": "OFFER",
                "name": "Samson 70\" LED UHD Smart",
                "id": "98883e8f-0507-482f-bce2-2fb306cf6483",
                "parentId": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                "price": 32999
            },
            {
                "type": "OFFER",
                "name": "Phyllis 50\" LED UHD Smarter",
                "id": "74b81fda-9cdc-4b63-8927-c978afed5cf4",
                "parentId": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                "price": 49999
            }
        ],
        "updateDate": "2022-02-03T12:00:00.000Z"
    },
    {
        "items": [
            {
                "type": "OFFER",
                "name": "Goldstar 65\" LED UHD LOL Very Smart",
                "id": "73bc3b36-02d1-4245-ab35-3106c9ee1c65",
                "parentId": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                "price": 69999
            }
        ],
        "updateDate": "2022-02-03T15:00:00.000Z"
    }
]
INCORRECT_IMPORT_BATCHES = [
    # These items have incorrect uuid
    {
        "items": [
            {
                "type": "CATEGORY",
                "name": "Товары",
                "id": "0",
                "parentId": None
            }
        ],
        "updateDate": "2022-02-01T12:00:00.000Z"
    },
    {
        "items": [
            {
                "type": "CATEGORY",
                "name": "Товары",
                "id": "rty657i87ikyfjhsg",
                "parentId": None
            }
        ],
        "updateDate": "2022-02-01T12:00:00.000Z"
    },
    {
        "items": [
            {
                "type": "CATEGORY",
                "name": "Товары",
                "id": "y515e43f-f3f6-4471-bb77-6b455017a2d0yi",
                "parentId": None
            }
        ],
        "updateDate": "2022-02-01T12:00:00.000Z"
    },

    # This item have nonexistent or incorrect parent
    {
        "items": [
            {
                "type": "CATEGORY",
                "name": "Штучки",
                "id": "2baa3982-f2dd-11ec-b939-0242ac120002",
                "parentId": "40o3tk30ogmrfo"
            }
        ],
        "updateDate": "2022-02-01T12:00:00.000Z"
    },
    # This item doesn't have name
    {
        "items": [
            {
                "type": "CATEGORY",
                "name": None,
                "id": "2baa3982-f2dd-11ec-b939-0242ac120002",
                "parentId": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1"
            }
        ],
        "updateDate": "2022-02-01T12:00:00.000Z"
    },
    # This items have incorrect prices
    {
        "items": [
            {
                "type": "CATEGORY",
                "name": "Планшеты",
                "id": "c4238886-f2dc-11ec-b939-0242ac120002",
                "parentId": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
                "price": 80000
            },
        ],
        "updateDate": "2022-02-03T12:00:00.000Z"
    },
    {
        "items": [
            {
                "type": "OFFER",
                "name": "Xiaomi Pad 5 Global",
                "id": "c4238886-f2dc-11ec-b939-0242ac120002",
                "parentId": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
                "price": None
            },
        ],
        "updateDate": "2022-02-03T12:00:00.000Z"
    },
    {
        "items": [
            {
                "type": "OFFER",
                "name": "TCL 10 TABMAX 4G",
                "id": "c4238886-f2dc-11ec-b939-0242ac120002",
                "parentId": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
            },
        ],
        "updateDate": "2022-02-03T12:00:00.000Z"
    },
    {
        "items": [
            {
                "type": "OFFER",
                "name": "Samsung Galaxy Tab A7",
                "id": "c4238886-f2dc-11ec-b939-0242ac120002",
                "parentId": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
                "price": -90000
            }
        ],
        "updateDate": "2022-02-03T12:00:00.000Z"
    },
    # There is no updateDate or updateDate is incorrect
    {
        "items": [
            {
                "type": "CATEGORY",
                "name": "НЕВЕРОЯТНЫЕ ТОВАРЫ",
                "id": "c4238886-f2dc-11ec-b939-0242ac120002",
                "parentId": None
            },
        ]
    },
    {
        "items": [
            {
                "type": "CATEGORY",
                "name": "НЕВЕРОЯТНЫЕ ТОВАРЫ",
                "id": "c4238886-f2dc-11ec-b939-0242ac120002",
                "parentId": None
            },
        ],
        "updateDate": "10/29/2539 B.E."
    },
]
CORRECT_NODES_BATCHES = [
    (
        'nodes/069cb8d7-bbdd-47d3-ad8f-82ef4c269df1',
        {
            "type": "CATEGORY",
            "name": "Товары",
            "id": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
            "price": 58599,
            "parentId": None,
            "date": "2022-02-03T15:00:00.000Z",
            "children": [
                {
                    "type": "CATEGORY",
                    "name": "Смартфоны",
                    "id": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
                    "price": 69999,
                    "parentId": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
                    "date": "2022-02-02T12:00:00.000Z",
                    "children": [
                        {
                            "type": "OFFER",
                            "name": "jPhone 13",
                            "id": "863e1a7a-1304-42ae-943b-179184c077e3",
                            "price": 79999,
                            "parentId": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
                            "date": "2022-02-02T12:00:00.000Z",
                            "children": None
                        },
                        {
                            "type": "OFFER",
                            "name": "Xomiа Readme 10",
                            "id": "b1d8fd7d-2ae3-47d5-b2f9-0f094af800d4",
                            "price": 59999,
                            "parentId": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
                            "date": "2022-02-02T12:00:00.000Z",
                            "children": None
                        }
                    ]
                },
                {
                    "type": "CATEGORY",
                    "name": "Телевизоры",
                    "id": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                    "price": 50999,
                    "parentId": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
                    "date": "2022-02-03T15:00:00.000Z",
                    "children": [
                        {
                            "type": "OFFER",
                            "name": "Samson 70\" LED UHD Smart",
                            "id": "98883e8f-0507-482f-bce2-2fb306cf6483",
                            "price": 32999,
                            "parentId": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                            "date": "2022-02-03T12:00:00.000Z",
                            "children": None
                        },
                        {
                            "type": "OFFER",
                            "name": "Phyllis 50\" LED UHD Smarter",
                            "id": "74b81fda-9cdc-4b63-8927-c978afed5cf4",
                            "price": 49999,
                            "parentId": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                            "date": "2022-02-03T12:00:00.000Z",
                            "children": None
                        },
                        {
                            "type": "OFFER",
                            "name": "Goldstar 65\" LED UHD LOL Very Smart",
                            "id": "73bc3b36-02d1-4245-ab35-3106c9ee1c65",
                            "price": 69999,
                            "parentId": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                            "date": "2022-02-03T15:00:00.000Z",
                            "children": None
                        }
                    ]
                }
            ]
        }
    ),
    (
        'nodes/1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2',
        {
            "type": "CATEGORY",
            "name": "Телевизоры",
            "id": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
            "parentId": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
            "price": 50999,
            "date": "2022-02-03T15:00:00.000Z",
            "children": [
                {
                    "type": "OFFER",
                    "name": "Samson 70\" LED UHD Smart",
                    "id": "98883e8f-0507-482f-bce2-2fb306cf6483",
                    "parentId": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                    "price": 32999,
                    "date": "2022-02-03T12:00:00.000Z",
                    "children": None,
                },
                {
                    "type": "OFFER",
                    "name": "Phyllis 50\" LED UHD Smarter",
                    "id": "74b81fda-9cdc-4b63-8927-c978afed5cf4",
                    "parentId": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                    "price": 49999,
                    "date": "2022-02-03T12:00:00.000Z",
                    "children": None
                },
                {
                    "type": "OFFER",
                    "name": "Goldstar 65\" LED UHD LOL Very Smart",
                    "id": "73bc3b36-02d1-4245-ab35-3106c9ee1c65",
                    "parentId": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                    "price": 69999,
                    "date": "2022-02-03T15:00:00.000Z",
                    "children": None
                }
            ]
        }
    ),
    (
        'nodes/d515e43f-f3f6-4471-bb77-6b455017a2d2',
        {
            "type": "CATEGORY",
            "name": "Смартфоны",
            "id": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
            "price": 69999,
            "parentId": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
            "date": "2022-02-02T12:00:00.000Z",
            "children": [
                {
                    "type": "OFFER",
                    "name": "jPhone 13",
                    "id": "863e1a7a-1304-42ae-943b-179184c077e3",
                    "price": 79999,
                    "parentId": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
                    "date": "2022-02-02T12:00:00.000Z",
                    "children": None
                },
                {
                    "type": "OFFER",
                    "name": "Xomiа Readme 10",
                    "id": "b1d8fd7d-2ae3-47d5-b2f9-0f094af800d4",
                    "price": 59999,
                    "parentId": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
                    "date": "2022-02-02T12:00:00.000Z",
                    "children": None
                }
            ]
        }
    )
]
INCORRECT_NODES_BATCHES = [
    # Incorrect uuid
    ('nodes/1', 400),
    ('nodes/2', 400),
    # Not found
    ('nodes/60e6c814-f2f0-11ec-b939-0242ac120002', 404),
    ('nodes/9ec49468-f2f0-11ec-b939-0242ac120002', 404),
]
DELETING_BATCHES = [
    # Incorrect uuid
    ('delete/1', 400),
    ('delete/2', 400),
    # Not found
    ('delete/60e6c814-f2f0-11ec-b939-0242ac120002', 404),
    ('delete/9ec49468-f2f0-11ec-b939-0242ac120002', 404),
    # Correct deleting
    ('delete/d515e43f-f3f6-4471-bb77-6b455017a2d2', 200)
]
SALES_BATCHES = [
    (
        'sales?date=2022-02-04T00%3A00%3A00.000Z',
        [
            {
                "type": "OFFER",
                "name": "Samson 70\" LED UHD Smart",
                "id": "98883e8f-0507-482f-bce2-2fb306cf6483",
                "price": 32999,
                "parentId": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                "date": "2022-02-03T12:00:00.000Z",
                "children": []
            },
            {
                "type": "OFFER",
                "name": "Phyllis 50\" LED UHD Smarter",
                "id": "74b81fda-9cdc-4b63-8927-c978afed5cf4",
                "price": 49999,
                "parentId": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                "date": "2022-02-03T12:00:00.000Z",
                "children": []
            },
            {
                "type": "OFFER",
                "name": "Goldstar 65\" LED UHD LOL Very Smart",
                "id": "73bc3b36-02d1-4245-ab35-3106c9ee1c65",
                "price": 69999,
                "parentId": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                "date": "2022-02-03T15:00:00.000Z",
                "children": []
            }
        ]
    ),
]
DELETE_ALL = 'delete/069cb8d7-bbdd-47d3-ad8f-82ef4c269df1'


URL = 'http://0.0.0.0:80/'


def deep_sort_children(node: dict) -> None:
    if node.get("children"):
        node["children"].sort(key=lambda x: x["id"])

        for child in node["children"]:
            deep_sort_children(child)


class TestRestApi(TestCase):
    def test(self) -> None:
        self.correct_import()
        self.incorrect_import()
        self.correct_nodes()
        self.incorrect_nodes()
        self.deleting()
        self.sales()
        self.delete_all()
        print('ALL TESTS PASSED')

    def correct_import(self) -> None:
        print('Test correct import')
        for idx, batch in enumerate(CORRECT_IMPORT_BATCHES):
            json_data = json.dumps(batch)
            response = requests.post(url=URL + 'imports', json=json_data)
            assert response.status_code == 200, \
                f'Expected status code 200,' \
                f' but got {response.status_code} {response.json()}'
            print(f'{idx + 1} Batch completed')
        print('Test correct import completed')

    def incorrect_import(self) -> None:
        print('Test incorrect import')
        for idx, batch in enumerate(INCORRECT_IMPORT_BATCHES):
            json_data = json.dumps(batch)
            response = requests.post(url=URL + 'imports', json=json_data)
            assert response.status_code == 400, \
                f'Expected status code 400, but got {response.status_code}'
            print(f'{idx + 1} Batch completed')
        print('Test incorrect import completed')

    def correct_nodes(self) -> None:
        print('Test correct nodes')
        for idx, branch in enumerate(CORRECT_NODES_BATCHES):
            relative_url, data = branch
            response = requests.get(url=URL + relative_url)
            res_data = response.json()
            deep_sort_children(data)
            deep_sort_children(res_data)
            assert data == res_data, f'Expected {data}, but got {res_data}'
            print(f'{idx + 1} Batch completed')
        print('Test correct nodes completed')

    def incorrect_nodes(self) -> None:
        print('Test incorrect nodes')
        for idx, branch in enumerate(INCORRECT_NODES_BATCHES):
            relative_url, code = branch
            response = requests.get(url=URL + relative_url)
            assert response.status_code == code, \
                f'Expected code {code}, but got {response.status_code}'
            print(f'{idx + 1} Batch completed')
        print('Test incorrect nodes completed')

    def deleting(self) -> None:
        print('Test deleting')
        for idx, branch in enumerate(DELETING_BATCHES):
            relative_url, code = branch
            response = requests.delete(url=URL + relative_url)
            assert response.status_code == code, \
                f'Expected code {code}, but got {response.status_code}'
            print(f'{idx + 1} Batch completed')
        print('Test correct deleting completed')

    def delete_all(self):
        requests.delete(URL + DELETE_ALL)

    def sales(self) -> None:
        print('Test sales')
        for idx, branch in enumerate(SALES_BATCHES):
            relative_url, data = branch
            response = requests.get(url=URL + relative_url)
            res_data = response.json()
            assert res_data == data, \
                f'Expected data {data}, but got {res_data}'
            print(f'{idx + 1} Batch completed')
        print('Test correct sales completed')
