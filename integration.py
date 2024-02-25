import unittest
import requests
import psycopg2
from time import sleep
import json
import sys
import os

from opentelemetry.sdk.metrics import export

from app.main import doc_health


def check_connect():
    try:
        conn = psycopg2.connect(
            dbname='DocumentsDB',
            user='artemenkov',
            password='roman',
            host='localhost',
            port='5432'
        )
        conn.close()
        return True
    except Exception as e:
        return False


class TestIntegration(unittest.TestCase):
    # CMD: python tests/integration.py

    def test_db_connection(self):
        sleep(5)
        self.assertEqual(check_connect(), True)

    def test_document_service_connection(self):
        res = doc_health()
        # r = requests.get("http://localhost:8000/health", verify=False)
        self.assertEqual(res.status_code, 200)

    def test_save_service_connection(self):
        # r = requests.get("http://localhost:8001/health", verify=False)
        self.assertEqual(r.status_code, 200)


if __name__ == '__main__':
    unittest.main()
