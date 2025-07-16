
# Electrical Project Manager

A modern web application for managing electrical projects, built with React frontend and Flask backend.

## Features

- **Project Management**: Create, view, and manage electrical projects
- **Node & PLC Configuration**: Create and configure hardware nodes and PLCs
- **I/O Assignment**: Assign input/output points to hardware modules
- **Hardware Catalog**: Manage hardware components and their specifications
- **Authentication**: Secure login system with JWT tokens

## Technology Stack

### Frontend
- **React 18** with TypeScript
- **React Router** for navigation
- **Tailwind CSS** for styling
- **Vite** for development and building

### Backend
- **Flask** with SQLite database
- **JWT Authentication**
- **CORS** enabled for cross-origin requests
- **SQLite** for development database

## Quick Start

### Prerequisites
- Node.js 18+ and npm
- Python 3.8+

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
   pip install flask flask-cors sqlite3
   cd ..
   ```

### Development

**Option 1: Automatic startup (Recommended)**
```bash
python start_dev.py
```

**Option 2: Manual startup**

1. **Start Flask backend** (Terminal 1):
   ```bash
   cd backend
   python flask_api_adapter.py
   ```

2. **Start React frontend** (Terminal 2):
   ```bash
   npm run dev
   ```

### Access the Application

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:5000
- **Default Login**: username: `admin`, password: `admin`

## Project Structure

```
electrical-project-manager/
├── src/                    # React frontend source
│   ├── components/        # React components
│   ├── contexts/         # React contexts (Auth, etc.)
│   ├── utils/           # Utility functions and API calls
│   └── App.tsx          # Main App component
├── backend/             # Flask backend
│   ├── flask_api_adapter.py  # Main Flask application
│   └── database.db      # SQLite database (auto-created)
├── public/             # Static assets
└── README.md          # This file
```

## API Endpoints

### Authentication
- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - User logout
- `GET /api/auth/me` - Get current user

### Projects
- `GET /api/progetti` - Get all projects
- `POST /api/progetti` - Create new project
- `DELETE /api/progetti/{id}` - Delete project
- `GET /api/progetto/{id}` - Get project details

### Nodes & Hardware
- `GET /api/lista_nodi` - Get all nodes
- `POST /api/crea_nodo` - Create new node
- `GET /api/catalogo_hw` - Get hardware catalog
- `GET /api/hw_nodo_list` - Get hardware assigned to node
- `POST /api/hw_nodo_add` - Assign hardware to node
- `DELETE /api/hw_nodo_list/{id}` - Remove hardware from node

### I/O Management
- `GET /api/io_unassigned` - Get unassigned I/O points
- `GET /api/io_assigned` - Get assigned I/O points
- `POST /api/io_assign` - Assign I/O to module
- `DELETE /api/io_assign` - Unassign I/O from module

## Features Implemented

✅ **User Authentication** - JWT-based login/logout  
✅ **Project Management** - Create, view, delete projects  
✅ **Node Management** - Create and manage hardware nodes  
✅ **Hardware Catalog** - View and assign hardware components  
✅ **I/O Assignment** - Assign I/O points to hardware modules  
✅ **Responsive Design** - Mobile-friendly interface  

## Development Notes

- The Flask backend includes sample data for testing
- Authentication is simplified for development (admin/admin)
- Database is automatically initialized on first run
- CORS is configured for local development

## Building for Production

```bash
npm run build
```

The built files will be in the `dist/` directory.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License.
