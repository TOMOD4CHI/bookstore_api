# FastAPI Bookstore API

A modern, secure REST API for managing a bookstore built with FastAPI, featuring user authentication, book management, and Redis caching.

## 🚀 Features

- **User Authentication**: JWT-based authentication system with secure password hashing
- **Book Management**: Full CRUD operations for books with ownership control
- **Security**: Password hashing with bcrypt and JWT token authentication
- **Database**: SQLAlchemy ORM with SQLite (easily configurable for other databases)
- **Caching**: Redis integration for improved performance (optional)
- **Validation**: Pydantic models for request/response validation
- **Authorization**: Users can only modify their own books

## 📋 Requirements

- Python 3.8+
- Redis (optional, for caching)
- SQLite (default) or any SQL database supported by SQLAlchemy

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd fastapi-bookstore
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```env
   SECRET_KEY=your-super-secret-key-here
   DATABASE_URL=sqlite:///./bookstore.db
   ```

5. **Start Redis (optional, for caching)**
   ```bash
   redis-server
   ```

6. **Run the application**
   ```bash
   uvicorn main:app --reload
   ```

The API will be available at `http://localhost:8000`

## 📚 API Documentation

Once the server is running, you can access:
- **Interactive API Docs**: http://localhost:8000/docs (Swagger UI)
- **Alternative Docs**: http://localhost:8000/redoc (ReDoc)

## 🔐 Authentication

The API uses JWT (JSON Web Tokens) for authentication. Tokens expire after 30 minutes.

### Authentication Flow:
1. Register a new user or login with existing credentials
2. Receive a JWT access token
3. Include the token in the `Authorization` header: `Bearer <your_token>`

## 📖 API Endpoints

### User Management

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/register` | Register a new user | ❌ |
| POST | `/login` | Login and get access token | ❌ |
| GET | `/me` | Get current user info | ✅ |

### Book Management

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/books` | List all books with filters | ❌ |
| GET | `/books/{book_id}` | Get a specific book | ❌ |
| GET | `/books/my` | Get current user's books | ✅ |
| POST | `/books` | Create a new book | ✅ |
| PUT | `/books/{book_id}` | Update a book (owner only) | ✅ |
| DELETE | `/books/{book_id}` | Delete a book (owner only) | ✅ |

## 📝 Usage Examples

### 1. Register a new user
```bash
curl -X POST "http://localhost:8000/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "bookworm",
    "password": "securepassword123"
  }'
```

### 2. Login
```bash
curl -X POST "http://localhost:8000/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "bookworm",
    "password": "securepassword123"
  }'
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### 3. Add a book (authenticated)
```bash
curl -X POST "http://localhost:8000/books" \
  -H "Authorization: Bearer <your_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "The Python Guide",
    "author": "John Doe",
    "price": 29.99
  }'
```

### 4. List books with filters
```bash
curl "http://localhost:8000/books?title=python&max_price=50&limit=10"
```

### 5. Get your books (authenticated)
```bash
curl -X GET "http://localhost:8000/books/my" \
  -H "Authorization: Bearer <your_token>"
```

## 🏗️ Project Structure

```
├── main.py              # FastAPI application entry point
├── auth.py              # JWT authentication and password hashing
├── database.py          # Database connection and configuration
├── tables.py            # SQLAlchemy table definitions
├── models.py            # Pydantic models for validation
├── crud.py              # Database operations
├── cache.py             # Redis caching utilities
├── routes/
│   ├── __init__.py
│   ├── users.py         # User-related endpoints
│   └── books.py         # Book-related endpoints
├── requirements.txt     # Project dependencies
├── .env                 # Environment variables (not in repo)
└── .gitignore          # Git ignore rules
```

## 🗄️ Database Schema

### Users Table
- `id`: Primary key (Integer)
- `username`: Unique username (String)
- `password_hash`: Hashed password (String)

### Books Table
- `id`: Primary key (Integer)
- `title`: Book title (String)
- `author`: Book author (String)
- `price`: Book price (Float)
- `owner_id`: Foreign key to users table (Integer)

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | JWT secret key | `fallback-secret-key` |
| `DATABASE_URL` | Database connection URL | Required |

### Model Configuration

You can modify the JWT token expiration time in `auth.py`:
```python
TOKEN_EXPIRE_MINUTES = 30  # Change as needed
```

## 🚀 Advanced Features

### Redis Caching
The application includes Redis caching support for better performance. Caching is currently commented out but can be enabled by uncommenting the relevant sections in `routes/books.py`.

### Query Parameters for Book Filtering
- `title`: Filter by book title (partial match)
- `author`: Filter by author name (partial match)
- `max_price`: Maximum price filter
- `min_price`: Minimum price filter
- `limit`: Number of results (1-50, default: 10)
- `offset`: Pagination offset (default: 0)

## 🧪 Testing

You can test the API using:
- **Thunder Client** (VS Code extension)
- **Postman**
- **curl** commands (examples provided above)
- **FastAPI's built-in docs** at `/docs`

## 🔒 Security Features

- **Password Hashing**: Uses bcrypt for secure password storage
- **JWT Authentication**: Stateless authentication with expiring tokens
- **Authorization**: Users can only modify their own books
- **Input Validation**: Pydantic models validate all input data
- **SQL Injection Protection**: SQLAlchemy ORM prevents SQL injection

## 🛡️ Production Considerations

Before deploying to production:

1. **Change the SECRET_KEY**: Use a strong, random secret key
2. **Use a production database**: PostgreSQL, MySQL, etc.
3. **Set up proper logging**: Configure logging for monitoring
4. **Enable HTTPS**: Use SSL/TLS certificates
5. **Rate limiting**: Implement rate limiting for API endpoints
6. **Environment variables**: Use proper environment variable management
7. **Database migrations**: Set up proper database migration strategy

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📞 Support

If you encounter any issues or have questions, please open an issue on GitHub or contact the maintainer.
