import os
from datetime import datetime

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