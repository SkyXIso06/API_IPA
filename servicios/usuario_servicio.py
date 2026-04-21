from typing import Optional,List
from modelos.usuarios import Usuario
from repositorios.usaurio_repositorio import UsuarioRepository

class UsuarioClass:
    def __init__(self, repo: UsuarioRepository):
        self.repo = repo
        
    def create_usuario(self, data:dict)->Usuario:
        usuario=Usuario(
            nombre=data["nombre"],
            apellidos=data["apellidos"],
            correo=data["correo"],
            contraseña=data["contraseña"],
            nickname=data["nickname"],
            fecha_nacimiento=data["fecha_nacimiento"],
            telefono=data["telefono"],
            direccion=data["direccion"],
            imagen=data["imagen"]
        )
        self.repo.add(usuario)
        return usuario

