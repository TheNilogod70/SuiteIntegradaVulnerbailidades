import os
import subprocess
import logging
import shutil
import time
import random
from datetime import datetime
from modules import nmap_module, nikto_module
from utils import report_generator

# Configuración del logging
def configurar_logging():
    """Configura el sistema de logging para la suite."""
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    logging.basicConfig(
        filename='logs/suite.log',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

def crear_setup_sh():
    """
    Crea el archivo setup.sh con el contenido por defecto si no existe.
    """
    contenido = '''#!/bin/bash

# Colores para los mensajes
VERDE='\\033[0;32m'
AMARILLO='\\033[1;33m'
ROJO='\\033[0;31m'
NC='\\033[0m' # No Color

echo -e "${AMARILLO}=== Configuración de la Suite de Auditoría de Seguridad ===${NC}\\n"

# Verificar si el script se está ejecutando como root
if [ "$EUID" -ne 0 ]; then
    echo -e "${ROJO}[!] Este script requiere privilegios de root.${NC}"
    echo -e "${ROJO}[!] Por favor, ejecútelo con sudo.${NC}"
    exit 1
fi

# Verificar e instalar Python3
echo -e "${AMARILLO}[*] Verificando Python3...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${AMARILLO}[*] Instalando Python3...${NC}"
    apt-get update && apt-get install -y python3
else
    echo -e "${VERDE}[+] Python3 ya está instalado.${NC}"
fi

# Verificar e instalar Nmap
echo -e "${AMARILLO}[*] Verificando Nmap...${NC}"
if ! command -v nmap &> /dev/null; then
    echo -e "${AMARILLO}[*] Instalando Nmap...${NC}"
    apt-get update && apt-get install -y nmap
else
    echo -e "${VERDE}[+] Nmap ya está instalado.${NC}"
fi

# Verificar e instalar Nikto
echo -e "${AMARILLO}[*] Verificando Nikto...${NC}"
if ! command -v nikto &> /dev/null; then
    echo -e "${AMARILLO}[*] Instalando Nikto...${NC}"
    apt-get update && apt-get install -y nikto
else
    echo -e "${VERDE}[+] Nikto ya está instalado.${NC}"
fi

# Crear directorios necesarios
echo -e "${AMARILLO}[*] Creando directorios necesarios...${NC}"
mkdir -p logs reports
echo -e "${VERDE}[+] Directorios creados:${NC}"
echo -e "  - logs/"
echo -e "  - reports/"

# Dar permisos de ejecución a main.py
echo -e "${AMARILLO}[*] Configurando permisos de main.py...${NC}"
if [ -f "main.py" ]; then
    chmod +x main.py
    echo -e "${VERDE}[+] Permisos de ejecución otorgados a main.py${NC}"
else
    echo -e "${ROJO}[!] Error: No se encontró el archivo main.py${NC}"
    exit 1
fi

echo -e "\\n${VERDE}[+] Configuración completada exitosamente!${NC}"
'''
    
    try:
        with open('setup.sh', 'w') as f:
            f.write(contenido)
        os.chmod('setup.sh', 0o755)  # Dar permisos de ejecución
        logging.info("Archivo setup.sh creado exitosamente")
        return True
    except Exception as e:
        logging.error(f"Error al crear setup.sh: {str(e)}")
        return False

def ejecutar_setup():
    """
    Ejecuta el script setup.sh con sudo.
    Maneja el caso en que el usuario cancele el prompt de sudo.
    """
    try:
        # Intentar ejecutar setup.sh con sudo
        resultado = subprocess.run(['sudo', 'bash', 'setup.sh'], 
                                 capture_output=True, 
                                 text=True)
        
        if resultado.returncode == 0:
            logging.info("setup.sh ejecutado exitosamente")
            return True
        else:
            logging.warning(f"setup.sh falló con código {resultado.returncode}")
            return False
            
    except subprocess.CalledProcessError as e:
        logging.error(f"Error al ejecutar setup.sh: {str(e)}")
        return False
    except KeyboardInterrupt:
        print("\n[!] Configuración cancelada por el usuario")
        logging.warning("Ejecución de setup.sh cancelada por el usuario")
        return False
    except Exception as e:
        logging.error(f"Error inesperado al ejecutar setup.sh: {str(e)}")
        return False

def validar_nombre_archivo(nombre: str) -> bool:
    """
    Valida que el nombre del archivo sea válido.
    
    Args:
        nombre (str): Nombre del archivo a validar
        
    Returns:
        bool: True si el nombre es válido, False en caso contrario
    """
    if not nombre or not nombre.strip():
        return False
    
    # Caracteres no permitidos en nombres de archivo
    caracteres_invalidos = '<>:"/\\|?*'
    return not any(caracter in nombre for caracter in caracteres_invalidos)

def verificar_dependencias():
    """Verifica que las herramientas necesarias estén instaladas."""
    print("\nVerificando herramientas necesarias...")
    herramientas = {"nmap": "Nmap", "nikto": "Nikto"}
    faltantes = []

    for comando, nombre in herramientas.items():
        if not shutil.which(comando):
            faltantes.append(nombre)

    if faltantes:
        print("\n[!] Faltan las siguientes herramientas:")
        for herramienta in faltantes:
            print(f"  - {herramienta}")
        print("\nInstálelas antes de continuar.")
        logging.error(f"Herramientas faltantes: {', '.join(faltantes)}")
        exit(1)
    else:
        print("[+] Todas las herramientas necesarias están instaladas.")
        logging.info("Todas las herramientas necesarias están instaladas.")

def limpiar_pantalla():
    """Limpia la pantalla de la terminal."""
    os.system('cls' if os.name == 'nt' else 'clear')

def generar_marco_binario(ancho, alto):
    """Genera un marco de 1s y 0s."""
    return ''.join(random.choice('10') for _ in range(ancho * alto))

def mostrar_logo():
    """Muestra el logo de la suite con una animación de números binarios."""
    logo_lines = [
        "  _______ ______ _______            _____ _____ _______     __",
        " |__   __|  ____|  ____| /\\        / ____|_   _|  __ \\ \\   / /",
        "    | |  | |__  | |__   /  \\      | (___   | | | |  | \\ \\_/ /",
        "    | |  |  __| |  __| / /\\ \\      \\___ \\  | | | |  | |\\   /",
        "    | |  | |____| |___/ ____ \\     ____) |_| |_| |__| | | |",
        "    |_|  |______|_____/_/    \\_\\   |_____/|_____|_____/  |_|",
        "",
        "            SISTEMA INTEGRADO DE DETECCIÓN DE VULNERABILIDADES",
        "                          TdeA - SIDV v1.0"
    ]
    
    # Dimensiones del marco
    ancho = 80
    alto = 15
    duracion = 2  # segundos
    fps = 10
    frames = duracion * fps
    
    try:
        for _ in range(frames):
            limpiar_pantalla()
            
            # Generar marco binario
            marco = generar_marco_binario(ancho, 1)
            
            # Imprimir marco superior
            print(marco)
            print()
            
            # Imprimir logo con marcos laterales
            for linea in logo_lines:
                marco_izq = random.choice('10')
                marco_der = random.choice('10')
                print(f"{marco_izq} {linea.center(ancho-4)} {marco_der}")
            
            print()
            # Imprimir marco inferior
            print(marco)
            
            time.sleep(1/fps)
            
    except KeyboardInterrupt:
        pass
    
    finally:
        limpiar_pantalla()
        # Mostrar versión final del logo
        print()
        for linea in logo_lines:
            print(linea.center(ancho))
        print()

def mostrar_barra_progreso(duracion: int = 5):
    """
    Muestra una barra de progreso simulada.
    
    Args:
        duracion (int): Duración en segundos de la simulación
    """
    pasos = 50
    for i in range(pasos + 1):
        porcentaje = (i / pasos) * 100
        barra = "=" * i + ">" + " " * (pasos - i)
        print(f"\r[{barra}] {porcentaje:.0f}%", end="")
        time.sleep(duracion / pasos)
    print()

def ejecutar_comando(comando: str) -> str:
    """
    Ejecuta un comando y captura su salida.
    
    Args:
        comando (str): El comando a ejecutar
        
    Returns:
        str: La salida del comando
    """
    try:
        resultado = subprocess.run(comando, shell=True, capture_output=True, text=True)
        salida = resultado.stdout.strip()
        print(f"\n[DEBUG] Output length: {len(salida)} characters")
        
        if not salida or len(salida) < 10:
            print("\n[!] Warning: No output was captured. The report may be empty.")
            
        return salida
    except Exception as e:
        print(f"\n[!] Error al ejecutar el comando: {str(e)}")
        logging.error(f"Error al ejecutar comando: {str(e)}")
        return ""

def mostrar_reporte(ruta_archivo: str):
    """
    Muestra el contenido de un reporte en la terminal.
    
    Args:
        ruta_archivo (str): Ruta del archivo de reporte
    """
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as f:
            contenido = f.read()
            print("\n=== Contenido del Reporte ===")
            print(contenido)
    except Exception as e:
        print(f"\n[!] Error al leer el reporte: {str(e)}")

def listar_reportes():
    """
    Lista los reportes disponibles y permite seleccionar uno para ver.
    """
    if not os.path.exists('reports'):
        print("\n[!] No hay reportes disponibles.")
        return
        
    reportes = [f for f in os.listdir('reports') if f.endswith('.txt')]
    if not reportes:
        print("\n[!] No hay reportes disponibles.")
        return
        
    print("\n=== Reportes Disponibles ===")
    for i, reporte in enumerate(reportes, 1):
        print(f"{i}. {reporte}")
        
    try:
        seleccion = int(input("\nSeleccione un reporte (número) o 0 para volver: "))
        if seleccion == 0:
            return
        if 1 <= seleccion <= len(reportes):
            mostrar_reporte(os.path.join('reports', reportes[seleccion-1]))
        else:
            print("\n[!] Selección inválida.")
    except ValueError:
        print("\n[!] Por favor ingrese un número válido.")

def mostrar_menu():
    """Muestra el menú principal de la suite."""
    print("\n=== Suite de Auditoría de Seguridad ===")
    print("1. Escanear con Nmap")
    print("2. Analizar con Nikto")
    print("3. Ver Reportes Generados")
    print("4. Salir")

def confirmar_salida() -> bool:
    """
    Solicita confirmación antes de salir del programa.
    
    Returns:
        bool: True si el usuario confirma la salida, False en caso contrario
    """
    respuesta = input("\n¿Está seguro que desea salir? (s/n): ").lower()
    return respuesta == 's'

def ejecutar():
    """Función principal de ejecución de la suite."""
    # Configurar logging
    configurar_logging()
    logging.info("Iniciando suite de auditoría de seguridad")
    
    # Verificar y crear setup.sh si no existe
    if not os.path.exists('setup.sh'):
        print("\n[!] Creando script de configuración...")
        if crear_setup_sh():
            print("[+] Script de configuración creado exitosamente")
        else:
            print("[!] Error al crear el script de configuración")
    
    # Ejecutar setup.sh
    print("\n[!] Ejecutando configuración inicial...")
    if ejecutar_setup():
        print("[+] Configuración completada exitosamente")
    else:
        print("[!] La configuración no se completó correctamente")
        print("[!] Algunas funcionalidades podrían no estar disponibles")
    
    mostrar_logo()
    verificar_dependencias()
    
    while True:
        mostrar_menu()
        opcion = input("\nSeleccione una opción: ")

        if opcion == '1':
            objetivo = input("\nIngrese la IP o dominio objetivo: ")
            logging.info(f"Iniciando escaneo Nmap en {objetivo}")
            
            print("\nIniciando escaneo...")
            mostrar_barra_progreso()
            
            comando = f"nmap -sV -sC {objetivo}"
            salida = ejecutar_comando(comando)
            print("\n=== Resultados del Escaneo ===")
            print(salida)
            
            respuesta = input("\n¿Desea generar un reporte? (s/n): ").lower()
            if respuesta == 's':
                nombre_archivo = input("\nIngrese el nombre del archivo de reporte: ")
                if validar_nombre_archivo(nombre_archivo):
                    datos = {
                        "comando": comando,
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "salida": salida
                    }
                    ruta_reporte = f"reports/{nombre_archivo}.txt"
                    report_generator.generar_reporte(datos, ruta_reporte)
                    print(f"\n[+] Reporte generado: {os.path.abspath(ruta_reporte)}")
                    print("Informe guardado correctamente. Pulse M para volver al menú principal.")
                    while True:
                        tecla = input().lower()
                        if tecla == 'm':
                            break
                else:
                    print("\n[!] Nombre de archivo inválido. No use caracteres especiales.")

        elif opcion == '2':
            objetivo = input("\nIngrese el dominio objetivo (con http/https): ")
            logging.info(f"Iniciando escaneo Nikto en {objetivo}")
            
            print("\nIniciando escaneo...")
            mostrar_barra_progreso()
            
            comando = f"nikto -h {objetivo}"
            salida = ejecutar_comando(comando)
            print("\n=== Resultados del Escaneo ===")
            print(salida)
            
            respuesta = input("\n¿Desea generar un reporte? (s/n): ").lower()
            if respuesta == 's':
                nombre_archivo = input("\nIngrese el nombre del archivo de reporte: ")
                if validar_nombre_archivo(nombre_archivo):
                    datos = {
                        "comando": comando,
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "salida": salida
                    }
                    ruta_reporte = f"reports/{nombre_archivo}.txt"
                    report_generator.generar_reporte(datos, ruta_reporte)
                    print(f"\n[+] Reporte generado: {os.path.abspath(ruta_reporte)}")
                    print("Informe guardado correctamente. Pulse M para volver al menú principal.")
                    while True:
                        tecla = input().lower()
                        if tecla == 'm':
                            break
                else:
                    print("\n[!] Nombre de archivo inválido. No use caracteres especiales.")

        elif opcion == '3':
            listar_reportes()

        elif opcion == '4':
            if confirmar_salida():
                print("\nSaliendo de la suite. ¡Hasta pronto!")
                logging.info("Suite finalizada por el usuario")
                break
            else:
                print("\nContinuando con la suite...")
                continue

        else:
            print("\n[!] Opción no válida. Intente de nuevo.")
            logging.warning(f"Opción inválida seleccionada: {opcion}")

if __name__ == "__main__":
    ejecutar()
