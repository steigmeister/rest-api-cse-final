```markdown
# 📚 Library REST API – CSE1 Final Project

A secure, fully-featured **CRUD REST API** for managing a **Library database** (Authors & Books), built with **Flask**, **MySQL**, and **JWT authentication**. Supports **JSON** and **XML** output formats, includes **search**, **input validation**, and **automated tests**.

---

## ✅ Features

- ✅ **CRUD operations** for Authors and Books  
- 🔒 **JWT authentication** for secure access  
- 📦 **Dual output**: `?format=json` (default) or `?format=xml`  
- 🔍 **Search endpoint**: `/search?q=...`  
- 🧪 **Pytest coverage** for all core endpoints  
- 🛡️ Proper **HTTP status codes**: 200, 201, 400, 401, 404  
- 🌐 RESTful design compliant with CSE1 finals rubric

---

## 🛠️ Installation

> 💡 **Note**: This guide uses **Git Bash on Windows 11**

### 1. Clone the Repository

```bash
git clone https://github.com/steigmeister/library-rest-api-final.git
cd library-rest-api-final

```

### 2. Set Up MySQL Database

> Ensure **XAMPP** is installed and **MySQL is running**.

- Open **phpMyAdmin** at `http://localhost/phpmyadmin`
- Create a database named `library_db`
- Import the provided `library_db.sql` **OR** run the following SQL:

```sql
CREATE TABLE Authors (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    birth_year INT,
    nationality VARCHAR(50)
);

CREATE TABLE Books (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    isbn VARCHAR(20) UNIQUE,
    publication_year INT,
    author_id INT,
    FOREIGN KEY (author_id) REFERENCES Authors(id) ON DELETE CASCADE
);

```

### 3. Create and Activate Virtual Environment

```bash
python -m venv venv
source venv/Scripts/activate  # On Windows Git Bash
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

> ✅ `requirements.txt` includes:  
> `Flask`, `Flask-MySQLdb`, `PyJWT`, `pytest`, and secure transitive dependencies.

### 5. Set JWT Secret (Environment Variable)

Create a `.env` file (never committed):

```bash
echo "JWT_SECRET=$(python -c 'import secrets; print(secrets.token_urlsafe(32))')" > .env
```

✅ This generates a strong, random secret.

### 6. Run the Application

```bash
python app.py
```

The API is now running at:  
👉 **http://127.0.0.1:5000**

---

## 🧪 Running Tests

```bash
pytest test_app.py -v
```

✅ Expected output:
```
5 passed in 0.30s
```

Tests cover:
- JWT login
- JSON/XML output
- CRUD operations
- Search
- Security (401 without token)

---

## 📡 API Usage (via `curl` in Bash)

### 1. Get JWT Token

```bash
TOKEN=$(curl -s -X POST http://127.0.0.1:5000/login | jq -r '.token')
echo "Token: $TOKEN"
```

> 💡 Install `jq` via: `choco install jq` (Windows) or `sudo apt install jq` (Linux)

### 2. Get Authors (JSON)

```bash
curl -H "Authorization: Bearer $TOKEN" http://127.0.0.1:5000/authors
```

### 3. Get Authors (XML)

```bash
curl -H "Authorization: Bearer $TOKEN" "http://127.0.0.1:5000/authors?format=xml"
```

### 4. Search for "Rowling"

```bash
curl -H "Authorization: Bearer $TOKEN" "http://127.0.0.1:5000/search?q=Rowling"
```

### 5. Create New Author

```bash
curl -X POST http://127.0.0.1:5000/authors \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "Octavia Butler", "birth_year": 1947, "nationality": "American"}'
```

---

## 🔐 Security

- All endpoints (except `/login`) require:  
  `Authorization: Bearer <token>`
- Invalid/missing token → `401 Unauthorized`
- Missing required fields (e.g., `name`) → `400 Bad Request`
- Secret stored in `.env` → **never in code or Git**

---

## 📁 Project Structure

```
.
├── app.py                 # Main Flask API
├── test_app.py            # Pytest test suite
├── requirements.txt       # Dependencies
├── .gitignore             # Excludes venv, .env, cache
├── .env                   # Local JWT secret (ignored by Git)
└── README.md              # This file
```

---


## 📚 References

- [Flask](https://flask.palletsprojects.com/)
- [PyJWT](https://pyjwt.readthedocs.io/)
- [pytest](https://docs.pytest.org/)
- [Flask-MySQLdb](https://flask-mysqldb.readthedocs.io/)

---

> **Built with ❤️ for CSE1 – Palawan State University**  
> By: Troyjan Rana (BSCS-3, Block II)
```
