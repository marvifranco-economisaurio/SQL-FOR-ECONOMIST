import pandas as pd
import requests
from datetime import datetime
from dateutil.relativedelta import relativedelta # Necesitas: pip install python-dateutil

# 1. Configurar fechas dinámicas
hoy = datetime.now()
hace_un_ano = hoy - relativedelta(years=1)

# Convertir a formato string para la API
fecha_fin = hoy.strftime('%Y-%m-%d')
fecha_inicio = hace_un_ano.strftime('%Y-%m-%d')

codigo_serie = "PD04637PD"

# 2. Construir URL
url = f"https://estadisticas.bcrp.gob.pe/estadisticas/series/api/{codigo_serie}/json/{fecha_inicio}/{fecha_fin}"

try:
    response = requests.get(url)
    data = response.json()

    # 3. Procesar DataFrame
    df = pd.DataFrame(data['periods'])
    df['values'] = df['values'].str[0]
    df['values'] = pd.to_numeric(df['values'])
    
    df.columns = ['Fecha', 'Tipo_Cambio']

    # 4. Mostrar información
    print(f"Rango consultado: {fecha_inicio} al {fecha_fin}")
    print(f"Total de días con datos: {len(df)}")
    print("-" * 30)
    print(df.head()) # Los primeros del año pasado
    print("...")
    print(df.tail()) # Los más recientes de hoy

except Exception as e:
    print(f"Error: {e}")