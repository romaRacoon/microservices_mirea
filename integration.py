import unittest
import requests
import psycopg2
from time import sleep
import json
import sys
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR / 'document_service/app'))

from document_service.app import main as main_1
from save_service.app import main as main_2

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
        r = main_1.doc_health()
        self.assertEqual(r, "'message': 'service is active'")

    def test_save_service_connection(self):
        r = main_2.doc_health()
        self.assertEqual(r.status_code, 200)


if __name__ == '__main__':
    unittest.main()
