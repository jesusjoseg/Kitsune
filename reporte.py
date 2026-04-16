import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Image,SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch
from datetime import date


# -----------------------------------------------------
# 1. Función de CÁLCULO Y EXTRACCIÓN DE DETALLES
# -----------------------------------------------------

# Reporte.py - FUNCIÓN OBTENER DATOS (CORREGIDA)

def obtener_datos_reporte(fecha_str, con):
    """
    Calcula y devuelve los detalles de Venta, Compra y el Capital para la fecha.
    """
    cur = con.cursor()

    # --- 1. Detalle y Total de Ventas ---
    cur.execute(
        """
        SELECT 
            DV.cantidad,                      -- Columna en Detalles_Ventas
            P.Nombre AS Producto,             -- Nombre del Producto
            (DV.cantidad * DV.PrecioUnitario), -- SubTotal (calculado)
            V.TotalVenta 
        FROM Detalles_Ventas DV
        JOIN VENTA V ON DV.idVentas = V.idVentas  -- <--- CORRECCIÓN DE ID
        JOIN Productos P ON DV.idProducto = P.idProducto  -- <--- CORRECCIÓN DE ID
        WHERE strftime('%Y-%m-%d', V.Fecha) = ?
        ORDER BY P.Nombre
        """,
        (fecha_str,)
    )
    detalle_ventas = cur.fetchall()

    # Calcular Total Venta
    cur.execute(
        "SELECT SUM(TotalVenta) FROM VENTA WHERE strftime('%Y-%m-%d', Fecha) = ?",
        (fecha_str,)
    )
    total_ventas = cur.fetchone()[0] or 0.0

    # --- 2. Detalle y Total de Compras ---
    cur.execute(
        """
        SELECT 
            P.Nombre AS Producto, 
            DC.Cantidad,                      -- Columna en Detalles_Compra
            DC.PrecioCom,                     -- Precio por unidad al comprar
            C.MontCompra
        FROM Detalles_Compra DC
        JOIN COMPRA C ON DC.idCompra = C.idCompra  -- <--- CORRECCIÓN DE ID
        JOIN Productos P ON DC.idProducto = P.idProducto  -- <--- CORRECCIÓN DE ID
        WHERE strftime('%Y-%m-%d', C.Fecha) = ?
        ORDER BY P.Nombre
        """,
        (fecha_str,)
    )
    detalle_compras = cur.fetchall()

    # Calcular Total Compra
    cur.execute(
        "SELECT SUM(MontCompra) FROM COMPRA WHERE strftime('%Y-%m-%d', Fecha) = ?",
        (fecha_str,)
    )
    total_compras = cur.fetchone()[0] or 0.0

    # --- 3. Cálculo del Capital ---
    # FÓRMULA SOLICITADA: Venta + Compra
    capital_bruto = total_ventas - total_compras

    # Devolvemos un diccionario con todos los datos
    return {
        "fecha": fecha_str,
        "detalle_ventas": detalle_ventas,
        "total_ventas": total_ventas,
        "detalle_compras": detalle_compras,
        "total_compras": total_compras,
        "capital_bruto": capital_bruto
    }

# -----------------------------------------------------
# 2. Función de GENERACIÓN DE PDF
# -----------------------------------------------------

def generar_reporte_pdf(datos_reporte):
    """
    Genera un PDF usando los detalles y totales calculados,
    con un encabezado que incluye una imagen junto al título.
    """
    from Conexion import cur,con
    fecha_str = datos_reporte["fecha"]

    Reportedir = "pdf/Reporte"
    os.makedirs(Reportedir, exist_ok=True)
    nombre_archivo = f"Reporte_{fecha_str}.pdf"
    filepath = os.path.join(Reportedir, nombre_archivo)

    # Configuración del documento PDF
    doc = SimpleDocTemplate(filepath, pagesize=letter,
                            topMargin=0.5 * inch, bottomMargin=0.5 * inch)
    styles = getSampleStyleSheet()
    Story = []

    # ----------------------------------------
    # ENCABEZADO CON IMAGEN Y TÍTULO
    # ----------------------------------------
    # Ruta de la imagen del logo (asegúrate de que exista)
    cur.execute("""SELECT Ruta_Logo
                   FROM Configuracion;""")
    Logo = cur.fetchone()
    ImagenLogo=Logo[0] if Logo else "Imagen/logo.png"
    ruta_logo = f"{ImagenLogo}"  # Ejemplo: archivo dentro de la carpeta del script

    if os.path.exists(ruta_logo):
        logo = Image(ruta_logo, width=1.0 * inch, height=1.0 * inch)
    else:
        logo = Paragraph("<b>[LOGO]</b>", styles['Normal'])  # Por si no hay imagen
    cur.execute("""SELECT Nombre FROM Configuracion;""")
    Resultado= cur.fetchone()
    datosEmpresa= Resultado[0] if Resultado else "Empresa"
    titulo = Paragraph(f"<b>REPORTE DIARIO DE {datosEmpresa}</b>", styles['Title'])

    # Usamos una tabla para colocar imagen y texto uno al lado del otro
    encabezado = Table([[logo, titulo]], colWidths=[1.2 * inch, 5.8 * inch])
    encabezado.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (1, 0), (1, 0), 'CENTER'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))

    Story.append(encabezado)
    Story.append(Spacer(1, 6))
    Story.append(Paragraph(f"Fecha del Reporte: <b>{fecha_str}</b>", styles['Heading2']))
    Story.append(Spacer(1, 18))

    # ----------------------------------------
    # 1. TABLA DE VENTAS
    # ----------------------------------------
    Story.append(Paragraph("<b>1. DETALLE DE VENTAS</b>", styles['h3']))
    Story.append(Spacer(1, 6))
    detalle_ventas = datos_reporte["detalle_ventas"]
    data_ventas = [["Cant.", "Producto", "Sub Total", "Total Venta"]]

    for row in detalle_ventas:
        data_ventas.append([
            str(row[0]),
            row[1],
            f"${row[2]:,.2f}",
            f"${row[3]:,.2f}"
        ])

    t_ventas = Table(data_ventas, colWidths=[0.5 * inch, 3.0 * inch, 1.0 * inch, 1.0 * inch])
    t_ventas.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkgreen),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('ALIGN', (1, 1), (1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
    ]))
    Story.append(t_ventas)
    Story.append(Spacer(1, 18))

    # ----------------------------------------
    # 2. TABLA DE COMPRAS
    # ----------------------------------------
    Story.append(Paragraph("<b>2. DETALLE DE COMPRAS</b>", styles['h3']))
    Story.append(Spacer(1, 6))
    detalle_compras = datos_reporte["detalle_compras"]
    data_compras = [["Producto", "Cant.", "Precio Compra", "Total Compra"]]

    for row in detalle_compras:
        data_compras.append([
            row[0],
            str(row[1]),
            f"${row[2]:,.2f}",
            f"${row[3]:,.2f}"
        ])

    t_compras = Table(data_compras, colWidths=[3.0 * inch, 0.5 * inch, 1.0 * inch, 1.0 * inch])
    t_compras.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkred),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('ALIGN', (0, 1), (0, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
    ]))
    Story.append(t_compras)
    Story.append(Spacer(1, 24))

    # ----------------------------------------
    # 3. RESUMEN DE CAPITAL
    # ----------------------------------------
    Story.append(Paragraph("<b>3. RESUMEN DE CAPITAL</b>", styles['h2']))
    Story.append(Spacer(1, 12))

    data_capital = [
        ["MÉTRICA", "VALOR"],
        ["Total de Ventas", f"${datos_reporte['total_ventas']:,.2f}"],
        ["Total de Compras", f"${datos_reporte['total_compras']:,.2f}"],
        ["Ganacias BRUTO (Venta - Compra)", f"${datos_reporte['capital_bruto']:,.2f}"],
    ]

    t_capital = Table(data_capital, colWidths=[200, 100])
    t_capital.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 3), (-1, 3), 'Helvetica-Bold'),
        ('TEXTCOLOR', (0, 3), (-1, 3), colors.red),
    ]))
    Story.append(t_capital)
    Story.append(Spacer(1, 24))

    # Construir el PDF
    doc.build(Story)

    return filepath