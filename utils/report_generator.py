import os
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph, Spacer
from reportlab.lib.units import inch

def generar_reporte(datos: dict, ruta_archivo: str):
    """
    Genera un reporte de texto con los resultados de los escaneos.
    
    Args:
        datos (dict): Diccionario con los datos del reporte (comando, timestamp, salida)
        ruta_archivo (str): Ruta completa del archivo de reporte
    """
    # Crear el directorio reports si no existe
    directorio = os.path.dirname(ruta_archivo)
    if not os.path.exists(directorio):
        try:
            os.makedirs(directorio)
        except Exception as e:
            print(f"[ERROR] No se pudo crear el directorio {directorio}: {str(e)}")
            return False
    
    try:
        # Abrir el archivo en modo escritura
        with open(ruta_archivo, 'w', encoding='utf-8') as archivo:
            # Escribir el encabezado del reporte
            archivo.write(f"=== Reporte de Auditoría de Seguridad ===\n")
            archivo.write(f"Fecha y hora: {datos['timestamp']}\n")
            archivo.write(f"Comando ejecutado: {datos['comando']}\n")
            archivo.write("=" * 50 + "\n\n")
            
            # Escribir la salida del comando
            archivo.write(datos['salida'])
            archivo.write("\n" + "=" * 50 + "\n")
        
        print(f"[OK] Reporte escrito exitosamente: {ruta_archivo}")
        return True
        
    except Exception as e:
        print(f"[ERROR] No se pudo escribir el reporte en: {ruta_archivo}")
        print(f"[ERROR] Detalles: {str(e)}")
        return False

def generar_reporte_pdf(datos: dict, ruta_pdf: str):
    """
    Genera un reporte PDF con los resultados de los escaneos.
    
    Args:
        datos (dict): Diccionario con los datos del reporte (comando, timestamp, salida)
        ruta_pdf (str): Ruta completa del archivo PDF
    """
    # Crear el directorio si no existe
    directorio = os.path.dirname(ruta_pdf)
    if not os.path.exists(directorio):
        try:
            os.makedirs(directorio)
        except Exception as e:
            print(f"[ERROR] No se pudo crear el directorio {directorio}: {str(e)}")
            return False

    try:
        # Crear el canvas del PDF
        c = canvas.Canvas(ruta_pdf, pagesize=letter)
        width, height = letter
        
        # Estilos
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=16,
            spaceAfter=30
        )
        normal_style = styles['Normal']
        
        # Título
        title = Paragraph("TdeA - SIDV: Security Audit Report", title_style)
        title.wrapOn(c, width-2*inch, height)
        title.drawOn(c, inch, height-1.5*inch)
        
        # Información del reporte
        info = [
            Paragraph(f"<b>Fecha y hora:</b> {datos['timestamp']}", normal_style),
            Paragraph(f"<b>Comando ejecutado:</b> {datos['comando']}", normal_style),
            Spacer(1, 0.5*inch)
        ]
        
        # Agregar información
        y = height - 2.5*inch
        for item in info:
            item.wrapOn(c, width-2*inch, height)
            item.drawOn(c, inch, y)
            y -= 0.3*inch
        
        # Línea separadora
        c.line(inch, y, width-inch, y)
        y -= 0.5*inch
        
        # Resultados del escaneo
        resultados = Paragraph(f"<b>Resultados del escaneo:</b><br/><br/>{datos['salida']}", normal_style)
        resultados.wrapOn(c, width-2*inch, height)
        resultados.drawOn(c, inch, y-2*inch)
        
        # Guardar el PDF
        c.save()
        print(f"[OK] PDF report saved successfully at {ruta_pdf}")
        return True
        
    except Exception as e:
        print(f"[ERROR] Failed to generate PDF report: {str(e)}")
        return False 