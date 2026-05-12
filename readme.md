# Documentación API - Sistema de Ventas

**Base URL:** `http://localhost:5000`

**Versión:** 1.0.0

**Autor:** Eduardo Vanoye Chi, Mauricio Jiménez de León

---

## Autenticación

La API utiliza **JWT (JSON Web Tokens)** para proteger los endpoints.

- **Secret Key:** `123456789` (configurada en `main.py`)

### Endpoints públicos (sin token):
- `POST /auth/login`
- `POST /usuario/` (registro)

### Endpoints protegidos (requieren token):
- Productos, ventas y reportes.

### Cómo enviar el token:

```http
Authorization: Bearer <token_jwt> ```

1) Login

Ruta: POST /auth/login
Descripción: Autentica al usuario y genera un token JWT.
Autorización: ❌ No requiere

Parámetros

Campo|	Tipo|	Requerido|	Descripción|	Ejemplo
correo|	string|	✅|	Correo registrado|	luis@mail.com
contraseña|	string|	✅|	Contraseña del usuario|	Pass1234

Ejemplo de Request (JSON)

{
  "correo": "luis@mail.com",
  "contraseña": "Pass1234"
}

Responses

Código|	Descripción|	Ejemplo
200|	Login exitoso|	{"token": "eyJ...", "usuario": {"nickname": "luismtz", "correo": "luis@mail.com"}}
400|	Faltan campos|	{"error": "Correo y contraseña son requeridos"}
401|	Credenciales incorrectas|	{"error": "Credenciales incorrectas"}

Errores comunes

Error|	Causa|	Solución
"Correo y contraseña son requeridos"|	No se enviaron ambos campos|	Enviar correo y contraseña en el Form Data
"Credenciales incorrectas"|	Correo o contraseña no coinciden|	Verificar credenciales en la BD

Notas / Validaciones:
El controlador usa request.form.to_dict(), no JSON.
La identidad del token es el correo del usuario.
El SP subyacente es sp_Login.

Ejemplo curl

curl -X POST http://localhost:5000/auth/login \
  -d "correo=luis@mail.com" \
  -d "contraseña=Pass1234"

2) Registrar usuario

Ruta: POST /usuario/
Descripción: Crea una nueva cuenta de usuario con validaciones de seguridad.
Autorización: ❌ No requiere

Parámetros

Campo|	Tipo|	Requerido|	Descripción|	Ejemplo
nombre|	string|	✅|	Nombre(s)|	Luis
apellidos|	string|	✅|	Apellidos|	Martínez López
correo|	string|	✅|	Correo único|	luis@mail.com
contraseña|	string|	✅|	Mín 8 carac, 1 mayús, 1 minús, 1 núm|	Pass1234
nickname|	string|	✅|	Nombre de usuario|	luismtz
fecha_nacimiento|	string|	✅|	Formato YYYY-MM-DD|	2000-05-15
telefono|	string|	❌|	Teléfono 10 dígitos|	8123456789
direccion|	string|	❌|	Dirección|	Calle 123
imagen|	file|	❌|	Imagen (campo de formulario)|	foto.jpg

Ejemplo de Request (JSON)

{
  "nombre": "Luis",
  "apellidos": "Martínez",
  "correo": "luis@mail.com",
  "contraseña": "Pass1234",
  "nickname": "luismtz",
  "fecha_nacimiento": "2000-05-15",
  "telefono": "8123456789",
  "direccion": "Calle 123"
}

Responses

Código|	Descripción|	Ejemplo
201|	Usuario registrado|	{"nombre": "Luis", "apellidos": "Martínez", "correo": "luis@mail.com", ...}
400|	Error de validación|	{"error": "La contraseña no cumple con los requisitos de seguridad"}
400|	Correo duplicado|	{"error": "El correo ya esta registrado"}
400|	Menor de edad|	{"error": "El usuario debe ser mayor de edad"}

Errores comunes

Error|	Causa|	Solución
"El campo X es obligatorio"|	Falta un campo requerido|	Enviar todos los campos obligatorios
"La contraseña no cumple..."|	Contraseña débil|	8+ caracteres con mayúscula, minúscula y número
"El correo ya esta registrado"|	Correo duplicado en BD|	Usar otro correo
"El usuario debe ser mayor de edad"|	Fecha reciente|	Usar fecha con 18+ años de antigüedad

Notas / Validaciones:
Regex contraseña: ^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$
Mayoría de edad: Se calcula con el año de nacimiento (≥ 18 años).
Formato correo: Debe contener @.
El SP subyacente es sp_registrarUsuario.
La imagen se almacena como MEDIUMBLOB.

Ejemplo curl

curl -X POST http://localhost:5000/usuario/ \
  -d "nombre=Luis" \
  -d "apellidos=Martínez" \
  -d "correo=luis@mail.com" \
  -d "contraseña=Pass1234" \
  -d "nickname=luismtz" \
  -d "fecha_nacimiento=2000-05-15"

3) Crear producto

Ruta: POST /producto/
Descripción: Agrega un nuevo producto al catálogo.
Autorización: ✅ Bearer <token>

Parámetros

Campo|	Tipo|	Requerido|	Descripción|	Ejemplo
nombre|	string|	✅|	Nombre del producto|	Coca-Cola
descripcion|	string|	✅|	Descripción detallada|	Refresco 600ml
precio|	decimal|	✅|	Precio unitario (>0)|	25.50
existencias|	int|	✅|	Cantidad en stock (≥0)|	100
unidades|	string|	✅|	Tipo de unidad|	pza
estatus|	bit|	❌|	1=Activo, 0=Inactivo|	1
imagen|	file|	❌|	Imagen del producto|	producto.jpg

Ejemplo de Request (JSON)

{
  "nombre": "Coca-Cola",
  "descripcion": "Refresco 600ml",
  "precio": 25.50,
  "existencias": 100,
  "unidades": "pza",
  "estatus": 1
}

Responses

Código|	Descripción|	Ejemplo
201|	Producto creado|	{"producto_id": 1, "nombre": "Coca-Cola", "precio": 25.50, ...}
400|	Faltan campos|	{"error": "El campo nombre es obligatorio"}
400|	Precio inválido|	{"error": "El precio debe ser mayor a cero"}
400|	Existencias negativas|	{"error": "Las existencias no pueden ser negativas"}

Errores comunes

Error|	Causa|	Solución
"No se enviaron datos del producto"|	Request sin Form Data|	Enviar campos en el body
"El campo X es obligatorio"|	Falta campo requerido|	Incluir nombre, descripcion, precio, existencias, unidades
"Precio o Existencias tienen un formato invalido"|	Texto en campo numérico|	Enviar números válidos

Notas / Validaciones:
precio debe ser > 0.
existencias no pueden ser negativas.
Usa el SP sp_gestionProducto con opcion=1.
estatus se convierte: '1', 'true', 'on' → 1, resto → 0.

Ejemplo curl

curl -X POST http://localhost:5000/producto/ \
  -H "Authorization: Bearer <token>" \
  -d "nombre=Coca-Cola" \
  -d "descripcion=Refresco 600ml" \
  -d "precio=25.50" \
  -d "existencias=100" \
  -d "unidades=pza"

4) Obtener producto por ID

Ruta: GET /producto/{producto_id}
Descripción: Devuelve la información detallada de un producto.
Autorización: ✅ Bearer <token>

Parámetros

Campo|	Tipo|	Requerido|	Descripción
producto_id|	int|	✅|	ID del producto (>0)

Ejemplo de Request (JSON)

{
  "producto_id": 1
}

Responses

Código|	Descripción|	Ejemplo
200|	Producto encontrado|	{"producto_id": 1, "nombre": "Coca-Cola", "precio": 25.50, ...}
400|	ID inválido|	{"error": "El ID del producto debe ser un numero positivo"}
404|	No encontrado|	{"error": "Producto no encontrado"}

Errores comunes

Error|	Causa|	Solución
"El ID del producto debe ser un numero positivo"|	Se envió producto_id ≤ 0|	Usar un ID mayor a 0
"Producto no encontrado"|	El ID no existe en la base de datos|	Verificar que el producto exista

Notas / Validaciones:
producto_id debe ser > 0.
La imagen se devuelve en base64.
Usa el SP sp_obtenerProductoPorId.

Ejemplo curl

curl -X GET http://localhost:5000/producto/1 \
  -H "Authorization: Bearer <token>"

5) Actualizar producto

Ruta: PUT /producto/{producto_id}
Descripción: Actualiza los datos de un producto existente.
Autorización: ✅ Bearer <token>

Parámetros

Campo|	Tipo|	Requerido|	Descripción
producto_id|	int|	✅|	ID del producto a modificar

Body: Cualquier campo: nombre, descripcion, precio, existencias, estatus, unidades, imagen.

Ejemplo de Request(JSON)

{
  "precio": 28.00,
  "existencias": 150
}

Responses

Código|	Descripción|	Ejemplo
200|	Actualización exitosa|	{"producto_id": 1, "precio": 28.00, "existencias": 150, ...}
400|	Precio inválido|	{"error": "El precio debe ser mayor a cero"}
404|	No encontrado|	{"error": "Producto no encontrado"}

Errores comunes

Error|	Causa|	Solución
"Producto no encontrado"|	El ID no existe en la BD|	Verificar que el producto exista antes de actualizar
"El precio debe ser mayor a cero"|	Se envió precio ≤ 0|	Enviar un precio positivo
"Precio o Existencias tienen un formato invalido"|	Se envió texto en campo numérico|	Enviar números válidos para precio y existencias

Notas / Validaciones:
Solo actualiza los campos enviados (actualización parcial).
Usa sp_gestionProducto con opcion=2.
La imagen no se retorna completa en la respuesta.

Ejemplo curl

curl -X PUT http://localhost:5000/producto/1 \
  -H "Authorization: Bearer <token>" \
  -d "precio=28.00"

6) Crear venta

Ruta: POST /venta/
Descripción: Registra una venta completa. Valida stock, resta existencias y calcula totales automáticamente.
Autorización: ✅ Bearer <token>

Parámetros

Campo|	Tipo|	Requerido|	Descripción|	Ejemplo
caja_numero|	int|	✅|	Número de caja|	1
productos|	array|	✅|	Lista de productos|	[{"producto_id": 1, "cantidad": 2}]

Objeto en el array productos:

Campo|	Tipo|	Requerido|	Descripción
producto_id|	int|	✅|	ID del producto
cantidad|	int|	✅|	Cantidad a vender

Ejemplo de Request (JSON)

{
  "caja_numero": 1,
  "productos": [
    {"producto_id": 1, "cantidad": 2},
    {"producto_id": 5, "cantidad": 1}
  ]
}

Responses

Código|	Descripción|	Ejemplo
201|	Venta registrada|	{"mensaje": "Venta registrada con exito", "ticket": 101}
400|	Datos incompletos|	{"error": "Datos incompletos (caja_numero o productos faltantes)"}
400|	Stock insuficiente|	{"error": "Stock insuficiente.", "mensaje": "No se pudo completar la venta"}
400|	Producto inactivo|	{"error": "Producto inactivo."}

Errores comunes

Error|	Causa|	Solución
"Datos incompletos (caja_numero o productos faltantes)"|	Falta caja_numero o productos|	Enviar ambos en el JSON
"Stock insuficiente."|	cantidad > existencias|	Reducir cantidad o verificar stock
"Producto inactivo."|	Producto con estatus=0|	Usar un producto activo

Notas / Validaciones
El correo del usuario se obtiene del token JWT (get_jwt_identity()).
Transacción atómica: Si un detalle falla, se hace ROLLBACK de toda la venta.
Usa los SPs: sp_crearVenta y sp_agregarDetalleVenta.

Ejemplo curl

curl -X POST http://localhost:5000/venta/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{"caja_numero": 1, "productos": [{"producto_id": 1, "cantidad": 2}]}'

7) Reporte por caja

Ruta: GET /reporte/caja
Descripción: Ventas realizadas en una caja en un rango de fechas.
Autorización: ✅ Bearer <token>

Parámetros

Campo|	Tipo|	Requerido|	Descripción|	Ejemplo
caja|	int|	✅|	Número de caja|	1
inicio|	string|	✅|	Fecha inicio (YYYY-MM-DD)|	2026-05-01
fin|	string|	✅|	Fecha fin (YYYY-MM-DD)|	2026-05-31

Ejemplo de Request (JSON)

{
  "caja": 1,
  "inicio": "2026-05-01",
  "fin": "2026-05-31"
}

Responses

Código|	Descripción|	Ejemplo
200|	Datos encontrados|	[{"nombre": "Coca-Cola", "caja_numero": 1, "total_producto": 51.00}]
400|	Parámetros faltantes|	{"error": "Faltan parametros (caja, inicio, fin)"}
400|	Fechas inválidas|	{"error": "La fecha de inicio no puede ser mayor a la de fin"}
404|	Sin resultados|	{"error": "No se encontraron datos para la caja especificada"}

Errores Comunes

Error|	Causa|	Solución
"Faltan parametros (caja, inicio, fin)"|	No se envió alguno de los 3 parámetros|	Enviar caja, inicio y fin en el query string
"El ID de caja debe ser un numero entero"|	Se envió texto en lugar de número|	Enviar un número entero en caja
"La fecha de inicio no puede ser mayor a la de fin"|	inicio es posterior a fin|	Corregir el orden de las fechas
"No se encontraron datos para la caja especificada"|	La caja no tiene ventas en ese rango|	Ampliar el rango de fechas o verificar que la caja tenga ventas

Notas / Validaciones:
inicio no puede ser mayor que fin.
Las fechas deben tener formato YYYY-MM-DD.
Usa el SP sp_reporteVentaCaja.

Ejemplo curl

curl "http://localhost:5000/reporte/caja?caja=1&inicio=2026-05-01&fin=2026-05-31" \
  -H "Authorization: Bearer <token>"


8) Reporte por producto

Ruta: GET /reporte/producto
Descripción: Ventas de un producto específico en un rango de fechas.
Autorización: ✅ Bearer <token>

Parámetros

Campo|	Tipo|	Requerido|	Descripción|	Ejemplo
producto_id|	int|	✅|	ID del producto|	1
inicio|	string|	✅|	Fecha inicio (YYYY-MM-DD)|	2026-05-01
fin|	string|	✅|	Fecha fin (YYYY-MM-DD)|	2026-05-31

Ejemplo de Request (JSON)

{
  "producto_id": 1,
  "inicio": "2026-05-01",
  "fin": "2026-05-31"
}

Responses

Código|	Descripción|	Ejemplo
200|	Datos encontrados|	[{"nombre": "Coca-Cola", "total_producto": 51.00}]
400|	Parámetros faltantes|	{"error": "Faltan parametros (producto, inicio, fin)"}
400|	Fechas inválidas|	{"error": "La fecha de inicio no puede ser mayor a la de fin"}
404|	Producto no existe|	{"error": "El producto con ID 999 no existe en el catalogo"}
404|	Sin resultados|	{"error": "No se encontraron datos para el producto especificado"}

Errores Comunes

Error|	Causa|	Solución
"Faltan parametros (producto, inicio, fin)"|	No se envió alguno de los 3 parámetros|	Enviar producto_id, inicio y fin en el query string
"El ID de producto debe ser un numero entero"|	Se envió texto en lugar de número|	Enviar un número entero en producto_id
"El producto con ID X no existe en el catalogo"|	El ID no está registrado en Producto|	Verificar que el producto exista
"La fecha de inicio no puede ser mayor a la de fin"|	inicio es posterior a fin|	Corregir el orden de las fechas
"No se encontraron datos para el producto especificado"|	El producto existe pero no tiene ventas en el rango|	Ampliar el rango de fechas o verificar que haya ventas registradas

Notas / Validaciones:
Primero verifica que el producto exista en el catálogo.
Usa el SP sp_reporteVentaProducto.

Ejemplo curl

curl "http://localhost:5000/reporte/producto?producto_id=1&inicio=2026-05-01&fin=2026-05-31" \
  -H "Authorization: Bearer <token>"

Códigos de Error HTTP

Código|	Significado|	Cuándo ocurre
200|	OK|	Petición exitosa
201|	Created|	Recurso creado
400|	Bad Request|	Datos inválidos o faltantes
401|	Unauthorized|	Token faltante o inválido
404|	Not Found|	Recurso no encontrado
500|	Internal Server Error|	Error de BD o servidor

Changelog
Fecha|	Versión|	Cambios
2026-05-11|	1.0.0|	Documentación inicial completa