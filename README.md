# Zipway URL Shortener - Backend

A high-performance, scalable URL shortening service built with FastAPI and clean architecture principles. This backend provides a robust API for creating short URLs, tracking analytics, and managing content with enterprise-grade security and performance features.

## 🚀 Key Features

- **Clean Architecture**: Implemented with proper separation of concerns (Controllers, Services, Repositories, Views)
- **URL Shortening**: Create shortened URLs with automatic UUID generation or custom aliases
- **Smart Redirection**: Fast redirect service with click tracking and analytics
- **Custom Aliases**: Support for user-defined custom short IDs with comprehensive validation
- **Click Analytics**: Track and monitor URL usage statistics with detailed reporting
- **Admin Dashboard**: Protected admin endpoints with token-based authentication
- **Rate Limiting**: Intelligent rate limiting to prevent abuse and ensure service stability
- **Input Validation**: Comprehensive URL validation and alias sanitization with security rules
- **Reserved Path Protection**: System prevents conflicts with reserved routes and system paths
- **Health Monitoring**: Built-in health check endpoints for uptime monitoring
- **CORS Support**: Configurable cross-origin resource sharing
- **Database Abstraction**: Clean repository pattern for database operations

## 🏗️ Architecture

This project follows **Clean Architecture** principles with clear separation of concerns:

```
app/
├── controllers/     # Business logic orchestration
├── services/        # Core business rules and operations
├── repositories/    # Data access layer
├── models/          # Data models and schemas
├── views/           # Response models and DTOs
├── routes/          # API endpoint definitions
├── dependencies/    # Shared utilities and middleware
└── database.py      # Database configuration
```

### Architecture Benefits

- **Maintainability**: Clear separation makes code easy to understand and modify
- **Testability**: Each layer can be tested independently
- **Scalability**: Easy to add new features without affecting existing code
- **Flexibility**: Can easily swap implementations (e.g., different databases)

## 🔧 Technology Stack

- **[FastAPI](https://fastapi.tiangolo.com/)** - High-performance, modern API framework with automatic documentation
- **[SQLAlchemy](https://www.sqlalchemy.org/)** - SQL toolkit and ORM for database operations
- **[SQLite](https://www.sqlite.org/)** - Lightweight, serverless database
- **[Uvicorn](https://www.uvicorn.org/)** - Lightning-fast ASGI server
- **[SlowAPI](https://github.com/laurentS/slowapi)** - Rate limiting middleware
- **[Pydantic](https://pydantic-docs.helpmanual.io/)** - Data validation using Python type annotations
- **[Python-dotenv](https://github.com/theskumar/python-dotenv)** - Environment variable management
- **[ShortUUID](https://github.com/skorokithakis/shortuuid)** - URL-safe unique identifier generation
- **[Validators](https://github.com/kvesteri/validators)** - URL format validation

## 📁 Project Structure

```
zipwayAPI/
├── app/                     # Application directory
│   ├── controllers/         # Business logic orchestration
│   │   ├── url_controller.py
│   │   └── admin_controller.py
│   ├── services/           # Core business rules
│   │   └── url_service.py
│   ├── repositories/       # Data access layer
│   │   └── url_repository.py
│   ├── models/            # Data models and schemas
│   │   ├── url.py         # SQLAlchemy model
│   │   └── _init_.py      # Pydantic schemas
│   ├── views/             # Response models and DTOs
│   │   ├── url_views.py
│   │   └── admin_views.py
│   ├── routes/            # API endpoint definitions
│   │   ├── url_routes.py
│   │   └── admin_routes.py
│   ├── dependencies/      # Shared utilities and middleware
│   │   ├── auth.py        # Authentication logic
│   │   ├── limiter.py     # Rate limiting configuration
│   │   └── validators.py  # URL and alias validation
│   ├── __init__.py
│   ├── database.py        # Database configuration
│   └── main.py           # FastAPI application setup
├── .env                   # Environment variables (create from .env.example)
├── .env.example          # Environment variables template
├── .gitignore            # Git ignore file
├── Dockerfile            # Docker container definition
├── requirements.txt      # Python dependencies
├── README.md            # Project documentation
└── shortener.db         # SQLite database (auto-created on first run)
```

## 🛠️ Environment Variables

Create a `.env` file in the project root with the following variables:

```bash
# Server Configuration
HOST=0.0.0.0
PORT=8000
ENV=development # Options: development, staging, production

# Authentication
ADMIN_API_TOKEN=your_secure_admin_token_here


# CORS Configuration
ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

### Environment Variables Explained

- **HOST**: Server bind address (use 0.0.0.0 for Docker)
- **PORT**: Server port (default: 8000)
- **ENV**: Environment mode affecting CORS and logging
- **ADMIN_API_TOKEN**: Secure token for admin endpoints (generate a strong random string)
- **ALLOWED_ORIGINS**: Comma-separated list of allowed CORS origins

## 🚀 Running Locally

### Prerequisites

- Python 3.8 or higher
- pip package manager

### With Python (Recommended for Development)

1. **Clone and navigate to the project**:

   ```bash
   git clone https://github.com/esdrassantos06/zipwayAPI.git
   cd zipwayAPI
   ```

2. **Create and activate virtual environment**:

   ```bash
   python -m venv venv

   # On Linux/macOS:
   source venv/bin/activate

   # On Windows:
   venv\Scripts\activate
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:

   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Run the application**:

   ```bash
   # Development mode with auto-reload
   python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

   # Or run directly
   python -m app.main
   ```

### With Docker

1. **Build the Docker image**:

   ```bash
   docker build -t zipway-backend .
   ```

2. **Run the container**:

   ```bash
   docker run -d \
     --name zipway-backend-container \
     -p 8000:8000 \
     -v $(pwd)/shortener.db:/app/shortener.db \
     --env-file .env \
     zipway-backend
   ```

3. **Container management**:

   ```bash
   # Start existing container
   docker start zipway-backend-container

   # Stop container
   docker stop zipway-backend-container

   # View logs
   docker logs zipway-backend-container

   # Remove container
   docker rm zipway-backend-container
   ```

## 📝 API Documentation

Once the server is running, access the comprehensive API documentation:

- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

### API Endpoints

| Endpoint            | Method | Description                          | Rate Limit | Auth Required |
| ------------------- | ------ | ------------------------------------ | ---------- | ------------- |
| `/`                 | GET    | API information and available routes | 100/minute | No            |
| `/ping`             | GET    | Health check endpoint                | Unlimited  | No            |
| `/url/shorten`      | POST   | Create a shortened URL               | 20/minute  | No            |
| `/url/{short_id}`   | GET    | Redirect to the original URL         | 200/minute | No            |
| `/admin/stats`      | GET    | Get usage statistics                 | 10/minute  | Yes (Bearer)  |
| `/admin/delete_url` | DELETE | Delete a shortened URL               | 10/minute  | Yes (Bearer)  |

### Request/Response Examples

#### Create Short URL

```bash
curl -X POST "http://localhost:8000/url/shorten" \
  -H "Content-Type: application/json" \
  -d '{
    "target_url": "https://example.com",
    "short_id": "my-link"
  }'
```

Response:

```json
{
  "id": "my-link",
  "target_url": "https://example.com",
  "short_url": "/url/my-link"
}
```

#### Get Statistics (Admin)

```bash
curl -X GET "http://localhost:8000/admin/stats?limit=10" \
  -H "Authorization: Bearer YOUR_ADMIN_TOKEN"
```

#### Delete URL (Admin)

```bash
curl -X DELETE "http://localhost:8000/admin/delete_url?short_id=abc123" \
  -H "Authorization: Bearer YOUR_ADMIN_TOKEN"
```

## 🗄️ Database Schema

The application uses SQLite with the following schema:

```sql
CREATE TABLE urls (
    id TEXT PRIMARY KEY,                    -- Short URL identifier
    target_url TEXT NOT NULL,               -- Original long URL
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- Creation timestamp
    clicks INTEGER DEFAULT 0               -- Click counter
);
```

### Database Operations

- **Connection Management**: Context manager for safe database connections
- **Auto-initialization**: Tables created automatically on startup
- **Transaction Safety**: All operations use proper transaction handling
- **Error Handling**: Comprehensive error logging and graceful degradation

## 🛡️ Security Features

### Authentication

- **Admin Token**: Bearer token authentication for protected endpoints
- **Environment-based**: Tokens stored securely in environment variables
- **Secure Headers**: Proper WWW-Authenticate headers for failed auth

### Input Validation

- **URL Validation**: Strict URL format validation using validators library
- **Alias Sanitization**: Custom ID sanitization removing special characters and accents
- **Reserved Path Protection**: Prevents conflicts with system routes and common paths
- **Pattern Validation**: Blocks suspicious patterns and system-reserved names

### Rate Limiting

- **Per-endpoint Limits**: Different limits for different endpoint types
- **IP-based**: Rate limiting based on client IP address
- **Configurable**: Easy to adjust limits based on needs

### CORS Security

- **Origin Control**: Configurable allowed origins
- **Environment-aware**: Automatic development origin inclusion

## 🚀 Deployment

### Deploying to Render

1. **Prepare Repository**:

   ```bash
   git add .
   git commit -m "Ready for deployment"
   git push origin main
   ```

2. **Create Render Service**:

   - Connect your Git repository
   - Choose "Web Service"
   - Set **Build Command**: `pip install -r requirements.txt`
   - Set **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

3. **Configure Environment Variables**:
   Add all variables from your `.env` file to Render's environment variables section.

4. **Deploy**: Click "Create Web Service"

### Deploying to Railway

1. **Connect Repository**: Link your GitHub repository
2. **Environment Variables**: Add your configuration
3. **Deploy**: Railway auto-detects Python and deploys

### Deploying to Heroku

1. **Create app**: `heroku create your-app-name`
2. **Set environment variables**:
   ```bash
   heroku config:set ADMIN_API_TOKEN=your_token
   heroku config:set BASE_URL=https://your-frontend.com
   ```
3. **Deploy**: `git push heroku main`

## 📊 Monitoring and Maintenance

### Health Monitoring

Use services like UptimeRobot or Better Stack to monitor your `/ping` endpoint:

- **URL**: `https://your-backend.onrender.com/ping`
- **Interval**: 5 minutes (less if you can)
- **Method**: GET
- **Expected Response**: `{"status": "ok"}`

## 🧪 Testing

### Manual Testing

Test the API using the interactive documentation at `/docs` or with curl:

```bash
# Test health endpoint
curl http://localhost:8000/ping

# Test URL shortening
curl -X POST http://localhost:8000/url/shorten \
  -H "Content-Type: application/json" \
  -d '{"target_url": "https://example.com"}'
```

### Automated Testing (Future Enhancement)

Recommended testing stack:

- **[pytest](https://docs.pytest.org/)** - Testing framework
- **[pytest-asyncio](https://github.com/pytest-dev/pytest-asyncio)** - Async testing support
- **[httpx](https://www.python-httpx.org/)** - HTTP testing client
- **[TestClient](https://fastapi.tiangolo.com/tutorial/testing/)** - FastAPI testing utilities

## 🔧 Development

### Code Structure

- **Clean Architecture**: Clear separation between controllers, services, repositories, and views
- **Type Hints**: Full type annotation support throughout the codebase
- **Error Handling**: Comprehensive exception handling with proper HTTP status codes
- **Dependency Injection**: Factory functions for clean dependency management

### Performance Considerations

- **Database Indexing**: Consider adding indexes for large datasets
- **Connection Pooling**: SQLAlchemy connection pooling for better performance
- **Caching**: Consider implementing Redis for high-traffic scenarios

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and test thoroughly
4. Commit your changes: `git commit -am 'Add some feature'`
5. Push to the branch: `git push origin feature-name`
6. Create a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

If you encounter any issues:

1. Check the [API documentation](http://localhost:8000/redoc) for endpoint details
2. Review the logs for error messages
3. Ensure all environment variables are properly configured
4. Verify database permissions and file access

For additional support, please open an issue in the repository.
