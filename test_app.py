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

    def test_add_author(self):
        new_author = {"name": "Test Author", "birth_year": 1990, "nationality": "Testland"}
        response = self.app.post('/authors', json=new_author, headers={'Authorization': f'Bearer {self.token}'})
        self.assertEqual(response.status_code, 201)
        self.assertIn('message', response.get_json())

    def test_update_author(self):
        
        self.app.post('/authors', json={"name": "Author to Update"}, headers={'Authorization': f'Bearer {self.token}'})
        
        get_resp = self.app.get('/authors', headers={'Authorization': f'Bearer {self.token}'})
        authors = get_resp.get_json()
        author_id = authors[-1]['id']
        
        updated = {"name": "Updated Name", "birth_year": 2000, "nationality": "Updated"}
        response = self.app.put(f'/authors/{author_id}', json=updated, headers={'Authorization': f'Bearer {self.token}'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('message', response.get_json())

    def test_delete_author(self):
        
        self.app.post('/authors', json={"name": "Author to Delete"}, headers={'Authorization': f'Bearer {self.token}'})
        get_resp = self.app.get('/authors', headers={'Authorization': f'Bearer {self.token}'})
        authors = get_resp.get_json()
        author_id = authors[-1]['id']
        response = self.app.delete(f'/authors/{author_id}', headers={'Authorization': f'Bearer {self.token}'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('message', response.get_json())

    def test_search(self):
        
        response = self.app.get('/search?q=Orwell', headers={'Authorization': f'Bearer {self.token}'})
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        
        if isinstance(data, list):
            self.assertGreater(len(data), 0)
        else:
            
            self.assertNotEqual(data.get('message'), 'No results found')

if __name__ == '__main__':
    unittest.main()