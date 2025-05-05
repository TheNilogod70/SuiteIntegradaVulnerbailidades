import subprocess
import re

def ejecutar_nikto(objetivo):
    """
    Ejecuta un escaneo de Nikto en el objetivo especificado.
    
    Args:
        objetivo (str): URL a escanear (debe comenzar con http:// o https://)
        
    Returns:
        str: Resultado del escaneo o mensaje de error
    """
    # Validar que el objetivo no esté vacío
    if not objetivo:
        return "Error: No se proporcionó un objetivo"
    
    # Validar que sea una URL válida
    url_pattern = r'^https?://[a-zA-Z0-9][a-zA-Z0-9-]{1,61}[a-zA-Z0-9]\.[a-zA-Z]{2,}(?:/[^\s]*)?$'
    
    if not re.match(url_pattern, objetivo):
        return "Error: URL inválida. Debe comenzar con http:// o https:// y ser un dominio válido"
    
    try:
        # Ejecutar el comando nikto
        comando = ['nikto', '-h', objetivo]
        resultado = subprocess.run(
            comando,
            capture_output=True,
            text=True,
            check=True
        )
        
        return resultado.stdout
        
    except subprocess.CalledProcessError as e:
        return f"Error al ejecutar Nikto: {e.stderr}"
    except FileNotFoundError:
        return "Error: Nikto no está instalado o no está en el PATH"
    except Exception as e:
        return f"Error inesperado: {str(e)}" 