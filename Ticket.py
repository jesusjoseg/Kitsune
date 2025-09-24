from reportlab.lib.pagesizes import letter
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from datetime import datetime
import os

from scipy.cluster.hierarchy import int_floor

recibo = datetime.now()
def CreaTicket():
    tickeDir = "pdf/Ticker"
    os.makedirs(tickeDir,exist_ok=True)
    h,w = letter
    fecha = str(recibo)
    fecha = fecha.replace("."," ")
    fecha = fecha.replace(":","-")
    filepacht = os.path.join(tickeDir, f"ticker{fecha}.pdf")
    c =canvas.Canvas(filepacht,letter)
    c.setFont("Helvetica",11)
    c.drawString(49, h - 49, "Cuka Boutique")
    c.drawString(49, h - 65, f"Fecha: {datetime.now()}")
    #c.drawString(49, h - 80, f"Hora: {recibo_dt.strftime('%H:%M:%S')}")
    c.drawString(49, h - 100, "Gracias por su compra.")
    c.save()
if __name__ == "__main__":
        CreaTicket()