# URL Shortener API

A fast and efficient URL shortener service built with FastAPI, PostgreSQL, and Docker.

## What This Project Does

This URL shortener takes long URLs and creates short, easy-to-share links. When someone clicks the short link, they get redirected to the original URL. The service also tracks how many times each link has been clicked.

## Features

- 🚀 Convert long URLs into short codes (e.g., `https://example.com/abc123`)
- 📊 Track click statistics for each shortened URL
- 🔗 Redirect users from short URLs to original URLs
- 🐳 Docker support for easy deployment
- 📝 Automatic API documentation with Swagger UI
- 🔒 Production-ready with proper error handling

## Tech Stack

- **FastAPI** - Modern web framework for building APIs
- **PostgreSQL** - Reliable relational database for storing URLs
- **SQLAlchemy** - SQL toolkit and ORM for database operations
- **Docker** - Containerization for easy deployment
- **Pydantic** - Data validation using Python type annotations

## Project Structure

```
url-shortener/
├── app/
│   ├── __init__.py
│   ├── main.py              # Application entry point
│   ├── config.py            # Configuration settings
│   ├── api/
│   │   └── routes/
│   │       └── urls.py      # API endpoints for URL operations
│   ├── core/
│   │   └── database.py      # Database connection and session management
│   ├── models/
│   │   └── url.py           # Database models (URL table structure)
│   ├── schemas/
│   │   └── url.py           # Pydantic schemas for API request/response
│   └── services/
│       └── url_service.py   # Business logic for URL operations
├── docker-compose.yml       # Docker services configuration
├── Dockerfile              # Docker image build instructions
├── requirements.txt        # Python dependencies
└── README.md
```

## How It Works

### 1. URL Shortening Process
1. User sends a long URL to `/shorten` endpoint
2. System generates a random 6-character code (e.g., "abc123")
3. Stores the mapping in PostgreSQL database
4. Returns the short URL to the user

### 2. URL Redirection Process
1. User visits short URL (e.g., `yourdomain.com/abc123`)
2. System looks up the short code in database
3. Increments click counter
4. Redirects user to original URL

### 3. Statistics Tracking
- Each URL has a click counter
- Users can check stats via `/stats/{short_code}` endpoint
- Tracks creation date and active status

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/shorten` | Create a short URL |
| `GET` | `/{short_code}` | Redirect to original URL |
| `GET` | `/stats/{short_code}` | Get URL statistics |
| `GET` | `/` | Welcome message |
| `GET` | `/health` | Health check |

## Getting Started

### Prerequisites

- Python 3.9+
- Docker and Docker Compose
- Git

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/summii/url-shortener.git
cd url-shortener
```

2. **Create virtual environment**
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
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/urlshortener
SECRET_KEY=your-secret-key-here
BASE_URL=http://localhost:8000
```

5. **Start PostgreSQL with Docker**
```bash
docker-compose up -d postgres
```

6. **Run the application**
```bash
uvicorn app.main:app --reload
```

The API will be available at:
- **Main API**: http://localhost:8000
- **Swagger Documentation**: http://localhost:8000/docs
- **ReDoc Documentation**: http://localhost:8000/redoc

### Using Docker (Recommended)

1. **Clone and navigate to project**
```bash
git clone https://github.com/summii/url-shortener.git
cd url-shortener
```

2. **Create .env file**
```env
DATABASE_URL=postgresql://postgres:postgres@postgres:5432/urlshortener
SECRET_KEY=your-secret-key-here
BASE_URL=http://localhost:8000
```

3. **Start all services**
```bash
docker-compose up -d
```

## Usage Examples

### 1. Shorten a URL
```bash
curl -X POST "http://localhost:8000/shorten" \
     -H "Content-Type: application/json" \
     -d '{"original_url": "https://www.google.com"}'
```

**Response:**
```json
{
  "id": 1,
  "short_code": "abc123",
  "short_url": "http://localhost:8000/abc123",
  "original_url": "https://www.google.com",
  "is_active": true,
  "clicks": 0,
  "created_at": "2024-01-01T12:00:00Z"
}
```

### 2. Visit Short URL
Open `http://localhost:8000/abc123` in browser → redirects to Google

### 3. Get Statistics
```bash
curl "http://localhost:8000/stats/abc123"
```

**Response:**
```json
{
  "id": 1,
  "short_code": "abc123",
  "short_url": "http://localhost:8000/abc123",
  "original_url": "https://www.google.com",
  "is_active": true,
  "clicks": 5,
  "created_at": "2024-01-01T12:00:00Z"
}
```

## Database Schema

The application uses a single `urls` table:

| Column | Type | Description |
|--------|------|-------------|
| `id` | Integer | Primary key |
| `original_url` | Text | The original long URL |
| `short_code` | String(10) | Unique 6-character identifier |
| `is_active` | Boolean | Whether URL is active (default: true) |
| `clicks` | Integer | Number of times URL was accessed |
| `created_at` | DateTime | When URL was created |

## Key Components Explained

### 1. `app/main.py`
- Entry point of the application
- Sets up FastAPI app with routes
- Creates database tables on startup

### 2. `app/models/url.py`
- Defines the database structure using SQLAlchemy
- URL model with all necessary fields

### 3. `app/schemas/url.py`
- Pydantic models for API request/response validation
- Ensures data integrity and provides automatic documentation

### 4. `app/services/url_service.py`
- Business logic for URL operations
- Functions to create short URLs, generate codes, and track clicks

### 5. `app/api/routes/urls.py`
- API endpoints that handle HTTP requests
- Uses dependency injection for database sessions

### 6. `app/core/database.py`
- Database connection setup
- Session management for database operations

## Development

### Running Tests
```bash
# Add test commands here when tests are implemented
pytest
```

### Code Formatting
```bash
black app/
isort app/
```

### Database Management

Access pgAdmin (if using docker-compose):
- URL: http://localhost:5050
- Email: admin@admin.com
- Password: admin

## Deployment

### Environment Variables for Production
```env
DATABASE_URL=postgresql://user:password@host:port/database
SECRET_KEY=your-very-secure-secret-key
BASE_URL=https://yourdomain.com
```

### Docker Production Build
```bash
docker build -t url-shortener .
docker run -p 8000:8000 --env-file .env url-shortener
```

## Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Ensure PostgreSQL is running
   - Check DATABASE_URL in .env file
   - Verify database credentials

2. **Port Already in Use**
   - Change port in uvicorn command: `--port 8001`
   - Or stop other services using port 8000

3. **Docker Issues**
   - Restart Docker services: `docker-compose restart`
   - Rebuild images: `docker-compose build --no-cache`

### Logs
```bash
# View application logs
docker-compose logs app

# View database logs
docker-compose logs postgres
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is open source and available under the MIT License.