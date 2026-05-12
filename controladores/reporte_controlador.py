from flask import Blueprint, jsonify, request
from repositorios.reportes_repositorio import ReporteRepository
from servicios.producto_servicio import ProductoClass as service_producto
from database import Database
from flask_jwt_extended import jwt_required
import base64

reporte_bp = Blueprint("reports", __name__)
db = Database()
repo = ReporteRepository(db)

@reporte_bp.get("/caja")
@jwt_required()
def get_reporte_caja():
    # 1.Extraemos los datos del Form Data
    caja_id = request.args.get("caja")
    fecha_inicio = request.args.get("inicio")
    fecha_fin = request.args.get("fin")
    #2. Validacion de parametros
    if not all([caja_id, fecha_inicio, fecha_fin]):
        return jsonify({"error": "Faltan parametros (caja, inicio, fin)"}), 400
    
    # 3. Validacion de tipos de datos
    try:
        caja_id = int(caja_id) # Validar que la caja sea un numero
    except ValueError:
        return jsonify({"error": "El ID de caja debe ser un numero entero"}), 400

    # 4. Validacion de logica   
    if fecha_inicio > fecha_fin:
        return jsonify({"error": "La fecha de inicio no puede ser mayor a la de fin"}), 400
    
    resultado =repo.ventas_por_caja(caja_id, fecha_inicio, fecha_fin)
    if resultado is None or len(resultado) == 0:
        return jsonify({"error": "No se encontraron datos para la caja especificada"}), 404
    return jsonify(resultado), 200

@reporte_bp.get("/producto")
@jwt_required()
def get_reporte_producto():
   
    producto_id = request.args.get("producto_id")
    fecha_inicio = request.args.get("inicio")
    fecha_fin = request.args.get("fin")
    
    if not all([producto_id, fecha_inicio, fecha_fin]):
        return jsonify({"error": "Faltan parametros (producto, inicio, fin)"}), 400
    try:
        producto_id = int(producto_id) 
    except ValueError:
        return jsonify({"error": "El ID de producto debe ser un numero entero"}), 400
    
    producto = service_producto.get_producto(producto_id) 
    if not producto:
        return jsonify({"error": f"El producto con ID {producto_id} no existe en el catalogo"}), 404
    
    if fecha_inicio > fecha_fin:
        return jsonify({"error": "La fecha de inicio no puede ser mayor a la de fin"}), 400
    
    resultado = repo.ventas_por_producto(producto_id, fecha_inicio, fecha_fin)
    if resultado is None or len(resultado) == 0:
        return jsonify({"error": "No se encontraron datos para el producto especificado"}), 404
    return jsonify(resultado), 200