from flask import Flask, request, make_response, jsonify
from flask_mysqldb import MySQL
import json
import xml.etree.ElementTree as ET
from functools import wraps
import jwt
import datetime

app = Flask(__name__)
app.config.from_pyfile('config.py')

mysql = MySQL(app)

# JWT Secret
SECRET_KEY = 'library_secret_key_123'

# JWT Auth Decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        try:
            token = token.replace('Bearer ', '')
            data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        except:
            return jsonify({'message': 'Token is invalid'}), 401
        return f(*args, **kwargs)
    return decorated

# Helper: Convert dict list to XML
def dict_to_xml(tag, d):
    elem = ET.Element(tag)
    for key, val in d.items():
        child = ET.SubElement(elem, key)
        child.text = str(val) if val is not None else ''
    return elem

def list_to_xml(root_tag, items, item_tag):
    root = ET.Element(root_tag)
    for item in items:
        root.append(dict_to_xml(item_tag, item))
    return ET.tostring(root, encoding='unicode')

# Helper: Get format from query param
def get_format():
    return request.args.get('format', 'json').lower()

# --- AUTH ENDPOINT ---
@app.route('/login', methods=['POST'])
def login():
    token = jwt.encode({
        'user': 'user',
        'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=24)
    }, SECRET_KEY, algorithm='HS256')
    return jsonify({'token': token})

# --- AUTHORS ENDPOINTS ---
@app.route('/authors', methods=['GET'])
@token_required
def get_authors():
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, name, birth_year, nationality FROM Authors")
    rows = cur.fetchall()
    cur.close()

    authors = []
    for row in rows:
        authors.append({
            'id': row[0],
            'name': row[1],
            'birth_year': row[2],
            'nationality': row[3]
        })

    fmt = get_format()
    if fmt == 'xml':
        xml_str = list_to_xml('authors', authors, 'author')
        response = make_response(xml_str)
        response.headers['Content-Type'] = 'application/xml'
        return response
    else:
        return jsonify(authors)

@app.route('/authors', methods=['POST'])
@token_required
def add_author():
    data = request.get_json()
    name = data.get('name')
    birth_year = data.get('birth_year')
    nationality = data.get('nationality')

    if not name:
        return jsonify({'error': 'Name is required'}), 400

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO Authors (name, birth_year, nationality) VALUES (%s, %s, %s)",
                (name, birth_year, nationality))
    mysql.connection.commit()
    cur.close()
    return jsonify({'message': 'Author added'}), 201

@app.route('/authors/<int:id>', methods=['PUT'])
@token_required
def update_author(id):
    data = request.get_json()
    name = data.get('name')
    birth_year = data.get('birth_year')
    nationality = data.get('nationality')

    cur = mysql.connection.cursor()
    cur.execute("UPDATE Authors SET name=%s, birth_year=%s, nationality=%s WHERE id=%s",
                (name, birth_year, nationality, id))
    mysql.connection.commit()
    cur.close()
    return jsonify({'message': 'Author updated'})

@app.route('/authors/<int:id>', methods=['DELETE'])
@token_required
def delete_author(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM Authors WHERE id=%s", (id,))
    mysql.connection.commit()
    cur.close()
    return jsonify({'message': 'Author deleted'})

# --- BOOKS ENDPOINTS ---
@app.route('/books', methods=['GET'])
@token_required
def get_books():
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT b.id, b.title, b.isbn, b.publication_year, b.author_id, a.name as author_name
        FROM Books b
        LEFT JOIN Authors a ON b.author_id = a.id
    """)
    rows = cur.fetchall()
    cur.close()

    books = []
    for row in rows:
        books.append({
            'id': row[0],
            'title': row[1],
            'isbn': row[2],
            'publication_year': row[3],
            'author_id': row[4],
            'author_name': row[5]
        })

    fmt = get_format()
    if fmt == 'xml':
        xml_str = list_to_xml('books', books, 'book')
        response = make_response(xml_str)
        response.headers['Content-Type'] = 'application/xml'
        return response
    else:
        return jsonify(books)

@app.route('/books', methods=['POST'])
@token_required
def add_book():
    data = request.get_json()
    title = data.get('title')
    isbn = data.get('isbn')
    pub_year = data.get('publication_year')
    author_id = data.get('author_id')

    if not title:
        return jsonify({'error': 'Title is required'}), 400

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO Books (title, isbn, publication_year, author_id) VALUES (%s, %s, %s, %s)",
                (title, isbn, pub_year, author_id))
    mysql.connection.commit()
    cur.close()
    return jsonify({'message': 'Book added'}), 201

@app.route('/books/<int:id>', methods=['PUT'])
@token_required
def update_book(id):
    data = request.get_json()
    title = data.get('title')
    isbn = data.get('isbn')
    pub_year = data.get('publication_year')
    author_id = data.get('author_id')

    cur = mysql.connection.cursor()
    cur.execute("UPDATE Books SET title=%s, isbn=%s, publication_year=%s, author_id=%s WHERE id=%s",
                (title, isbn, pub_year, author_id, id))
    mysql.connection.commit()
    cur.close()
    return jsonify({'message': 'Book updated'})

@app.route('/books/<int:id>', methods=['DELETE'])
@token_required
def delete_book(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM Books WHERE id=%s", (id,))
    mysql.connection.commit()
    cur.close()
    return jsonify({'message': 'Book deleted'})

# --- SEARCH ENDPOINT ---
@app.route('/search', methods=['GET'])
@token_required
def search():
    query = request.args.get('q', '').strip()
    if not query:
        return jsonify({'error': 'Search query "q" is required'}), 400

    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT 'author' as type, id, name as title, NULL as isbn, birth_year as year FROM Authors WHERE name LIKE %s
        UNION
        SELECT 'book' as type, id, title, isbn, publication_year as year FROM Books WHERE title LIKE %s
    """, (f'%{query}%', f'%{query}%'))
    rows = cur.fetchall()
    cur.close()

    results = []
    for row in rows:
        results.append({
            'type': row[0],
            'id': row[1],
            'title': row[2],
            'isbn': row[3],
            'year': row[4]
        })

    fmt = get_format()
    if fmt == 'xml':
        xml_str = list_to_xml('results', results, 'item')
        response = make_response(xml_str)
        response.headers['Content-Type'] = 'application/xml'
        return response
    else:
        return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)