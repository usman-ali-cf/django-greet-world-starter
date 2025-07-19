"""
SQLAlchemy version of crea_nodo.py

Automatically creates a default PLC node called "CPU01" and, based on the IO count in t_io
for the given project, inserts the necessary hardware modules into t_hw_nodo using async SQLAlchemy.
"""
import logging
import math
import asyncio
from typing import Dict, Any, Optional, Tuple, List, AsyncGenerator
from sqlalchemy import func, text, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

# Import models and database session
from models.project import Node, HardwareNode
from models.hardware import Hardware, IO
from core.database import AsyncSessionLocal


class PLCConfigurator:
    """Handles the automatic configuration of PLC nodes and hardware modules."""
    
    # Define IO types and their corresponding default hardware and capacity columns
    IO_TYPES = [
        "Input Digitale Fail-Safe",
        "Output Digitale Fail-Safe",
        "Input Digitale",
        "Output Digitale",
        "Input Analogico Corrente",
        "Input Analogico Tensione",
        "Output Analogico Corrente",
        "Output Analogico Tensione"
    ]
    
    DEFAULT_BOARDS = {
        "Input Digitale Fail-Safe": "FDI16",
        "Output Digitale Fail-Safe": "FDO16",
        "Input Digitale": "DI16",
        "Output Digitale": "DO16",
        "Input Analogico Corrente": "AI4 (4-20mA)",
        "Input Analogico Tensione": "AI4 (0-10V)",
        "Output Analogico Corrente": "AO4 (4-20mA)",
        "Output Analogico Tensione": "AO4 (0-10V)"
    }
    
    CAPACITY_COLUMNS = {
        "Input Digitale Fail-Safe": "F-DI",
        "Output Digitale Fail-Safe": "F-DO",
        "Input Digitale": "DI",
        "Output Digitale": "DO",
        "Input Analogico Corrente": "AI",
        "Input Analogico Tensione": "AI",
        "Output Analogico Corrente": "AO",
        "Output Analogico Tensione": "AO"
    }
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.slot_counter = 1
    
    async def get_or_create_plc_node(self, project_id: int) -> Tuple[Node, bool]:
        """
        Get an existing PLC node or create a new one if it doesn't exist.
        
        Args:
            project_id: ID of the project
            
        Returns:
            Tuple of (node, is_new) where is_new is True if the node was just created
        """
        node_name = "CPU01"
        
        # Try to find existing node
        result = await self.db.execute(
            select(Node).where(
                Node.id_prg == project_id,
                Node.nome_nodo == node_name
            )
        )
        node = result.scalars().first()
        
        if node:
            logger.info(f"PLC node {node_name} already exists with ID {node.id_nodo}")
            # Delete existing hardware modules if any
            result = await self.db.execute(
                select(HardwareNode).where(
                    HardwareNode.id_nodo == node.id_nodo
                )
            )
            existing_modules = result.scalars().all()
            
            if existing_modules:
                logger.info(f"Deleting {len(existing_modules)} existing hardware modules")
                for module in existing_modules:
                    await self.db.delete(module)
                await self.db.commit()
                
            return node, False
        else:
            # Create new PLC node
            new_node = Node(
                id_prg=project_id,
                nome_nodo=node_name,
                descrizione="Nodo PLC creato automaticamente",
                tipo_nodo="PLC"
            )
            self.db.add(new_node)
            await self.db.commit()
            await self.db.refresh(new_node)
            logger.info(f"Created new PLC node with ID {new_node.id_nodo}")
            return new_node, True
    
    async def get_io_counts(self, project_id: int) -> Dict[str, int]:
        """
        Get the count of IOs for each IO type in the project.
        
        Args:
            project_id: ID of the project
            
        Returns:
            Dictionary mapping IO types to their counts
        """
        counts = {}
        for io_type in self.IO_TYPES:
            result = await self.db.execute(
                select(func.count(IO.id_io)).where(
                    IO.id_prg == project_id,
                    IO.tipo == io_type
                )
            )
            count = result.scalar()
            counts[io_type] = count or 0
        
        logger.info(f"IO counts by type: {counts}")
        return counts
    
    async def configure_hardware_modules(self, project_id: int, node_id: int) -> int:
        """
        Configure hardware modules based on IO counts.
        
        Args:
            project_id: ID of the project
            node_id: ID of the node to configure
            
        Returns:
            Number of modules configured
        """
        io_counts = await self.get_io_counts(project_id)
        modules_configured = 0
        
        for io_type in self.IO_TYPES:
            count_io = io_counts.get(io_type, 0)
            if count_io <= 0:
                continue
                
            board_name = self.DEFAULT_BOARDS[io_type]
            capacity_col = self.CAPACITY_COLUMNS[io_type]
            
            # Get hardware details
            result = await self.db.execute(
                select(Hardware).where(Hardware.nome_hw == board_name)
            )
            hardware = result.scalars().first()
            
            if not hardware:
                logger.warning(f"Default board {board_name} not found for {io_type}")
                continue
                
            # Get capacity using raw SQL since the column name might contain special characters
            result = await self.db.execute(
                text(f'SELECT "{capacity_col}" FROM t_cat_hw WHERE id_hw = :id_hw'),
                {"id_hw": hardware.id_hw}
            )
            capacity = result.scalar()
            
            if not capacity or capacity <= 0:
                logger.warning(f"Invalid capacity for {board_name}")
                continue
                
            num_modules = math.ceil(count_io / capacity)
            logger.info(
                f"→ {io_type}: {count_io} IOs → {num_modules} modules "
                f"({capacity} per module)"
            )
            
            # Add hardware modules
            for _ in range(num_modules):
                module = HardwareNode(
                    id_nodo=node_id,
                    id_hw=hardware.id_hw,
                    slot=self.slot_counter,
                    quantita=1
                )
                self.db.add(module)
                self.slot_counter += 1
                modules_configured += 1
        
        await self.db.commit()
        return modules_configured


async def crea_nodo_plc_automatico(project_id: int) -> Dict[str, Any]:
    """
    Automatically create a PLC node and configure hardware modules based on IO requirements.
    """
    async with AsyncSessionLocal() as db:
        try:
            configurator = PLCConfigurator(db)

            node, is_new = await configurator.get_or_create_plc_node(project_id)
            modules_configured = await configurator.configure_hardware_modules(project_id, node.id_nodo)

            message = (
                f"PLC node created successfully: "
                f"{'created' if is_new else 'updated'} "
                f"and {modules_configured} hardware modules configured."
            )

            return {
                "success": True,
                "message": message,
                "node_id": node,
                "modules_configured": modules_configured,
                "is_new": is_new
            }

        except SQLAlchemyError as e:
            await db.rollback()
            logger.error(f"Error in automatic PLC node creation: {e}")
            return {
                "success": False,
                "message": f"Error: {str(e)}"
            }
        except Exception as e:
            await db.rollback()
            logger.error(f"Unexpected error in automatic PLC node creation: {e}")
            return {
                "success": False,
                "message": f"Unexpected error: {str(e)}"
            }


async def main():
    import sys
    if len(sys.argv) > 1:
        project_id = int(sys.argv[1])
        # Create a new database session for standalone execution
        async with AsyncSessionLocal() as db:
            result = await crea_nodo_plc_automatico(project_id, db)
            print(result)
    else:
        print("Usage: python crea_nodo_alchemy.py <project_id>")
        sys.exit(1)

# For backward compatibility
if __name__ == "__main__":
    asyncio.run(main())
