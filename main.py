from flask import Flask, jsonify, request
from controladores.usuario_controlador import usuario_bp
from controladores.producto_controlador import producto_bp
from controladores.venta_controlador import venta_bp
from controladores.reporte_controlador import reporte_bp
import mysql.connector as mc
from flask_jwt_extended import JWTManager
from controladores.auth_controlador import auth_bp
app = Flask(__name__)
app.config["JWT_SECRET_KEY"]="123456789"
jwt=JWTManager(app)
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(usuario_bp, url_prefix="/usuario")
app.register_blueprint(producto_bp, url_prefix="/producto")
app.register_blueprint(venta_bp, url_prefix="/venta")
app.register_blueprint(reporte_bp, url_prefix="/reporte")


#Rutas
if __name__ == "__main__":
    app.run(debug=True)