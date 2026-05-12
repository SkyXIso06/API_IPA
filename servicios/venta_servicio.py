from typing import List
from modelos.venta import Venta
from modelos.detalle_venta import DetalleVenta
from repositorios.venta_repositorio import VentaRepository

class VentaClass:
    def __init__(self, repo: VentaRepository):
        self.repo = repo
        
    def create_venta(self, venta_data: dict, detalles_data: List[dict]) -> int:
        # 1. Instanciamos Venta y asignamos atributos manualmente
        venta = Venta()
        venta.caja_numero = venta_data["caja_numero"]
        venta.usuario_id = venta_data["usuario_correo"] # Este valor viene del token, no del cliente
        
        detalles = []
        # 2. Procesamos la lista de productos
        for item in detalles_data:
            detalle = DetalleVenta()
            detalle.producto_id = item["producto_id"]
            detalle.cantidad = item["cantidad"]
            
            
            detalles.append(detalle)
        
        # 3. Mandamos al repositorio y retornamos el folio (ticket)
        try:
            venta_id = self.repo.add(venta, detalles)
            return venta_id
        except Exception as e:
            raise e