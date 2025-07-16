"""
SQLAlchemy version of carica_file_utenze_mock.py

• Reads the Excel file
• Inserts rows into t_utenza and (if potenza>0) t_potenza using SQLAlchemy
• NO avviamento, NO PLC creation, NO IO auto-assign
"""
import os
import logging
import pandas as pd
from typing import Dict, Any, Tuple
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

# Required columns in the Excel file
REQUIRED_COLUMNS = [
    "nome_utenza", "descrizione", "tensione", "zona",
    "DI", "DO", "AI", "AO", "FDI", "FDO", "potenza"
]

# Import models and database session
from models.utility import Utenza, Potenza
from models.project import Project
from core.database import SessionLocal


def get_db() -> Session:
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def load_excel_file(path: str) -> pd.DataFrame:
    """
    Load and validate the Excel file.
    
    Args:
        path: Path to the Excel file
        
    Returns:
        DataFrame containing the loaded data or an empty DataFrame if there's an error
    """
    if not os.path.exists(path):
        logger.error("Excel file not found: %s", path)
        return pd.DataFrame()

    try:
        # Read the Excel file
        df = pd.read_excel(path, sheet_name="FoglioUtenze")
        
        # Check for missing columns
        missing_columns = [col for col in REQUIRED_COLUMNS if col not in df.columns]
        if missing_columns:
            logger.error("Missing required columns: %s", missing_columns)
            return pd.DataFrame()
            
        return df
        
    except Exception as e:
        logger.error("Error reading Excel file: %s", str(e), exc_info=True)
        return pd.DataFrame()


def get_category(row: pd.Series) -> str:
    """
    Determine the category based on the 'potenza' value.
    
    Args:
        row: DataFrame row containing the data
        
    Returns:
        'potenza' if potenza > 0, otherwise 'utenza'
    """
    return "potenza" if (pd.notna(row["potenza"]) and row["potenza"] > 0) else "utenza"


def check_existing_utilities(db: Session, project_id: int) -> bool:
    """
    Check if utilities exist for the given project.
    
    Args:
        db: Database session
        project_id: Project ID to check
        
    Returns:
        True if utilities exist, False otherwise
    """
    return db.query(Utenza).filter(Utenza.id_prg == project_id).count() > 0


def delete_existing_utilities(db: Session, project_id: int) -> None:
    """
    Delete all utilities and power entries for the given project.
    
    Note: Due to the cascade relationship, deleting Utenza will also delete related Potenza entries.
    
    Args:
        db: Database session
        project_id: Project ID to delete utilities for
    """
    try:
        # Delete all utilities for the project
        db.query(Utenza).filter(Utenza.id_prg == project_id).delete()
        db.commit()
        logger.info("Deleted utilities for project %s", project_id)
        
    except SQLAlchemyError as e:
        db.rollback()
        logger.error("Error deleting utilities: %s", str(e), exc_info=True)
        raise


def insert_utilities(db: Session, df: pd.DataFrame, project_id: int) -> int:
    """
    Insert utilities and power entries into the database.
    
    Args:
        db: Database session
        df: DataFrame containing the utility data
        project_id: Project ID to associate with the utilities
        
    Returns:
        Number of utilities inserted, or 0 if there was an error
    """
    inserted = 0
    
    try:
        # Verify project exists
        project = db.query(Project).filter(Project.id_prg == project_id).first()
        if not project:
            logger.error("Project with ID %s not found", project_id)
            return 0
        
        for _, row in df.iterrows():
            # Create new utility
            utility = Utenza(
                id_prg=project_id,
                nome_utenza=row["nome_utenza"],
                descrizione=row["descrizione"],
                categoria=row["categoria"],
                tensione=row["tensione"],
                zona=row["zona"],
                DI=row["DI"],
                DO=row["DO"],
                AI=row["AI"],
                AO=row["AO"],
                FDI=row["FDI"],
                FDO=row["FDO"],
                potenza=row["potenza"]
            )
            
            db.add(utility)
            db.flush()  # Flush to get the ID
            
            # If it's a power utility, create a power entry
            if row["categoria"] == "potenza" and row["potenza"] > 0:
                power = Potenza(
                    id_prg=project_id,
                    id_utenza=utility.id_utenza,
                    nome=row["nome_utenza"],
                    potenza=row["potenza"],
                    tensione=row["tensione"],
                    descrizione=row["descrizione"],
                    zona=row["zona"]
                )
                db.add(power)
            
            inserted += 1
        
        db.commit()
        logger.info("Inserted %d utilities for project %s", inserted, project_id)
        return inserted
        
    except SQLAlchemyError as e:
        db.rollback()
        logger.error("Error inserting utilities: %s", str(e), exc_info=True)
        return 0


def process_excel_file(project_id: int, file_path: str) -> Dict[str, Any]:
    """
    Process the Excel file and import utilities into the database.
    
    Args:
        project_id: Project ID to associate the utilities with
        file_path: Path to the Excel file
        
    Returns:
        Dictionary containing the result of the operation
    """
    db = next(get_db())
    
    try:
        # Check if file exists
        if not os.path.exists(file_path):
            return {"success": False, "message": f"File not found: {file_path}"}
        
        # Load and validate Excel file
        df = load_excel_file(file_path)
        if df.empty:
            return {"success": False, "message": "Invalid or empty Excel file"}
        
        # Add category column
        df["categoria"] = df.apply(get_category, axis=1)
        
        # Check for existing utilities
        if check_existing_utilities(db, project_id):
            delete_existing_utilities(db, project_id)
        
        # Insert utilities
        count = insert_utilities(db, df, project_id)
        
        if count == 0:
            return {"success": False, "message": "No utilities were imported"}
            
        return {
            "success": True,
            "message": f"Successfully imported {count} utilities",
            "count": count
        }
        
    except Exception as e:
        logger.error("Error processing Excel file: %s", str(e), exc_info=True)
        return {"success": False, "message": f"Error processing file: {str(e)}"}
    finally:
        db.close()


def validate_uploaded_file(file_storage) -> Tuple[bool, str]:
    """
    Validate the uploaded file.
    
    Args:
        file_storage: FileStorage object from the request
        
    Returns:
        Tuple of (is_valid, message)
    """
    if not file_storage or not file_storage.filename:
        return False, "No file selected"
        
    if not file_storage.filename.lower().endswith((".xlsx", ".xls", ".xlsm")):
        return False, "Unsupported file format. Please upload an Excel file"
        
    return True, "OK"


# For backward compatibility with existing code
_process_excel_and_autoflow = process_excel_file
verifica_file_caricato = validate_uploaded_file
