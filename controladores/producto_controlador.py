
from flask import Blueprint, jsonify, request
from servicios.producto_servicio import ProductoClass as ProductoService
from repositorios.productos_repositorio import ProductoRepository
from database import Database
from flask_jwt_extended import jwt_required
import base64

producto_bp = Blueprint("products", __name__)
db = Database()
service = ProductoService(ProductoRepository(db))


@producto_bp.post("/")
@jwt_required()
def crear():
    try:
        # 1. Validar que vengan datos en el Form
        if not request.form:
            return jsonify({"error": "No se enviaron datos del producto"}), 400
            
        producto = request.form.to_dict()
        
        # 2. Validacion de campos obligatorios 
        campos_obligatorios = ["nombre", "descripcion", "precio", "existencias", "unidades"]
        for campo in campos_obligatorios:
            if campo not in producto or not producto[campo]:
                return jsonify({"error": f"El campo {campo} es obligatorio"}), 400

        # 3. Validacion de tipos de datos (Numeros positivos)
        try:
            if float(producto["precio"]) <= 0:
                return jsonify({"error": "El precio debe ser mayor a cero"}), 400
            if int(producto["existencias"]) < 0:
                return jsonify({"error": "Las existencias no pueden ser negativas"}), 400
        except ValueError:
            return jsonify({"error": "Precio o Existencias tienen un formato invalido"}), 400

        foto = request.files.get("imagen")
        if foto:
            producto["imagen"] = foto.read()
        
        producto_creado = service.create_producto(producto)
        data_resp = producto_creado.__dict__.copy()
      
        if data_resp.get("imagen"):
            data_resp["imagen"] = base64.b64encode(data_resp["imagen"]).decode("utf-8")

        return jsonify(data_resp), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@producto_bp.get("/<int:producto_id>")
@jwt_required()
def obtener(producto_id):
    try:
        # Validacion del ID
        if producto_id <= 0:
            return jsonify({"error": "El ID del producto debe ser un numero positivo"}), 400

        producto = service.get_producto(producto_id)
        if not producto:
            return jsonify({"error": "Producto no encontrado"}), 404

        data_resp = producto.__dict__.copy()
        if data_resp.get("imagen"):
            data_resp["imagen"] = base64.b64encode(data_resp["imagen"]).decode("utf-8")

        return jsonify(data_resp), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    


@producto_bp.put("/<int:producto_id>")
@jwt_required()
def actualizar(producto_id):
    try:
        # 1. Validar existencia
        producto_existente = service.get_producto(producto_id)
        if not producto_existente:
            return jsonify({"error": "Producto no encontrado"}), 404

        # 2. Leer datos 
        data = request.form.to_dict()
        foto = request.files.get("imagen")

        if foto:
            data["imagen"] = foto.read()

        # 3. Validaciones 
        if "precio" in data and float(data["precio"]) <= 0:
            return jsonify({"error": "El precio debe ser mayor a cero"}), 400

        # 4. Actualizar
        producto_actualizado = service.update_producto(producto_id, data)
        
        # 5. Respuesta 
        resp = producto_actualizado.__dict__.copy()
        if resp.get("imagen"):
            resp["imagen"] = base64.b64encode(resp["imagen"]).decode("utf-8")

        return jsonify(resp), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400