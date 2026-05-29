from typing import Optional,List
from modelos.productos import Productos
from repositorios.productos_repositorio import ProductoRepository

class ProductoClass:
    def __init__(self, repo: ProductoRepository):
        self.repo = repo
        
    def create_producto(self, data:dict)->Productos:
        producto=Productos(
            nombre=data["nombre"],
            descripcion=data["descripcion"],
            precio=data["precio"],
            existencias=data["existencias"],
            estatus=data["estatus"],
            unidades=data["unidades"],
            imagen=data["imagen"]
        )
        producto.producto_id = self.repo.add(producto)

        return producto
    
    def get_producto(self, producto_id) -> Optional[Productos]:
        return self.repo.get_by_id(producto_id)
    
    
    
    def update_producto(self, producto_id:int, data:dict) -> Optional[Productos]:
        producto = self.repo.get_by_id(producto_id)
        if not producto:
            return None
        for key, value in data.items():
            if hasattr(producto, key):
             setattr(producto, key, value)

        self.repo.update(producto)
        producto = self.repo.get_by_id(producto_id)  # Obtener el producto actualizado
        return producto
    
    
   

