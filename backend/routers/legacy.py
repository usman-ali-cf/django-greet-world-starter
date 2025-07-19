"""
Legacy routes for backward compatibility
"""
from fastapi import APIRouter, Depends, HTTPException, status, Request, UploadFile, File, Form, Body
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
from scripts.carica_file_utenze_mock_alchemy import process_excel_file, validate_uploaded_file
from models.utility import Utenza, Potenza
from models.project import Project, Node
from sqlalchemy import select, text, func, update
from models import Hardware, HardwareNode
from models.legacy import NodiPrg
from scripts.crea_nodo_alchemy import crea_nodo_plc_automatico

router = APIRouter(tags=["legacy"])

# Configure logging
logger = logging.getLogger(__name__)

# Upload folder configuration
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def check_existing_utilities(db: AsyncSession, project_id: int) -> bool:
    """Check if utilities exist for the given project"""
    result = db.execute(
        db.query(Utenza).filter(Utenza.id_prg == project_id)
    )
    return result.scalar() is not None

@router.post("/progetti/{id_prg}/carica_file_utenze")
async def route_carica_file_utenze(
    id_prg: int,
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
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
        
        # Validate uploaded file
        is_valid, message = validate_uploaded_file(file)
        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "status": "error",
                    "message": message
                }
            )
        
        # Generate unique filename
        file_ext = os.path.splitext(file.filename)[1]
        unique_filename = f"{uuid.uuid4().hex}{file_ext}"
        file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
        
        # Save the file temporarily
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Process the Excel file using SQLAlchemy ORM
        result = await process_excel_file(db, id_prg, file_path)
        
        # Clean up the temporary file
        try:
            os.remove(file_path)
        except OSError:
            logger.warning(f"Could not remove temporary file: {file_path}")
        
        if not result["success"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "status": "error",
                    "message": result["message"]
                }
            )
        
        return {
            "status": "success",
            "message": result["message"],
            "data": {
                "projectId": id_prg,
                "fileName": file.filename,
                "utilitiesImported": result.get("count", 0),
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
async def get_progetti(
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get all projects"""
    try:
        # Fetch projects from database using SQLAlchemy ORM
        result = await db.execute(select(Project))
        projects_db = result.scalars().all()
        
        projects = []
        for project in projects_db:
            projects.append({
                "id_prg": project.id_prg,
                "nome": project.nome,
                "descrizione": project.descrizione,
                "data_creazione": project.data_creazione.isoformat() if project.data_creazione else None,
                "url_dettaglio": f"/project/{project.id_prg}"
            })
        
        return projects
        
    except Exception as e:
        logger.error(f"Error fetching projects: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching projects"
        )

@router.get("/lista_nodi")
async def get_lista_nodi(
    id_prg: int,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get all nodes for a specific project"""
    try:
        # Fetch nodes from database using SQLAlchemy ORM
        result = await db.execute(
            select(NodiPrg)
            .where(NodiPrg.id_prg == id_prg)
        )
        nodes_db = result.scalars().all()
        
        nodes = []
        for node in nodes_db:
            nodes.append({
                "id_nodo": node.id_nodo,
                "nome_nodo": node.nome_nodo,
                "descrizione": node.descrizione,
                "note": node.note,
                "tipo": node.tipo,
                "id_prg": node.id_prg
            })
        
        return nodes
        
    except Exception as e:
        logger.error(f"Error fetching nodes for project {id_prg}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching nodes"
        )

@router.get("/hw_nodo_list")
async def get_hw_nodo_list(
    id_nodo: int,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get hardware for a specific node"""
    try:
        # Fetch hardware nodes from database using SQLAlchemy ORM
        result = await db.execute(
            select(
                HardwareNode.id_nodo_hw,
                HardwareNode.slot,
                HardwareNode.quantita,
                Hardware.nome_hw,
                Hardware.DI,
                Hardware.DO,
                Hardware.AI,
                Hardware.AO
            )
            .join(Hardware, HardwareNode.id_hw == Hardware.id_hw)
            .where(HardwareNode.id_nodo == id_nodo)
            .order_by(HardwareNode.slot)
        )
        
        hw_rows = result.all()
        hardware = []
        
        for row in hw_rows:
            # Determine hardware type based on I/O configuration
            tipo = "DI" if row.DI > 0 else "DO" if row.DO > 0 else "AI" if row.AI > 0 else "AO" if row.AO > 0 else "MIXED"
            
            hardware.append({
                "id_nodo_hw": row.id_nodo_hw,
                "slot": row.slot,
                "nome_hw": row.nome_hw,
                "tipo": tipo,
                "DI": row.DI or 0,
                "DO": row.DO or 0,
                "AI": row.AI or 0,
                "AO": row.AO or 0,
                "quantita": row.quantita
            })
        
        return hardware
        
    except Exception as e:
        logger.error(f"Error fetching node hardware: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching node hardware"
        )

@router.get("/catalogo_hw")
async def get_catalogo_hw(
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    try:
        # Use SQLAlchemy ORM for all columns except F-DI and F-DO
        result = await db.execute(select(
            Hardware.id_hw,
            Hardware.nome_hw,
            Hardware.descrizione_hw,
            Hardware.DI,
            Hardware.DO,
            Hardware.AI,
            Hardware.AO,
            Hardware.F_DI,
            Hardware.F_DO
        ))
        hw_rows = result.all()
        hw_list = []
        for row in hw_rows:
            # get these values from the result: id_hw, nome_hw, descrizione_hw, DI, DO, AI, AO, "F-DI", "F-DO"

            hw_list.append({
                "id_hw": row.id_hw,
                "nome_hw": row.nome_hw,
                "descrizione_hw": row.descrizione_hw,
                "DI": row.DI,
                "DO": row.DO,
                "AI": row.AI,
                "AO": row.AO,
                "F_DI": row.F_DI,  # F-DI
                "F_DO": row.F_DO   # F-DO
            })
        return hw_list
    except Exception as e:
        logger.error(f"Errore nell'API catalogo_hw: {e}")
        return []

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
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    API per aggiornare la tabella delle utenze.
    """
    if not id_prg:
        return {"error": "ID progetto mancante"}
    try:
        result = await db.execute(
            select(Utenza).where(Utenza.id_prg == id_prg, Utenza.categoria == 'utenza')
        )
        utenze = result.scalars().all()
        # Convert to dicts for JSON serialization
        utenze_list = [
            {
                "id_utenza": u.id_utenza,
                "nome_utenza": u.nome_utenza,
                "descrizione": u.descrizione,
                "categoria": u.categoria,
                "tipo_comando": u.tipo_comando, 
                "tensione": u.tensione,
                "zona": u.zona,
                "DI": u.DI,
                "DO": u.DO,
                "AI": u.AI,
                "AO": u.AO,
                "FDI": u.FDI,
                "FDO": u.FDO,
                "elaborata": u.elaborata,
            }
            for u in utenze
        ]
        return {"utenze": utenze_list}
    except Exception as e:
        logger.error(f"Errore nell'API aggiorna_tabella_utenze: {e}")
        return {"error": "Errore interno del server"}

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
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    if not id_prg:
        return {"error": "ID progetto mancante"}
    try:
        result = await db.execute(
            select(
                Potenza.id_potenza,
                Potenza.nome,
                Potenza.potenza,
                Potenza.tensione,
                Potenza.descrizione,
                Potenza.elaborato
            ).where(Potenza.id_prg == id_prg)
        )
        rows = result.all()
        utenze = [
            {
                "id_potenza": r.id_potenza,
                "nome": r.nome,
                "potenza": r.potenza,
                "tensione": r.tensione,
                "descrizione": r.descrizione,
                "elaborato": r.elaborato
            }
            for r in rows
        ]
        return {"utenze": utenze}
    except Exception as e:
        logger.error(f"Errore nell'API potenza: {e}")
        return {"error": "Errore interno del server"}

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
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get current startup option for a power utility.
    
    Args:
        id_potenza: Power utility ID
        
    Returns:
        dict: Current startup option
    """
    try:
        from models.utility import Potenza
        
        result = await db.execute(
            select(Potenza.id_opzione_avviamento)
            .where(Potenza.id_potenza == id_potenza)
        )
        
        option = result.scalar()
        
        return {
            "id_opzione_avviamento": option
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
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
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
        
        # Update the Potenza record in the database
        from models.utility import Potenza
        
        result = await db.execute(
            update(Potenza)
            .where(Potenza.id_potenza == id_potenza, Potenza.id_prg == id_prg)
            .values(
                id_opzione_avviamento=opzione_avviamento,
                elaborato='1'  # Mark as processed
            )
        )
        
        await db.commit()
        
        # Check if any rows were updated
        if result.rowcount == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "status": "error",
                    "message": f"Potenza con ID {id_potenza} non trovata nel progetto {id_prg}"
                }
            )
        
        logger.info(f"Successfully assigned startup option {opzione_avviamento} to power utility {id_potenza} in project {id_prg}")
        
        return {
            "status": "success",
            "message": "Opzione di avviamento assegnata con successo",
            "data": {
                "id_prg": id_prg,
                "id_potenza": id_potenza,
                "opzione_avviamento": opzione_avviamento,
                "elaborato": "1",
                "updated_rows": result.rowcount
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error assigning startup option: {str(e)}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "status": "error",
                "message": f"Errore durante l'assegnazione dell'opzione di avviamento: {str(e)}"
            }
        )

@router.post("/crea_plc_automatico")
async def crea_plc_automatico(
    data: dict = Body(...),
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    id_prg = data.get("id_prg")
    if not id_prg:
        return {"error": "ID progetto non trovato"}
    try:
        result = await crea_nodo_plc_automatico(id_prg, db)
        if not result.get("success"):
            return result, 500
        return result
    except Exception as e:
        logger.error(f"Errore in crea_plc_automatico: {e}")
        return {"error": str(e)}

@router.post("/hw_nodo_add")
async def hw_nodo_add(
    data: dict = Body(...),
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    try:
        id_nodo = data.get('id_nodo')
        id_hw = data.get('id_hw')
        id_prg = data.get('id_prg')
        quantita = data.get('quantita', 1)
        
        if not id_nodo or not id_hw or not id_prg:
            return {"error": "I campi id_nodo, id_hw e id_prg sono obbligatori"}
        
        # Verify that the node exists and belongs to the specified project
        result = await db.execute(select(Node).where(Node.id_nodo == id_nodo))
        node = result.scalars().first()
        if not node:
            return {"error": "Nodo non trovato o non appartiene al progetto specificato"}
        
        # Calculate next slot for this node
        result = await db.execute(
            select(func.max(HardwareNode.slot)).where(HardwareNode.id_nodo == id_nodo)
        )
        max_slot = result.scalar()
        slot = (max_slot or 0) + 1
        
        # Convert quantita to integer
        try:
            quantita = int(quantita)
        except ValueError:
            return {"error": "Il campo quantita deve essere un numero"}
        
        # Insert hardware node
        hw_node = HardwareNode(
            id_nodo=id_nodo,
            id_prg=id_prg,
            id_hw=id_hw,
            slot=slot,
            quantita=quantita
        )
        db.add(hw_node)
        await db.commit()
        await db.refresh(hw_node)
        
        return {"message": "Hardware aggiunto al nodo", "id_nodo_hw": hw_node.id_nodo_hw}
    except Exception as e:
        logger.error(f"Errore in hw_nodo_add: {e}")
        return {"error": str(e)}

@router.delete("/hw_nodo_list/{id_nodo_hw}")
async def hw_nodo_delete(
    id_nodo_hw: int,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    try:
        # Get the record to delete
        result = await db.execute(select(HardwareNode).where(HardwareNode.id_nodo_hw == id_nodo_hw))
        record = result.scalars().first()
        if not record:
            return {"error": "Record non trovato"}
        
        id_nodo = record.id_nodo
        deleted_slot = record.slot
        
        # Delete the record
        await db.delete(record)
        
        # Update slots for remaining records
        await db.execute(
            update(HardwareNode)
            .where(HardwareNode.id_nodo == id_nodo, HardwareNode.slot > deleted_slot)
            .values(slot=HardwareNode.slot - 1)
        )
        
        await db.commit()
        return {"message": "Hardware rimosso dal nodo", "id_nodo_hw": id_nodo_hw}
    except Exception as e:
        logger.error(f"Errore in hw_nodo_delete: {e}")
        return {"error": str(e)}
