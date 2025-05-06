# Suite Integrada de Auditoría de Vulnerabilidades (TdeA - SIDV)

Esta suite permite realizar auditorías de seguridad básicas usando herramientas como Nmap y Nikto, centralizando los resultados en reportes organizados. Incluye una barra de progreso, un sistema de reportes, verificación de dependencias automática y se ejecuta directamente en entornos Linux con Bash.

## ✅ Requisitos del Sistema

- **Sistema operativo:** Kali Linux o cualquier distribución basada en Debian
- **Entorno:** Terminal Bash (no funciona en CMD ni PowerShell)
- **Interfaz:** CLI (línea de comandos)
- **Usuario:** Debe tener permisos sudo o root para ejecutar setup.sh

### Dependencias:
- Python 3
- Nmap
- Nikto

## 🚀 Instalación y Uso

1. Clonar el repositorio:

   ```bash
   git clone https://github.com/TheNilogod70/SuiteIntegradaVulnerbailidades.git
   ```

2. Ingresar al directorio del proyecto:

   ```bash
   cd SuiteIntegradaVulnerbailidades
   ```

3. Ejecutar la suite (se autoconfigura al inicio):

   ```bash
   python3 main.py
   ```

   🔐 **NOTA:** Se solicitará contraseña sudo al correr el setup automáticamente.

## ⚙️ Cómo funciona

- Al iniciar, verifica e instala automáticamente herramientas requeridas
- Muestra un logo de bienvenida animado
- Presenta un menú con 4 opciones:
   1. Escanear con Nmap
   2. Analizar con Nikto
   3. Ver reportes generados
   4. Salir
- Al realizar un análisis, se muestra una barra de progreso
- Finalizado el escaneo, puedes generar un reporte que se guarda en la carpeta `reports/`
- Los reportes pueden visualizarse directamente desde la suite

## 📘 Manual del Usuario

- Ejecuta la suite con permisos adecuados (sudo si se solicita)
- Usa dominios válidos (http:// o https://) para Nikto y direcciones IP o dominios para Nmap
- Para generar reportes, usa nombres simples, sin caracteres especiales
- Para ver reportes anteriores, elige la opción 3 del menú

## 📝 Notas Adicionales

- No se requiere conexión a internet para escanear IPs locales
- Los reportes son archivos `.txt` que pueden abrirse desde cualquier editor de texto
- El script `setup.sh` se genera automáticamente si no existe

## 👨‍💻 Créditos y Licencia

- Desarrollado por: TheNilogod70
- Licencia: MIT 