from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import cm, mm
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from datetime import datetime
import os

def CreaTicket(ventaid,metodo,Cleinte,totalventa,detalleTicket):
   TicketAncho = 81 *mm
   alturaLinea = len(detalleTicket)*5*mm
   AlturaBase = 91*mm
   TicketAlto = alturaLinea+AlturaBase
   Caperta = "pdf/Ticker"
   if not os.path.exists(Caperta):
       os.makedirs(Caperta)
   FechaRecibo = datetime.now().strftime("%Y%m%d_%H%M%S")
   Nombre =os.path.join(Caperta,f"Ticket{ventaid} {FechaRecibo}.pdf")
   c = canvas.Canvas(Nombre,pagesize=(TicketAncho,TicketAlto))
   Linea = TicketAlto - 5 * mm
   c.setFont('Helvetica-Bold', 10)
   c.drawCentredString(TicketAncho/2,Linea,"Cuka´s Boutique y Belleza")
   Linea-= 4 * mm
   c.setFont("Helvetica",8)
   c.drawCentredString(TicketAncho/2,Linea,"Francisco I. Madero 222, Baca, 33898")
   Linea -= 3 * mm
   c.drawCentredString(TicketAncho / 2, Linea, "Hidalgo del Parral, Chih.")
   Linea -= 3 * mm
   c.drawCentredString(TicketAncho / 2, Linea, "Tel: 6271066876")
   Linea -= 3 * mm
   c.drawCentredString(TicketAncho/2,Linea,"RFC: CATB780409HN1")
   Linea-= 3 * mm
   c.drawCentredString(TicketAncho / 2, Linea, "________________________________________")
   Linea -= 4 * mm
   c.drawString(5*mm,Linea,f"Fecha:{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
   Linea -= 3 * mm
   c.drawString(5*mm,Linea,f"Venta id: {ventaid}")
   Linea -= 3 * mm
   c.drawString(5*mm,Linea,f"Cliente: {Cleinte}")
   Linea -= 5 * mm
   c.line(5*mm,Linea,TicketAncho- 5 * mm,Linea)
   Linea-= 4 * mm
   c.setFont('Helvetica-Bold', 7)
   c.drawString(5*mm,Linea,"Articulo")
   c.drawString(45 * mm, Linea, "Cant.")
   c.drawString(55 * mm, Linea, "Precio")
   c.drawString(68 * mm, Linea, "SubT")
   Linea -= 4 * mm
   c.setFont('Helvetica', 7)
   for nombre,Cantidad, precio, subtotal in detalleTicket:
       c.drawString(5*mm,Linea,f"{nombre[:20]}...")
       c.drawString(45 * mm, Linea, f"{Cantidad}")
       c.drawString(55 * mm, Linea, f"${precio}")
       c.drawString(68 * mm, Linea, f"${subtotal}")
       Linea -= 4 * mm
   Linea -= 3 * mm
   c.line(5*mm,Linea,TicketAncho - 5 * mm,Linea)
   Linea -= 4 * mm
   c.setFont("Helvetica-Bold",9)
   c.drawString(25*mm,Linea,"Total a Pagar:")
   c.drawString(65 * mm, Linea, f"${totalventa}")
   Linea-= 4 * mm
   c.setFont("Helvetica",8)
   c.drawString(25 * mm, Linea, f"Metodo de Pago: {metodo}")
   Linea-= 7 * mm
   c.setFont('Helvetica-Bold', 7)
   c.drawCentredString(TicketAncho/2,Linea,"¡Gracias por su compra!")
   Linea-= 3 * mm
   c.drawCentredString(TicketAncho / 2, Linea, "Conserve este recibo para cualquier aclaración.=^.w.^=")
   c.showPage()
   c.save()
   return Nombre