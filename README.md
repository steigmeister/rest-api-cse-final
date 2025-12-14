```markdown
# 📚 Library REST API – CSE1 Final Project

A secure and fully-featured **CRUD REST API** for managing a **Library database** (Authors and Books), built with **Flask**, **MySQL**, and **JWT authentication**. Supports **JSON** and **XML** output formats, includes **search functionality**, **input validation**, and **comprehensive test coverage**.

---

## ✨ Features

- ✅ **Full CRUD operations** for Authors and Books  
- 🔒 **JWT-based authentication** for protected endpoints  
- 📦 **Dual output format**:  
  - Default: **JSON**  
  - Optional: **XML** via `?format=xml`  
- 🔍 **Search endpoint**: `/search?q=<query>` (searches both authors and books)  
- 🧪 **7 automated tests** using `pytest` (covers all core features)  
- 🛡️ **Proper HTTP status codes**:  
  - `200 OK`, `201 Created`  
  - `400 Bad Request` (invalid input)  
  - `401 Unauthorized` (missing/invalid token)  
  - `404 Not Found` (resource not found)  
- 🌐 RESTful design compliant with CSE1 grading rubric

---

## 🛠️ Installation

### Prerequisites
- **Python 3.10+**
- **XAMPP** (or any MySQL server)
- **Git**

### Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/steigmeister/rest-api-cse-final.git
   cd rest-api-cse-final
   ```

2. **Set up MySQL Database**
   - Start **XAMPP** → Launch **MySQL**
   - Open **phpMyAdmin** (`http://localhost/phpmyadmin`)
   - Create a database named `library_db`
   - Import the provided `library_db.sql` (or run the table creation + seed SQL)

3. **Create and activate virtual environment**
   ```powershell
   # Windows (PowerShell)
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Set JWT secret (environment variable)**
   ```powershell
   # PowerShell
   $env:JWT_SECRET="your_strong_secret_here"
   ```
   > 🔐 **Never hardcode secrets in source code.**

6. **Run the application**
   ```bash
   python app.py
   ```
   The API is now running at: **http://127.0.0.1:5000**

---

## 🧪 Testing

Run the full test suite:
```bash
pytest test_app.py -v
```

✅ Expected output:
```
7 passed in X.XXs
```

Tests cover:
- JWT login
- JSON and XML output
- Create, Read, Update, Delete (Authors)
- Search functionality
- Security and validation

---

## 📡 API Endpoints

> 🔑 All endpoints (except `/login`) require:  
> `Authorization: Bearer <your_token>`

### Authentication
| Method | Endpoint | Description |
|--------|---------|-------------|
| `POST` | `/login` | Get JWT token (no auth required) |

### Authors
| Method | Endpoint | Description |
|--------|---------|-------------|
| `GET` | `/authors` | List all authors |
| `POST` | `/authors` | Create new author |
| `PUT` | `/authors/<id>` | Update author by ID |
| `DELETE` | `/authors/<id>` | Delete author by ID |

### Books
| Method | Endpoint | Description |
|--------|---------|-------------|
| `GET` | `/books` | List all books |
| `POST` | `/books` | Create new book |
| `PUT` | `/books/<id>` | Update book by ID |
| `DELETE` | `/books/<id>` | Delete book by ID |

### Search
| Method | Endpoint | Description |
|--------|---------|-------------|
| `GET` | `/search?q=<query>` | Search authors and books by name/title |

### Output Format
Append `?format=json` (default) or `?format=xml` to any `GET` endpoint.

---

## 📥 Example Requests (PowerShell)

### Get JWT Token
```powershell
$token = (Invoke-RestMethod http://127.0.0.1:5000/login -Method POST).token
```

### Get Authors in JSON
```powershell
Invoke-RestMethod http://127.0.0.1:5000/authors -Headers @{Authorization="Bearer $token"}
```

### Get Authors in XML
```powershell
(Invoke-WebRequest "http://127.0.0.1:5000/authors?format=xml" -Headers @{Authorization="Bearer $token"}).Content
```

### Search for "Orwell"
```powershell
Invoke-RestMethod "http://127.0.0.1:5000/search?q=Orwell" -Headers @{Authorization="Bearer $token"}
```

---

## 🔐 Security

- JWT secret is loaded from environment variable (`JWT_SECRET`)
- All sensitive endpoints are protected by `@token_required` decorator
- Input validation prevents incomplete records (e.g., missing `name` → `400`)
- No hardcoded credentials in source code

> 💡 **Note**: Generate a strong secret using:  
> `python -c "import secrets; print(secrets.token_urlsafe(32))"`

---

## 📁 Project Structure

```
.
├── app.py                 # Main Flask application
├── test_app.py            # Pytest test suite (7 tests)
├── requirements.txt       # Project dependencies
├── .gitignore             # Excludes venv, cache
├── README.md              # This file
└── library_db.sql         # Database dump (in submission package)
```

---
