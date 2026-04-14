from PyQt5 import QtWidgets,QtCore,QtGui
from PyQt5.QtWidgets import QMainWindow
from datashader import layout


class Apertura(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Configuración Inicial - Kitsune")
        self.setFixedSize(400,500)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        layout = QtWidgets.QVBoxLayout()

        self.label = QtWidgets.QLabel("<h2>¡Bienvenido a Kitsune!</h2>")
        self.Txt_nombre=QtWidgets.QLineEdit()
        self.Txt_nombre.setPlaceholderText("Nombre De Tu Empresa")
        layout.addWidget(self.Txt_nombre)
        layout.addWidget(QtWidgets.QLabel("El giro de Negocio:"))
        self.cbx_rubro = QtWidgets.QComboBox()
        self.cbx_rubro.addItems(["Abarrotes","Boutique","Farmacia","Ferreteria","Otro"])
        layout.addWidget(self.cbx_rubro)
        layout.addSpacing(20)
        layout