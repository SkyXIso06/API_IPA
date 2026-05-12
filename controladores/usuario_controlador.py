from flask import Blueprint, jsonify, request
from servicios.usuario_servicio import UsuarioClass as UsuarioService
from repositorios.usaurio_repositorio import UsuarioRepository
from database import Database
from flask_jwt_extended import jwt_required
import base64
usuario_bp = Blueprint("students", __name__)
db = Database()
service = UsuarioService(UsuarioRepository(db))
import re
import datetime

@usuario_bp.post("/")
def crear():
    try:
        if not request.form:
            return jsonify({"error": "No se enviaron datos del usuario"}), 400

        usuario = request.form.to_dict()

        # Array de campos obligatorios 
        campos_obligatorios = [
            "nombre", 
            "apellidos", 
            "correo", 
            "contraseña", 
            "nickname", 
            "fecha_nacimiento"
        ]
        regla_password = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$"
        # 1. Validacion de presencia
        for campo in campos_obligatorios:
            if campo not in usuario or not usuario[campo].strip():
                return jsonify({"error": f"El campo {campo} es obligatorio"}), 400

        if "@" not in usuario["correo"]:
            return jsonify({"error": "El formato del correo es invalido"}), 400
        
        # 2. Validacion de mayor de edad
        try:
            # Extraemos el año de nacimiento
            anio_nacimiento = datetime.datetime.strptime(usuario["fecha_nacimiento"], "%Y-%m-%d").year
            anio_actual = datetime.datetime.now().year
            
            # Calculo 
            if (anio_actual - anio_nacimiento) < 18:
                return jsonify({"error": "El usuario debe ser mayor de edad"}), 400
        except ValueError:
            return jsonify({"error": "El formato de la fecha de nacimiento es invalido"}), 400
        

        # 3. Validacion de formato de contraseña
        if not re.match(regla_password, usuario["contraseña"]):
            return jsonify({"error": "La contraseña no cumple con los requisitos de seguridad"}), 400

        # 4.Manejo de la imagen
        foto = request.files.get("imagen")
        if foto:
            usuario["imagen"] = foto.read()

        #5. Llamada al servicio
        usuario_creado = service.create_usuario(usuario)

        # 6.Respuesta
        data_resp = usuario_creado.__dict__.copy()
        if data_resp.get("imagen"):
            data_resp["imagen"] = base64.b64encode(data_resp["imagen"]).decode("utf-8")

        return jsonify(data_resp), 201

    except Exception as e:
        # Si el error es por el UNIQUE del correo en la base de datos
        if "Duplicate entry" in str(e):
            return jsonify({"error": "El correo ya esta registrado"}), 400
        return jsonify({"error": str(e)}), 400