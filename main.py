import sqlite3
from io import BytesIO
import requests
from PIL.Image import Image
from PyQt5.QtCore import QTimer, QSize, QDate, Qt
from PyQt5.QtGui import QIcon,QFont,QPixmap
from PyQt5.QtWidgets import (QWidget, QApplication,QPushButton,QLabel, QMainWindow,
                             QVBoxLayout,QHBoxLayout,QTabWidget,QMenuBar ,QComboBox,
                             QLineEdit,QTableWidget,QSpinBox,QDoubleSpinBox,
                             QFileDialog,QDateEdit,QTableWidgetItem,QMessageBox)
import sys
import os
from Conexion import con,cur
from PIL import Image
import mimetypes
import reporte
from datetime import datetime, date
from Ticket import CreaTicket
import platform
import subprocess
class Mainwindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.tab = QTabWidget()
        #self.setStyleSheet("background-color: black")#  #este codigo es ara cambia el color de background
        self.setCentralWidget(self.tab)
        Bar =self.menuBar()
        file = Bar.addMenu("File")
        file.addAction("New")
        self.Widget = QWidget()
        self.Widget1 = QWidget()
        self.Widget2 = QWidget()
        self.Widget3 = QWidget()
        self.Widget4 = QWidget()
        self.Widget5 = QWidget()
        layout = QVBoxLayout()
        cur.execute("SELECT Nombre FROM Configuracion WHERE id = 1")
        datos = cur.fetchone()
        self.setWindowTitle(f"Kitsune - POS De {datos[0]}")
        self.setGeometry(100,100,800,640)
        self.setLayout(layout)
        self.tab.addTab(self.Widget,"Ventas")
        self.tab.addTab(self.Widget1, "Compras")
        self.tab.addTab(self.Widget2, "Invectarios")
        self.tab.addTab(self.Widget3, "Registrar Clientes")
        self.tab.addTab(self.Widget4,"Clientes")
        self.tab.addTab(self.Widget5, "Reporte")
        self.CreaTabla()
        self.venta()
        self.Compras()
        self.Invectario()
        self.Clientes()
        self.Cliente2()
        self.Reporte()
        self.setStyleSheet("""
        QPushButton{
            background-color: #2c3e50;
            color : white;
            font-family: 'Segoe UI', sans-serif;
            font-size: 14px;
            border-radius: 15px; /* Esto da el efecto redondeado suave */
            padding: 8px 16px;
            border: none;}
        QPushButton:hover{
            background-color:#e67e22;}
        QPushButton:pressed{
            background-color:#d35400}
        QLineEdit, QComboBox,QDoubleSpinBox,QDateEdit{
            border:2px solid #bdc3c7;
            border-radius:10px;
            padding:5px;
            background-color: #ffffff;
            selection-background-color:#e67e22;}
        QTableWidget{
            gridline-color: #ecf0f1;
            border: 1px solid #dcdde1;
            border-radius:8px;
        }
        QHeaderView::section{
            background-color: #2c3e50;
            color: white;
            padding: 5px;
            border: 1px solid #34495e;
            font-weight: bold;
        }
        QTabBar::tab{
            background: #ecf0f1;
            border: 1px solid #bdc3c7;
            padding: 10px 20px;
            margin-right: 2px;
            border-top-left-radius:10px;
            border-top-right-radius:10px;
        }
        QTabBar::tab:selected{
            background:#e67e22;
            color: white;
            border-bottom:none;
        }""")
    def DescargaImagen(self):#sirve para descarga imagenes de internet  desde una url.
        FileImagen="Imagen/Download"
        os.makedirs(FileImagen,exist_ok=True)
        url = self.LineImagen.text()
        NombreImage = self.LNCodigoIn.text()
        try:
            descargar = requests.get(url,stream=True)
            descargar.raise_for_status()
            codificado = descargar.headers.get('content-type')
            extesion = mimetypes.guess_extension(codificado)
            Contenido = descargar.content
            if extesion ==".webp":#esto sirve por si la imagen es de tipo webp lo trasforma a png
                try:
                    imagenes = Image.open(BytesIO(Contenido))
                    ExtrecionF =".png"
                    Archivotem = os.path.join(FileImagen,f"{NombreImage}{ExtrecionF}")
                    imagenes.save(Archivotem,"PNG")
                    print(f"Éxito: Imagen WebP convertida y guardada como PNG en {Archivotem}")

                except Exception as e:
                    print(f"Error en abri el webp: {e}")
            else:
                TempFIle = os.path.join(FileImagen,f"{NombreImage}{extesion}")
                with open(TempFIle,"wb") as f:
                    for chunk in descargar.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                print ("Descargado imagene")
        except requests.exceptions.RequestException as e:
            print(f"Error en la descarga de imagagen {e}")
    def Cliente2(self):
        # Contenedor principal de la ventana de gestión de clientes
        ventanaCliente = QVBoxLayout()

        # -------------------- Sección de Búsqueda de Cliente --------------------
        HoriazontalClien2 = QHBoxLayout()
        Etiqueta1 = QLabel("<b>Clientes</b>")
        Etiqueta1.setAlignment(Qt.AlignCenter)

        NombreRe = QLabel("Nombre: ")
        self.ComboCliente2 = QComboBox()

        # Rellenar ComboBox con clientes
        try:
            cur.execute("SELECT IdCliente, Nombre, Apellido FROM Clientes ORDER BY Nombre")
            RefClientes4 = cur.fetchall()
            self.ComboCliente2.clear()
            self.ComboCliente2.addItem("--- Selecciona un Cliente ---", userData=None)
            for idCliente, Nombre, Apellido in RefClientes4:
                NobreCompeto = f"{Nombre} {Apellido}"
                # userData guarda el ID del cliente
                self.ComboCliente2.addItem(NobreCompeto, userData=idCliente)
        except Exception as e:
            QMessageBox.critical(self, "Error DB", f"Error al cargar clientes: {e}")

        self.BuscarCliente = QPushButton("Buscar Cliente")

        HoriazontalClien2.addWidget(NombreRe)
        HoriazontalClien2.addWidget(self.ComboCliente2)

        ventanaCliente.addWidget(Etiqueta1)
        ventanaCliente.addLayout(HoriazontalClien2)
        ventanaCliente.addWidget(self.BuscarCliente)

        # Widget que contendrá la información dinámica de crédito/edición
        self.WidgetDetalleCredito = QWidget()
        self.LayoutDetalleCredito = QVBoxLayout(self.WidgetDetalleCredito)

        ventanaCliente.addWidget(self.WidgetDetalleCredito)

        self.Widget4.setLayout(ventanaCliente)
        self.BuscarCliente.clicked.connect(self.AbriClinete)
    def Configuracion(self):
        from Apertura import Apertura
        ventanaConfi = Apertura()
        ventanaConfi.show()

    def AbriClinete(self):
        self.id_cliente_seleccionado = self.ComboCliente2.currentData()
        if self.id_cliente_seleccionado is None:
            QMessageBox.warning(self, "Advertencia", "Debe Seleccionar un Cliente Por favor")
            return

    # Obtener el saldo pendiente total del cliente
        try:
        # Se obtiene la suma de todos los saldos pendientes para este cliente
            cur.execute("""
                    SELECT SUM(C.saldo_pendiente) 
                    FROM Cuentas_Por_Cobrar C
                    JOIN VENTA V ON C.idVentas = V.idVentas
                    WHERE V.idCliente = ? AND C.saldo_pendiente > 0
                """, (self.id_cliente_seleccionado,))

            resultado = cur.fetchone()
            saldo_pendiente_total = resultado[0] if resultado and resultado[0] else 0.00

        # Obtener los datos completos del cliente para edición (incluyendo "Cantidad")
            cur.execute("""
                    SELECT Nombre, Apellido, Telefono, Direccion, Referencias, Cantidad 
                    FROM Clientes 
                    WHERE idCliente = ?
                """, (self.id_cliente_seleccionado,))
            datos_cliente = cur.fetchone()

            self.MostrarDetalleCliente(datos_cliente, saldo_pendiente_total)

        except Exception as e:
            QMessageBox.critical(self, "Error DB", f"Error al obtener el saldo del cliente: {e}")
    # --- 3. FUNCIÓN PARA CONSTRUIR LA INTERFAZ DE CRÉDITO Y EDICIÓN ---
    def MostrarDetalleCliente(self, datos_cliente, saldo_pendiente_total):
    # Limpiar el widget de detalle previo
        while self.LayoutDetalleCredito.count():
            child = self.LayoutDetalleCredito.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
    # Se extraen las 6 columnas según el esquema del usuario
        nombre, apellido, telefono, direccion, referencias, cantidad_real = datos_cliente
    # -------------------- Sección de Edición de Cliente --------------------
        self.LayoutDetalleCredito.addWidget(QLabel("<hr>"))
        self.LayoutDetalleCredito.addWidget(QLabel("<b>Modificar Cliente</b>"))
    # Nombre
        HLayoutNombre = QHBoxLayout()
        HLayoutNombre.addWidget(QLabel("Nombre:"))
        self.ENombre = QLineEdit(nombre)
        HLayoutNombre.addWidget(self.ENombre)
        self.LayoutDetalleCredito.addLayout(HLayoutNombre)
    # Apellido
        HLayoutApellido = QHBoxLayout()
        HLayoutApellido.addWidget(QLabel("Apellido:"))
        self.EApellido = QLineEdit(apellido)
        HLayoutApellido.addWidget(self.EApellido)
        self.LayoutDetalleCredito.addLayout(HLayoutApellido)
    # Teléfono
        HLayoutTelefono = QHBoxLayout()
        HLayoutTelefono.addWidget(QLabel("Teléfono:"))
        self.ETelefono = QLineEdit(telefono)
        HLayoutTelefono.addWidget(self.ETelefono)
        self.LayoutDetalleCredito.addLayout(HLayoutTelefono)
    # Direccion
        HLayoutDireccion = QHBoxLayout()
        HLayoutDireccion.addWidget(QLabel("Dirección:"))
        self.EDireccion = QLineEdit(direccion)
        HLayoutDireccion.addWidget(self.EDireccion)
        self.LayoutDetalleCredito.addLayout(HLayoutDireccion)
    # Límite de Crédito (Combo Box con valores fijos)
        HLayoutCantidadReal = QHBoxLayout()
        HLayoutCantidadReal.addWidget(QLabel("Límite Crédito:"))
        self.ComboLimiteCredito = QComboBox()
    # Opciones de límite de crédito
        limites = [0.0,500.0,1000.0,1500.0, 2000.0,2500.0, 3000.0,3500.0, 4000.0,4500.0, 5000.0,5500.0, 6000.0,6500.0, 7000.0,7500.0, 8000.0,8500.0, 9000.0,9500.0, 10000.0]
    # Agregar los límites al ComboBox
        indice_actual = 0
        for i, limite in enumerate(limites):
            texto_limite = f"${limite:.2f}"
            self.ComboLimiteCredito.addItem(texto_limite, userData=limite)

        # Buscar la cantidad actual para seleccionarla
            if cantidad_real is not None and abs(cantidad_real - limite) < 0.01:
                indice_actual = i

        self.ComboLimiteCredito.setCurrentIndex(indice_actual)

        HLayoutCantidadReal.addWidget(self.ComboLimiteCredito)
        self.LayoutDetalleCredito.addLayout(HLayoutCantidadReal)

    # Referencias (ComboBox de clientes)
        HLayoutReferencias = QHBoxLayout()
        HLayoutReferencias.addWidget(QLabel("Referencias:"))
        self.ComboReferencias = QComboBox()

    # Rellenar el ComboBox con todos los clientes (excepto el que se está editando)
        try:
            cur.execute("SELECT Nombre, Apellido FROM Clientes WHERE idCliente != ? ORDER BY Nombre",
                    (self.id_cliente_seleccionado,))
            clientes_referencia = cur.fetchall()

            self.ComboReferencias.addItem("--- Sin Referencia ---")  # Opción para no tener referencia

        # Agregar los clientes restantes al ComboBox
            for nombre_ref, apellido_ref in clientes_referencia:
                nombre_completo_ref = f"{nombre_ref} {apellido_ref}"
                self.ComboReferencias.addItem(nombre_completo_ref)

        except Exception as e:
            QMessageBox.critical(self, "Error DB", f"Error al cargar clientes de referencia: {e}")

    # Establecer el valor actual de 'referencias'
        if referencias:
            index = self.ComboReferencias.findText(referencias)
            if index != -1:
                self.ComboReferencias.setCurrentIndex(index)

        HLayoutReferencias.addWidget(self.ComboReferencias)
        self.LayoutDetalleCredito.addLayout(HLayoutReferencias)

    # Botón Guardar
        self.BGuardarCambios = QPushButton("Guardar Cambios del Cliente")
        self.BGuardarCambios.setStyleSheet("background-color: #4CAF50; color: white;")
        self.LayoutDetalleCredito.addWidget(self.BGuardarCambios)

    # Conexión del botón de guardar
        self.BGuardarCambios.clicked.connect(self.ActualizarCliente)

    # -------------------- Sección de Deuda y Pago --------------------

        self.LayoutDetalleCredito.addWidget(QLabel("<hr>"))
        self.LayoutDetalleCredito.addWidget(QLabel("<b>Gestión de Crédito</b>"))

    # 1. Saldo Pendiente Actual
        self.LSaldoPendiente = QLabel(
        f"<b>Saldo Pendiente Total: </b> <font color='red'>${saldo_pendiente_total:.2f}</font>")
        self.LayoutDetalleCredito.addWidget(self.LSaldoPendiente)

    # 2. Campo de Pago
        HLayoutPago = QHBoxLayout()
        HLayoutPago.addWidget(QLabel("Monto a Pagar: $"))
        self.EPago = QLineEdit()
        self.EPago.setPlaceholderText("0.00")
        HLayoutPago.addWidget(self.EPago)
        self.BRegistrarPago = QPushButton("Registrar Pago")
        HLayoutPago.addWidget(self.BRegistrarPago)

        self.LayoutDetalleCredito.addLayout(HLayoutPago)

    # Conexión del botón de pago
        self.BRegistrarPago.clicked.connect(lambda: self.ProcesarPagoCredito(saldo_pendiente_total))

    # Si el saldo es cero, deshabilita el pago
        if saldo_pendiente_total <= 0:
            self.BRegistrarPago.setEnabled(False)
            self.EPago.setEnabled(False)
            self.LSaldoPendiente.setText("<b>Saldo Pendiente Total: </b> <font color='green'>$0.00</font>")
            self.LayoutDetalleCredito.addWidget(QLabel("<i>Este cliente no tiene deudas pendientes.</i>"))
    # --- 4. FUNCIÓN PARA PROCESAR EL PAGO Y ACTUALIZAR LA DB ---
    def ProcesarPagoCredito(self, saldo_pendiente_total):
        try:
            monto_pago = float(self.EPago.text())
        except ValueError:
            QMessageBox.warning(self, "Error de Entrada", "Por favor, ingrese un monto numérico válido.")
            return

        if monto_pago <= 0:
            QMessageBox.warning(self, "Error de Pago", "El monto a pagar debe ser positivo.")
            return

        if monto_pago > saldo_pendiente_total:
            QMessageBox.warning(self, "Error de Pago",
                            f"El pago (${monto_pago:.2f}) excede el saldo pendiente total (${saldo_pendiente_total:.2f}).")
            return

    # --- LÓGICA DE APLICACIÓN DE PAGO (FIFO: First-In, First-Out) ---
        pago_restante = monto_pago

        try:
        # 1. Obtener todas las deudas pendientes para este cliente, ordenadas por la más antigua (por idVentas)
            cur.execute("""
                    SELECT C.idCuentas_Por_Cobrar, C.saldo_pendiente  -- CORREGIDO: Usando idCuentas_Por_Cobrar
                    FROM Cuentas_Por_Cobrar C
                    JOIN VENTA V ON C.idVentas = V.idVentas
                    WHERE V.idCliente = ? AND C.saldo_pendiente > 0
                    ORDER BY V.idVentas ASC 
                """, (self.id_cliente_seleccionado,))

            deudas_pendientes = cur.fetchall()

        # CORREGIDO: Usando el nombre de variable idCuentas_Por_Cobrar
            for idCuentas_Por_Cobrar, saldo_pendiente in deudas_pendientes:
                if pago_restante <= 0:
                    break

            # Determinar cuánto del pago cubre esta deuda
                monto_aplicado = min(pago_restante, saldo_pendiente)

            # 2. Actualizar la tabla Cuentas_Por_Cobrar
                nuevo_saldo = saldo_pendiente - monto_aplicado

                cur.execute("""
                        UPDATE Cuentas_Por_Cobrar
                        SET monto_pagado = monto_pagado + ?, saldo_pendiente = ?
                        WHERE idCuentas_Por_Cobrar = ?  -- CORREGIDO: Usando idCuentas_Por_Cobrar
                    """, (monto_aplicado, nuevo_saldo, idCuentas_Por_Cobrar))
                pago_restante -= monto_aplicado
            con.commit()
            QMessageBox.information(self, "Pago Registrado",
                                f"Se registraron ${monto_pago:.2f} como pago a crédito con éxito.")
        # Recargar la interfaz de cliente para reflejar el nuevo saldo
            self.AbriClinete()
        except Exception as e:
            con.rollback()
            QMessageBox.critical(self, "Error DB", f"Error al procesar el pago. Transacción revertida: {e}")
    def ActualizarCliente(self):
        nombre = self.ENombre.text().strip()
        apellido = self.EApellido.text().strip()
        telefono = self.ETelefono.text().strip()
        direccion = self.EDireccion.text().strip()
        referencias = self.ComboReferencias.currentText()
        if referencias == "--- Sin Referencia ---":
            referencias = ""
        limite_credito = self.ComboLimiteCredito.currentData()
        if not nombre or not apellido:
            QMessageBox.warning(self, "Datos Incompletos", "El nombre y el apellido son obligatorios.")
            return
        try:
            cur.execute("""
                    UPDATE Clientes 
                    SET Nombre = ?, Apellido = ?, Telefono = ?, Direccion = ?, Referencias = ?, Cantidad = ?
                    WHERE idCliente = ?
                """, (nombre, apellido, telefono, direccion, referencias, limite_credito, self.id_cliente_seleccionado))
            con.commit()
            QMessageBox.information(self, "Actualización Exitosa",
                                "Los datos del cliente han sido actualizados con éxito.")
            self.Cliente2()
            index = self.ComboCliente2.findData(self.id_cliente_seleccionado)
            if index != -1:
                self.ComboCliente2.setCurrentIndex(index)
            self.AbriClinete()
        except Exception as e:
            con.rollback()
            QMessageBox.critical(self, "Error DB", f"Error al actualizar el cliente. Transacción revertida: {e}")
    def Reporte(self):
        VentanaReporte = QVBoxLayout()
        HorizontalRE = QHBoxLayout()
        LReporte = QLabel("<b>Reporte</b>")
        LReporte.setFont(QFont("Arial", 12))
        self.DateReporte = QDateEdit()
        self.DateReporte.setCalendarPopup(True)
        self.DateReporte.setDate(QDate.currentDate())
        self.ButtonReporte = QPushButton("Crear Reporte")
        self.ButtonReporte.clicked.connect(self.AgregarReporte)
        self.TablaRe = QTableWidget(0, 2)
        self.TablaRe.setHorizontalHeaderLabels(["Fecha", "Reporte"])
        self.TablaRe.setColumnWidth(0, 150)
        self.TablaRe.setColumnWidth(1, 300)
        self.TablaRe.cellClicked.connect(self.AbrirPDFDiario)
        HorizontalRE.addWidget(LReporte)
        HorizontalRE.addWidget(self.DateReporte)
        HorizontalRE.addWidget(self.ButtonReporte)
        VentanaReporte.addLayout(HorizontalRE)
        VentanaReporte.addWidget(self.TablaRe)
        self.Widget5.setLayout(VentanaReporte)
        self.CargarHistorialReportes()
    def CargarHistorialReportes(self):
        """
        Carga todos los archivos PDF del directorio pdf/Reporte en la tabla.
        """
        carpeta = "pdf/Reporte"
        self.TablaRe.setRowCount(0)
        if not os.path.exists(carpeta):
            os.makedirs(carpeta)
            return

        archivos = sorted(os.listdir(carpeta), reverse=True)
        for archivo in archivos:
            if archivo.endswith(".pdf"):
                fecha = archivo.replace("Reporte_", "").replace(".pdf", "")
                fila = self.TablaRe.rowCount()
                self.TablaRe.insertRow(fila)
                self.TablaRe.setItem(fila, 0, QTableWidgetItem(fecha))
                self.TablaRe.setItem(fila, 1, QTableWidgetItem(archivo))

        self.TablaRe.resizeColumnsToContents()
    def AgregarReporte(self):
        """
        Genera un nuevo reporte PDF y actualiza la tabla.
        """
        fecha_seleccionada = self.DateReporte.date().toString("yyyy-MM-dd")

        try:
            datos_reporte = reporte.obtener_datos_reporte(fecha_seleccionada, con)
            ruta_pdf = reporte.generar_reporte_pdf(datos_reporte)

            QMessageBox.information(self, "PDF Creado",
                                    f"Reporte guardado en:\n{ruta_pdf}")

            # Actualizamos historial después de crear uno nuevo
            self.CargarHistorialReportes()

        except Exception as e:
            QMessageBox.critical(self, "Error de Reporte",
                                 f"Ocurrió un error al generar el reporte:\n{e}")
    def AbrirPDFDiario(self, row, column):
        """
        Abre el PDF seleccionado en la tabla (clic simple en cualquier celda).
        """
        try:
            archivo = self.TablaRe.item(row, 1).text()
            ruta_completa = os.path.join("pdf/Reporte", archivo)

            if not os.path.exists(ruta_completa):
                QMessageBox.warning(self, "Archivo no encontrado",
                                    "El reporte PDF no existe en el directorio.")
                return

            if os.name == "nt":  # Windows
                os.startfile(ruta_completa)
            elif sys.platform == "darwin":  # macOS
                os.system(f"open '{ruta_completa}'")
            else:  # Linux
                os.system(f"xdg-open '{ruta_completa}'")

        except Exception as e:
            QMessageBox.critical(self, "Error al abrir",
                                 f"No se pudo abrir el archivo PDF:\n{e}")
    def CreaTabla(self): # Esto es para crea toda las tabla de la base de dato
        cur.execute("""Create table if not exists Tipo(idTipo INTEGER PRIMARY KEY AUTOINCREMENT, 
        Tipo Text not null unique,
        Descripcion1 Text,
        Descripcion2 Text,
        Descripcion3 Text
        )""")
        cur.execute("""Create TABLE IF NOT EXISTS Clientes(idCliente INTEGER PRIMARY KEY AUTOINCREMENT,
         Nombre Text not null,
         Apellido Text not null,
         Telefono Text ,
         Direccion Text,
         Referencias Text,
         Cantidad Real
         );""")
        cur.execute("""CREATE TABLE IF NOT EXISTS Productos(idProducto INTEGER PRIMARY KEY AUTOINCREMENT,
        Codigo Text Not null,
        Nombre Text Not null,
        Marca Text Not null,
        Tipo INTEGER Not Null,
        Descripcion Text not null,
        PVentas Real ,
        PComra Real not null,
        UrlImagen Text,
        Stock Integer,
        FOREIGN KEY (Tipo) REFERENCES Tipo(idTipo));""")
        cur.execute("""CREATE TABLE if not exists COMPRA(idCompra INTEGER PRIMARY KEY AUTOINCREMENT  ,
         Fecha TEXT NOT NULL,
         MontCompra REAL NOt NUll
         );""")
        cur.execute("""CREATE TABLE IF NOT EXISTS Detalles_Compra(idDetalles_Compra INTEGER PRIMARY KEY AUTOINCREMENT,
        idCompra INTEGER not null,
        idProducto INTEGER not null,
        Cantidad INTEGER NOT NULL,
        PrecioCom REAL NOT NULL,
        FOREIGN KEY (idCompra) REFERENCES COMPRA(idCompra),
        FOREIGN KEY (idProducto) REFERENCES Productos(idProducto));""")
        cur.execute("""CREATE TABLE IF NOT EXISTS VENTA(idVentas INTEGER PRIMARY KEY AUTOINCREMENT,
        Fecha TEXT NOT NULL,
        TotalVenta REAL NOT NULL,
        TipoPago TEXT NOT NULL,
        idCliente INTEGER,
        FOREIGN KEY(idCliente) REFERENCES Clientes(idCliente));""")
        cur.execute("""CREATE TABLE IF NOT EXISTS Detalles_Ventas(idDetalles_Ventas INTEGER PRIMARY KEY AUTOINCREMENT,
        idVentas INTEGER NOT NULL,
        idProducto INTEGER NOT NULL,
        cantidad INTEGER NOT NULL,
        PrecioUnitario REAL NOT NULL,
        FOREIGN KEY (idVentas) REFERENCES VENTA(idVentas),
        FOREIGN KEY (idProducto) REFERENCES Productos(idProducto));""")
        cur.execute("""CREATE TABLE IF NOT EXISTS Cuentas_Por_Cobrar(idCuentas_Por_Cobrar INTEGER PRIMARY KEY AUTOINCREMENT,
        idVentas INTEGER,
        monto_credito REAL,
        monto_pagado REAL,
        saldo_pendiente REAL,
        FOREIGN KEY (idVentas) REFERENCES VENTA(idVentas));""")
        cur.execute("""CREATE TABLE IF NOT EXISTS Contenido_tipo(id INTEGER PRIMARY KEY AUTOINCREMENT,
                       tipo integer NOT NULL,
                       Descripcion1 Text,
                       Descripcion2 Text,
                       Descripcion3 Text,
                       FOREIGN KEY (tipo) REFERENCES Tipo(idTipo));""")

        cur.execute("""INSERT OR IGNORE INTO Tipo (Tipo) VALUES ('Ropa'); """)
        cur.execute("""INSERT OR IGNORE INTO Tipo (Tipo) VALUES ('Bolsa');""")
        cur.execute("""INSERT OR IGNORE INTO Tipo (Tipo) VALUES ('Perfume');""")
        cur.execute("""INSERT OR IGNORE INTO Tipo (Tipo) VALUES ('Accesorios');""")
        con.commit()
    def venta(self):#Esto es la esctutura de la ventana de ventas
        vent_ventas =QVBoxLayout()
        horizon1= QHBoxLayout()
        horizon2 =QHBoxLayout()
        EcodigoV = QLabel("Codigo: ")
        self.LNCodigo =QLineEdit()
        self.LNCodigo.setPlaceholderText("Codigo de barra")
        ECantidad = QLabel("Cantidad: ")
        self.SCantidad = QSpinBox()
        self.ButtonAgregar =QPushButton("Agregar Carrito")
        horizon1.addWidget(EcodigoV)
        horizon1.addWidget(self.LNCodigo)
        horizon1.addWidget(ECantidad)
        horizon1.addWidget(self.SCantidad)
        horizon1.addWidget(self.ButtonAgregar)
        vent_ventas.addLayout(horizon1)
        self.Tabla = QTableWidget(0,7)
        #self.Tabla.setRowCount()
        self.Tabla.setHorizontalHeaderLabels(["Imagen","codigo","Nombre","Precios","cantidad","subtotal","Eliminar"])
        Etota =QLabel("Total: ")
        self.Etotal =QLabel("<b>$0.00</b>")
        EMetodo = QLabel("Metodo de Pago")
        self.ComboMetodo = QComboBox()
        self.ComboMetodo.addItems(["Efectivo","Credito"])
        ECliente = QLabel("Cliente")
        self.ComboCliente =QComboBox()
        self.ComboCliente.addItem("Selecionar Cliente: ")
        cur.execute("SELECT Nombre || ' ' || Apellido as NombreCliente FROM Clientes")
        RefClientes2 = cur.fetchall()
        for t in RefClientes2:
            self.ComboCliente.addItem(t[0])
        horizon2.addWidget(Etota)
        horizon2.addWidget(self.Etotal)
        horizon2.addWidget(EMetodo)
        horizon2.addWidget(self.ComboMetodo)
        horizon2.addWidget(ECliente)
        horizon2.addWidget(self.ComboCliente)
        self.ButtonVenta = QPushButton("Regristra Venta")
        vent_ventas.addWidget(self.Tabla)
        vent_ventas.addLayout(horizon2)
        vent_ventas.addWidget(self.ButtonVenta)
        self.Widget.setLayout(vent_ventas)
        self.ButtonVenta.clicked.connect(self.RegristraVentas)
        self.ButtonAgregar.clicked.connect(self.AgregarCarrito)
    def Compras(self): #esto es la ventana de compra
        vent_Compras = QVBoxLayout()
        HorizontalCom = QHBoxLayout()
        CodigoCom = QLabel("Codigo: ")
        self.LECodigoCom =QLineEdit()
        HorizontalCom.addWidget(CodigoCom)
        HorizontalCom.addWidget(self.LECodigoCom)
        HorizontalCom1 = QHBoxLayout()
        LNombreCom = QLabel("Nombre: ")
        self.lENombreCom =QLineEdit()
        HorizontalCom1.addWidget(LNombreCom)
        HorizontalCom1.addWidget(self.lENombreCom)
        HorizontalCom2 = QHBoxLayout()
        LMarcaCom = QLabel("Marca: ")
        self.LeMarcaCom =QLineEdit()
        HorizontalCom2.addWidget(LMarcaCom)
        HorizontalCom2.addWidget(self.LeMarcaCom)
        HorizontalCom3 = QHBoxLayout()
        LTipoCom = QLabel("Tipo: ")
        self.TipoCom = QComboBox()
        self.TipoCom.addItem("Selecciona tipo")
        cur.execute("""Select Tipo from Tipo""")
        Tipo = cur.fetchall()
        for t in Tipo:
            self.TipoCom.addItem(t[0])
        HorizontalCom3.addWidget(LTipoCom)
        HorizontalCom3.addWidget(self.TipoCom)
        HorizontalCom4 = QHBoxLayout()
        LDescripcionCom =QLabel("Descripcion: ")
        self.LDescripcionCom1 = QLabel()
        self.LDescripcionCom2 = QLabel()
        self.LDescripcionCom3 = QLabel()
        self.ComboDescripcionCom1 = QComboBox()
        self.ComboDescripcionCom2 = QComboBox()
        self.ComboDescripcionCom3 = QComboBox()
        HorizontalCom4.addWidget(LDescripcionCom)
        HorizontalCom4.addWidget(self.LDescripcionCom1)
        HorizontalCom4.addWidget(self.ComboDescripcionCom1)
        HorizontalCom4.addWidget(self.LDescripcionCom2)
        HorizontalCom4.addWidget(self.ComboDescripcionCom2)
        HorizontalCom4.addWidget(self.LDescripcionCom3)
        HorizontalCom4.addWidget(self.ComboDescripcionCom3)
        self.TipoCom.currentTextChanged.connect(self.CambioDEscricion)
        HorizontalCom5 = QHBoxLayout()
        LPrecioCom = QLabel("Precio de compra: ")
        self.SPrecioComre = QDoubleSpinBox()
        self.SPrecioComre.setMaximum(999999.99)
        HorizontalCom5.addWidget(LPrecioCom)
        HorizontalCom5.addWidget(self.SPrecioComre)
        HorizontalCom6 = QHBoxLayout()
        LStrockCom = QLabel("Strock: ")
        self.SStrockCom = QSpinBox()
        HorizontalCom6.addWidget(LStrockCom)
        HorizontalCom6.addWidget(self.SStrockCom)
        HorizontalCom7 = QHBoxLayout()
        self.LEstadoCom = QLabel("Estado")
        self.LEstadoCom.setFixedSize(QSize(199,45))
        HorizontalCom7.addWidget(self.LEstadoCom)
        HorizontalCom8 = QHBoxLayout()
        self.ButtonCom =QPushButton("Regrista Compra")
        HorizontalCom8.addWidget(self.ButtonCom)
        etiqueta=QLabel("<b>Esta es la prestana de Compra<b>")
        etiqueta.setFont(QFont("arial",12))
        etiqueta.setFixedSize(QSize(263,32))
        vent_Compras.addWidget(etiqueta)
        vent_Compras.addLayout(HorizontalCom)
        vent_Compras.addLayout(HorizontalCom1)
        vent_Compras.addLayout(HorizontalCom2)
        vent_Compras.addLayout(HorizontalCom3)
        vent_Compras.addLayout(HorizontalCom4)
        vent_Compras.addLayout(HorizontalCom5)
        vent_Compras.addLayout(HorizontalCom6)
        vent_Compras.addLayout(HorizontalCom7)
        vent_Compras.addLayout(HorizontalCom8)
        self.Widget1.setLayout(vent_Compras)
        self.ButtonCom.clicked.connect(self.RegristaCom)
    def RegristaCom(self):
        CodigoCom = self.LECodigoCom.text()
        Nombre = self.lENombreCom.text()
        Marca = self.LeMarcaCom.text()
        tipo = self.TipoCom.currentIndex()
        if self.TipoCom.currentIndex() == 1:
            Opcion1 = self.ComboDescripcionCom1.currentText()
            Opcion2 = self.ComboDescripcionCom2.currentText()
            Opcion3 = self.ComboDescripcionCom3.currentText()
            Descricion = f"Talla: {Opcion1}, Material: {Opcion2}, Color: {Opcion3}"
        elif self.TipoCom.currentIndex() == 2:
            Opcion1 = self.ComboDescripcionCom1.currentText()
            Opcion2 = self.ComboDescripcionCom2.currentText()
            Opcion3 = self.ComboDescripcionCom3.currentText()
            Descricion = f"Modelos: {Opcion1}, Material:  {Opcion2}, Tamaño: {Opcion3}"
        elif self.TipoCom.currentIndex() == 3:
            Opcion1 = self.ComboDescripcionCom1.currentText()
            Opcion2 = self.ComboDescripcionCom2.currentText()
            Opcion3 = self.ComboDescripcionCom3.currentText()
            Descricion = f"Aroma: {Opcion1}, Volumen:  {Opcion2}, Concetracion: {Opcion3}"
        elif self.TipoCom.currentIndex() == 4:
            Opcion1 = self.ComboDescripcionCom1.currentText()
            Opcion2 = self.ComboDescripcionCom2.currentText()
            Opcion3 = self.ComboDescripcionCom3.currentText()
            Descricion = f"Material: {Opcion1}, Tipo de accesorio:  {Opcion2}, Medida/Ajuste: {Opcion3}"
        elif self.TipoCom.currentIndex() == 0:
            print("Seecina otra cosa")
            QMessageBox.warning(self,"Error de escritura","Por favor seleciona un tipo")
            return
        precioCom = float(self.SPrecioComre.text())
        Strock = int(self.SStrockCom.text())
        if not (CodigoCom and Nombre and Marca and tipo and precioCom and Strock):
            QMessageBox.warning(self,"Falta de Datos","Por Favor de llenar los Datos")
            return
        print(f"{CodigoCom}, {Nombre}, {Marca}, {tipo}, {Descricion}, {precioCom}, {Strock}")
        try:
            cur.execute("""SELECT idProducto,Stock  FROM Productos WHERE Codigo = ?""",(CodigoCom,))
            dato = cur.fetchone()
            idProducto = None
            if dato:
                idProducto = dato[0]
                StockA = dato[1]
                NuevoStock = StockA + Strock
                fechaActual = date.today().strftime("%Y-%m-%d")
                TotalCom = precioCom * float(Strock)
                cur.execute("""
                               UPDATE Productos
                               SET Stock = ?, PComra = ?
                               WHERE idProducto = ?;
                           """, (NuevoStock, precioCom, idProducto))

                # ✅ Registrar compra y detalle de compra aunque ya exista
                cur.execute("INSERT INTO COMPRA (Fecha, MontCompra) VALUES (?, ?)", (fechaActual, TotalCom))
                idCompra = cur.lastrowid
                cur.execute("""
                               INSERT INTO Detalles_Compra (idCompra, idProducto, Cantidad, PrecioCom)
                               VALUES (?, ?, ?, ?)
                           """, (idCompra, idProducto, Strock, precioCom))

                QMessageBox.information(self, "Producto Existente",
                                        f"Stock de {CodigoCom} actualizado a {NuevoStock}.")
            else:
                cur.execute("""INSERT INTO Productos(Codigo,Nombre,Marca,Tipo,Descripcion,PComra ,Stock ) VALUES(?,?,?,?,?,?,?)""",(CodigoCom,Nombre,Marca,tipo,Descricion,precioCom,Strock))
                print("Dato actualizados")
                idProducto  =cur.lastrowid
                QMessageBox.information(self,"Productos Agregador",f"el Productos fue agregador con codigo {CodigoCom} ")
                fechaActual = date.today().strftime("%Y-%m-%d")
                TotalCom = precioCom * float(Strock)
                cur.execute("""INSERT INTO COMPRA(Fecha,MontCompra) VALUES(?,?)""",(fechaActual,TotalCom))
                idCompra = cur.lastrowid
                cur.execute("""INSERT INTO Detalles_Compra(idCompra,idProducto,Cantidad,PrecioCom) VALUES(?,?,?,?)""",(idCompra,idProducto,Strock,precioCom))
            con.commit()
        except sqlite3.Error as e:
            con.rollback()
            error_message = f"Error de Base de Datos: {e}"
            self.LEstadoCom.setText(f"Estado: Error en DB")
            QMessageBox.critical(self, "Error de Base de Datos", error_message)
        except Exception as e:
            QMessageBox.critical(self, "Error Inesperado", f"Ocurrió un error inesperado: {e}")
        cur.execute("select Codigo,UrlImagen,Nombre,Marca,Tipo,Descripcion,PVentas ,PComra,Stock from Productos ")
        Tabla2 = cur.fetchall()
        numFila1 = len(Tabla2)
        self.TablaInvertario.setRowCount(numFila1)
        for Valorfila1, regristo1 in enumerate(Tabla2):
            for ValorColumna1, Valoew1 in enumerate(regristo1):
                if ValorColumna1 == 1:
                    label = QLabel()
                    Pixmap = QPixmap(str(Valoew1))
                    Pixmap = Pixmap.scaled(199, 299)
                    label.setPixmap(Pixmap)
                    label.setScaledContents(True)
                    self.TablaInvertario.setCellWidget(Valorfila1, ValorColumna1, label)
                else:
                    tablaValores1 = QTableWidgetItem(str(Valoew1))
                    self.TablaInvertario.setItem(Valorfila1, ValorColumna1, tablaValores1)
        self.LECodigoCom.clear()
        self.lENombreCom.clear()
        self.LeMarcaCom.clear()
        self.TipoCom.setCurrentIndex(0)
        self.SPrecioComre.setValue(0.0)
        self.SStrockCom.setValue(0)
    def Invectario(self):#esta es la ventana de invertario que mostrara los dato de la tabla Productros
        Vent_Invectstio= QVBoxLayout()
        HorizontaInve1 = QHBoxLayout()#Codigo de Escaneor de barra
        ECodigo = QLabel("Codigo: ")
        self.LNCodigoIn = QLineEdit()
        HorizontaInve1.addWidget(ECodigo)
        HorizontaInve1.addWidget(self.LNCodigoIn)
        HorizontaInve2 = QHBoxLayout()#Imagen de productor
        LImagen =QLabel("Imagen: ")
        self.ComboImagen = QComboBox()
        self.ComboImagen.addItems(["Url","Archivo"])
        self.LineImagen = QLineEdit()
        self.FileImagen = QLineEdit()
        self.FileImagen.setReadOnly(True)
        self.FileImagen.hide()
        self.ComboImagen.currentIndexChanged.connect(self.CambioFile)
        self.ButtonFIle= QPushButton("...")#se usada este boton Para Puebla de descagar y modificacion de imagen
        self.ButtonFIle.setFixedSize(21,21)
        self.ButtonFIle.hide()
        HorizontaInve2.addWidget(LImagen)
        HorizontaInve2.addWidget(self.ComboImagen)
        HorizontaInve2.addWidget(self.LineImagen)
        HorizontaInve2.addWidget(self.FileImagen)
        HorizontaInve2.addWidget(self.ButtonFIle)
        #HorizontaInve2.addWidget(FileIMagen)
        HorizontaInve3 = QHBoxLayout()#Nombre de producto
        LNombreIn= QLabel("Nombre: ")
        self.LENombreIn =QLineEdit()
        HorizontaInve3.addWidget(LNombreIn)
        HorizontaInve3.addWidget(self.LENombreIn)
        HorizontaInve4 = QHBoxLayout()#Marca de producto
        LMarca =QLabel("Marca: ")
        self.LEMarca =QLineEdit()
        HorizontaInve4.addWidget(LMarca)
        HorizontaInve4.addWidget(self.LEMarca)
        HorizontaInve5 = QHBoxLayout()#Tipo de prodcucto
        LTipo =QLabel("Tipo: ")
        self.ComboTipo=QComboBox()
        self.ComboTipo.addItem("Selecciona tipo")
        cur.execute("""Select Tipo from Tipo""")
        Tipo = cur.fetchall()
        for t in Tipo:
            self.ComboTipo.addItem(t[0])
        HorizontaInve5.addWidget(LTipo)
        HorizontaInve5.addWidget(self.ComboTipo)
        HorizontaInve51 = QHBoxLayout()
        LDescripcionI = QLabel("Descripcion: ")
        self.LDescripcionInve = QLineEdit()
        HorizontaInve51.addWidget(LDescripcionI)
        HorizontaInve51.addWidget(self.LDescripcionInve)
        HorizontaInve6 = QHBoxLayout()#recio de venta de producto
        LRecioVenta =QLabel("Precio de venta: ")
        self.SRecioVEnta =QDoubleSpinBox()
        self.SRecioVEnta.setMaximum(999999.99)
        HorizontaInve6.addWidget(LRecioVenta)
        HorizontaInve6.addWidget(self.SRecioVEnta)
        HorizontaInve7 = QHBoxLayout()#recio de comra de producto
        LRpecioComra = QLabel("Precio de compra: ")
        self.SrecioComra=QDoubleSpinBox()
        self.SrecioComra.setMaximum(999999.99)
        HorizontaInve7.addWidget(LRpecioComra)
        HorizontaInve7.addWidget(self.SrecioComra)
        HorizontaInve8 = QHBoxLayout()#Strock de roducto
        LStrock =QLabel("Strock: ")
        self.SStrock  =QSpinBox()
        HorizontaInve8.addWidget(LStrock)
        HorizontaInve8.addWidget(self.SStrock)
        HorizontaInve9 = QHBoxLayout()
        self.ButtonActulizar =QPushButton("Actualizar")
        self.ButtonNuevo = QPushButton("Nuevo/Limpiar")#se encargar de limiar el formulario
        self.ButtonEliminar = QPushButton("Eliminar")
        HorizontaInve9.addWidget(self.ButtonActulizar)
        HorizontaInve9.addWidget(self.ButtonNuevo)
        HorizontaInve9.addWidget(self.ButtonEliminar)
        #Aqui Va la tabla de todo los productos
        self.TablaInvertario =QTableWidget(0,9)
        self.TablaInvertario.setHorizontalHeaderLabels(["Codigo","Imagen","Nombre","Marca","Tipo","Descripcion","Precio Venta","Precio Compra","Stock"])
        cur.execute("select Codigo,UrlImagen,Nombre,Marca,Tipo,Descripcion,PVentas ,PComra,Stock from Productos ")
        Tabla2 = cur.fetchall()
        numFila1 = len(Tabla2)
        self.TablaInvertario.setRowCount(numFila1)
        for Valorfila1, regristo1 in enumerate(Tabla2):
            for ValorColumna1, Valoew1 in enumerate(regristo1):
                if ValorColumna1 ==1 :
                    label =QLabel()
                    Pixmap = QPixmap(str(Valoew1))
                    Pixmap = Pixmap.scaled(199,299)
                    label.setPixmap(Pixmap)
                    label.setScaledContents(True)
                    self.TablaInvertario.setCellWidget(Valorfila1,ValorColumna1,label)
                else:
                    tablaValores1 = QTableWidgetItem(str(Valoew1))
                    self.TablaInvertario.setItem(Valorfila1, ValorColumna1, tablaValores1)
        Vent_Invectstio.addLayout(HorizontaInve1)
        Vent_Invectstio.addLayout(HorizontaInve2)
        Vent_Invectstio.addLayout(HorizontaInve3)
        Vent_Invectstio.addLayout(HorizontaInve4)
        Vent_Invectstio.addLayout(HorizontaInve5)
        Vent_Invectstio.addLayout(HorizontaInve51)
        Vent_Invectstio.addLayout(HorizontaInve6)
        Vent_Invectstio.addLayout(HorizontaInve7)
        Vent_Invectstio.addLayout(HorizontaInve8)
        Vent_Invectstio.addLayout(HorizontaInve9)
        Vent_Invectstio.addWidget(self.TablaInvertario)
        self.Widget2.setLayout(Vent_Invectstio)
        self.ButtonFIle.clicked.connect(self.FileDialogo)
        self.ButtonActulizar.clicked.connect(self.Actulizarproducto)
        self.ButtonNuevo.clicked.connect(self.LimpiezaInvectario)
        self.ButtonEliminar.clicked.connect(self.EliminarInvectario)
    def LimpiezaInvectario(self):
        self.LNCodigoIn.clear()
        self.LENombreIn.clear()
        self.LEMarca.clear()
        self.FileImagen.clear()
        self.FileImagen.hide()
        self.ButtonFIle.hide()
        self.LineImagen.clear()
        self.LineImagen.show()
        self.LDescripcionInve.clear()
        self.SStrock.setValue(0)
        self.SRecioVEnta.setValue(0.0)
        self.SrecioComra.setValue(0.0)
        self.ComboTipo.setCurrentIndex(0)
        self.ComboImagen.setCurrentIndex(0)
    def EliminarInvectario(self):
        CodigoE = self.LNCodigoIn.text()
        if not (CodigoE):
            QMessageBox.warning(self,"Error","Por Favor Pon un codigo de Producto")
            return 
        respuesta = QMessageBox.question(self,"Corfimancion",f"Esta seguro de eliminar el Producto {CodigoE}",QMessageBox.Yes | QMessageBox.No,QMessageBox.No)
        if respuesta == QMessageBox.Yes:
            cur.execute("""DELETE FROM Productos WHERE Codigo = ?""",(CodigoE,))
            con.commit()
            self.LNCodigoIn.clear()
            cur.execute("select Codigo,UrlImagen,Nombre,Marca,Tipo,Descripcion,PVentas ,PComra,Stock from Productos ")
            Tabla2 = cur.fetchall()
            numFila1 = len(Tabla2)
            self.TablaInvertario.setRowCount(numFila1)
            for Valorfila1, regristo1 in enumerate(Tabla2):
                for ValorColumna1, Valoew1 in enumerate(regristo1):
                    if ValorColumna1 == 1:
                        label = QLabel()
                        Pixmap = QPixmap(str(Valoew1))
                        Pixmap = Pixmap.scaled(199, 299)
                        label.setPixmap(Pixmap)
                        label.setScaledContents(True)
                        self.TablaInvertario.setCellWidget(Valorfila1, ValorColumna1, label)
                    else:
                        tablaValores1 = QTableWidgetItem(str(Valoew1))
                        self.TablaInvertario.setItem(Valorfila1, ValorColumna1, tablaValores1)
    def ClickTable(self):
        return
    def FileDialogo(self):
        Archivo = QFileDialog.getOpenFileName(self,"","","Archivos de Imagen (*.PNG *.JPG *.JPEG)")
        RUTA = Archivo[0]
        self.FileImagen.setText(RUTA)
    def CambioFile(self):
        if self.ComboImagen.currentIndex()==0:
            self.LineImagen.show()
            self.FileImagen.hide()
            self.ButtonFIle.hide()
        else:
            self.LineImagen.hide()
            self.FileImagen.show()
            self.ButtonFIle.show()
    def Actulizarproducto(self):
        CodigoImagen = self.LNCodigoIn.text()
        UrlImagen = None
        if self.ComboImagen.currentIndex() == 0:
            if self.LineImagen.text().endswith(".png"):
                self.DescargaImagen()
                UrlImagen =f"Imagen/Download/{CodigoImagen}.png"
            elif self.LineImagen.text().endswith(".jpg"):
                self.DescargaImagen()
                UrlImagen = f"Imagen/Download/{CodigoImagen}.jpg"
            elif self.LineImagen.text().endswith(".jpeg"):
                self.DescargaImagen()
                UrlImagen = f"Imagen/Download/{CodigoImagen}.jpeg"
            elif self.LineImagen.text().endswith(".webp"):
                self.DescargaImagen()
                UrlImagen =f"Imagen/Download/{CodigoImagen}.png"
        elif self.ComboImagen.currentIndex()==1:
            UrlImagen = self.FileImagen.text()
        print(UrlImagen)
        NombreAct = self.LENombreIn.text()
        Marca = self.LEMarca.text()
        Tipo = self.ComboTipo.currentIndex()
        Descripcion = self.LDescripcionInve.text()
        PVentas = self.SRecioVEnta.text()
        PComra = self.SrecioComra.text()
        Stock = self.SStrock.text()
        cur.execute("""UPDATE Productos SET Nombre = ? , UrlImagen = ?,Marca = ?, Tipo = ?,Descripcion = ?,PVentas = ?,PComra = ? ,Stock = ? WHERE Codigo = ?;""",(NombreAct,UrlImagen,Marca,Tipo,Descripcion,PVentas,PComra,Stock ,CodigoImagen))
        con.commit()
        cur.execute("select Codigo,UrlImagen,Nombre,Marca,Tipo,Descripcion,PVentas ,PComra,Stock from Productos ")
        Tabla2 = cur.fetchall()
        numFila1 = len(Tabla2)
        self.TablaInvertario.setRowCount(numFila1)
        for Valorfila1, regristo1 in enumerate(Tabla2):
            for ValorColumna1, Valoew1 in enumerate(regristo1):
                if ValorColumna1 == 1:
                    label = QLabel()
                    Pixmap = QPixmap(str(Valoew1))
                    Pixmap = Pixmap.scaled(199, 299)
                    label.setPixmap(Pixmap)
                    label.setScaledContents(True)
                    self.TablaInvertario.setCellWidget(Valorfila1, ValorColumna1, label)
                else:
                    tablaValores1 = QTableWidgetItem(str(Valoew1))
                    self.TablaInvertario.setItem(Valorfila1, ValorColumna1, tablaValores1)
    def Clientes(self):#este es la ventana de regristro de cliente
        RegCliente= QVBoxLayout()
        HorizontalCliente1 =QHBoxLayout()
        LNombreC = QLabel("Nombre: ")
        self.Nombrec = QLineEdit()
        self.Nombrec.setPlaceholderText("NombreApellido")
        HorizontalCliente1.addWidget(LNombreC)
        HorizontalCliente1.addWidget(self.Nombrec)
        HorizontalCliente2 = QHBoxLayout()
        LApellidoC = QLabel("Apellido: ")
        self.Apellido = QLineEdit()
        self.Apellido.setPlaceholderText("Apellido")
        HorizontalCliente2.addWidget(LApellidoC)
        HorizontalCliente2.addWidget(self.Apellido)
        HorizontalCliente3 = QHBoxLayout()
        LTelefonoC = QLabel("Telefono: ")
        self.Telefono = QLineEdit()
        self.Telefono.setPlaceholderText("Telefono")
        HorizontalCliente3.addWidget(LTelefonoC)
        HorizontalCliente3.addWidget(self.Telefono)
        HorizontalCliente4 = QHBoxLayout()
        LDirecionC = QLabel("Direcion: ")
        self.Direcion = QLineEdit()
        self.Direcion.setPlaceholderText("Direcion")
        HorizontalCliente4.addWidget(LDirecionC)
        HorizontalCliente4.addWidget(self.Direcion)
        HorizontalCliente5 = QHBoxLayout()
        LRefrerenciaC = QLabel("Refrerencia: ")
        self.Refrerencia = QComboBox()
        self.Refrerencia.addItem("Refrerencia: ")
        cur.execute("SELECT Nombre || ' ' || Apellido as NombreCliente FROM Clientes")
        RefClientes = cur.fetchall()
        for t in RefClientes:
            self.Refrerencia.addItem(t[0])
        HorizontalCliente5.addWidget(LRefrerenciaC)
        HorizontalCliente5.addWidget(self.Refrerencia)
        HorizontalCliente6 = QHBoxLayout()
        LCantidaC = QLabel("Cantida: ")
        self.Cantida = QComboBox()
        self.Cantida.setCurrentIndex(0)
        self.Cantida.addItem("Elegir Cantida")
        self.Cantida.addItems(
            ["$0.0","$500.0","$1000.0","$1500.0", "$2000.0","$2500.0", "3000.0","$3500.0", "$4000.0","$4500.0", "$5000.0","$5500.0", "$6000.0","$6500.0", "$7000.0","$7500.0", "$8000.0","$8500.0", "$9000.0","$9500.0"," $10000.0"])
        HorizontalCliente6.addWidget(LCantidaC)
        HorizontalCliente6.addWidget(self.Cantida)
        Etiquetas = QLabel("<b>Regristo de clientes</b>")
        Etiquetas.setFont(QFont("Arial",12))
        self.TablaCliente =QTableWidget(0,6)
        self.TablaCliente.setHorizontalHeaderLabels(["Nombre","Apellido","Telefono","Direcion","Refrerencia","Cantida"])
        cur.execute("select Nombre,Apellido,Telefono,Direccion,Referencias,cantidad from clientes  ")
        Tabla = cur.fetchall()
        numFila = len(Tabla)
        self.TablaCliente.setRowCount(numFila)
        for Valorfila, regristo in enumerate(Tabla):
            for ValorColumna , Valoew in enumerate(regristo):
                tablaValores =QTableWidgetItem(str(Valoew))
                self.TablaCliente.setItem(Valorfila,ValorColumna,tablaValores)
        self.EStado = QLabel("aqui")
        Button1 =QPushButton("Regristar")
        RegCliente.addWidget(Etiquetas)
        RegCliente.addLayout(HorizontalCliente1)
        RegCliente.addLayout(HorizontalCliente2)
        RegCliente.addLayout(HorizontalCliente3)
        RegCliente.addLayout(HorizontalCliente4)
        RegCliente.addLayout(HorizontalCliente5)
        RegCliente.addLayout(HorizontalCliente6)
        RegCliente.addWidget(Button1)
        RegCliente.addWidget(self.EStado)
        RegCliente.addWidget(self.TablaCliente)
        self.Widget3.setLayout(RegCliente)
        Button1.clicked.connect(self.Regristar)
    def Regristar(self):#este es para regrista los cliente de uso de creditos
        nombre = self.Nombrec.text()
        apellido = self.Apellido.text()
        telefono = self.Telefono.text()
        direcion = self.Direcion.text()
        refrerencia = self.Refrerencia.currentIndex()
        if refrerencia == 0:
            print("Refrerencia esta Vacio")
            refrerencia2 = ""
        elif refrerencia > 0 :
            refrerencia2 =self.Refrerencia.currentText()
        indice = self.Cantida.currentIndex()
        if indice == 0:
            self.EStado.setText("<b>Seleciona un valor en Catidad</b>")
            return
        cantidad = self.Cantida.currentText().replace("$", "").replace(",", "")
        print(f"Nombre: {nombre} Apellido: {apellido} Telefono: {telefono} Direcion {direcion} Refrerancia: {refrerencia2} Cantidad: {cantidad}")
        cur.execute("""INSERT INTO Clientes (Nombre,Apellido,Telefono,Direccion,Referencias,Cantidad)VALUES(?,?,?,?,?,?)""",(nombre,apellido,telefono,direcion,refrerencia2,cantidad))
        con.commit()
        print("Cliente Regristado")
        self.Nombrec.clear()
        self.Apellido.clear()
        self.Telefono.clear()
        self.Direcion.clear()
        self.Refrerencia.setCurrentIndex(0)
        self.Cantida.setCurrentIndex(0)
        self.EStado.setText("Cliente Regristado")
        self.ActulizarCliente()
        QTimer.singleShot(3000,self.EStado.clear)
    def ActulizarCliente(self):
        self.Refrerencia.clear()
        self.Refrerencia.addItem("Refrerencia: ")
        cur.execute("SELECT Nombre || ' ' || Apellido as NombreCliente FROM Clientes")
        RefClientes = cur.fetchall()
        for t in RefClientes:
            self.Refrerencia.addItem(t[0])
        cur.execute("select Nombre,Apellido,Telefono,Direccion,Referencias,cantidad from clientes ")
        Tabla = cur.fetchall()
        numFila = len(Tabla)
        self.TablaCliente.setRowCount(numFila)
        for Valorfila, regristo in enumerate(Tabla):
            for ValorColumna, Valoew in enumerate(regristo):
                tablaValores = QTableWidgetItem(str(Valoew))
                self.TablaCliente.setItem(Valorfila, ValorColumna, tablaValores)
    def AgregarCarrito(self):
        Articulor = self.LNCodigo.text()
        Cantidad  = self.SCantidad.value()
        if not Articulor or Cantidad <= 0:
            QMessageBox.warning(self,"error","Los campo esta vacio")
            return 
        try:
            cur.execute("""SELECT Nombre, PVentas, Stock, UrlImagen FROM Productos WHERE Codigo = ?""",(Articulor,))
            articulo = cur.fetchone()
        except Exception as e:
            QMessageBox.warning(self,"Error",f"Ocurrio un error en la base de dato:{e}")
            return
        if articulo is None:
            QMessageBox.warning(self,"Articulo",f"No se Encontro producto: {Articulor} ")
            return
        nombre, precio, stock, imagen_ruta = articulo
        ProductoRegristrado =False
        for row in range(self.Tabla.rowCount()):
            CodigoA = self.Tabla.item(row,1).text()
            if CodigoA == Articulor:
                ProductoRegristrado =True
                CantidadActual = int(self.Tabla.item(row,4).text())
                NuevaCantidad = CantidadActual + Cantidad
                if NuevaCantidad>stock:
                    QMessageBox.warning(self,"Cantidad","No Hay suficiente productos")
                    return
                precioUnitario = self.Tabla.item(row,3).text().replace("$","")
                precioU= float(precioUnitario)
                nuevosubtotal=NuevaCantidad*precioU
                self.Tabla.item(row,4).setText(str(NuevaCantidad))
                self.Tabla.item(row,5).setText(f"${nuevosubtotal}")
                break
        if not ProductoRegristrado:
            if Cantidad>stock:
                QMessageBox.warning(self,"Cantidad","No Hay suficiente productos")
                return

            subtotal = Cantidad*precio
            fila = self.Tabla.rowCount()
            self.Tabla.insertRow(fila)

            labelImagen = QLabel()
            labelImagen.setAlignment(Qt.AlignCenter)
            if imagen_ruta:
                Imagenfila = QPixmap(imagen_ruta)
                if not Imagenfila.isNull():
                    escalado=Imagenfila.scaled(83, 83, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                    labelImagen.setPixmap(escalado)
                else:
                    labelImagen.setText("❌ Error")
            else:
                labelImagen.setPixmap("No hay imagenes")
            self.Tabla.setCellWidget(fila,0,labelImagen)
            self.Tabla.setRowHeight(fila,88)
            def CrearFila(text):
                item = QTableWidgetItem(str(text))
                item.setTextAlignment(Qt.AlignCenter)
                return item
            self.Tabla.setItem(fila,1,CrearFila(Articulor))
            self.Tabla.setItem(fila, 2, CrearFila(nombre))
            self.Tabla.setItem(fila, 3, CrearFila(f"${precio}"))
            self.Tabla.setItem(fila, 4, CrearFila(Cantidad))
            self.Tabla.setItem(fila, 5, CrearFila(f"${subtotal}"))
            BotonELiminar = QPushButton("X")
            BotonELiminar.setStyleSheet("background-color: red; color: white;")
            BotonELiminar.clicked.connect(self.EliminarArticulo)
            self.Tabla.setCellWidget(fila, 6, BotonELiminar)
        self.ActulizarprecioVencta()
        self.LNCodigo.clear()
        self.SCantidad.setValue(0)
    def ActulizarprecioVencta(self):
        total = 0.0
        for row in range(self.Tabla.rowCount()):
            subtotalTabla = self.Tabla.item(row,5).text().replace("$","")
            try:
                total += float(subtotalTabla)
            except ValueError:
                pass
        try:
            self.Etotal.setText(f"<b>${total:.2f}</b>")
        except AttributeError:
            pass
    def EliminarArticulo(self):
        Button = self.sender()
        if Button and isinstance(Button, QPushButton):
            index = self.Tabla.indexAt(Button.pos())
            if index.isValid():
                row = index.row()
                self.Tabla.removeRow(row)
                self.ActulizarprecioVencta()
    def RegristraVentas(self):
        if self.Tabla.rowCount() == 0:
            QMessageBox.warning(self, "Vacio", "NO hay nada que vende")
            return

            # Obtener datos de la interfaz
        metodo = self.ComboMetodo.currentText()  # Renombre: metodo_pago -> metodo
        Cliente = self.ComboCliente.currentText()  # Renombre: cliente_nombre_completo -> Cliente

        # Limpiar y convertir el total a float
        try:
            # Se asegura de limpiar el tag <b> también
            Total = self.Etotal.text().replace("<b>$", "").replace("</b>", "")
            Totalv = float(Total)  # Renombre: total_venta -> Totalv
        except ValueError:
            QMessageBox.critical(self, "Error de Total", "El campo de total contiene un valor no numérico.")
            return

        clinteid = None  # Renombre: cliente_id -> clinteid

        # 2. Obtener el ID del cliente y verificar requisito de crédito
        # CORRECCIÓN: Se ajusta la condición para verificar correctamente el "Credito"
        if metodo == "Credito" and self.ComboCliente.currentIndex() == 0:
            QMessageBox.critical(self, "Error de Crédito", "Debe seleccionar un cliente para una venta a Crédito.")
            return

        if self.ComboCliente.currentIndex() > 0:
            try:
                # Obtener el idCliente de la tabla Clientes
                cur.execute("""SELECT idCliente FROM Clientes WHERE Nombre || ' ' || Apellido = ?""", (Cliente,))
                resultado = cur.fetchone()
                if resultado:
                    clinteid = resultado[0]
                else:
                    QMessageBox.warning(self, "Cliente no Encontrado",
                                        f"El cliente '{Cliente}' no se encontró en la base de datos.")
                    return
            except Exception as e:
                QMessageBox.critical(self, "Error DB", f"Error al obtener ID del cliente: {e}")
                return

        try:
            # --- PASO 3: Registrar la Venta Principal (Tabla VENTA) ---
            fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cur.execute("""INSERT INTO VENTA(Fecha,TotalVenta,TipoPago,idCliente) VALUES(?, ?, ?, ?)""",
                        (fecha_actual, Totalv, metodo, clinteid))

            ventaid = cur.lastrowid  # Renombre: venta_id -> ventaid
            detalle_ticket = []

            # --- PASO 4 y 5: Procesar Productos, Detalle de Venta y Actualización de Stock ---
            for row in range(self.Tabla.rowCount()):
                codigo_producto = self.Tabla.item(row, 1).text()
                nombre = self.Tabla.item(row, 2).text()
                precio_unitario = float(self.Tabla.item(row, 3).text().replace('$', ''))
                cantidad = int(self.Tabla.item(row, 4).text())
                subtotal = float(self.Tabla.item(row, 5).text().replace('$', ''))

                # CORRECCIÓN: Se corrige la sintaxis SQL de la consulta (faltaba FROM y se duplicaba WHERE)
                cur.execute("""SELECT idProducto FROM Productos WHERE Codigo = ?""", (codigo_producto,))
                resultado_producto = cur.fetchone()

                if resultado_producto is None:
                    raise Exception(f"Producto con código {codigo_producto} no encontrado para detalle de venta.")

                idproducto = resultado_producto[0]  # Renombre: id_producto -> idproducto

                # 4a. Registrar detalle de venta (Tabla Detalles_Ventas)
                cur.execute("""INSERT INTO Detalles_Ventas (idVentas, idProducto, cantidad, PrecioUnitario) 
                                  VALUES (?, ?, ?, ?)""", (ventaid, idproducto, cantidad, precio_unitario))

                # 4b. Actualizar Stock (Tabla Productos)
                cur.execute("UPDATE Productos SET Stock = Stock - ? WHERE Codigo = ?", (cantidad, codigo_producto))

                detalle_ticket.append((nombre, cantidad, precio_unitario, subtotal))

            # --- PASO 6: Manejar Cuentas por Cobrar (Si es Crédito) ---
            if metodo == "Credito":
                cur.execute("""INSERT INTO Cuentas_Por_Cobrar (idVentas, monto_credito, monto_pagado, saldo_pendiente)
                                       VALUES (?, ?, ?, ?)""", (ventaid, Totalv, 0.00, Totalv))

            # CORRECCIÓN: Se usa cur.connection.commit() para ser consistente con el cursor
            cur.connection.commit()

            # --- PASO 7: Generar el Recibo ---
            rutaTicket = CreaTicket(ventaid, metodo, Cliente, Totalv,
                                    detalle_ticket)  # Renombre: ruta_ticket -> rutaTicket
            try:
                sistema = platform.system()
                if sistema == "Windows":
                    # Intenta abrir el archivo con el programa predeterminado
                    os.startfile(rutaTicket)
                elif sistema == "Darwin":  # macOS
                    subprocess.Popen(['open', rutaTicket])
                else:  # Linux y otros (usa xdg-open)
                    subprocess.Popen(['xdg-open', rutaTicket])
            # --- PASO 8: Mensaje de Éxito (Actualizado con nuevos nombres de variables) ---

                QMessageBox.information(self, "Venta Exitosa",
                                    f"Venta #{ventaid} registrada con éxito.\nTotal: ${Totalv:.2f}\nRecibo generado en: {rutaTicket}")
            except Exception as open_error:
                # Si la apertura falla, solo avisa que se guardó.
                QMessageBox.warning(self, "Error al Abrir Ticket",
                                    f"El ticket se guardó en: {rutaTicket}, pero no se pudo abrir automáticamente. Por favor, ábralo manualmente. Error: {open_error}")
            # --- PASO 9: Limpiar la Interfaz ---
            self.Tabla.setRowCount(0)
            self.Etotal.setText("<b>$0.00</b>")
            self.ComboMetodo.setCurrentIndex(0)
            self.ComboCliente.setCurrentIndex(0)
            self.LNCodigo.clear()
            self.SCantidad.setValue(0)

        except Exception as e:
            cur.connection.rollback()
            QMessageBox.critical(self, "Error de Venta", f"No se pudo completar la venta. Transacción revertida: {e}")
    def CambioDEscricion(self):
        self.ComboDescripcionCom1.clear()
        self.ComboDescripcionCom2.clear()
        self.ComboDescripcionCom3.clear()
        self.LDescripcionCom1.clear()
        self.LDescripcionCom2.clear()
        self.LDescripcionCom3.clear()
        if self.TipoCom.currentText() == "Ropa":
            self.LDescripcionCom1.setText("Tallar: ")
            self.ComboDescripcionCom1.addItems(["CH","M","G","ExG"])
            self.LDescripcionCom2.setText("Material: ")
            self.ComboDescripcionCom2.addItems(["Algondon","Seda","Poliéster","Lana","Nylon","Elastano","Rayón","Denim","Franela","Terciopelo","Gabardina"])
            self.LDescripcionCom3.setText("Color: ")
            self.ComboDescripcionCom3.addItems(["Blanco","Negro","Gris","Beige","Azul","Verde","Rojo","Rosa","Amarillo","Morado","Multi Color"])
        elif self.TipoCom.currentText() =="Bolsa":
            self.LDescripcionCom1.setText("Modelo: ")
            self.ComboDescripcionCom1.addItems(["Tote", "Hobo", "Bandolera", "Mochila", "Clutch", "Crossbody"])
            self.LDescripcionCom2.setText("Material: ")
            self.ComboDescripcionCom2.addItems(["Piel", "Tela", "Algodón", "Yute", "Nylon", "Sintético"])
            self.LDescripcionCom3.setText("Tamaño: ")
            self.ComboDescripcionCom3.addItems(["CH", "M", "G", "ExG"])
        elif self.TipoCom.currentText() =="Perfume":
            self.LDescripcionCom1.setText("Aroma: ")
            self.ComboDescripcionCom1.addItems(["Floral", "Amaderado", "Cítrico", "Oriental"," Fougère","Acuático"])
            self.LDescripcionCom2.setText("Volumen(ml): ")
            self.ComboDescripcionCom2.addItems(["30ml", "50ml", "75ml", "100ml","125ml"])
            self.LDescripcionCom3.setText("Concentración: ")
            self.ComboDescripcionCom3.addItems(["Agua de colonia (EdC)", "Agua de colonia (EdT)", "Agua de perfume (EdP)", "Perfume"])
        elif self.TipoCom.currentText() =="Accesorios":
            self.LDescripcionCom1.setText("Material: ")
            self.ComboDescripcionCom1.addItems(["Oro", "Lata", "Cobre", "Bronze"])
            self.LDescripcionCom2.setText("Tipo de Accesorio: ")
            self.ComboDescripcionCom2.addItems(["Collar", "Anillo", "Pulsera", "Aretes","Bufanda","Cinturón","Lentes"])
            self.LDescripcionCom3.setText("Medida / Ajuste: ")
            self.ComboDescripcionCom3.addItems(["Ajustable", "Individual", " S/M", "L/XL","60cm","Anillo"])
    def resource_path(relative_path):
        base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
        return os.path.join(base_path, relative_path)
    ruta_logo = resource_path("Imagen/logo.png")
    ruta_logo2 = resource_path("Imagen/logo2.png")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    try:
        # Verificamos si ya hay datos de la empresa
        cur.execute("SELECT COUNT(*) FROM Configuracion")
        config_existe = cur.fetchone()[0]

        if config_existe > 0:
            ventana = Mainwindow()
        else:
            from Apertura import Apertura

            ventana = Apertura()

        ventana.show()
        sys.exit(app.exec_())
    except Exception as e:
        # Si la tabla ni siquiera existe, mandamos a Apertura
        from Apertura import Apertura

        ventana = Apertura()
        ventana.show()
        sys.exit(app.exec_())