from dataclasses import dataclass
class Productos:
    def __init__(
        self,
        nombre,
        descripcion,
        precio,
        existencias,
        estatus,
        unidades,
        imagen,
        producto_id=None
    ):
        self.producto_id = producto_id
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio
        self.existencias = existencias
        self.estatus = estatus
        self.unidades = unidades
        self.imagen = imagen