import pytest
import requests
from uuid import UUID, uuid4
from datetime import datetime
import unittest


document_url = 'http://localhost:8000'
get_docs_url = f'{document_url}/get_docs'
add_doc_url = f'{document_url}/add_doc'
get_doc_by_id_url = f'{document_url}/doc_by_id/'
delete_doc_url = f'{document_url}/delete_document'

save_url = 'http://localhost:8001'


document = {
    "id": "8dcae814-7f01-407b-b85f-2bb12093d881",
    "owner_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "title": "Test",
    "body": "lalalalala"
}


class TestComponent(unittest.TestCase):
    # CMD: python tests/integration.py

    def test_1_get_docs(self):
        res = requests.get(f"{get_docs_url}")
        self.assertTrue(res != None)

    def test_2_add_doc(self):
        res = requests.post(f"{add_doc_url}", json=document)
        self.assertEqual(res.status_code, 200)

    def test_3_get_doc_by_id(self):
        res = requests.get(f"{get_doc_by_id_url}?{document['id']}").json()
        self.assertTrue(res, document)

    def test_4_delete_doc(self):
        res = requests.delete(f"{delete_doc_url}?doc_id={document['id']}").json()
        self.assertEqual(res, "Success")

if __name__ == '__main__':
    unittest.main()