
# Electrical Project Manager

A comprehensive electrical project management system built with React frontend and FastAPI backend.

## Features

- **Project Management**: Create, view, and manage electrical projects
- **Node and PLC Management**: Create and configure electrical nodes and PLCs
- **Hardware Assignment**: Assign hardware modules to nodes
- **I/O Configuration**: Manage input/output assignments
- **JWT Authentication**: Secure authentication system
- **Modern UI**: Responsive React interface with Tailwind CSS

## Tech Stack

### Frontend
- **React 18**: Modern React with hooks and function components
- **TypeScript**: Type-safe JavaScript
- **Tailwind CSS**: Utility-first CSS framework
- **React Router**: Client-side routing
- **Vite**: Fast build tool and dev server

### Backend
- **FastAPI**: Modern, fast Python web framework
- **SQLAlchemy**: Python SQL toolkit and ORM
- **PostgreSQL**: Database
- **JWT Authentication**: JSON Web Token authentication
- **Pydantic**: Data validation using Python type annotations

## Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- PostgreSQL database

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd electrical-project-manager
   ```

2. **Install frontend dependencies**
   ```bash
   npm install
   ```

3. **Install backend dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

4. **Configure the database**
   - Update `backend/core/config.py` with your PostgreSQL connection details
   - The database will be automatically initialized on first run

### Development

**Option 1: Start everything with one command**
```bash
python start_dev.py
```

**Option 2: Start services separately**

1. **Start FastAPI backend** (Terminal 1):
   ```bash
   cd backend
   uvicorn main:app --reload --port 8000
   ```

2. **Start React frontend** (Terminal 2):
   ```bash
   npm run dev
   ```

The application will be available at:
- **Frontend**: http://localhost:8080
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

### Default Login
- **Username**: `admin`
- **Password**: `secret`

## Project Structure

```
├── src/                    # React frontend source
│   ├── components/         # React components
│   ├── contexts/          # React contexts (Auth)
│   ├── utils/             # Utility functions
│   └── main.tsx           # Application entry point
├── backend/               # FastAPI backend
│   ├── core/              # Core configuration and security
│   ├── models/            # SQLAlchemy models
│   ├── routers/           # API route handlers
│   ├── schemas/           # Pydantic schemas
│   ├── services/          # Business logic services
│   └── main.py            # FastAPI application entry point
└── start_dev.py           # Development startup script
```

## API Endpoints

### Authentication
- `POST /api/auth/login` - User login
- `GET /api/auth/me` - Get current user
- `POST /api/auth/logout` - User logout

### Projects
- `GET /api/projects/` - List all projects
- `POST /api/projects/` - Create new project
- `GET /api/projects/{id}` - Get project details
- `DELETE /api/projects/{id}` - Delete project

### Nodes
- `GET /api/nodes/project/{project_id}` - Get nodes by project
- `POST /api/nodes/` - Create new node
- `POST /api/nodes/plc/auto/{project_id}` - Auto-create PLC

### Hardware
- `GET /api/hardware/catalog` - Get hardware catalog
- `GET /api/hardware/node/{node_id}` - Get node hardware
- `POST /api/hardware/node` - Add hardware to node

### I/O
- `GET /api/io/unassigned` - Get unassigned I/O
- `GET /api/io/assigned` - Get assigned I/O
- `POST /api/io/assign` - Assign I/O to module

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is proprietary software. All rights reserved.
