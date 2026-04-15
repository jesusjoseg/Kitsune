from PyQt5 import QtCore,QtGui
from PyQt5.QtWidgets import (QMainWindow,QVBoxLayout,QFileDialog,QLabel,QLineEdit,QComboBox,QPushButton,QMessageBox,QWidget)
from Conexion import con,cur


class Apertura(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Configuración Inicial - Kitsune")
        self.setFixedSize(400,500)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.Widget= QWidget()
        self.setCentralWidget(self.Widget)
        layout = QVBoxLayout(self.Widget)

        self.label = QLabel("<h2>¡Bienvenido a Kitsune!</h2>")
        layout.addWidget(self.label)
        self.Txt_nombre=QLineEdit()
        self.Txt_nombre.setPlaceholderText("Nombre De Tu Empresa")
        layout.addWidget(self.Txt_nombre)
        self.Direcion=QLineEdit()
        self.Direcion.setPlaceholderText("Direcion de Tu Empresa")
        layout.addWidget(self.Direcion)
        self.Telefono=QLineEdit()
        self.Telefono.setPlaceholderText("Telefono de Tu Empresa")
        layout.addWidget(self.Telefono)
        self.Rfc=QLineEdit()
        self.Rfc.setPlaceholderText("Rfc de Tu Empresa")
        layout.addWidget(self.Rfc)
        self.Logo=QPushButton("Logo de tu Empresa")
        self.LogoText=QLineEdit()
        self.LogoText.isModified()
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

    def guardar_y_cerrar(self):
        if self.Txt_nombre.text() == "":
            QMessageBox.warning(self,"Antecion","Ponle un Nombre a tu Negocio")
            return
        self.Aceptar()
    def Aceptar(self):
        nombre = self.Txt_nombre.text()
        cbx_rubro = self.cbx_rubro.currentText()

        try:
            from main import Mainwindow
            self.Nueva_ventana=Mainwindow()
            self.Nueva_ventana.show()
            self.close()
        except Exception as e:
            QMessageBox.critical(self,"",f"{e}")