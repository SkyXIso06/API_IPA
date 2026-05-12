from dataclasses import dataclass
@dataclass
class Productos:
    producto_id: int
    nombre: str
    descripcion: str
    precio: float
    existencias: int
    estatus: bool
    unidades: str
    imagen: bytearray