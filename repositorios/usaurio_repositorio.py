from typing import List, Optional
from modelos.usuarios import Usuario

from database import Database

class UsuarioRepository:
    def __init__(self, db: Database):
        self.db = db

    def add(self,usuario: Usuario ):
        conn = self.db.connect()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    CALL sp_registrarUsuario (%s,%s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
                        usuario.nombre,
                        usuario.apellidos,
                        usuario.correo,
                        usuario.contraseña,
                        usuario.nickname,
                        usuario.fecha_nacimiento,
                        usuario.telefono,
                        usuario.direccion,
                        usuario.imagen
                    )
                    )
                
            conn.commit()
        finally:
            conn.close()


    def login(self, correo, password) -> Optional[Usuario]:
        conn = self.db.connect()
        try:
           
            with conn.cursor(dictionary=True) as cur:
                cur.execute("CALL sp_Login(%s, %s)", (correo, password))
                row = cur.fetchone() 
                
                if row:
                    return Usuario(
                        nombre=row["nombre"],
                        apellidos=row["apellidos"],
                        correo=row["correo"],
                        contraseña=row["contraseña"],
                        nickname=row["nickname"],
                        fecha_nacimiento=row["fecha_nacimiento"],
                        telefono=row["telefono"],
                        direccion=row["direccion"],
                        imagen=row["imagen"]
                    )
        finally:
            conn.close()
        return None