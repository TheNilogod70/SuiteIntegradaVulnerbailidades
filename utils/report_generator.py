import os
from datetime import datetime

def generar_reporte(resultados: list, nombre_archivo: str):
    """
    Genera un reporte de texto con los resultados de los escaneos.
    
    Args:
        resultados (list): Lista de tuplas (herramienta, resultado)
        nombre_archivo (str): Nombre del archivo de reporte (sin extensión)
    """
    # Crear el directorio reports si no existe
    if not os.path.exists('reports'):
        os.makedirs('reports')
    
    # Obtener la fecha y hora actual
    fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Crear el nombre completo del archivo
    nombre_completo = os.path.join('reports', f"{nombre_archivo}.txt")
    
    try:
        # Abrir el archivo en modo escritura
        with open(nombre_completo, 'w', encoding='utf-8') as archivo:
            # Escribir el encabezado del reporte
            archivo.write(f"=== Reporte de Auditoría de Seguridad ===\n")
            archivo.write(f"Fecha y hora: {fecha_actual}\n")
            archivo.write("=" * 50 + "\n\n")
            
            # Escribir los resultados de cada herramienta
            for herramienta, resultado in resultados:
                archivo.write(f"=== Resultados de {herramienta} ===\n")
                archivo.write(resultado)
                archivo.write("\n" + "=" * 50 + "\n\n")
                
        return f"Reporte generado exitosamente: {nombre_completo}"
        
    except Exception as e:
        return f"Error al generar el reporte: {str(e)}" 