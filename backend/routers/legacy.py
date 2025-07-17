"""
Legacy routes for backward compatibility
"""
from fastapi import APIRouter, Depends, HTTPException, status, Request, UploadFile, File, Form
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional, Dict, Any
import os
import shutil
import uuid
from datetime import datetime
import logging
from core.database import get_db
from core.security import get_current_user

router = APIRouter(tags=["legacy"])

# Configure logging
logger = logging.getLogger(__name__)

# Upload folder configuration
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@router.post("/progetti/{id_prg}/carica_file_utenze")
async def route_carica_file_utenze(
    id_prg: int,
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user)
):
    """
    Endpoint per il caricamento del file delle utenze.
    
    Args:
        id_prg: ID del progetto a cui associare le utenze
        file: Il file Excel da caricare
        
    Returns:
        dict: Risposta standardizzata con stato e dati
    """
    try:
        # Validate file type
        if not file.filename.lower().endswith(('.xls', '.xlsx')):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "status": "error",
                    "message": "Formato file non supportato. Caricare un file Excel (.xls o .xlsx)"
                }
            )
        
        # Generate unique filename
        file_ext = os.path.splitext(file.filename)[1]
        unique_filename = f"{uuid.uuid4().hex}{file_ext}"
        file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
        
        # Save the file temporarily
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # For now, return a success response
        # In a real implementation, you would process the Excel file here
        return {
            "status": "success",
            "message": f"File {file.filename} caricato con successo per il progetto {id_prg}",
            "data": {
                "projectId": id_prg,
                "fileName": file.filename,
                "storedPath": file_path,
                "uploadedAt": datetime.now().isoformat()
            }
        }
        
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

@router.get("/download_template")
async def download_template():
    """
    Download the Excel template file for utilities upload.
    """
    try:
        template_path = os.path.join("file_utili", "Template.xlsx")
        
        if not os.path.exists(template_path):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Template file not found"
            )
        
        return FileResponse(
            path=template_path,
            filename="Template.xlsx",
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error downloading template: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error downloading template file"
        )

@router.get("/progetti")
async def get_progetti(current_user: dict = Depends(get_current_user)):
    """Get all projects"""
    try:
        # Mock data for now - replace with actual database query
        projects = [
            {
                "id_prg": 1,
                "nome": "Progetto Test 1",
                "descrizione": "Descrizione progetto test 1",
                "data_creazione": "2024-01-01",
                "url_dettaglio": "/project/1"
            },
            {
                "id_prg": 2,
                "nome": "Progetto Test 2", 
                "descrizione": "Descrizione progetto test 2",
                "data_creazione": "2024-01-02",
                "url_dettaglio": "/project/2"
            }
        ]
        
        return projects
        
    except Exception as e:
        logger.error(f"Error fetching projects: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching projects"
        )

@router.get("/lista_nodi")
async def get_lista_nodi(current_user: dict = Depends(get_current_user)):
    """Get all nodes"""
    try:
        # Mock data for now - replace with actual database query
        nodes = [
            {
                "id_nodo": 1,
                "nome_nodo": "Nodo 1",
                "descrizione": "Descrizione nodo 1"
            },
            {
                "id_nodo": 2,
                "nome_nodo": "Nodo 2",
                "descrizione": "Descrizione nodo 2"
            }
        ]
        
        return nodes
        
    except Exception as e:
        logger.error(f"Error fetching nodes: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching nodes"
        )

@router.get("/hw_nodo_list")
async def get_hw_nodo_list(
    id_nodo: int,
    current_user: dict = Depends(get_current_user)
):
    """Get hardware for a specific node"""
    try:
        # Mock data for now - replace with actual database query
        hardware = [
            {
                "id_nodo_hw": 1,
                "slot": 1,
                "nome_hw": "Modulo DI",
                "tipo": "DI",
                "DI": 8,
                "DO": 0,
                "AI": 0,
                "AO": 0
            },
            {
                "id_nodo_hw": 2,
                "slot": 2,
                "nome_hw": "Modulo DO",
                "tipo": "DO",
                "DI": 0,
                "DO": 8,
                "AI": 0,
                "AO": 0
            }
        ]
        
        return hardware
        
    except Exception as e:
        logger.error(f"Error fetching node hardware: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching node hardware"
        )

@router.get("/catalogo_hw")
async def get_catalogo_hw(current_user: dict = Depends(get_current_user)):
    """Get hardware catalog"""
    try:
        # Mock data for now - replace with actual database query
        catalog = [
            {
                "id_hw": 1,
                "nome_hw": "Modulo DI 8 canali",
                "descrizione_hw": "Modulo input digitali 8 canali",
                "tipo": "DI",
                "DI": 8,
                "DO": 0,
                "AI": 0,
                "AO": 0
            },
            {
                "id_hw": 2,
                "nome_hw": "Modulo DO 8 canali",
                "descrizione_hw": "Modulo output digitali 8 canali",
                "tipo": "DO",
                "DI": 0,
                "DO": 8,
                "AI": 0,
                "AO": 0
            }
        ]
        
        return catalog
        
    except Exception as e:
        logger.error(f"Error fetching hardware catalog: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching hardware catalog"
        )

@router.get("/io_unassigned")
async def get_io_unassigned(
    tipo: str,
    current_user: dict = Depends(get_current_user)
):
    """Get unassigned I/O by type"""
    try:
        # Mock data for now - replace with actual database query
        io_list = [
            {
                "id_io": 1,
                "descrizione": "DI_1 - Sensore temperatura",
                "selezionato": False
            },
            {
                "id_io": 2,
                "descrizione": "DI_2 - Sensore pressione",
                "selezionato": False
            }
        ]
        
        return io_list
        
    except Exception as e:
        logger.error(f"Error fetching unassigned I/O: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching unassigned I/O"
        )

@router.get("/io_assigned")
async def get_io_assigned(
    id_modulo: int,
    id_nodo: int,
    current_user: dict = Depends(get_current_user)
):
    """Get assigned I/O for a module"""
    try:
        # Mock data for now - replace with actual database query
        io_list = [
            {
                "id_io": 3,
                "descrizione": "DO_1 - Attuatore valvola",
                "selezionato": False
            },
            {
                "id_io": 4,
                "descrizione": "DO_2 - Motore pompa",
                "selezionato": False
            }
        ]
        
        return io_list
        
    except Exception as e:
        logger.error(f"Error fetching assigned I/O: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching assigned I/O"
        )

@router.get("/aggiorna_tabella")
async def aggiorna_tabella_utenze(
    id_prg: int,
    current_user: dict = Depends(get_current_user)
):
    """Get utilities for a project"""
    try:
        # Mock data for now - replace with actual database query
        utilities = [
            {
                "id_utenza": 1,
                "nome_utenza": "Sensore Temperatura 1",
                "descrizione": "Sensore di temperatura per ambiente",
                "categoria": "Sensore",
                "tipo_comando": "Automatico",
                "tensione": "24V",
                "zona": "Zona A",
                "DI": 1,
                "DO": 0,
                "AI": 1,
                "AO": 0,
                "FDI": 0,
                "FDO": 0,
                "elaborata": 0
            },
            {
                "id_utenza": 2,
                "nome_utenza": "Motore Pompa 1",
                "descrizione": "Motore per pompa di circolazione",
                "categoria": "Attuatore",
                "tipo_comando": "Manuale",
                "tensione": "400V",
                "zona": "Zona B",
                "DI": 0,
                "DO": 1,
                "AI": 0,
                "AO": 0,
                "FDI": 0,
                "FDO": 0,
                "elaborata": 1
            }
        ]
        
        return {"utenze": utilities}
        
    except Exception as e:
        logger.error(f"Error fetching utilities: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching utilities"
        )

@router.get("/selezione_utenza")
async def selezione_utenza(
    id_utenza: int,
    current_user: dict = Depends(get_current_user)
):
    """Get selection for a utility"""
    try:
        # Mock data for now - replace with actual database query
        selection = {
            "id_cat": 1,
            "id_sottocat": 1,
            "id_opzione": 1
        }
        
        return {"selezione": selection}
        
    except Exception as e:
        logger.error(f"Error fetching utility selection: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching utility selection"
        )

@router.get("/sottocategorie")
async def get_sottocategorie(
    id_categoria: int,
    current_user: dict = Depends(get_current_user)
):
    """Get subcategories for a category"""
    try:
        # Mock data based on category ID
        subcategories_map = {
            1: [  # Sensore
                {"id_sottocategoria": 1, "sottocategoria": "Sensore di livello"},
                {"id_sottocategoria": 2, "sottocategoria": "Sensore di pressione"},
                {"id_sottocategoria": 3, "sottocategoria": "Sensore di posizione"},
                {"id_sottocategoria": 4, "sottocategoria": "Sensore di prossimità"},
                {"id_sottocategoria": 5, "sottocategoria": "Sensore di presenza"}
            ],
            2: [  # Attuatore
                {"id_sottocategoria": 6, "sottocategoria": "Valvola"},
                {"id_sottocategoria": 7, "sottocategoria": "Motore"},
                {"id_sottocategoria": 8, "sottocategoria": "Pompa"}
            ],
            3: [  # Comando operatore
                {"id_sottocategoria": 9, "sottocategoria": "Pulsante"},
                {"id_sottocategoria": 10, "sottocategoria": "Interruttore"}
            ],
            4: [  # Segnalazione
                {"id_sottocategoria": 11, "sottocategoria": "Luce"},
                {"id_sottocategoria": 12, "sottocategoria": "Sirena"}
            ],
            5: [  # Dispositivo di sicurezza
                {"id_sottocategoria": 13, "sottocategoria": "Interblocco"},
                {"id_sottocategoria": 14, "sottocategoria": "Fusibile"}
            ]
        }
        
        subcategories = subcategories_map.get(id_categoria, [])
        return subcategories
        
    except Exception as e:
        logger.error(f"Error fetching subcategories: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching subcategories"
        )

@router.get("/opzioni")
async def get_opzioni(
    id_sottocategoria: int,
    current_user: dict = Depends(get_current_user)
):
    """Get options for a subcategory"""
    try:
        # Mock data based on subcategory ID
        options_map = {
            1: [  # Sensore di livello
                {"id_opzione": 1, "opzione": "Livello minimo (NO)"},
                {"id_opzione": 2, "opzione": "Livello massimo (NC)"}
            ],
            2: [  # Sensore di pressione
                {"id_opzione": 3, "opzione": "Pressione alta"},
                {"id_opzione": 4, "opzione": "Pressione bassa"}
            ],
            6: [  # Valvola
                {"id_opzione": 5, "opzione": "Apertura"},
                {"id_opzione": 6, "opzione": "Chiusura"}
            ],
            7: [  # Motore
                {"id_opzione": 7, "opzione": "Avvio"},
                {"id_opzione": 8, "opzione": "Arresto"}
            ]
        }
        
        options = options_map.get(id_sottocategoria, [])
        return options
        
    except Exception as e:
        logger.error(f"Error fetching options: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching options"
        )

@router.get("/dettagli")
async def get_dettagli(
    id_utenza: int,
    id_categoria: int,
    id_sottocategoria: int,
    id_opzione: int,
    id_prg: int,
    current_user: dict = Depends(get_current_user)
):
    """Get details for a utility configuration"""
    try:
        # Mock data - in real implementation, this would generate details based on the utility's I/O configuration
        details = [
            {
                "tipo": "Digital Input",
                "descrizione": "DI_1 - Sensore di livello",
                "simboli": ["S1", "B1"]
            },
            {
                "tipo": "Digital Output", 
                "descrizione": "DO_1 - Valvola di controllo",
                "simboli": ["S10", "B1"]
            }
        ]
        
        return {"dettagli": details}
        
    except Exception as e:
        logger.error(f"Error fetching details: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching details"
        )

@router.post("/conferma")
async def conferma(
    current_user: dict = Depends(get_current_user)
):
    """Confirm utility configuration"""
    try:
        # Mock confirmation - in real implementation, this would save the configuration
        return {
            "status": "success",
            "message": "Configurazione confermata con successo"
        }
        
    except Exception as e:
        logger.error(f"Error confirming configuration: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error confirming configuration"
        )

@router.post("/preelabora_utenze")
async def preelabora_utenze(
    current_user: dict = Depends(get_current_user)
):
    """Pre-process all utilities"""
    try:
        # Mock pre-processing - in real implementation, this would process all utilities
        return {
            "status": "success",
            "message": "Pre-elaborazione completata per tutte le utenze"
        }
        
    except Exception as e:
        logger.error(f"Error pre-processing utilities: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error pre-processing utilities"
        )

@router.post("/reset_opzione")
async def reset_opzione(
    current_user: dict = Depends(get_current_user)
):
    """Reset option for utilities"""
    try:
        # Mock implementation
        return {
            "status": "success",
            "message": "Opzione resettata con successo"
        }
    except Exception as e:
        logger.error(f"Error resetting option: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error resetting option"
        )

# =============================================================================
# POTENZA ENDPOINTS
# =============================================================================

@router.get("/potenza")
async def api_potenza(
    id_prg: int,
    current_user: dict = Depends(get_current_user)
):
    """
    Get power utilities for a project.
    
    Args:
        id_prg: Project ID
        
    Returns:
        dict: Power utilities data
    """
    try:
        # Mock data for power utilities
        utenze = [
            {
                "id_potenza": 1,
                "nome": "Motore Pompa 1",
                "potenza": 5.5,
                "tensione": 400,
                "descrizione": "Motore pompa di circolazione",
                "elaborato": 0
            },
            {
                "id_potenza": 2,
                "nome": "Ventilatore Condizionamento",
                "potenza": 2.2,
                "tensione": 230,
                "descrizione": "Ventilatore sistema condizionamento",
                "elaborato": 1
            },
            {
                "id_potenza": 3,
                "nome": "Compressore Aria",
                "potenza": 7.5,
                "tensione": 400,
                "descrizione": "Compressore aria compressa",
                "elaborato": 0
            }
        ]
        
        return {"utenze": utenze}
        
    except Exception as e:
        logger.error(f"Error fetching power utilities: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching power utilities"
        )

@router.get("/opzioni_avviamento")
async def get_opzioni_avviamento(
    current_user: dict = Depends(get_current_user)
):
    """
    Get startup options for power utilities.
    
    Returns:
        dict: Startup options data
    """
    try:
        # Mock data for startup options
        opzioni = [
            {
                "id_opzione": 1,
                "descrizione": "Avviamento diretto semplice"
            },
            {
                "id_opzione": 2,
                "descrizione": "Avviamento diretto con inversione"
            },
            {
                "id_opzione": 3,
                "descrizione": "Partenza con protezione in morsettiera"
            }
        ]
        
        return {"opzioni": opzioni}
        
    except Exception as e:
        logger.error(f"Error fetching startup options: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching startup options"
        )

@router.get("/get_opzione_potenza")
async def get_opzione_potenza(
    id_potenza: int,
    current_user: dict = Depends(get_current_user)
):
    """
    Get current startup option for a power utility.
    
    Args:
        id_potenza: Power utility ID
        
    Returns:
        dict: Current startup option
    """
    try:
        # Mock data - in real implementation, query the database
        # For now, return a random option or none
        import random
        opzioni = [1, 2, 3, None]
        selected_option = random.choice(opzioni)
        
        return {
            "id_opzione_avviamento": selected_option
        }
        
    except Exception as e:
        logger.error(f"Error fetching power utility option: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching power utility option"
        )

@router.post("/assegna_avviamento")
async def assegna_avviamento(
    request: Request,
    current_user: dict = Depends(get_current_user)
):
    """
    Assign startup option to a power utility.
    
    Request Body:
        - id_prg: Project ID
        - id_potenza: Power utility ID
        - opzione_avviamento: Startup option ID
        
    Returns:
        dict: Assignment result
    """
    try:
        data = await request.json()
        id_prg = data.get("id_prg")
        id_potenza = data.get("id_potenza")
        opzione_avviamento = data.get("opzione_avviamento")
        
        # Validate required fields
        if not all([id_prg, id_potenza, opzione_avviamento]):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "status": "error",
                    "message": "Tutti i parametri sono obbligatori (id_prg, id_potenza, opzione_avviamento)"
                }
            )
        
        # Mock implementation - in real app, update database
        logger.info(f"Assigning startup option {opzione_avviamento} to power utility {id_potenza} in project {id_prg}")
        
        return {
            "status": "success",
            "message": "Opzione di avviamento assegnata con successo",
            "data": {
                "id_prg": id_prg,
                "id_potenza": id_potenza,
                "opzione_avviamento": opzione_avviamento,
                "updated_rows": 1
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error assigning startup option: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "status": "error",
                "message": f"Errore durante l'assegnazione dell'opzione di avviamento: {str(e)}"
            }
        )
