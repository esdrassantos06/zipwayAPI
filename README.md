# Zipway URL Shortener - Backend

This is the backend service for the Zipway URL shortener application, built with FastAPI and SQLite. A fast, secure, and scalable URL shortening service with comprehensive features including custom aliases, click tracking, and admin controls.

## 🚀 Features

- **URL Shortening**: Create shortened URLs with automatic UUID generation or custom aliases
- **Smart Redirection**: Fast redirect service with click tracking
- **Custom Aliases**: Support for user-defined custom short IDs with validation and sanitization
- **Click Analytics**: Track and monitor URL usage statistics
- **Admin Dashboard**: Protected admin endpoints with token-based authentication
- **Rate Limiting**: Intelligent rate limiting to prevent abuse and ensure service stability
- **Health Monitoring**: Built-in health check endpoints for uptime monitoring
- **CORS Support**: Configurable cross-origin resource sharing
- **Input Validation**: Comprehensive URL validation and alias sanitization
- **Reserved Path Protection**: System prevents conflicts with reserved routes

## 🔧 Technology Stack

- **[FastAPI](https://fastapi.tiangolo.com/)** - High-performance, modern API framework
- **[SQLite](https://www.sqlite.org/)** - Lightweight, serverless database
- **[Uvicorn](https://www.uvicorn.org/)** - Lightning-fast ASGI server
- **[SlowAPI](https://github.com/laurentS/slowapi)** - Rate limiting middleware
- **[Pydantic](https://pydantic-docs.helpmanual.io/)** - Data validation using Python type annotations
- **[Python-dotenv](https://github.com/theskumar/python-dotenv)** - Environment variable management
- **[ShortUUID](https://github.com/skorokithakis/shortuuid)** - URL-safe unique identifier generation
- **[Validators](https://github.com/kvesteri/validators)** - URL format validation

## 📁 Project Structure

```
backend/
├── app/                     # Application directory
│   ├── __init__.py          # Package initializer
│   ├── auth.py              # JWT/Token authentication logic
│   ├── database.py          # Database operations and connection management
│   ├── limiter.py           # Rate limiting configuration and rules
│   ├── main.py              # FastAPI application, routes, and middleware
│   └── models.py            # Pydantic data models and schemas
├── .env                     # Environment variables (create from .env.example)
├── .env.example             # Environment variables template
├── .gitignore               # Git ignore file
├── Dockerfile               # Docker container definition
├── requirements.txt         # Python dependencies
├── README.md                # Project documentation
└── shortener.db             # SQLite database (auto-created on first run)
```

## 🛠️ Environment Variables

Create a `.env` file in the backend directory with the following variables:

```bash
# Server Configuration
HOST=0.0.0.0
PORT=8000
ENV=development # Options: development, staging, production

# Authentication
ADMIN_API_TOKEN=your_secure_admin_token_here

# URLs
BASE_URL=http://localhost:3000        # Frontend URL for short link generation
BACKEND_URL=http://localhost:8000     # Backend URL for API calls

# CORS Configuration
ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

### Environment Variables Explained

- **HOST**: Server bind address (use 0.0.0.0 for Docker)
- **PORT**: Server port (default: 8000)
- **ENV**: Environment mode affecting CORS and logging
- **ADMIN_API_TOKEN**: Secure token for admin endpoints (generate a strong random string)
- **BASE_URL**: Frontend URL used to construct complete short URLs
- **BACKEND_URL**: Backend API URL for internal references
- **ALLOWED_ORIGINS**: Comma-separated list of allowed CORS origins

## 🚀 Running Locally

### Prerequisites

- Python 3.8 or higher
- pip package manager

### With Python (Recommended for Development)

1. **Clone and navigate to the project**:
   ```bash
   git clone <your-repo-url>
   cd zipway-backend
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
   python app/main.py
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

| Endpoint             | Method | Description                          | Rate Limit    | Auth Required |
|----------------------|--------|--------------------------------------|---------------|---------------|
| `/`                  | GET    | API information and available routes | 100/minute    | No           |
| `/ping`              | GET    | Health check endpoint                | Unlimited     | No           |
| `/shorten`           | POST   | Create a shortened URL               | 20/minute     | No           |
| `/{short_id}`        | GET    | Redirect to the original URL         | 200/minute    | No           |
| `/stats`             | GET    | Get usage statistics                 | 10/minute     | Yes (Bearer) |
| `/delete_url`        | DELETE | Delete a shortened URL               | 10/minute     | Yes (Bearer) |

### Request/Response Examples

#### Create Short URL
```bash
curl -X POST "http://localhost:8000/shorten" \
  -H "Content-Type: application/json" \
  -d '{
    "target_url": "https://example.com",
    "custom_id": "my-link"
  }'
```

#### Get Statistics (Admin)
```bash
curl -X GET "http://localhost:8000/stats?limit=10" \
  -H "Authorization: Bearer YOUR_ADMIN_TOKEN"
```

#### Delete URL (Admin)
```bash
curl -X DELETE "http://localhost:8000/delete_url?short_id=abc123" \
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

### Input Validation
- **URL Validation**: Strict URL format validation using validators library
- **Alias Sanitization**: Custom ID sanitization removing special characters
- **Reserved Path Protection**: Prevents conflicts with system routes

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
- **Interval**: 5 minutes
- **Method**: GET
- **Expected Response**: `{"status": "ok"}`

### Log Monitoring
The application includes comprehensive logging:

```python
# Configure logging level in production
logging.basicConfig(level=logging.INFO)
```

### Database Maintenance
- **Backup**: Regular SQLite database backups
- **Cleanup**: Consider implementing URL expiration for inactive links
- **Monitoring**: Track database size and performance

## 🧪 Testing

### Manual Testing
Test the API using the interactive documentation at `/docs` or with curl:

```bash
# Test health endpoint
curl http://localhost:8000/ping

# Test URL shortening
curl -X POST http://localhost:8000/shorten \
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
- **Separation of Concerns**: Clear separation between routes, database, auth, and models
- **Type Hints**: Full type annotation support
- **Error Handling**: Comprehensive exception handling
- **Logging**: Structured logging for debugging and monitoring

### Adding New Features

1. **Database Changes**: Update `database.py` for new operations
2. **API Routes**: Add new endpoints in `main.py`
3. **Data Models**: Define new Pydantic models in `models.py`
4. **Authentication**: Extend `auth.py` for new auth requirements

### Performance Considerations
- **Database Indexing**: Consider adding indexes for large datasets
- **Connection Pooling**: SQLite connection management
- **Caching**: Consider Redis for high-traffic deployments
- **Rate Limiting**: Adjust limits based on usage patterns

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

1. Check the [API documentation](http://localhost:8000/docs) for endpoint details
2. Review the logs for error messages
3. Ensure all environment variables are properly configured
4. Verify database permissions and file access

For additional support, please open an issue in the repository.