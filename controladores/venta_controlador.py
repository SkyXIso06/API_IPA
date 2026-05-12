from flask import Blueprint, jsonify, request
from repositorios.venta_repositorio import VentaRepository
from servicios.venta_servicio import VentaClass as VentaService
from database import Database
from flask_jwt_extended import jwt_required, get_jwt_identity

venta_bp = Blueprint("sales", __name__)
db = Database()
service = VentaService(VentaRepository(db))

@venta_bp.post("/")
@jwt_required()
def post_venta():
    try:
        data = request.get_json()
        
        # Validacion basica de entrada
        if not data or "caja_numero" not in data or "productos" not in data:
            return jsonify({"error": "Datos incompletos (caja_numero o productos faltantes)"}), 400

        # usuario_correo viene del token de sesion
        venta_data = {
            "caja_numero": data["caja_numero"],
            "usuario_correo": get_jwt_identity() 
        }
        
        # detalles_data es la lista de productos
        detalles_data = data["productos"] 
        
        # Llamada al servicio
        folio = service.create_venta(venta_data, detalles_data)
        
        # Respuesta exitosa (201 Created)
        return jsonify({
            "mensaje": "Venta registrada con exito",
            "ticket": folio
        }), 201

    except Exception as e:
        
        return jsonify({
            "error": str(e),
            "mensaje": "No se pudo completar la venta"
        }), 400