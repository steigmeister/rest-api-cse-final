import unittest
from app import app, SECRET_KEY
import jwt

class LibraryAPITestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.token = jwt.encode({'user': 'test', 'exp': 9999999999}, SECRET_KEY, algorithm='HS256')

    def test_login(self):
        response = self.app.post('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.get_json())

    def test_get_authors_json(self):
        response = self.app.get('/authors', headers={'Authorization': f'Bearer {self.token}'})
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.get_json(), list)

    def test_get_authors_xml(self):
        response = self.app.get('/authors?format=xml', headers={'Authorization': f'Bearer {self.token}'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('<authors>', response.get_data(as_text=True))

    def test_search(self):
        response = self.app.get('/search?q=Rowling', headers={'Authorization': f'Bearer {self.token}'})
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.get_json()), 0)

if __name__ == '__main__':
    unittest.main()