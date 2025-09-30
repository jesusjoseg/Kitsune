import os
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate,Table,TableStyle,paragraph,Spacer
from reportlab.lib.styles import getSampleStyleSheet
from datetime import date


hoy = date.today()
def Reporte():
    h,w =letter
    Reportedir = "pdf/Reporte"
    os.makedirs(Reportedir,exist_ok=True)
    filepathc =os.path.join(Reportedir,f"Reporte{hoy}.pdf")
    c = canvas.Canvas(filepathc,letter)
    c.drawString(49,h-49,f"Reporte del dia de: {hoy}",1)
    c.save()

if __name__ == "__main__":
    Reporte()
