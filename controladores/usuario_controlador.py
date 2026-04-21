from flask import Blueprint, jsonify, request
from servicios.usuario_servicio import UsuarioClass as UsuarioService
from repositorios.usaurio_repositorio import UsuarioRepository
from database import Database
from flask_jwt_extended import jwt_required
import base64
usuario_bp = Blueprint("students", __name__)
db = Database()
service = UsuarioService(UsuarioRepository(db))

@usuario_bp.post("/")
def crear():
    try:
        usuario=request.form.to_dict()
        foto=request.files.get("imagen")
        if foto:
            usuario["imagen"]=foto.read()
        usuario = service.create_usuario(usuario)

        data_resp = usuario.__dict__.copy()
      
        if data_resp.get("imagen"):
            data_resp["imagen"] = base64.b64encode(data_resp["imagen"]).decode("utf-8")

        return jsonify(data_resp), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
