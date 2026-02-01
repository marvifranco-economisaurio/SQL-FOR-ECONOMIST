# 📈 BCRP Data Extractor: Python para Economistas

Este repositorio contiene una herramienta eficiente en Python para automatizar la extracción de series de tiempo desde la API del **Banco Central de Reserva del Perú (BCRP)**. Está diseñado para facilitar la transición de datos desde fuentes oficiales hacia entornos de análisis como **Pandas**, **SQL Server** o **Power BI**.

## 🚀 Funcionalidades
* **Rango Dinámico:** Calcula automáticamente un periodo de **un año atrás** desde la fecha actual para mantener los datos siempre frescos.
* **Manejo de API:** Gestiona la estructura JSON del BCRP, resolviendo errores comunes de tipos de datos (listas anidadas).
* **Data Cleaning:** Convierte los valores de texto a formato numérico (`float64`) para cálculos inmediatos.
* **Orientado a Proyectos:** Estructura ideal para ser integrado en flujos de trabajo de econometría y finanzas públicas.

## 🛠️ Requisitos
Asegúrate de tener instaladas las siguientes librerías:

```bash
pip install pandas requests python-dateutil

📖 Uso del Script
El script solicita la serie de Tipo de Cambio (Venta) por defecto, pero es fácilmente adaptable a cualquier código de serie del BCRP.

Python
import pandas as pd
import requests
from datetime import datetime
from dateutil.relativedelta import relativedelta

# 1. Configuración de fechas dinámicas (1 año de ventana)
hoy = datetime.now()
hace_un_ano = hoy - relativedelta(years=1)

fecha_fin = hoy.strftime('%Y-%m-%d')
fecha_inicio = hace_un_ano.strftime('%Y-%m-%d')

# 2. Conexión con la API
codigo_serie = "PD04637PD"  # Ejemplo: Tipo de Cambio
url = f"[https://estadisticas.bcrp.gob.pe/estadisticas/series/api/](https://estadisticas.bcrp.gob.pe/estadisticas/series/api/){codigo_serie}/json/{fecha_inicio}/{fecha_fin}"

# 3. Procesamiento a DataFrame
response = requests.get(url)
data = response.json()
df = pd.DataFrame(data['periods'])

# Limpieza: Extraer valor de la lista y convertir a número
df['values'] = pd.to_numeric(df['values'].str[0])
df.columns = ['Fecha', 'Valor']

print(df.head())
📊 Aplicaciones
Este código es parte de un ecosistema de herramientas para la gestión de datos económicos, incluyendo:

Automatización de reportes macroeconómicos.

Carga de datos históricos en bases de datos SQL.

Análisis de volatilidad en series de tiempo.

Desarrollado como parte de: Proyectos de Investigación Económica y Datapolis.