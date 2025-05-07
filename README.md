# 🛡️ TdeA - SIDV: Suite Integrada de Detección de Vulnerabilidades

**Versión:** 1.7 BETA  
**Desarrollado por:** TheNiloGod  
**Semillero de Ciberseguridad, Tecnológico de Antioquia**

---

## 📈 Descripción del Proyecto

TdeA - SIDV es una herramienta de auditoría de seguridad en consola (CLI), diseñada para estudiantes, investigadores y profesionales que requieren realizar escaneos básicos de vulnerabilidades de manera automatizada y estructurada.

Incluye:
- Escaneos con **Nmap** (detección de puertos/servicios)
- Análisis con **Nikto** (vulnerabilidades web)
- Generación de reportes automáticos en `.txt` y `.pdf`
- Ejecución guiada desde terminal con interfaz amigable

---

## 🚀 Instalación

### 🌟 Requisitos
- Sistema operativo: **Kali Linux**, Debian, Ubuntu o derivado (físico o virtualizado)
- **Python 3** instalado
- Acceso a `sudo`

### 📅 Instalación en sistema Linux nativo
```bash
git clone https://github.com/TheNilogod70/SuiteIntegradaVulnerbailidades.git
cd SuiteIntegradaVulnerbailidades
sudo python3 main.py
```
> ✅ El sistema ejecutará automáticamente `setup.sh` para:
> - Instalar Nmap, Nikto y ReportLab (PDF)
> - Crear carpetas `logs/` y `reports/`
> - Otorgar permisos de ejecución

### 🚀 Instalación en máquina virtual (VirtualBox / VMware)
1. Descarga Kali Linux desde: [https://www.kali.org/get-kali/](https://www.kali.org/get-kali/)
2. Crea una máquina virtual con al menos:
   - 2 GB RAM
   - 2 CPU
   - 15 GB de disco
3. Instala Git:
```bash
sudo apt update && sudo apt install git
```
4. Clona el proyecto y ejecútalo:
```bash
git clone https://github.com/TheNilogod70/SuiteIntegradaVulnerbailidades.git
cd SuiteIntegradaVulnerbailidades
sudo python3 main.py
```

---

## 📚 Uso de la Suite

### ▶ Menú principal:
```
1. Escanear con Nmap
2. Analizar con Nikto
3. Ver reportes generados
4. Salir
```

### ✏️ Escanear:
- Opcion 1: IP o dominio (ej: 127.0.0.1 o google.com)
- Opcion 2: URL completa (ej: http://testphp.vulnweb.com)
- Se mostrará barra de carga durante el análisis

### 📃 Reporte:
- Se pregunta si desea generar un reporte
- El usuario ingresa el nombre del archivo
- Luego se ofrece generar también el archivo en **PDF**
- Ambos archivos se guardan en `reports/`

### 📑 Ver reportes:
- Opcion 3: listar reportes `.txt` existentes
- Selecciona un número y se muestra su contenido

---

## 📂 Estructura de Carpetas
```
SuiteIntegradaVulnerbailidades/
├── main.py
├── setup.sh
├── modules/
│   ├── nmap_module.py
│   └── nikto_module.py
├── utils/
│   └── report_generator.py
├── reports/      # reportes generados
└── logs/         # registros internos
```

---

## 📰 Resultado esperado

- Reportes en `reports/` con nombre personalizado
- Contenido en PDF incluye:
  - Fecha y hora
  - Comando ejecutado
  - Resultados completos
- PDF listo para entrega ante jurado o archivo académico

---

## ⚡ Recomendaciones

- Ejecutar como `sudo` para evitar errores de permisos
- Usar una red de prueba o entorno controlado
- No reemplazar reportes existentes sin cambiar nombre
- Ideal para presentaciones o talleres de auditoría

---

## 🔧 Futuras mejoras (v2.x)

- Exportación a HTML interactivo
- Integración con herramientas como `wpscan`, `sqlmap`
- Modo silencioso / verbose
- Soporte multilingüístico (ES/EN)

---

## 📖 Licencia y autoría

Este proyecto fue desarrollado con fines académicos por **TheNiloGod** para el **Semillero de Ciberseguridad del Tecnológico de Antioquia**.

Se permite su uso, modificación y extensión siempre que se mantenga el crédito al autor.

> © 2025 TheNiloGod. Todos los derechos reservados.
