from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from servicios.usuario_servicio import UsuarioClass
from repositorios.usaurio_repositorio import UsuarioRepository
from database import Database

auth_bp = Blueprint("auth", __name__)
db = Database()
service = UsuarioClass(UsuarioRepository(db))

@auth_bp.post("/login")
def login():
    usuario=request.form.to_dict()
    correo = usuario.get("correo")
    password = usuario.get("contraseña")
    
    if not correo or not password:
        return jsonify({"error": "Correo y contraseña son requeridos"}), 400

  
    usuario = service.login_usuario(correo, password)

    if usuario:
    
        token = create_access_token(identity=usuario.correo)
        
        
        return jsonify({
            "token": token,
            "usuario": {
                "nickname": usuario.nickname,
                "correo": usuario.correo
            }
        }), 200
    
    return jsonify({"error": "Credenciales incorrectas"}), 401