# High Precision Pi Calculation API

This FastAPI server calculates Pi to high precision using the Chudnovsky algorithm and provides an API to retrieve the current calculated value.

## Features

- Calculates Pi to a configurable maximum number of decimal places (defined by environment variable)
- Continuously increases precision during runtime
- Caches results in Redis for quick retrieval
- Protected API endpoint with API key authentication
- Rate limiting to prevent abuse
- Clean architecture following SOLID principles

## Setup

### Environment Variables

Create a `.env` file with the following variables:

```
API_KEY=your_api_key_here
MAX_DECIMAL_POINTS=10000
REDIS_URL=redis://redis:6379/0
```

### Running with Docker Compose

```bash
docker-compose up -d
```

This will start both the FastAPI server and Redis.

### Manual Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Start Redis:
```bash
# Install Redis if not already installed
docker run -d -p 6379:6379 redis:alpine
```

3. Run the FastAPI server:
```bash
uvicorn app.main:app --reload
```

## API Endpoints

### GET /api/pi

Returns the current Pi value and number of decimal places.

**Headers**:
- `x-api-key`: API key for authentication

**Response**:
```json
{
  "pi": "3.14159265358979323846...",
  "dp": "1000"
}
```

## Testing

Run unit tests:
```bash
pytest tests/unit
```

Run e2e tests:
```bash
pytest tests/e2e
```

## Performance

- The Pi calculation uses the efficient Chudnovsky algorithm
- Results are cached in Redis for fast retrieval
- The API is designed for quick response times 