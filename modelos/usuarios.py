from dataclasses import dataclass
@dataclass
class Usuario:
    nombre: str
    apellidos:str
    correo:str
    contraseña:str
    nickname:str
    fecha_nacimiento:str
    telefono:str
    direccion:str
    imagen:bytearray