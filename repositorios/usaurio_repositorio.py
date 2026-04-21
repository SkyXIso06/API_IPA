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