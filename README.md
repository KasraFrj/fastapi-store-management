# 🛒 FastAPI Store Management System

A full-featured RESTful API for e-commerce store management, built with **FastAPI** and **PostgreSQL**.

---

## ✨ Features

- 🔐 **Authentication** — User registration and login with `bcrypt` password hashing and `JWT` token-based auth
- 📦 **Product Management** — Full CRUD operations for products
- 🛍️ **Cart System** — Smart shopping cart with relational item-product linking via SQLAlchemy ORM
- 📄 **Auto Documentation** — Interactive Swagger UI at `/docs` with built-in token authorization

---

## 🛠 Tech Stack

| Layer | Technology |
|---|---|
| Framework | FastAPI |
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| Auth | PyJWT + Passlib (bcrypt) |
| Server | Uvicorn |

---

## 📁 Project Structure

```
fastapi-store-management/
├── app/
│   ├── main.py          # App entry point & router registration
│   ├── models.py        # SQLAlchemy database models
│   ├── schemas.py       # Pydantic request/response schemas
│   ├── crud.py          # Database operations
│   ├── auth.py          # JWT & password utilities
│   └── database.py      # DB connection & session
├── requirements.txt
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- PostgreSQL running locally

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/KasraFrj/fastapi-store-management.git
cd fastapi-store-management

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
```

### Configuration

Create a `.env` file in the root directory:

```env
DATABASE_URL=postgresql://your_user:your_password@localhost:5432/store_db
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Run the Application

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

---

## 📖 API Endpoints

### Auth
| Method | Endpoint | Description |
|---|---|---|
| POST | `/auth/register` | Register a new user |
| POST | `/auth/login` | Login and receive JWT token |

### Products
| Method | Endpoint | Description |
|---|---|---|
| GET | `/products` | List all products |
| GET | `/products/{id}` | Get a single product |
| POST | `/products` | Create a product |
| PUT | `/products/{id}` | Update a product |
| DELETE | `/products/{id}` | Delete a product |

### Cart
| Method | Endpoint | Description |
|---|---|---|
| GET | `/cart` | View current user's cart |
| POST | `/cart/items` | Add item to cart |
| DELETE | `/cart/items/{id}` | Remove item from cart |

> 📝 Full interactive documentation available at `http://localhost:8000/docs`

---

## 🔒 Authentication

This API uses **JWT Bearer tokens**. After logging in, include the token in your requests:

```
Authorization: Bearer <your_token>
```

In Swagger UI (`/docs`), click the **Authorize** button and paste your token to test protected endpoints.

---

## 📬 Contact

**Kasra** — [@KasraFrj](https://github.com/KasraFrj)
