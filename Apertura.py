from PyQt5 import QtCore,QtGui
from PyQt5.QtWidgets import (QMainWindow,QVBoxLayout,QLabel,QLineEdit,QComboBox,QPushButton,QMessageBox)

class Apertura(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Configuración Inicial - Kitsune")
        self.setFixedSize(400,500)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        layout = QVBoxLayout()

        self.label = QLabel("<h2>¡Bienvenido a Kitsune!</h2>")
        self.Txt_nombre=QLineEdit()
        self.Txt_nombre.setPlaceholderText("Nombre De Tu Empresa")
        layout.addWidget(self.Txt_nombre)
        layout.addWidget(QLabel("El giro de Negocio:"))
        self.cbx_rubro = QComboBox()
        self.cbx_rubro.addItems(["Abarrotes","Boutique","Farmacia","Ferreteria","Otro"])
        layout.addWidget(self.cbx_rubro)
        layout.addSpacing(20)
        self.BotonAper =QPushButton("Aceptar")
        self.BotonAper.setFixedHeight(40)
        self.BotonAper.clicked.connect(self.Aceptar)
        layout.addWidget(self.BotonAper)

    def guardar_y_cerrar(self):
        if self.Txt_nombre.text() == "":
            QMessageBox.warning(self,"Antecion","Ponle un Nombre a tu Negocio")
            return
        self.Aceptar()