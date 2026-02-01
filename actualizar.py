# Este script actualiza y muestra el tipo de cambio del dólar en Perú para el último año desde la fecha actual.

import pandas as pd
import requests
from datetime import datetime
from dateutil.relativedelta import relativedelta # Necesitas: pip install python-dateutil
import matplotlib.pyplot as plt # Librería para graficar

# 1. Configurar fechas dinámicas
hoy = datetime.now()
hace_un_ano = hoy - relativedelta(years=1)

# Convertir a formato string para la API
fecha_fin = hoy.strftime('%Y-%m-%d')
fecha_inicio = hace_un_ano.strftime('%Y-%m-%d')

#codigo_serie = "PD04637PD" # Serie diaria del tipo de cambio del dólar
codigo_serie = "PN01207PM" # series mensual del tipo de cambio del dólar

# 2. Construir URL
url = f"https://estadisticas.bcrp.gob.pe/estadisticas/series/api/{codigo_serie}/json/{fecha_inicio}/{fecha_fin}"

try:
    response = requests.get(url)
    data = response.json()

    # 3. Procesar DataFrame
    df = pd.DataFrame(data['periods'])
    df['values'] = pd.to_numeric(df['values'].str[0])
    df.columns = ['Fecha', 'Tipo_Cambio']

    #corrección de formato de fecha
    meses_es_en = {
        'Ene': 'Jan',
        'Feb': 'Feb',
        'Mar': 'Mar',
        'Abr': 'Apr',
        'May': 'May',
        'Jun': 'Jun',
        'Jul': 'Jul',
        'Ago': 'Aug',
        'Set': 'Sep',
        'Oct': 'Oct',
        'Nov': 'Nov',
        'Dic': 'Dec'}

    # Eliminar puntos y reemplazar meses en español por inglés
    df['Fecha'] = df['Fecha'].str.replace('.', '', regex=False)

    for es, en in meses_es_en.items():
        df['Fecha'] = df['Fecha'].str.replace(es, en, regex=False) # regex sirve para evitar advertencias futuras
    df['Fecha'] = pd.to_datetime(df['Fecha'], errors ='coerce')

    # 4. Mostrar información
    print(f"Rango consultado: {fecha_inicio} al {fecha_fin}")
    print(f"Total de días con datos: {len(df)}")
    print("-" * 30)
    print(df.head()) # Los primeros del año pasado
    print("...")
    print(df.tail()) # Los más recientes de hoy
    
    # 5. Graficar los datos
    plt.figure(figsize=(12, 6)) # Define el tamaño de la figura
    plt.plot(df['Fecha'], df['Tipo_Cambio'],
            color = "#0b5b94", # Color azul BCRP
            linewidth=2,         # Grosor de la línea
            marker='o',          # Tipo de marcador
            markersize=4,       # Tamaño del marcador
            markerfacecolor='white',  # Color de relleno del marcador
            linestyle='-',      # Estilo de línea sólida
            label='Tipo de Cambio mensual BCRP'
            )

    plt.title('Evolución del Tipo de Cambio del Dólar en Perú', fontsize=15, fontweight='bold') # Título del gráfico y fuente
    plt.xlabel('Meses de Análisis', fontsize=12) # Etiqueta del eje X
    plt.ylabel('Tipo de Cambio (PEN/USD)', fontsize=12) # Etiqueta del eje Y
    plt.grid(True, linestyle='--', alpha=0.6) # Añadir cuadrícula
    plt.legend() # Mostrar leyenda
    plt.xticks(rotation=45) # Rotar etiquetas del eje X para mejor legibilidad
    plt.tight_layout() # Ajustar el diseño para evitar recortes
    plt.show() # Mostrar el gráfico

except Exception as e:
    print(f"Error: {e}")