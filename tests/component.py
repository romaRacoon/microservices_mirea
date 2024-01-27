import pytest
import requests
from uuid import UUID, uuid4
from datetime import datetime
import json

document_url = 'https://localhost:8000'
save_url = 'https://localhost:8001'
add_doc_url = f'{document_url}/add_doc'
get_doc_by_id_url = f'{document_url}/doc_by_id/'

document = {
    "id": str(uuid4()),
    "owner_id": "TrainModel123",
    "title": "SomeDirection",
    "body": str(datetime.now())
}


def test_train_get():
    pytest.assume(requests.post(add_doc_url, json=document) == 200)
    res = requests.get(f"{get_doc_by_id_url}/{document['id']}")
    pytest.assume('owner_id' in res.keys())
    pytest.assume('title' in res.keys())
    pytest.assume('body' in res.keys())
