import unittest
import json
import xml.etree.ElementTree as ET
from app import app, SECRET_KEY
import jwt

class LibraryAPITestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        # Generate a valid token
        self.token = jwt.encode({'user': 'test', 'exp': 9999999999}, SECRET_KEY, algorithm='HS256')

    def test_login(self):
        response = self.app.post('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', json.loads(response.data))

    def test_get_authors_json(self):
        response = self.app.get('/authors', headers={'Authorization': f'Bearer {self.token}'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')

    def test_get_authors_xml(self):
        response = self.app.get('/authors?format=xml', headers={'Authorization': f'Bearer {self.token}'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/xml')
        # Try parsing XML
        ET.fromstring(response.data)

    def test_add_author(self):
        response = self.app.post('/authors',
            json={'name': 'Test Author', 'birth_year': 1990, 'nationality': 'Testland'},
            headers={'Authorization': f'Bearer {self.token}'}
        )
        self.assertEqual(response.status_code, 201)

    def test_search(self):
        response = self.app.get('/search?q=Harry', headers={'Authorization': f'Bearer {self.token}'})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertGreater(len(data), 0)

if __name__ == '__main__':
    unittest.main()