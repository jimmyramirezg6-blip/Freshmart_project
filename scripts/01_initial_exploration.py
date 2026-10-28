# explorar_campaña.py
import pandas as pd

# Cargar los 3 archivos
clientes = pd.read_csv('data/raw/campana_verano_clientes.csv')
ventas = pd.read_csv('data/raw/campana_verano_ventas.csv')
productos = pd.read_csv('data/raw/productos_promo_verano.csv')

print('=' * 60)
print('CLIENTES DE LA CAMPAÑA')
print('=' * 60)
print(f'Filas : {len(clientes):,}')
print(f'Columnas : {list(clientes.columns)}')
print()
print(f'Duplicados: {clientes['cliente_id'].duplicated().sum()}')
print(f'IDs únicos {clientes['cliente_id'].nunique():,}')
print(f'→ Posibles duplicados : {len(clientes) - clientes['cliente_id'].nunique()}')
print()
print(f'Nulos por columna: {clientes.isnull().sum()}')
print(clientes.info())
print(clientes.head())

print('=' * 60)
print('VENTAS DE LA CAMPAÑA')
print('=' * 60)
print(f'Filas: {len(ventas):,}')
print(f'Columnas: {list(ventas.columns)}')
print()
print(ventas.info())
print()
print(ventas.head())
print('Nulos por columnas:')
print(ventas.isnull().sum())
print()
# Verificar el formato de fecha_compra
print('Muestra de fecha_compra')
print(ventas['fecha_compra'].sample(10, random_state=42).values)
print()
# Verificar el formato de precio
print('Muestras de precio')
print(ventas['precio'].sample(10, random_state=42).values)

#subir_a_raw.py - simular la estructura del data lake local 
import shutil
from pathlib import Path
from datetime import date

# configuracion
LAKE_ROOT = Path('freshmart-lake')
FUENTE = 'marketing'
FECHA = date(2024,9,16)

#archivos

archivos = [
    'campana_verano_clientes.csv',
    'campana_verano_ventas.csv', 
    'productos_promo_verano.csv'
]

for archivo in archivos: 
    tabla = archivo.replace('.csv','')
    
    destino = (
        LAKE_ROOT / 'raw' / FUENTE / tabla  / str(FECHA.year) / f'{FECHA.month:02d}'/ f'{FECHA.day:02d}'
    )
    
    destino.mkdir(parents=True, exist_ok=True)
    
    shutil.copy(f'data/raw/{archivo}', destino/archivo)
    print(f'✓ {archivo} → {destino}')


print('-' * 60)
print('AUDITORIA RÁPIDA')
print('-' * 60)

def auditoria_rapida(df:pd.DataFrame, nombre:str) -> dict: 
    """Genera un resumen de calidad básico de un DataFrame."""
    total_nulos = df.isnull().sum().sum()
    total_celdas = df.shape[0] * df.shape[1]
    return{
        'archivo': nombre, 
        'total_filas':len(df), 
        'total_columnas': len(df.columns), 
        'total_duplicadas': df.duplicated().sum(),
        'nulos_totales': total_nulos,
        'porcentaje_nulos': (100.0 * total_nulos/total_celdas)
    }

archivos = {
        'clientes': 'data/raw/campana_verano_clientes.csv',
        'ventas': 'data/raw/campana_verano_ventas.csv',
        'productos': 'data/raw/productos_promo_verano.csv',
}

for nombre, ruta in archivos.items():
    df = pd.read_csv(ruta)
    resumen = auditoria_rapida(df, nombre)
    print(f'\n{'='*60}')
    print(f'{resumen['archivo'].upper()}')
    print(f'{'='*60}')
    for k, v in resumen.items(): 
        if k != 'archivo': 
            print(f' {k}: {v}')