===================================================================

GUÍA RÁPIDA Y EJECUCIÓN DE LA APLICACIÓN

Este documento contiene las instrucciones esenciales para ejecutar la aplicación y las precauciones importantes para evitar fallos (crasheos).

INSTRUCCIONES DE EJECUCIÓN

Para iniciar la aplicación, simplemente da doble clic al archivo:

main.exe

El ejecutable se encuentra dentro de la carpeta 'dist'.

NOTA IMPORTANTE SOBRE EL INICIO: La primera vez que se ejecuta la aplicación, o si se han borrado los archivos de configuración, puede haber una demora notable. Esto sucede porque la aplicación está creando la base de datos (SQLite) y las carpetas necesarias para su funcionamiento (como 'pdf/Ticker'). Por favor, espere unos segundos hasta que la ventana principal aparezca.

PUNTOS CRÍTICOS Y PREVENCIÓN DE FALLOS

La aplicación puede fallar si los datos de los productos están incompletos en la base de datos:

CRASHEO EN VENTA (MÁS COMÚN):
Si intentas procesar un producto que no tiene un Precio de Venta (PVentas) definido, la aplicación se cerrará.

SOLUCIÓN: Asegúrate de que todos los productos a vender tengan un PVentas (Precio de Venta) con un valor numérico válido (Real o Float).

ERROR DE IMÁGENES/RECURSOS:
Si el producto no tiene una ruta de imagen válida (UrlImagen), la aplicación puede fallar al intentar cargarla.

SOLUCIÓN: Para evitar errores de carga, asegúrese de que la columna UrlImagen contenga una ruta o URL directa a un archivo de imagen.

RUTAS VÁLIDAS:

Archivos locales empaquetados: Imagen/nombre_archivo.png

URLs de descarga directa (ej.): http://ejemplo.com/mi_foto.jpg

RUTAS NO VÁLIDAS (CAUSAN CRASHEO):

No es válido usar data codificada en Base64 (ej.: data:image/jpeg;base64,...).

No es válido si la ruta es nula o vacía y no existe una imagen por defecto (default.png).

PROCESAMIENTO DE IMÁGENES DESCARGADAS

Cuando se utiliza una URL para la imagen de un producto, la aplicación sigue estas reglas de guardado y conversión para asegurar la compatibilidad:

Carpeta de Guardado: Todas las imágenes descargadas de una URL se guardan automáticamente dentro de la subcarpeta: Imagen/descargar/.

Conversión de Formato:

Si la imagen descargada es .webp, se convierte obligatoriamente a formato .png antes de guardarse en el disco.

Cualquier otro formato válido (.png, .jpg, .jpeg) se guarda con su extensión original.

FLUJO DE TRABAJO Y EDICIÓN DE DATOS

Las funcionalidades están distribuidas en pestañas según su propósito:

REGISTRO (Pestaña):

Propósito: Crear la ficha de nuevos clientes que podrán ser seleccionados para ventas a Crédito.

VENTA (Pestaña):

Propósito: Registrar transacciones de productos y generar el ticket.

Flujo de Carrito:

Se ingresa el Código del Producto y se selecciona la Cantidad en los campos de entrada.

Al presionar el botón "Agregar", el producto se añade a la tabla (carrito de ventas).

Dentro de la tabla, cada producto añadido tiene un botón para Eliminarlo de la venta.

Pago: Permite seleccionar el Método de Pago entre "Efectivo" o "Crédito". Si se elige Crédito, es obligatorio seleccionar un Cliente de la lista previamente registrado.

COMPRA (Pestaña):

Propósito: Agregar nuevos productos al inventario (Registrar Precio de Compra y Aumentar Stock).

INVENTARIO (Pestaña):

Propósito: Actualizar el producto existente (Modificar Precio de Venta (PVentas) e Imagen (UrlImagen)).

Uso: Contiene una tabla con todos los productos. La actualización se realiza buscando el producto por su Código. La tabla permite copiar los datos del producto para rellenar los campos de actualización fácilmente.

CLIENTE (Pestaña):

Propósito:

Actualizar datos personales del cliente (Nombre, Dirección, Teléfono, Límite de Crédito).

Consultar el Saldo pendiente (Deuda a Crédito).

Procesar Pagos para liquidar o reducir la deuda.

REPORTE (Pestaña):

Propósito: Generar informes de ventas. Primero se filtra la información mediante un calendario para seleccionar la fecha exacta del día deseado, y luego se muestra una tabla con los reportes disponibles.

Uso: Al dar clic en una celda de la tabla, se abrirá el reporte (PDF) seleccionado para su revisión o impresión.

===================================================================
/\_/\
( o.o )

^ <
===================================================================
