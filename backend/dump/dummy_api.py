from fastapi import APIRouter, Depends, HTTPException, Request, Response, status, Header, Path, Cookie
from fastapi.responses import JSONResponse, FileResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List, Union, Callable
import json
import os
from pydantic import BaseModel
import shutil
import logging
import secrets
from session_manager import session_manager
from datetime import timezone

# Security configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")
SESSION_COOKIE_NAME = "session_id"
SESSION_LIFETIME = 86400  # 1 day in seconds

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Models
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Union[str, None] = None

class User(BaseModel):
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = None

class UserInDB(User):
    hashed_password: str

# Mock user database - Replace with your actual user authentication
fake_users_db = {
    "admin": {
        "username": "admin",
        "full_name": "Administrator",
        "email": "admin@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",  # "secret"
        "disabled": False,
    }
}

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hash"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Generate a password hash"""
    return pwd_context.hash(password)

def get_user(db: dict, username: str) -> Optional[UserInDB]:
    """Get user from database"""
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)
    return None

def authenticate_user(db: dict, username: str, password: str) -> Optional[UserInDB]:
    """Authenticate a user"""
    user = get_user(db, username)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

async def get_current_user(session_id: str = Cookie(None, alias=SESSION_COOKIE_NAME)) -> UserInDB:
    """Get the current user from session"""
    if not session_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    
    session_data = session_manager.get_session(session_id)
    if not session_data or 'username' not in session_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session expired or invalid"
        )
    
    user = get_user(fake_users_db, session_data['username'])
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

from db_config_sqlite import get_db_connection
from scripts.crea_progetto import crea_progetto
from scripts.carica_file_utenze_mock import _process_excel_and_autoflow, utenze_esistenti, verifica_file_caricato
from scripts.assegna_io import assegna_io_automaticamente
from scripts.crea_nodo import crea_nodo_plc_automatico
from typing import List
from pydantic import BaseModel

# Models for hardware catalog
class HardwareItem(BaseModel):
    id_hw: int
    nome_hw: str
    descrizione_hw: str
    tipo: str
    DI: int = 0
    DO: int = 0
    AI: int = 0
    AO: int = 0
    F_DI: int = 0  # Note: Using underscore instead of hyphen for Python variable name
    F_DO: int = 0   # Note: Using underscore instead of hyphen for Python variable name
    Ox: float = 0.0
    Oy: float = 0.0
    L: float = 0.0
    H: float = 0.0
    blocco_grafico: Optional[str] = None

# Models for export and schema generation
class ExportRequest(BaseModel):
    id_prg: int
    format: str = "xml"  # or "csv", "json", etc.
    include_io: bool = True
    include_utilities: bool = True
    include_nodes: bool = True

class SchemaRequest(BaseModel):
    id_prg: int
    schema_type: str  # e.g., "electrical", "network", etc.
    options: Optional[Dict[str, Any]] = None

# Models for I/O management
class IOAssignmentBase(BaseModel):
    id_io: int
    codice: str
    descrizione: str
    tipo: str
    id_modulo: Optional[int] = None
    indirizzo: Optional[str] = None
    note: Optional[str] = None
    id_prg: int

class IOAssignmentCreate(BaseModel):
    id_io: int
    id_modulo: int
    indirizzo: str
    note: Optional[str] = None

class IOAssignmentRemove(BaseModel):
    id_io: int
    id_modulo: Optional[int] = None

# Models for node management
class NodeBase(BaseModel):
    id_nodo: int
    nome_nodo: str
    tipo_nodo: str
    descrizione: Optional[str] = None
    id_prg: int
    id_quadro: Optional[int] = None

class NodeCreate(BaseModel):
    nome_nodo: str
    tipo_nodo: str
    descrizione: Optional[str] = None
    id_prg: int
    id_quadro: Optional[int] = None

router = APIRouter()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Authentication endpoints
class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("/login")
async def login(
    request: Request,
    response: Response,
    login_data: LoginRequest,
    redirect_url: Optional[str] = None
):
    """
    Handle user login and create a session
    """
    # Get redirect_url from query parameters if not in form data
    if not redirect_url:
        # Get the raw query parameters from the request
        query_params = dict(request.query_params)
        redirect_url = query_params.get('redirect_url')
    
    user = authenticate_user(fake_users_db, login_data.username, login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    
    # Create session
    session_data = {
        'username': user.username,
        'user_id': user.username,  # Using username as user_id in this example
        'created_at': datetime.now(timezone.utc).isoformat(),
        'last_activity': datetime.now(timezone.utc).isoformat()
    }
    session_id = session_manager.create_session(session_data)
    
    # Set session cookie with proper attributes
    response.set_cookie(
        key=SESSION_COOKIE_NAME,
        value=session_id,
        max_age=SESSION_LIFETIME,
        expires=datetime.now(timezone.utc) + timedelta(seconds=SESSION_LIFETIME),
        httponly=True,
        secure=False,  # Set to True in production with HTTPS
        samesite='lax',
        path='/'  # Make cookie available on all paths
    )
    
    # Prepare response data
    response_data = {
        "status": "success",
        "message": "Login successful",
        "user": {
            "username": user.username,
            "email": user.email,
            "full_name": user.full_name
        },
        "redirect_url": redirect_url or "/"  # Use provided URL or default to home
    }
    
    # Return JSON response with redirect URL
    return response_data

@router.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

@router.post("/logout")
async def logout(
    response: Response,
    session_id: str = Cookie(None, alias=SESSION_COOKIE_NAME)
):
    """Handle user logout"""
    if session_id:
        session_manager.delete_session(session_id)
    
    # Clear the session cookie
    response.delete_cookie(SESSION_COOKIE_NAME)
    
    return {
        "status": "success",
        "message": "Logout successful"
    }

# Node management endpoints
@router.get("/nodes/{id_prg}", response_model=List[NodeBase])
async def get_nodes(
    id_prg: int,
    current_user: User = Depends(get_current_active_user)
):
    """Get list of nodes for a project"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Verify project exists and user has access
        cursor.execute("SELECT * FROM t_progetti WHERE id_prg = %s", (id_prg,))
        project = cursor.fetchone()
        
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Project with ID {id_prg} not found"
            )
        
        # Get nodes for the project
        cursor.execute("""
            SELECT * 
            FROM t_nodo 
            WHERE id_prg = %s
            ORDER BY nome_nodo
        """, (id_prg,))
        
        nodes = cursor.fetchall()
        
        # Convert to list of dictionaries with proper field names
        result = []
        for node in nodes:
            result.append({
                'id_nodo': node['id_nodo'],
                'nome_nodo': node['nome_nodo'],
                'tipo_nodo': node['tipo_nodo'],
                'descrizione': node['descrizione'],
                'id_prg': node['id_prg'],
                'id_quadro': node.get('id_quadro')
            })
        
        return result
        
    except Exception as e:
        logger.error(f"Error getting nodes: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving nodes"
        )
    finally:
        cursor.close()
        conn.close()

@router.post("/crea_nodo", response_model=NodeBase, status_code=status.HTTP_201_CREATED)
async def create_node(
    node: NodeCreate,
    current_user: User = Depends(get_current_active_user)
):
    """Create a new node"""
    conn = None
    cursor = None
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Verify project exists and user has access
        cursor.execute("SELECT * FROM t_progetti WHERE id_prg = ?", (node.id_prg,))
        project = cursor.fetchone()
        
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Project with ID {node.id_prg} not found"
            )
        
        # Insert new node
        # Insert new node
        cursor.execute("""
                       INSERT INTO t_nodo (nome_nodo, tipo_nodo, descrizione, id_prg, id_quadro)
                       VALUES (?, ?, ?, ?, ?)
                       """, (
                           node.nome_nodo,
                           node.tipo_nodo or 'PLC',  # Default to 'PLC' if not specified
                           node.descrizione,
                           node.id_prg,
                           node.id_quadro
                       ))

        node_id = cursor.lastrowid
        conn.commit()

        # Return the created node
        cursor.execute("""
            SELECT * FROM t_nodo WHERE id_nodo = ?
        """, (node_id,))
        
        created_node = cursor.fetchone()
        
        return {
            'id_nodo': created_node['id_nodo'],
            'nome_nodo': created_node['nome_nodo'],
            'tipo_nodo': created_node['tipo_nodo'],
            'descrizione': created_node['descrizione'],
            'id_prg': created_node['id_prg'],
            'id_quadro': created_node['id_quadro']
        }
        
    except Exception as e:
        if conn:
            conn.rollback()
        logger.error(f"Error creating node: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating node: {str(e)}"
        )
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# Hardware catalog endpoints
@router.get("/catalogo_hw", response_model=List[HardwareItem])
async def get_hardware_catalog(
    tipo: Optional[str] = None,
    current_user: User = Depends(get_current_active_user)
):
    """Get hardware catalog with optional filtering by type"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Explicitly list all fields to ensure proper mapping
        query = """
            SELECT 
                id_hw,
                nome_hw,
                descrizione_hw,
                tipo,
                DI,
                DO,
                AI,
                AO,
                "F-DI" as F_DI,
                "F-DO" as F_DO,
                Ox,
                Oy,
                L,
                H,
                blocco_grafico
            FROM t_cat_hw
            WHERE 1=1
        """
        params = []
        
        if tipo:
            query += " AND tipo = %s"
            params.append(tipo)
            
        query += " ORDER BY tipo, descrizione_hw"
        
        cursor.execute(query, params)
        items = cursor.fetchall()
        
        # Convert to list of dictionaries with proper field names
        result = []
        for item in items:
            # Ensure all fields are present with default values if None
            result_item = {
                'id_hw': item['id_hw'],
                'nome_hw': item['nome_hw'] or '',
                'descrizione_hw': item['descrizione_hw'] or '',
                'tipo': item['tipo'] or '',
                'DI': item['DI'] or 0,
                'DO': item['DO'] or 0,
                'AI': item['AI'] or 0,
                'AO': item['AO'] or 0,
                'F_DI': item['F_DI'] or 0,
                'F_DO': item['F_DO'] or 0,
                'Ox': float(item['Ox'] or 0.0),
                'Oy': float(item['Oy'] or 0.0),
                'L': float(item['L'] or 0.0),
                'H': float(item['H'] or 0.0),
                'blocco_grafico': item['blocco_grafico']
            }
            result.append(result_item)
        
        return result
        
    except Exception as e:
        logger.error(f"Error getting hardware catalog: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving hardware catalog"
        )
    finally:
        cursor.close()
        conn.close()

# I/O Management endpoints
@router.get("/io_unassigned")
async def get_unassigned_io(
    id_prg: int,
    current_user: User = Depends(get_current_active_user)
):
    """Get list of unassigned I/Os for a project"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Verify project exists and user has access
        cursor.execute("SELECT * FROM progetto WHERE id_prg = %s", (id_prg,))
        project = cursor.fetchone()
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found"
            )
        
        # Get unassigned I/Os for the project
        cursor.execute("""
            SELECT i.id_io, i.codice, i.descrizione, i.tipo, 
                   i.id_modulo, i.indirizzo, i.note, i.id_prg
            FROM io i
            WHERE i.id_prg = %s AND i.id_modulo IS NULL
            ORDER BY i.tipo, i.codice
        """, (id_prg,))
        
        io_list = cursor.fetchall()
        return io_list
        
    except Exception as e:
        logger.error(f"Error getting unassigned I/Os: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving unassigned I/Os"
        )
    finally:
        cursor.close()
        conn.close()

@router.get("/io_assigned")
async def get_assigned_io(
    id_modulo: int,
    current_user: User = Depends(get_current_active_user)
):
    """Get list of I/Os assigned to a module"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get assigned I/Os for the module
        cursor.execute("""
            SELECT i.id_io, i.codice, i.descrizione, i.tipo, 
                   i.id_modulo, i.indirizzo, i.note, i.id_prg
            FROM io i
            WHERE i.id_modulo = %s
            ORDER BY i.indirizzo, i.tipo, i.codice
        """, (id_modulo,))
        
        io_list = cursor.fetchall()
        return io_list
        
    except Exception as e:
        logger.error(f"Error getting assigned I/Os: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving assigned I/Os"
        )
    finally:
        cursor.close()
        conn.close()

@router.post("/io_assign")
async def assign_io(
    assignment: IOAssignmentCreate,
    current_user: User = Depends(get_current_active_user)
):
    """Assign an I/O to a module"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Start transaction
        cursor.execute("START TRANSACTION")
        
        # Assign I/O to module
        cursor.execute("""
            UPDATE io 
            SET id_modulo = %s, indirizzo = %s, note = %s
            WHERE id_io = %s
        """, (
            assignment.id_modulo,
            assignment.indirizzo,
            assignment.note,
            assignment.id_io
        ))
        
        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="I/O not found or already assigned"
            )
            
        conn.commit()
        return {"status": "success", "message": "I/O assigned successfully"}
        
    except HTTPException:
        conn.rollback()
        raise
    except Exception as e:
        conn.rollback()
        logger.error(f"Error assigning I/O: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error assigning I/O: {str(e)}"
        )
    finally:
        cursor.close()
        conn.close()

@router.delete("/io_assign/{io_id}")
async def remove_io_assignment(
    io_id: int,
    current_user: User = Depends(get_current_active_user)
):
    """Remove I/O assignment from a module"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Start transaction
        cursor.execute("START TRANSACTION")
        
        # Remove I/O assignment
        cursor.execute("""
            UPDATE io 
            SET id_modulo = NULL, indirizzo = NULL, note = NULL
            WHERE id_io = %s
        """, (io_id,))
        
        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="I/O not found or not assigned"
            )
            
        conn.commit()
        return {"status": "success", "message": "I/O assignment removed successfully"}
        
    except HTTPException:
        conn.rollback()
        raise
    except Exception as e:
        conn.rollback()
        logger.error(f"Error removing I/O assignment: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error removing I/O assignment: {str(e)}"
        )
    finally:
        cursor.close()
        conn.close()

# Export and Schema Generation endpoints
@router.get("/api/export_io")
async def export_io_data(
    request: ExportRequest,
    current_user: User = Depends(get_current_active_user)
):
    id_prg = request.id_prg  # Extract id_prg from the request
    """
    Export I/O data for a project in the specified format.
    Returns a file download response.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Verify project exists and user has access
        cursor.execute("SELECT * FROM progetto WHERE id_prg = %s", (id_prg,))
        project = cursor.fetchone()
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found"
            )
        
        # Build the export data based on request parameters
        export_data = {
            "project": project,
            "exported_at": datetime.utcnow().isoformat(),
            "exported_by": current_user.username,
            "data": {}
        }
        
        # Get all I/O data
        cursor.execute("""
            SELECT * FROM io 
            WHERE id_prg = %s
            ORDER BY id_io
        """, (id_prg,))
        export_data["data"]["io"] = cursor.fetchall()
        
        # Get all utilities data
        cursor.execute("""
            SELECT * FROM utenza 
            WHERE id_prg = %s
            ORDER BY id_utenza
        """, (id_prg,))
        export_data["data"]["utilities"] = cursor.fetchall()
        
        # Get all nodes data
        cursor.execute("""
            SELECT * FROM nodo 
            WHERE id_prg = %s
            ORDER BY id_nodo
        """, (id_prg,))
        export_data["data"]["nodes"] = cursor.fetchall()
        
        # Handle different export formats
        if request.format.lower() == "xml":
            import xml.etree.ElementTree as ET
            from xml.dom import minidom
            
            def dict_to_xml(tag, d):
                elem = ET.Element(tag)
                for key, val in d.items():
                    if isinstance(val, dict):
                        child = dict_to_xml(key, val)
                        elem.append(child)
                    elif isinstance(val, list):
                        for item in val:
                            if isinstance(item, dict):
                                child = dict_to_xml(key[:-1] if key.endswith('s') else key + '_item', item)
                                elem.append(child)
                    else:
                        child = ET.Element(key)
                        child.text = str(val) if val is not None else ''
                        elem.append(child)
                return elem
                
            root = dict_to_xml("export", export_data)
            xml_str = minidom.parseString(ET.tostring(root)).toprettyxml(indent="  ")
            
            # Save to a temporary file
            timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            filename = f"export_{project['nome']}_{timestamp}.xml"
            filepath = f"/tmp/{filename}"
            
            with open(filepath, 'w') as f:
                f.write(xml_str)
            
            return FileResponse(
                filepath,
                media_type="application/xml",
                filename=filename,
                headers={"Content-Disposition": f"attachment; filename={filename}"}
            )
            
        elif request.format.lower() == "json":
            import json
            
            filename = f"export_{project['nome']}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
            filepath = f"/tmp/{filename}"
            
            with open(filepath, 'w') as f:
                json.dump(export_data, f, indent=2, default=str)
            
            return FileResponse(
                filepath,
                media_type="application/json",
                filename=filename,
                headers={"Content-Disposition": f"attachment; filename={filename}"}
            )
            
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported export format: {request.format}"
            )
            
    except Exception as e:
        logger.error(f"Error generating export: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating export: {str(e)}"
        )
    finally:
        cursor.close()
        conn.close()

@router.get("/genera_schema")
async def generate_schema(
    id_prg: int,
    current_user: User = Depends(get_current_active_user)
):
    """
    Generate a schema/diagram for the project.
    This is a placeholder implementation that would generate a diagram.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Verify project exists and user has access
        cursor.execute("SELECT * FROM progetto WHERE id_prg = %s", (id_prg,))
        project = cursor.fetchone()
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found"
            )
        
        # This is a placeholder - in a real implementation, you would generate
        # a diagram using a library like graphviz, matplotlib, etc.
        # and return it as a file download.
        
        # For now, we'll return a success message with some mock data
        return {
            "status": "success",
            "message": "Schema generated successfully",
            "project_id": id_prg,
            "generated_at": datetime.utcnow().isoformat(),
            "download_url": f"/api/download/schema_{id_prg}.png"
        }
        
    except Exception as e:
        logger.error(f"Error generating schema: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating schema: {str(e)}"
        )
    finally:
        cursor.close()
        conn.close()

# Project endpoints
@router.get("/progetti")
async def api_progetti():
    """Restituisce tutti i progetti in JSON (id_prg, nome_progetto, descrizione, data_creazione)."""
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id_prg, nome_progetto as name, descrizione as description, 
                   data_creazione as createdAt
            FROM t_progetti
            ORDER BY data_creazione DESC
        """)
        
        # Convert rows to list of dicts with consistent field names
        progetti = [dict(row) for row in cursor.fetchall()]
        
        # Return with status for Vue frontend
        return {
            "status": "success",
            "data": progetti
        }
        
    except Exception as e:
        logger.error(f"Error fetching projects: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail={
                "status": "error",
                "message": f"Errore durante il recupero dei progetti: {str(e)}"
            }
        )
    finally:
        if conn:
            try:
                conn.close()
            except:
                pass

@router.get("/progetti/{id_prg}")
async def api_progetto(id_prg: int = Path(..., gt=0, description="ID del progetto da recuperare")):
    """
    Restituisce un progetto in base all'ID specificato.
    
    Args:
        id_prg: ID numerico positivo del progetto
        
    Returns:
        dict: Dettagli del progetto con status
        
    Raises:
        HTTPException: 400 per ID non valido, 404 se il progetto non esiste
    """
    # FastAPI's Path validation will handle non-integer values automatically
    # We'll add additional validation for the ID
    if not isinstance(id_prg, int) or id_prg <= 0:
        raise HTTPException(
            status_code=400,
            detail={
                "status": "error",
                "message": "ID progetto non valido. Deve essere un numero intero positivo."
            }
        )
    
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Use parameterized query to prevent SQL injection
        cursor.execute("""
            SELECT id_prg, nome_progetto as name, 
                   COALESCE(descrizione, '') as description, 
                   data_creazione as createdAt
            FROM t_progetti
            WHERE id_prg = ?
        """, (id_prg,))
        
        progetto = cursor.fetchone()
        
        if not progetto:
            raise HTTPException(
                status_code=404, 
                detail={
                    "status": "error",
                    "message": f"Progetto con ID {id_prg} non trovato"
                }
            )
            
        return {
            "status": "success",
            "data": dict(progetto)
        }
        
    except Exception as e:
        logger.error(f"Error fetching project: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail={
                "status": "error",
                "message": f"Errore durante il recupero del progetto: {str(e)}"
            }
        )
    finally:
        if conn:
            try:
                conn.close()
            except:
                pass

@router.post("/progetti")
async def api_crea_progetto(request: Request):
    """Crea un nuovo progetto."""
    conn = None
    try:
        data = await request.json()
        name = data.get("name")
        description = data.get("description", "")
        
        if not name:
            raise HTTPException(
                status_code=400, 
                detail={
                    "status": "error",
                    "message": "Il campo 'name' è obbligatorio"
                }
            )
            
        # Get current date for data_creazione
        data_creazione = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Call the existing function with all required parameters
        crea_progetto(name, description, data_creazione)
        
        # Get the created project
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id_prg, nome_progetto as name, descrizione as description, 
                   data_creazione as createdAt
            FROM t_progetti 
            ORDER BY id_prg DESC 
            LIMIT 1
        """)
        
        project = dict(cursor.fetchone())
        
        # Return with status for Vue frontend
        return {
            "status": "success",
            "data": project,
            "message": "Progetto creato con successo"
        }
        
    except HTTPException as e:
        raise
    except Exception as e:
        logger.error(f"Error creating project: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail={"message": f"Errore durante la creazione del progetto: {str(e)}"}
        )

@router.delete("/progetti/{id_prg}")
async def api_elimina_progetto(id_prg: int):
    """Elimina un progetto e tutte le sue dipendenze."""
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Verifica che il progetto esista
        cursor.execute("""
            SELECT id_prg, nome_progetto as name 
            FROM t_progetti 
            WHERE id_prg = ?
        """, (id_prg,))
        
        project = cursor.fetchone()
        if not project:
            raise HTTPException(
                status_code=404, 
                detail={
                    "status": "error",
                    "message": f"Progetto con ID {id_prg} non trovato"
                }
            )
            
        project = dict(project)
            
        # Inizia una transazione
        cursor.execute("BEGIN")
        
        try:
            # Elimina le dipendenze
            tabelle_da_eliminare = [
                "t_io", "t_potenza", "t_utenze", 
                "t_hw_nodo", "t_nodi_prg"
            ]
            
            for tabella in tabelle_da_eliminare:
                cursor.execute(f"DELETE FROM {tabella} WHERE id_prg = ?", (id_prg,))
            
            # Elimina il progetto
            cursor.execute("DELETE FROM t_progetti WHERE id_prg = ?", (id_prg,))
            
            # Commit della transazione
            conn.commit()
            
            # Return success response with status
            return {
                "status": "success",
                "message": f"Progetto '{project['name']}' eliminato con successo",
                "data": {
                    "id_prg": id_prg
                }
            }
            
        except Exception as e:
            # Rollback in caso di errore
            conn.rollback()
            raise e
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting project {id_prg}: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail={
                "status": "error",
                "message": f"Errore durante l'eliminazione del progetto: {str(e)}"
            }
        )
    finally:
        if conn:
            try:
                conn.close()
            except:
                pass

# File upload endpoints
UPLOAD_FOLDER = "uploaded_files"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@router.post("/progetti/{id_prg}/carica_file_utenze")
async def route_carica_file_utenze(id_prg: int, request: Request):
    """
    Endpoint per il caricamento del file delle utenze.
    
    Args:
        id_prg: ID del progetto a cui associare le utenze
        request: La richiesta HTTP contenente il file
        
    Returns:
        dict: Risposta standardizzata con stato e dati
    """
    conn = None
    try:
        # Verifica che il progetto esista
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id_prg, nome_progetto FROM t_progetti WHERE id_prg = ?", (id_prg,))
        progetto = cursor.fetchone()
        
        if not progetto:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "status": "error",
                    "message": f"Progetto con ID {id_prg} non trovato"
                }
            )
        
        # Elabora il file dalla richiesta
        form_data = await request.form()
        if "file" not in form_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail={
                    "status": "error",
                    "message": "Nessun file fornito"
                }
            )
            
        file = form_data["file"]
        filename = secure_filename(file.filename)
        
        if not filename.lower().endswith(('.xls', '.xlsx')):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail={
                    "status": "error",
                    "message": "Formato file non supportato. Caricare un file Excel (.xls o .xlsx)"
                }
            )
        
        # Crea la directory di upload se non esiste
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        
        # Genera un nome file univoco per evitare sovrascritture
        file_ext = os.path.splitext(filename)[1]
        unique_filename = f"{uuid.uuid4().hex}{file_ext}"
        file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
        
        # Salva il file temporaneamente
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Verifica se ci sono già utenze per questo progetto
        cursor.execute("SELECT COUNT(*) as count FROM t_utenza WHERE id_prg = ?", (id_prg,))
        count = cursor.fetchone()["count"]
        
        if count > 0:
            # Se ci sono già utenze, restituisci un flag invece di procedere
            return {
                "status": "confirmation_required",
                "message": "Sono già presenti utenze per questo progetto. Vuoi sovrascriverle?",
                "data": {
                    "projectId": id_prg,
                    "existingCount": count,
                    "tempFilePath": file_path,
                    "fileName": filename
                }
            }
        
        # Altrimenti procedi con l'elaborazione
        return await _processa_file_utenze(id_prg, file_path, filename)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Errore durante l'elaborazione del caricamento del file: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail={
                "status": "error",
                "message": f"Errore durante l'elaborazione del file: {str(e)}"
            }
        )
    finally:
        if conn:
            try:
                conn.close()
            except:
                pass

async def _processa_file_utenze(id_prg: int, file_path: str, original_filename: str = None):
    """
    Elabora il file delle utenze e popola il database.
    
    Args:
        id_prg: ID del progetto
        file_path: Percorso del file temporaneo
        original_filename: Nome originale del file (opzionale)
        
    Returns:
        dict: Risposta standardizzata con i risultati dell'importazione
    """
    conn = None
    try:
        # Qui andrebbe la logica per elaborare il file Excel
        # Per ora simuliamo un successo con dati di esempio
        
        # Esempio di dati simulati
        utenze_importate = 42
        
        # Crea un log dell'importazione
        import_log = {
            "timestamp": datetime.now().isoformat(),
            "filePath": file_path,
            "originalFileName": original_filename or os.path.basename(file_path),
            "importedCount": utenze_importate,
            "status": "completed"
        }
        
        # Simula la creazione di un nodo se necessario
        nodo_creato = None
        if utenze_importate > 0:
            # Simula la creazione di un nodo PLC
            nodo_creato = {
                "id_nodo": 1,
                "nome_nodo": "PLC_Default",
                "tipo_nodo": "PLC",
                "descrizione": "Nodo PLC creato automaticamente"
            }
        
        # Restituisci una risposta standardizzata
        return {
            "status": "success",
            "message": f"File elaborato con successo. Importate {utenze_importate} utenze.",
            "data": {
                "projectId": id_prg,
                "importedCount": utenze_importate,
                "nodeCreated": nodo_creato is not None,
                "nodeInfo": nodo_creato,
                "fileInfo": {
                    "originalName": original_filename or os.path.basename(file_path),
                    "storedPath": file_path,
                    "size": os.path.getsize(file_path) if os.path.exists(file_path) else 0,
                    "importedAt": datetime.now().isoformat()
                },
                "importLog": import_log
            }
        }
        
    except Exception as e:
        logger.error(f"Errore durante l'elaborazione del file: {str(e)}", exc_info=True)
        
        # Crea un log dell'errore
        error_log = {
            "timestamp": datetime.now().isoformat(),
            "filePath": file_path,
            "originalFileName": original_filename or os.path.basename(file_path) if file_path else None,
            "status": "failed",
            "error": str(e)
        }
        
        # Cerca di eliminare il file temporaneo in caso di errore
        try:
            if file_path and os.path.exists(file_path):
                os.remove(file_path)
        except Exception as e2:
            logger.error(f"Errore durante la pulizia del file temporaneo: {str(e2)}")
            error_log["cleanupError"] = str(e2)
            
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail={
                "status": "error",
                "message": f"Errore durante l'elaborazione del file: {str(e)}",
                "errorDetails": error_log
            }
        )
    finally:
        if conn:
            try:
                conn.close()
            except:
                pass
            conn.close()
        else:
            pass

@router.post("/io_assign")
async def api_io_assign(io_data: dict):
    """Assegna un IO a un modulo."""
    conn = None
    try:
        io_id = io_data.get("id")
        node_id = io_data.get("nodeId")
        address = io_data.get("address")
        
        if not all([io_id, node_id is not None, address is not None]):
            raise HTTPException(
                status_code=400, 
                detail={
                    "status": "error",
                    "message": "Tutti i campi sono obbligatori (id, nodeId, address)"
                }
            )
            
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Verify IO exists and is not already assigned
        cursor.execute("""
            SELECT 
                id_io as id,
                id_nodo_hw as nodeId,
                indirizzo as address,
                tipo_io as type,
                descrizione as description
            FROM t_io 
            WHERE id_io = ?
        """, (io_id,))
        
        io_record = cursor.fetchone()
        if not io_record:
            raise HTTPException(
                status_code=404, 
                detail={
                    "status": "error",
                    "message": f"IO con ID {io_id} non trovato"
                }
            )
            
        io_record = dict(io_record)
            
        if io_record["nodeId"] is not None:
            raise HTTPException(
                status_code=400, 
                detail={
                    "status": "error",
                    "message": f"L'IO {io_id} è già stato assegnato a un nodo"
                }
            )
        
        # Verify address is not already used for this node
        cursor.execute("""
            SELECT 
                id_io as id,
                tipo_io as type,
                descrizione as description
            FROM t_io 
            WHERE id_nodo_hw = ? AND indirizzo = ? AND id_io != ?
        """, (node_id, address, io_id))
        
        conflicting_io = cursor.fetchone()
        if conflicting_io:
            raise HTTPException(
                status_code=400, 
                detail={
                    "status": "error",
                    "message": f"Indirizzo {address} già utilizzato per questo nodo",
                    "data": dict(conflicting_io) if conflicting_io else None
                }
            )
        
        # Update the assignment
        cursor.execute("""
            UPDATE t_io 
            SET id_nodo_hw = ?, indirizzo = ?
            WHERE id_io = ?
        """, (node_id, address, io_id))
        
        # Get the updated IO record
        cursor.execute("""
            SELECT 
                id_io as id,
                tipo_io as type,
                indirizzo as address,
                descrizione as description,
                id_prg as projectId,
                id_nodo_hw as nodeId
            FROM t_io 
            WHERE id_io = ?
        """, (io_id,))
        
        updated_io = dict(cursor.fetchone())
        conn.commit()
        
        # Return success response with updated IO
        return {
            "status": "success",
            "message": "IO assegnato con successo",
            "data": updated_io
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error assigning IO: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail={
                "status": "error",
                "message": f"Errore durante l'assegnazione dell'IO: {str(e)}"
            }
        )
    finally:
        if conn:
            try:
                conn.close()
            except:
                pass

@router.get("/progetti/{id_prg}/io_non_assegnati")
async def api_io_non_assegnati(id_prg: int):
    """Restituisce gli I/O non ancora assegnati a un modulo."""
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Verify project exists
        cursor.execute("SELECT 1 FROM t_progetti WHERE id_prg = ?", (id_prg,))
        if not cursor.fetchone():
            raise HTTPException(
                status_code=404,
                detail={
                    "status": "error",
                    "message": f"Progetto con ID {id_prg} non trovato"
                }
            )
        
        cursor.execute("""
            SELECT 
                id_io as id,
                tipo_io as type,
                indirizzo as address,
                descrizione as description,
                id_prg as projectId
            FROM t_io
            WHERE id_prg = ? AND id_nodo_hw IS NULL
            ORDER BY tipo_io, indirizzo
        """, (id_prg,))
        
        # Return with status for Vue frontend
        return {
            "status": "success",
            "data": [dict(row) for row in cursor.fetchall()]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching unassigned IO: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail={
                "status": "error",
                "message": f"Errore durante il recupero degli IO non assegnati: {str(e)}"
            }
        )
    finally:
        if conn:
            try:
                conn.close()
            except:
                pass

@router.get("/progetti/{id_prg}/utenze")
async def api_utenze(id_prg: int):
    """Restituisce tutte le utenze di un progetto."""
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # First verify project exists
        cursor.execute("SELECT id_prg FROM t_progetti WHERE id_prg = ?", (id_prg,))
        if not cursor.fetchone():
            raise HTTPException(
                status_code=404,
                detail={
                    "status": "error",
                    "message": f"Progetto con ID {id_prg} non trovato"
                }
            )
        
        cursor.execute("""
            SELECT 
                id_utenza as id,
                nome_utenza as name,
                descrizione as description,
                categoria as category,
                tensione as voltage,
                zona as zone,
                DI as di,
                DO as do,
                AI as ai,
                AO as ao,
                FDI as fdi,
                FDO as fdo,
                potenza as power,
                id_cat as categoryId,
                id_sottocat as subcategoryId,
                id_opzione as optionId,
                elaborata as processed,
                taglio as cut
            FROM t_utenze
            WHERE id_prg = ?
            ORDER BY nome_utenza
        """, (id_prg,))
        
        utenze = [dict(row) for row in cursor.fetchall()]
        
        return {
            "status": "success",
            "data": utenze
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching utilities for project {id_prg}: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail={
                "status": "error",
                "message": f"Errore durante il recupero delle utenze: {str(e)}"
            }
        )

@router.put("/progetti/{id_prg}/configura_potenza")
async def route_salva_potenza(id_prg: int, request: Request):
    """Salva la configurazione della potenza."""
    conn = None
    try:
        data = await request.json()
        
        # Validate input data
        required_fields = [
            "contractedPower", "availablePower",
            "plantPower", "usedPower", "remainingPower"
        ]
        
        if not all(field in data for field in required_fields):
            raise HTTPException(
                status_code=400,
                detail={
                    "status": "error",
                    "message": "Tutti i campi della potenza sono obbligatori"
                }
            )
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Verify project exists
        cursor.execute("SELECT 1 FROM t_progetti WHERE id_prg = ?", (id_prg,))
        if not cursor.fetchone():
            raise HTTPException(
                status_code=404,
                detail={
                    "status": "error",
                    "message": f"Progetto con ID {id_prg} non trovato"
                }
            )
        
        # Update or insert configuration
        cursor.execute("""
            INSERT OR REPLACE INTO t_potenza 
            (id_prg, potenza_contrattuale, potenza_disponibile, 
             potenza_impianto, potenza_utilizzata, potenza_residua)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            id_prg,
            data["contractedPower"],
            data["availablePower"],
            data["plantPower"],
            data["usedPower"],
            data["remainingPower"]
        ))
        
        conn.commit()
        
        # Return success response with status
        return {
            "status": "success",
            "message": "Configurazione della potenza salvata con successo",
            "data": {
                "projectId": id_prg,
                "power": {
                    "id": cursor.lastrowid,
                    "contractedPower": data["contractedPower"],
                    "availablePower": data["availablePower"],
                    "plantPower": data["plantPower"],
                    "usedPower": data["usedPower"],
                    "remainingPower": data["remainingPower"]
                }
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error saving power configuration: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail={
                "status": "error",
                "message": f"Errore durante il salvataggio della configurazione della potenza: {str(e)}"
            }
        )
    finally:
        if conn:
            try:
                conn.close()
            except:
                pass

@router.get("/progetti/{id_prg}/configura_potenza")
async def route_configura_potenza(id_prg: int):
    """Endpoint per la configurazione della potenza."""
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Recupera le informazioni sulla potenza
        cursor.execute("""
            SELECT id_potenza, tipo_potenza, valore, unita_misura, descrizione
            FROM t_potenza
            WHERE id_prg = ?
        """, (id_prg,))
        
        potenze = [dict(row) for row in cursor.fetchall()]
        
        # Recupera le opzioni di avviamento disponibili
        cursor.execute("""
            SELECT id_opzione, nome_opzione, descrizione
            FROM t_opzioni_avviamento
            ORDER BY nome_opzione
        """)
        
        opzioni_avviamento = [dict(row) for row in cursor.fetchall()]
        
        return {
            "status": "success",
            "data": {
                "id_prg": id_prg,
                "potenze": potenze,
                "opzioni_avviamento": opzioni_avviamento
            }
        }
        
    except Exception as e:
        logger.error(f"Error fetching power configuration for project {id_prg}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

@router.post("/assegna_avviamento")
async def route_assegna_avviamento(request: Request):
    """
    Endpoint per l'assegnazione degli avviamenti.
    
    Args:
        request: La richiesta HTTP contenente i dati di assegnazione
        
    Request Body:
        - id_prg: ID del progetto (int, required)
        - id_potenza: ID della potenza da aggiornare (int, required)
        - id_opzione_avviamento: ID dell'opzione di avviamento da assegnare (int, required)
        
    Returns:
        dict: Risposta standardizzata con stato e dati aggiornati
    """
    conn = None
    try:
        data = await request.json()
        id_prg = data.get("id_prg")
        id_potenza = data.get("id_potenza")
        id_opzione_avviamento = data.get("id_opzione_avviamento")
        
        # Validazione input
        if not all([id_prg, id_potenza, id_opzione_avviamento]):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "status": "error",
                    "message": "Tutti i parametri sono obbligatori (id_prg, id_potenza, id_opzione_avviamento)"
                }
            )
            
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Verifica che l'opzione di avviamento esista
        cursor.execute("""
            SELECT id_opzione, nome_opzione, descrizione 
            FROM t_opzioni_avviamento 
            WHERE id_opzione = ?
        """, (id_opzione_avviamento,))
        
        opzione = cursor.fetchone()
        if not opzione:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "status": "error",
                    "message": f"Opzione di avviamento con ID {id_opzione_avviamento} non trovata"
                }
            )
        
        # Aggiorna l'opzione di avviamento
        cursor.execute("""
            UPDATE t_potenza
            SET id_opzione_avviamento = ?, 
                elaborato = 1,
                data_aggiornamento = CURRENT_TIMESTAMP
            WHERE id_potenza = ? AND id_prg = ?
            RETURNING id_potenza, id_opzione_avviamento, elaborato
        """, (id_opzione_avviamento, id_potenza, id_prg))
        
        result = cursor.fetchone()
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "status": "error",
                    "message": f"Potenza con ID {id_potenza} non trovata o non modificabile per il progetto {id_prg}"
                }
            )
            
        conn.commit()
        
        # Prepara la risposta con i dati aggiornati
        response_data = {
            "projectId": id_prg,
            "powerId": result[0],
            "starterOption": {
                "id": result[1],
                "name": opzione[1],
                "description": opzione[2]
            },
            "processed": bool(result[2])
        }
        
        return {
            "status": "success",
            "message": "Opzione di avviamento aggiornata con successo",
            "data": response_data
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Errore durante l'assegnazione dell'avviamento: {str(e)}", exc_info=True)
        if conn:
            conn.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "status": "error",
                "message": f"Errore durante l'aggiornamento dell'opzione di avviamento: {str(e)}"
            }
        )
    finally:
        if conn:
            try:
                conn.close()
            except:
                pass

# Aggiungi qui altri endpoint API necessari...

# Esporta il router per l'inclusione nell'app principale
__all__ = ["router"]
