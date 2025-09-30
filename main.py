from io import BytesIO
import requests
from PIL.Image import Image
from PyQt5.QtCore import QTimer,QSize,QDate
from PyQt5.QtGui import QIcon,QFont
from PyQt5.QtWidgets import (QWidget, QApplication,QPushButton,QLabel, QMainWindow,
                             QVBoxLayout,QHBoxLayout,QTabWidget,QMenuBar ,QComboBox,
                             QLineEdit,QRadioButton,QTableWidget,QSpinBox,QDoubleSpinBox,
                             QFileDialog,QDateEdit,QTableWidgetItem)
import sys
#from PyQt5.uic.Compiler.qtproxies import QtGui
#from win32con import VER_PLATFORM_WIN32_NT
import os
import io
from Conexion import con,cur
from PIL import Image
import mimetypes


class Mainwindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.tab = QTabWidget()
        #self.setStyleSheet("background-color: black")#  #este codigo es ara cambia el color de background
        self.setCentralWidget(self.tab)
        self.Widget = QWidget()
        self.Widget1 = QWidget()
        self.Widget2 = QWidget()
        self.Widget3 = QWidget()
        self.Widget4 = QWidget()
        self.Widget5 = QWidget()
        #self.setStyleSheet("QLabel {color: white}")
        layout = QVBoxLayout()
        self.setWindowTitle("no tengo nada")
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
    def DescargaImagen(self):
        FileImagen="Imagen/Download"
        os.makedirs(FileImagen,exist_ok=True)
        url = self.LineImagen.text()
        NombreImage = self.LENombreIn.text()
        try:
            descargar = requests.get(url,stream=True)
            descargar.raise_for_status()
            codificado = descargar.headers.get('content-type')
            extesion = mimetypes.guess_extension(codificado)
            Contenido = descargar.content
            if extesion ==".webp":
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
        ventanaCliente= QVBoxLayout()
        HoriazontalClien2=QHBoxLayout()
        Etiqueta1=QLabel("<b>Clientes<b>")
        NombreRe= QLabel("Nombre: ")
        ComboCliente2=QComboBox()
        HoriazontalClien2.addWidget(NombreRe)
        HoriazontalClien2.addWidget(ComboCliente2)
        ventanaCliente.addWidget(Etiqueta1)
        ventanaCliente.addLayout(HoriazontalClien2)
        self.Widget4.setLayout(ventanaCliente)
    def Reporte(self):
        VentanaReporte =QVBoxLayout()
        HorizontalRE = QHBoxLayout()
        LReporte = QLabel("<b>Reporte<b>")
        LReporte.setFont(QFont("Arial",12))
        DateReporte =QDateEdit()
        DateReporte.setCalendarPopup(True)
        DateReporte.setDate(QDate.currentDate())
        self.ButtonReporte =QPushButton("Crea Reporte")
        self.TablaRe = QTableWidget(0,2)
        self.TablaRe.setHorizontalHeaderLabels(["Fecha","Reporte"])
        HorizontalRE.addWidget(LReporte)
        HorizontalRE.addWidget(DateReporte)
        HorizontalRE.addWidget(self.ButtonReporte)
        VentanaReporte.addLayout(HorizontalRE)
        VentanaReporte.addWidget(self.TablaRe)
        self.Widget5.setLayout(VentanaReporte)
# Esto es para crea toda las tabla de la base de dato
    def CreaTabla(self):
        cur.execute("""Create table if not exists Tipo(idTipo INTEGER PRIMARY KEY AUTOINCREMENT, 
        Tipo Text not null unique)""")
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
        #cur.execute()
        #cur.execute()
        cur.execute("""INSERT OR IGNORE INTO Tipo (Tipo) VALUES ('Ropa'); """)
        cur.execute("""INSERT OR IGNORE INTO Tipo (Tipo) VALUES ('Bolsa');""")
        cur.execute("""INSERT OR IGNORE INTO Tipo (Tipo) VALUES ('Perfume');""")
        cur.execute("""INSERT OR IGNORE INTO Tipo (Tipo) VALUES ('Accesorios');""")
        con.commit()
#Esto es la esctutura de la ventana de ventas
    def venta(self):
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
        Etotal =QLabel("<b>$0.00</b>")
        #Etotal.
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
        horizon2.addWidget(Etotal)
        horizon2.addWidget(EMetodo)
        horizon2.addWidget(self.ComboMetodo)
        horizon2.addWidget(ECliente)
        horizon2.addWidget(self.ComboCliente)
        self.ButtonVenta = QPushButton("Regristra Venta")
        vent_ventas.addWidget(self.Tabla)
        vent_ventas.addLayout(horizon2)
        vent_ventas.addWidget(self.ButtonVenta)
        self.Widget.setLayout(vent_ventas)
        self.ButtonVenta.clicked.connect(self.Conexion)
    def Compras(self):
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
        #LDescripcionCom2 = QLabel()
        #LDescripcionCom3 = QLabel()
        self.ComboDescripcionCom1 = QComboBox()
        self.ComboDescripcionCom2 = QComboBox()
        self.ComboDescripcionCom3 = QComboBox()
        HorizontalCom4.addWidget(LDescripcionCom)
        HorizontalCom4.addWidget(self.LDescripcionCom1)
        HorizontalCom4.addWidget(self.ComboDescripcionCom1)
        HorizontalCom4.addWidget(self.ComboDescripcionCom2)
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
        #FileIMagen =QFileDialog()
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
        SStrock  =QSpinBox()
        HorizontaInve8.addWidget(LStrock)
        HorizontaInve8.addWidget(SStrock)
        HorizontaInve9 = QHBoxLayout()
        self.ButtonActulizar =QPushButton("Actualizar")
        self.ButtonNuevo = QPushButton("Nuevo/Limpiar")#se encargar de limiar el formulario
        self.ButtonEliminar = QPushButton("Eliminar")
        HorizontaInve9.addWidget(self.ButtonActulizar)
        HorizontaInve9.addWidget(self.ButtonNuevo)
        HorizontaInve9.addWidget(self.ButtonEliminar)
        #Aqui Va la tabla de todo los productos
        self.TablaInvertario =QTableWidget(0,8)
        self.TablaInvertario.setHorizontalHeaderLabels(["Codigo","Imagen","Nombre","Marca","Tipo","Precio Venta","Precio Compra","Stock"])
        Vent_Invectstio.addLayout(HorizontaInve1)
        Vent_Invectstio.addLayout(HorizontaInve2)
        Vent_Invectstio.addLayout(HorizontaInve3)
        Vent_Invectstio.addLayout(HorizontaInve4)
        Vent_Invectstio.addLayout(HorizontaInve5)
        Vent_Invectstio.addLayout(HorizontaInve6)
        Vent_Invectstio.addLayout(HorizontaInve7)
        Vent_Invectstio.addLayout(HorizontaInve8)
        Vent_Invectstio.addLayout(HorizontaInve9)
        Vent_Invectstio.addWidget(self.TablaInvertario)
        self.Widget2.setLayout(Vent_Invectstio)
        self.ButtonFIle.clicked.connect(self.FileDialogo)
        self.ButtonActulizar.clicked.connect(self.Actulizarproducto)
    def FileDialogo(self):
        pass
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
        if self.ComboImagen.currentIndex(0):
            CodigoImagen = self.LNCodigoIn.text()
            self.DescargaImagen()
            UrlImagen =f"Imagen/Download/{CodigoImagen}.png"
        elif self.ComboImagen.currentIndex(1):
            UrlImagen = self.LineImagen.text()
        cur.execute("""INSERT INTO """)
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
            ["$2,000.00", "$3,000.00", "$4,000.00", "$5,000.00", "$6,000.00", "$7,000.00", "$8,000.00", "$9,000.00",
             "$10,000.00"])
        HorizontalCliente6.addWidget(LCantidaC)
        HorizontalCliente6.addWidget(self.Cantida)
        Etiquetas = QLabel("<b>Regristo de clientes</b>")
        Etiquetas.setFont(QFont("Arial",12))
        self.TablaCliente =QTableWidget(0,6)
        self.TablaCliente.setHorizontalHeaderLabels(["Nombre","Apellido","Telefono","Direcion","Refrerencia","Cantida"])
        cur.execute("select Nombre,Apellido,Telefono,Direccion,Referencias,Cantidad from clientes ")
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
        cur.execute("select Nombre,Apellido,Telefono,Direccion,Referencias,Cantidad from clientes ")
        Tabla = cur.fetchall()
        numFila = len(Tabla)
        self.TablaCliente.setRowCount(numFila)
        for Valorfila, regristo in enumerate(Tabla):
            for ValorColumna, Valoew in enumerate(regristo):
                tablaValores = QTableWidgetItem(str(Valoew))
                self.TablaCliente.setItem(Valorfila, ValorColumna, tablaValores)

    def Conexion(self):#este codigo sirve para verdifica la funcionalida de botones (borra despuses)
        x = 404
        print("no hay codigo erro",x)
    def CambioDEscricion(self):
        self.ComboDescripcionCom1.clear()
        self.LDescripcionCom1.clear()
        if self.TipoCom.currentText() == "Ropa":
            self.LDescripcionCom1.setText("Tallar: ")
            self.ComboDescripcionCom1.addItems(["CH","M","G","ExG"])
            self.ComboDescripcionCom2.addItems(["CH","M","G","ExG"])
            self.ComboDescripcionCom3.addItems(["CH","M","G","ExG"])
        elif self.TipoCom.currentText() =="Bolsa":
            self.LDescripcionCom1.setText("Material: ")
            self.ComboDescripcionCom2.addItems(["CH", "M", "G", "ExG"])
            self.ComboDescripcionCom3.addItems(["CH", "M", "G", "ExG"])
            self.ComboDescripcionCom1.addItems(["piel", "tela", "Algodón", "Yute"])
        elif self.TipoCom.currentText() =="Perfume":
            self.LDescripcionCom1.setText("Material: ")
            self.ComboDescripcionCom2.addItems(["CH", "M", "G", "ExG"])
            self.ComboDescripcionCom3.addItems(["CH", "M", "G", "ExG"])
            self.ComboDescripcionCom1.addItems(["piel", "tela", "Algodón", "Yute"])
        elif self.TipoCom.currentText() =="Accesorios":
            self.LDescripcionCom1.setText("Material: ")
            self.ComboDescripcionCom1.addItems(["Oro", "Lata", "Cobre", "Bronze"])
            self.ComboDescripcionCom2.addItems(["piel", "tela", "Algodón", "Yute"])
            self.ComboDescripcionCom3.addItems(["CH", "M", "G", "ExG"])

app = QApplication(sys.argv)
app.setWindowIcon(QIcon("main_0e7c6a33-3a9d-403c-99c6-235aaa786b1d.jpg"))
window = Mainwindow()
window.show()
sys.exit(app.exec())