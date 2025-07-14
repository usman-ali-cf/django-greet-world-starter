"""
Hardware management service
"""
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, text, delete
from models.hardware import Hardware
from models.project import HardwareNode
from schemas.hardware import HardwareResponse, HardwareNodeCreate, HardwareNodeResponse
import logging

logger = logging.getLogger(__name__)


class HardwareService:
    """Service for handling hardware-related business logic"""
    
    async def get_hardware_catalog(self, db: AsyncSession, tipo: Optional[str] = None) -> List[HardwareResponse]:
        """Get hardware catalog with optional filtering by type"""
        try:
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
            params = {}
            
            if tipo:
                query += " AND tipo = :tipo"
                params["tipo"] = tipo
                
            query += " ORDER BY tipo, descrizione_hw"
            
            result = await db.execute(text(query), params)
            rows = result.fetchall()
            
            hardware_items = []
            for row in rows:
                item_dict = dict(row._mapping)
                # Ensure all fields have default values
                hardware_items.append(HardwareResponse(
                    id_hw=item_dict['id_hw'],
                    nome_hw=item_dict['nome_hw'] or '',
                    descrizione_hw=item_dict['descrizione_hw'] or '',
                    tipo=item_dict['tipo'] or '',
                    DI=item_dict['DI'] or 0,
                    DO=item_dict['DO'] or 0,
                    AI=item_dict['AI'] or 0,
                    AO=item_dict['AO'] or 0,
                    F_DI=item_dict['F_DI'] or 0,
                    F_DO=item_dict['F_DO'] or 0,
                    Ox=float(item_dict['Ox'] or 0.0),
                    Oy=float(item_dict['Oy'] or 0.0),
                    L=float(item_dict['L'] or 0.0),
                    H=float(item_dict['H'] or 0.0),
                    blocco_grafico=item_dict['blocco_grafico']
                ))
            
            return hardware_items
        except Exception as e:
            logger.error(f"Error getting hardware catalog: {e}")
            raise
    
    async def get_node_hardware(self, db: AsyncSession, node_id: int) -> List[HardwareNodeResponse]:
        """Get hardware assigned to a node"""
        try:
            query = """
                SELECT 
                    nh.id_nodo_hw,
                    nh.id_nodo,
                    nh.id_hw,
                    nh.slot,
                    nh.quantita,
                    h.nome_hw,
                    h.tipo,
                    h.DI,
                    h.DO
                FROM t_nodo_hw nh
                JOIN t_cat_hw h ON nh.id_hw = h.id_hw
                WHERE nh.id_nodo = :node_id
                ORDER BY nh.slot
            """
            
            result = await db.execute(text(query), {"node_id": node_id})
            rows = result.fetchall()
            
            hardware_nodes = []
            for row in rows:
                row_dict = dict(row._mapping)
                hardware_nodes.append(HardwareNodeResponse(**row_dict))
            
            return hardware_nodes
        except Exception as e:
            logger.error(f"Error getting node hardware: {e}")
            raise
    
    async def add_hardware_to_node(self, db: AsyncSession, hardware_data: HardwareNodeCreate) -> HardwareNodeResponse:
        """Add hardware to a node"""
        try:
            # Get next available slot if not specified
            if hardware_data.slot is None:
                slot_result = await db.execute(
                    text("SELECT COALESCE(MAX(slot), 0) + 1 as next_slot FROM t_nodo_hw WHERE id_nodo = :node_id"),
                    {"node_id": hardware_data.id_nodo}
                )
                next_slot = slot_result.scalar()
            else:
                next_slot = hardware_data.slot
            
            # Insert hardware node
            await db.execute(
                text("""
                    INSERT INTO t_nodo_hw (id_nodo, id_hw, slot, quantita)
                    VALUES (:id_nodo, :id_hw, :slot, :quantita)
                """),
                {
                    "id_nodo": hardware_data.id_nodo,
                    "id_hw": hardware_data.id_hw,
                    "slot": next_slot,
                    "quantita": hardware_data.quantita
                }
            )
            await db.commit()
            
            # Get the created hardware node
            result = await db.execute(
                text("""
                    SELECT 
                        nh.id_nodo_hw,
                        nh.id_nodo,
                        nh.id_hw,
                        nh.slot,
                        nh.quantita,
                        h.nome_hw,
                        h.tipo,
                        h.DI,
                        h.DO
                    FROM t_nodo_hw nh
                    JOIN t_cat_hw h ON nh.id_hw = h.id_hw
                    WHERE nh.id_nodo = :id_nodo AND nh.slot = :slot
                """),
                {"id_nodo": hardware_data.id_nodo, "slot": next_slot}
            )
            row = result.fetchone()
            
            if row:
                row_dict = dict(row._mapping)
                return HardwareNodeResponse(**row_dict)
            else:
                raise Exception("Failed to retrieve created hardware node")
                
        except Exception as e:
            logger.error(f"Error adding hardware to node: {e}")
            await db.rollback()
            raise
    
    async def remove_hardware_from_node(self, db: AsyncSession, hardware_node_id: int) -> bool:
        """Remove hardware from a node"""
        try:
            result = await db.execute(
                text("DELETE FROM t_nodo_hw WHERE id_nodo_hw = :id"),
                {"id": hardware_node_id}
            )
            await db.commit()
            
            return result.rowcount > 0
        except Exception as e:
            logger.error(f"Error removing hardware from node: {e}")
            await db.rollback()
            raise