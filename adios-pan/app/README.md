# App Adiós Pan

App web instalable (PWA): abre en el navegador, se agrega a la pantalla de inicio y funciona sin conexión.

- `index.html`: interfaz y lógica de la app.
- `recetas.py`: fuente de las 80 recetas. Después de editarla, ejecuta `python3 recetas.py` para regenerar `recetas.js`.
- `fotos/`: una foto por receta (`<id>.webp`, 640×640).
- `sw.js`: funcionamiento sin conexión. La app y las recetas se piden primero a la red, así que las recetas nuevas llegan solas.

## Acceso (inicio de sesión con el correo de la compra)

Hoy entra cualquier correo válido. Para conectar la base de datos de compradores:

1. Crea un servicio que reciba `POST` con el cuerpo `{"correo": "comprador@ejemplo.com"}`
   y responda `{"acceso": true}` si ese correo compró, o `{"acceso": false}` si no.
   Si vive en otro dominio, debe permitir CORS para el dominio de la app.
2. Pon su dirección en `CONFIG.API_VERIFICACION`, dentro de `index.html`.

Nada más cambia: toda la decisión está en la función `verificarAcceso(correo)`.
Hotmart puede llenar esa base de datos con sus webhooks de compra aprobada y de reembolso.

## Planes (fase de test)

Por ahora **todos los compradores acceden a todo**, compren el plan de $6.99 o el de $9.99.
El contenido del Plan Completo (almuerzos y cenas) irá dentro de esta misma app.
Si el producto se valida, la base de datos de accesos distinguirá los planes
(por ejemplo, que `API_VERIFICACION` responda también el plan del comprador).
