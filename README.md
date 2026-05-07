# 🦊 Kitsune POS - Sistema de Control de Ventas

**Kitsune POS** es una solución integral de punto de venta diseñada originalmente para la gestión de inventarios y ventas en boutiques, evolucionando a un sistema robusto aplicable a diversos tipos de negocios. Desarrollado en **Python** con una interfaz moderna en **PyQt5**.

---

## 🚀 Versiones del Proyecto (Ramas de Git)

El proyecto se gestiona mediante tres ramas principales para diferenciar las licencias y funcionalidades:

* **`main` (PRO):** Versión completa con reportes avanzados, gráficas de capital, gestión de clientes y sincronización.
* **`basica`:** Versión optimizada para ventas rápidas. Incluye Inventario y Ventas, pero oculta los módulos de Reportes y Clientes.
* **`demo`:** Versión de evaluación de 30 días. Incluye todas las funciones de la versión PRO pero con un bloqueo de seguridad por hardware (HWID) y tiempo.

---

## 🛠️ Características Principales

- **Gestión de Inventario:** Control de existencias, precios de compra y venta.
- **Punto de Venta (POS):** Interfaz intuitiva para realizar ventas y generar tickets en PDF.
- **Seguridad por Hardware:** Vinculación de licencia mediante ID único (Motherboard + CPU).
- **Reportes Profesionales:** Generación de reportes de capital y ganancias en PDF (ReportLab).
- **Base de Datos Flexible:** Uso de SQLite para velocidad local y validación mediante API PHP en InfinityFree.

---

## 📂 Estructura del Proyecto

- `main.py`: Punto de entrada de la aplicación y lógica de la interfaz principal.
- `Apertura.py`: Asistente de configuración inicial para nuevos negocios.
- `Conexion.py`: Gestión de la base de datos local `database.db`.
- `reporte.py`: Módulo de generación de reportes financieros.
- `Ticket.py`: Lógica para la creación de tickets de venta.
- `Seguridad.py`: (Nuevo) Validador de HWID y comunicación con el servidor de licencias.
- `TipoDatabase.py`: Inicialización de categorías y tipos de productos.

---

## 💻 Instalación para Desarrolladores

1. **Clonar el repositorio:**
   ```bash
   git clone [https://github.com/tu-usuario/kitsune-pos.git](https://github.com/tu-usuario/kitsune-pos.git)
   cd kitsune-pos
2. **Instalcion de Dependecias**
    ```bash
   pip install PyQt5 requests reportlab pillow
3. **Ejecuta la Aplicacion**
    ```bash
   python main.py
## Sistemas de licenciass
