from typing import List, Optional
from modelos.productos import Productos

from database import Database

class ProductoRepository:
    def __init__(self, db: Database):
        self.db = db

    def add(self, producto: Productos):
        conn = self.db.connect()
        try:
            estatus_final = 1 if str(producto.estatus).lower() in ['1', 'true', 'on'] else 0
            with conn.cursor() as cur:
                cur.execute(
                    """
                    CALL sp_gestionProducto (%s,%s, %s, %s, %s, %s,%s, %s, %s)
                    """,
                    (
                        1,  # Acción para agregar
                        producto.nombre,
                        0,  # ID no necesario para agregar
                        producto.descripcion,
                        producto.precio,
                        producto.existencias,
                        estatus_final,
                        producto.unidades,
                        producto.imagen
                    )
                    )
                
            conn.commit()
        finally:
            conn.close()

    def get_by_id(self, producto_id) -> Optional[Productos]:
        conn = self.db.connect()
        try:
            with conn.cursor(dictionary=True) as cur:
                cur.execute("CALL sp_obtenerProductoPorId(%s)", (producto_id,))
                row = cur.fetchone() 
                
                if row:
                    return Productos(
                        producto_id=row["producto_id"],
                        nombre=row["nombre"],
                        descripcion=row["descripcion"],
                        precio=row["precio"],
                        existencias=row["existencias"],
                        estatus=row["estatus"],
                        unidades=row["unidades"],
                        imagen=row["imagen"]
                    )
        finally:
            conn.close()
        return None
    
    def update(self, producto: Productos):
        conn = self.db.connect()
        try:
            estatus_final = 1 if str(producto.estatus).lower() in ['1', 'true', 'on'] else 0
            with conn.cursor() as cur:
                cur.execute(
                    """
                    CALL sp_gestionProducto (%s,%s, %s, %s, %s, %s,%s, %s, %s)
                    """,
                    (
                        2,  # Acción para actualizar
                        producto.nombre,
                        producto.producto_id,
                        producto.descripcion,
                        producto.precio,
                        producto.existencias,
                        estatus_final,
                        producto.unidades,
                        producto.imagen
                    )
                )
            conn.commit()
        finally:
            conn.close()
