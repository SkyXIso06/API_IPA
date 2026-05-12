class ReporteRepository:
    def __init__(self, db):
        self.db = db

    def ventas_por_caja(self, caja_id, inicio, fin):
        conn = self.db.connect()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("CALL sp_reporteVentaCaja(%s, %s, %s)", (caja_id, inicio, fin))
        res = cursor.fetchall()
        cursor.close()
        return res

    def ventas_por_producto(self, producto_id, inicio, fin):
        conn = self.db.connect()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("CALL sp_reporteVentaProducto(%s, %s, %s)", (producto_id, inicio, fin))
        res = cursor.fetchall()
        cursor.close()
        return res