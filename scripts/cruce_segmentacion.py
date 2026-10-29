import pandas as pd
from datetime import date
from pathlib import Path

# Cargar datos
clientes_campana = pd.read_csv('data/raw/campana_verano_clientes.csv')
clientes_muestra = pd.read_csv('data/raw/clientes.csv')
pedidos = pd.read_csv('data/raw/pedidos.csv')

# Convertir fechas: pedidos.csv trae ISO con hora y un 4$ en DD/MM/YYYY.

fechas = pd.to_datetime(pedidos['fecha_pedido'], format='ISO8601', errors='coerce')

resto  = fechas.isna()
fechas[resto] = pd.to_datetime(pedidos.loc[resto, 'fecha_pedido'], dayfirst=True, errors='coerce' )

pedidos['fecha_pedido'] = fechas

# Paso 1: Filtrar pedido últimos 3 meses (desde el 15 junio, arranque de la campaña)
fecha_corte = pd.Timestamp('2024-06-15')
pedidos_recientes = pedidos[
    (pedidos['fecha_pedido'] > fecha_corte) &
    (pedidos['estado'] != 'cancelado')
]
# Paso 2: Contar pedidos por cliente
conteo = (
    pedidos_recientes.
    groupby('cliente_id')
    .size()
    .reset_index(name='pedidos_3m')
)

# Paso 3: LEFT JOIN con clientes de la campaña
clientes_campana = clientes_campana.drop_duplicates(subset=['cliente_id'])
resultado = clientes_campana.merge(
    conteo, on='cliente_id', how='left'
)

resultado['pedidos_3m'] = resultado['pedidos_3m'].fillna(0).astype(int)
# Paso 4: Clasificar en segmentos

def clasificar(pedidos): 
    if pedidos > 6: 
        return 'premium'
    elif pedidos >= 2: 
        return 'regular'
    else: 
        return 'en_riesgo'
    
resultado['segmento_calculado'] = resultado['pedidos_3m'].apply(clasificar)

# Paso 5: Enriquecer los datos de la tabla muestra (nombre, fecha_registro)

muestra = clientes_muestra.drop_duplicates(subset=['cliente_id'])
resultado = resultado.merge(
    muestra[['cliente_id','nombre', 'fecha_registro']], 
    on='cliente_id', how='left'
    
)

# Resumen
print('Distribución de segmentos: ')
print(resultado['segmento_calculado'].value_counts())
print(f'\nClientes sin pedidos : {(resultado['pedidos_3m'] == 0).sum()}')

# Exportar datos
cols = ['cliente_id', 'nombre', 'fecha_registro',
              'pedidos_3m', 'segmento_calculado']

Path('output').mkdir(exist_ok=True)
ruta = 'output/segmentacion.csv'
resultado[cols].to_csv(ruta, index=False)
print(f'\nArchivo Exportado: {ruta}')

# Resumen de la segmentación

segmentacion = pd.read_csv('output/segmentacion.csv')

resumen = (
    segmentacion['segmento_calculado']
    .value_counts()
    .reset_index()
)

resumen.columns = ['segmento', 'cantidad']

# Calcular porcentaje :
resumen['porcentaje'] = (100.0 * resumen['cantidad'] / resumen['cantidad'].sum()).round(1)

# Ordernar de mayor a menor
resumen = resumen.sort_values('cantidad', ascending=False)

print('SEGMENTACIÓN DE CLIENTES - CAMPAÑA VERANO 2024')
print('='*50)
print(resumen.to_string(index=False))
print(f'\nTotal Clientes: {resumen['cantidad'].sum():,}')