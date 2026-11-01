# limpiar_ventas.py - Pipeline de limpieza de CSV de ventas
import pandas as pd
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s'
)

logger = logging.getLogger(__name__)

def normalizar_fechas(df: pd.DataFrame) -> pd.DataFrame: 
    
    logger.info('Normalizando fechas')
    antes_nulas = df['fecha_compra'].isna().sum()
    
    df['fecha_compra'] = pd.to_datetime(
        df['fecha_compra'], 
        format='mixed', 
        dayfirst=True 
    )
    despues_nulas = df['fecha_compra'].isna().sum()
    nuevas_nulas = despues_nulas - antes_nulas
    if nuevas_nulas > 0: 
        logger.warning(f' {nuevas_nulas} fecha no se pudieron parsear')
    else: 
        logger.info('  ✓ Todas las fechas parseadas correctamente')
    return df

def limpiar_precio(df: pd.DataFrame) -> pd.DataFrame: 
    
    logger.info('Limpiando columna precio')
    
    df['precio'] = (
        df['precio']
        .astype(str)
        .str.replace('€', '', regex=False)
        .str.replace(',','.')
        .astype(float)
    )

    negativos = (df['precio'] < 0).sum()
    if negativos > 0:
        logger.warning(f' {negativos} precios negativos detectados')
         
    logger.info(f' ✓ Precio convertido. Rango {df['precio'].min():.2f} - {df['precio'].max():.2f}')
    return df


def marcar_anonimos(df: pd.DataFrame) -> pd.DataFrame: 
    
    logger.info('Marcando ventas anónimas...')
    df['es_anonimo'] = df['cliente_id'].isna()
    n_anonimos = df['es_anonimo'].sum()
    logger.info(f' ✓ {n_anonimos} ventas anónimas marcadas ({100.0 * n_anonimos / len(df):.1f}%)')
    return df

def eliminar_duplicados(df: pd.DataFrame) -> pd.DataFrame: 
    """
    Elimina filas completamente duplicadas (misma venta_id, mismos datos)
    """
    logger.info('Eliminando duplicados...')
    antes = len(df)
    df = df.drop_duplicates()
    eliminados = antes - len(df)
    logger.info(f' ✓  {eliminados} duplicados eliminados')
    return df


def filtrar_cantidad_cero(df: pd.DataFrame) -> pd.DataFrame: 
    """
    Filtra ventas con cantidad = 0 (bug de la app, no son ventas reales)
    """
    antes = len(df)
    df = df[df['cantidad'] > 0]
    eliminados = antes - len(df)
    logger.info(f' ✓  {eliminados} filas con cantidad = 0 eliminados')
    return df


def limpiar_ventas_campana(ruta_csv: str) -> pd.DataFrame: 
    """
    Pipeline completo de limpieza para el CSV de ventas de campaña. 
    Aplica cada función en orden y loguea el resultado
    """
    
    logger.info( f' === Iniciando limpieza: {ruta_csv} ===')
    
    # cargar
    df = pd.read_csv(ruta_csv)
    logger.info(f'filas cargadas : {len(df):,}')
    
    # aplicar limpieza en orden
    df = eliminar_duplicados(df)
    df = normalizar_fechas(df)
    df = limpiar_precio(df)
    df = marcar_anonimos(df)
    df = filtrar_cantidad_cero(df)
    
    logger.info(f' === Limpieza completada. Filas finales : {len(df):,} ===')
    return df


# ejecutar

if __name__ == '__main__': 
    from pathlib import Path
    
    ventas_limpias = limpiar_ventas_campana('data/raw/campana_verano_ventas.csv')
    
    # Guardar en zona silver (como Parquet en un proyecto real)
    Path('output').mkdir(exist_ok=True)
    ventas_limpias.to_csv('output/silver_ventas_verano.csv', index=False)
    print(f'\nArchivo limpio guardado: output/silver_ventas_verano.csv')

    