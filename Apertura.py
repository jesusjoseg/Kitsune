from PyQt5 import QtCore,QtGui
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QApplication,QMainWindow,QVBoxLayout,QFileDialog,QLabel,QLineEdit,QComboBox,QPushButton,QMessageBox,QWidget)
from Conexion import con,cur





class Apertura(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Configuración Inicial - Kitsune")
        self.setFixedSize(400,500)
        self.setWindowIcon(QIcon("Imagen/gemini-svg.ico"))
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.Widget= QWidget()
        self.setCentralWidget(self.Widget)
        layout = QVBoxLayout(self.Widget)
        cur.execute("""create TABLE if not EXISTS Configuracion
        (id primary key CHECK(id=1),
            Nombre Text,
            Direcion Text,
            Ciudad Text,
            Telefono Text,
            RFC TEXT,
            Ruta_Logo Text,
            Mensaje_Agradecimiento text);""")
        con.commit()
        self.label = QLabel("<h2>¡Bienvenido a Kitsune!</h2>")
        layout.addWidget(self.label)
        self.Txt_nombre=QLineEdit()
        self.Txt_nombre.setPlaceholderText("Nombre De Tu Empresa")
        layout.addWidget(self.Txt_nombre)
        self.Direcion=QLineEdit()
        self.Direcion.setPlaceholderText("Direcion de Tu Empresa")
        layout.addWidget(self.Direcion)
        self.Ciudad=QLineEdit()
        self.Ciudad.setPlaceholderText("Ciudad y Estados")
        layout.addWidget(self.Ciudad)
        self.Telefono=QLineEdit()
        self.Telefono.setPlaceholderText("Telefono de Tu Empresa")
        layout.addWidget(self.Telefono)
        self.Rfc=QLineEdit()
        self.Rfc.setPlaceholderText("Rfc de Tu Empresa")
        layout.addWidget(self.Rfc)
        self.Logo=QPushButton("Logo de tu Empresa")
        self.LogoText=QLineEdit()
        self.LogoText.setReadOnly(True)
        self.Mensaje = QLineEdit()
        self.Mensaje.setPlaceholderText("Mensaje Para Ticket")
        layout.addWidget(self.Mensaje)
        layout.addWidget(self.Logo)
        layout.addWidget(self.LogoText)
        layout.addWidget(QLabel("El giro de Negocio:"))
        self.cbx_rubro = QComboBox()
        self.cbx_rubro.addItems(["Abarrotes","Boutique","Farmacia","Ferreteria","Otro"])
        layout.addWidget(self.cbx_rubro)
        layout.addSpacing(20)
        self.BotonAper =QPushButton("Finalizar Configuración")
        self.BotonAper.setFixedHeight(50)
        self.BotonAper.setStyleSheet("""
        QPushButton {
                background-color: #f39c12;
                color: white;
                font-size: 16px;
                font-weight: bold;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #e67e22;
            }
            """)

        self.BotonAper.clicked.connect(self.guardar_y_cerrar)
        layout.addWidget(self.BotonAper)
        self.Logo.clicked.connect(self.Cargar_Logo)

    def guardar_y_cerrar(self):
        if self.Txt_nombre.text() == "":
            QMessageBox.warning(self,"Antecion","Ponle un Nombre a tu Negocio")
            return
        self.Aceptar()
    def Aceptar(self):
        nombre = self.Txt_nombre.text()
        Direccion = self.Direcion.text()
        ciudad =self.Ciudad.text()
        Telefono = self.Telefono.text()
        Rfc = self.Rfc.text()
        ruta_logo = self.LogoText.text()
        mensaje = self.Mensaje.text()
        try:
            cur.execute("""
            INSERT OR REPLACE INTO Configuracion
            (id,Nombre,Direcion,Ciudad,Telefono,RFC,Ruta_Logo,Mensaje_Agradecimiento)
             VALUES(1,?,?,?,?,?,?,?)""",(nombre,Direccion,ciudad,Telefono,Rfc,ruta_logo,mensaje))
            con.commit()
            from main import Mainwindow
            self.Nueva_ventana=Mainwindow()
            self.Nueva_ventana.show()
            self.close()
        except Exception as e:
            QMessageBox.critical(self,"Error en la base de dato",f"no se pudo guardar:{e}")
    def Cargar_Logo(self):
        ruta, _ =QFileDialog.getOpenFileName(self, "Seleccionar Logo", "", "Imágenes (*.png *.jpg)")
        if ruta !="":
            self.LogoText.setText(ruta)
if __name__ == "__main__":
    import sys
    # Esto es lo que crea la 'app' que te falta
    app_kitsune = QApplication(sys.argv)
    ventana = Apertura()
    ventana.show()
    sys.exit(app_kitsune.exec_())