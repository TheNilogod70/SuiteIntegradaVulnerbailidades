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

def mostrar_menu():
    """Muestra el menú principal de la suite."""
    print("\n=== Suite de Auditoría de Seguridad ===")
    print("1. Escanear con Nmap")
    print("2. Analizar con Nikto")
    print("3. Generar Reporte")
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
    
    mostrar_logo()
    verificar_dependencias()
    
    resultados = []
    while True:
        mostrar_menu()
        opcion = input("\nSeleccione una opción: ")

        if opcion == '1':
            objetivo = input("\nIngrese la IP o dominio objetivo: ")
            logging.info(f"Iniciando escaneo Nmap en {objetivo}")
            resultado = nmap_module.ejecutar_nmap(objetivo)
            resultados.append(("Nmap", resultado))
            logging.info("Escaneo Nmap completado")

        elif opcion == '2':
            objetivo = input("\nIngrese el dominio objetivo (con http/https): ")
            logging.info(f"Iniciando escaneo Nikto en {objetivo}")
            resultado = nikto_module.ejecutar_nikto(objetivo)
            resultados.append(("Nikto", resultado))
            logging.info("Escaneo Nikto completado")

        elif opcion == '3':
            if not resultados:
                print("\n[!] No hay resultados para generar el reporte.")
                logging.warning("Intento de generar reporte sin resultados")
                continue
                
            nombre_archivo = input("\nIngrese el nombre del archivo de reporte: ")
            if not validar_nombre_archivo(nombre_archivo):
                print("\n[!] Nombre de archivo inválido. No use caracteres especiales.")
                logging.error(f"Nombre de archivo inválido: {nombre_archivo}")
                continue
                
            logging.info(f"Generando reporte: {nombre_archivo}")
            mensaje = report_generator.generar_reporte(resultados, nombre_archivo)
            print(f"\n{mensaje}")
            logging.info(f"Reporte generado: {nombre_archivo}")

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
