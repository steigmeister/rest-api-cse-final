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

# JWT Secret Key
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

# Helper: dict list to XML
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

# get the format from param
def get_format():
    return request.args.get('format', 'json').lower()

# --- AUTH ENDPOINT ---
@app.route('/login', methods=['POST'])
def login():
    token = jwt.encode({
        'user': 'user',
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
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