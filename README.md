# Electrical Project Manager

This is a full-stack application for managing electrical projects, now migrated from Flask to FastAPI while maintaining all existing functionality.

## Features

- Project management (create, read, update, delete projects)
- Utility configuration and management
- Power configuration
- I/O assignment
- Node creation and management
- Automatic I/O assignment
- Export functionality

## Tech Stack

- **Backend**: FastAPI (migrated from Flask)
- **Frontend**: Vue.js (existing frontend)
- **Database**: SQLite (existing database)
- **API**: RESTful API endpoints

## Prerequisites

- Python 3.8+
- Node.js 14+ (for frontend)
- SQLite3

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd django-greet-world-starter
```

### 2. Set Up Python Environment

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Set Up Frontend

```bash
cd frontend
npm install
npm run build
cd ..
```

### 4. Configure Environment Variables

Create a `.env` file in the root directory with the following content:

```env
# Database configuration
DATABASE_URL=sqlite:///./mysqlite3.db

# Security
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# File uploads
UPLOAD_FOLDER=./uploaded_files
MAX_CONTENT_LENGTH=16777216  # 16MB max upload size
```

### 5. Initialize the Database

```bash
# If you need to initialize a new database
python scripts/init_db.py
```

## Running the Application

### Backend (FastAPI)

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

### Frontend (Development Mode)

```bash
cd frontend
npm run serve
```

The frontend will be available at `http://localhost:8080`

## API Documentation

Once the backend is running, you can access the following:

- **Interactive API Docs (Swagger UI)**: `http://localhost:8000/docs`
- **Alternative API Docs (ReDoc)**: `http://localhost:8000/redoc`

## Project Structure

```
.
├── api/                    # API routes
├── db/                     # Database migrations and scripts
├── frontend/               # Vue.js frontend
├── scripts/                # Utility scripts
├── static/                 # Static files
├── templates/              # HTML templates (for legacy routes if needed)
├── .env                    # Environment variables
├── .gitignore
├── app_mock.py             # Legacy Flask application (for reference)
├── main.py                 # FastAPI application entry point
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## Migrating from Flask to FastAPI

This project was migrated from Flask to FastAPI. Key changes include:

1. **Application Structure**:
   - Moved from Flask's global app to FastAPI's dependency injection
   - Organized routes into separate modules
   - Added proper type hints and Pydantic models

2. **Dependencies**:
   - Replaced Flask-specific dependencies with FastAPI alternatives
   - Added async support where beneficial
   - Improved error handling and validation

3. **API Endpoints**:
   - Converted Flask routes to FastAPI path operations
   - Added OpenAPI documentation automatically
   - Improved request/response models

## License

[Your License Here]
