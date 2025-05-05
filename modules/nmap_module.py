import subprocess
import re

def ejecutar_nmap(objetivo):
    """
    Ejecuta un escaneo básico de Nmap en el objetivo especificado.
    
    Args:
        objetivo (str): IP o dominio a escanear
        
    Returns:
        str: Resultado del escaneo o mensaje de error
    """
    # Validar el formato del objetivo
    if not objetivo:
        return "Error: No se proporcionó un objetivo"
    
    # Patrón para validar IP o dominio
    ip_pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
    domain_pattern = r'^[a-zA-Z0-9][a-zA-Z0-9-]{1,61}[a-zA-Z0-9]\.[a-zA-Z]{2,}$'
    
    if not (re.match(ip_pattern, objetivo) or re.match(domain_pattern, objetivo)):
        return "Error: Formato de objetivo inválido. Debe ser una IP o dominio válido"
    
    try:
        # Ejecutar el comando nmap
        comando = ['nmap', '-sV', '-T4', objetivo]
        resultado = subprocess.run(
            comando,
            capture_output=True,
            text=True,
            check=True
        )
        
        return resultado.stdout
        
    except subprocess.CalledProcessError as e:
        return f"Error al ejecutar Nmap: {e.stderr}"
    except FileNotFoundError:
        return "Error: Nmap no está instalado o no está en el PATH"
    except Exception as e:
        return f"Error inesperado: {str(e)}" 