from typing import List
from modelos.venta import Venta
from modelos.detalle_venta import DetalleVenta

class VentaRepository:
    def __init__(self, db):
        self.db = db

    def add(self, venta: Venta, detalles: List[DetalleVenta]):
        conn = self.db.connect()
        cursor = conn.cursor()
        try:
            # 1. Iniciar transaccion para que si un detalle falla, se borre el folio
            conn.start_transaction()

            # 2. Llamar al SP para crear el encabezado y obtener el Folio
            # Usamos variables de sesion de MySQL para capturar el OUT
            cursor.execute("SET @p_folio = 0")
            cursor.execute("CALL sp_crearVenta(%s, %s, @p_folio)", 
                         (venta.caja_numero, venta.usuario_id))
            
            # Recuperamos el folio generado por el SP
            cursor.execute("SELECT @p_folio")
            venta_id = cursor.fetchone()[0]

            # 3. Insertar los detalles usando el SP (que ya resta stock y valida)
            for detalle in detalles:
                cursor.execute("CALL sp_agregarDetalleVenta(%s, %s, %s)", 
                             (venta_id, detalle.producto_id, detalle.cantidad))

            # 4. Si todo salio bien, confirmamos cambios
            conn.commit()
            return venta_id

        except Exception as e:
            # Si el SP lanza un error (como "Stock insuficiente"), hacemos rollback
            conn.rollback()
            print(f"Error en la venta: {e}")
            raise e # Re-lanzamos el error para que el controlador lo atrape
        finally:
            cursor.close()
            conn.close()