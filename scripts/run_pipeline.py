import pandas as pd
import logging
from pathlib import Path
from config import COLUMN_MAPPING, COLUMNAS_OBLIGATORIAS, CAMPANA_CONFIG

def aplicar_mapping(df:pd.DataFrame, campana:str) -> pd.DataFrame: 
    """
    Renombra columnas según el mapping de la campaña. 
    Valida que todas las columnas obligatorias existen después.
    """
    mapping = COLUMN_MAPPING.get(campana, {})
    
    if mapping: 
        df = df.rename(columns=mapping)
        
    # validad que tenemos todas las columnas obligatorias
    faltantes = set(COLUMNAS_OBLIGATORIAS) - set(df.columns)
    if faltantes: 
        raise ValueError(
            f' Campaña "{campana}": faltan columnas después del mapping: {faltantes}'
        )   
    return df

def normalizar_anonimos(df: pd.DataFrame, campana:str) -> pd.DataFrame: 
    """
    Unifica la representación de clientes anónimos. 
    Verano: NULL = anónimo. Primavera : -1 = anónimo. 
    Resultado: siempre NULL + columna 'es_anonimo'
    """
    config = CAMPANA_CONFIG[campana]
    
    if not config['anonimo_es_null']: 
        df.loc[df['cliente_id'] == -1 , 'cliente_id'] = None
    
    df['es_anonimo'] = df['cliente_id'].isna()
    return df

def limpiar_precio_flexible(df: pd.DataFrame, campana:str) -> pd.DataFrame: 
    """
    Limpia la columna precio según la configuración de la campaña. 
    - Verano: string '2,45 €' -> float 2.45
    - Primavera: ya es float, no hacer nada
    """
    config = CAMPANA_CONFIG[campana]
    
    if config['precio_es_string']: 
        df['precio'] = (
            df['precio']
            .astype(str)
            .str.replace('€', '', regex=False)
            .str.replace(',', '.')
            .astype(float)
        )
    else: 
        df['precio'] = df['precio'].astype(float)
    
    return df

def normalizar_fehcas_flexible(df:pd.DataFrame, campana: str) -> pd.DataFrame: 
    """
    Normlaizar fechas según la campaña. 
    - Verano : 3 formatos mezclados -> format='mixed'
    - Primavera: solo DD/MM/YYYY -> dayfirst = True
    """
    config = CAMPANA_CONFIG[campana]
    
    if config['fechas_mixtas']: 
        df['fecha_compra'] = pd.to_datetime(
            df['fecha_compra'], format='mixed', dayfirst=True
        )
    else: 
        df['fecha_compra'] = pd.to_datetime(
            df['fecha_compra'], dayfirst=True
        )
        
    return df
    

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(message)s')
logger = logging.getLogger(__name__)

def pipeline_campana(ruta_csv: str, campana:str) -> pd.DataFrame: 
    """
    Pipeline completo de ingesta y limpieza para cualquier campaña. 
    Args:
        ruta_csv: Rtua del archivo CSV original
        campana: Nombre de la campaña ('verano','primavera', etc.)
        
    returns: 
        DataFrame limpio con esquema estándar
    """
    
    logger.info(f'{'=' * 50}')
    logger.info(f'Pipeline: {campana} | Archivo: {ruta_csv}')
    logger.info(f'{'='*50}')
    
    # Carga
    df = pd.read_csv(ruta_csv)
    logger.info(f'[CARGA] {len(df):,} filas cargadas')
    
    # 2. Aplicar mapping de columnas
    df = aplicar_mapping(df, campana)
    logger.info(f'[MAPPING] columnas normalizadas al esquema estándar')
    
    # 3. Eliminar duplicados
    antes = len(df)
    df = df.drop_duplicates()
    logger.info(f'[DUPLICADOS] {antes - len(df)} eliminados')
        
    # 4. Normalizar fechas
    df = normalizar_fehcas_flexible(df, campana)
    logger.info(f'[FECHAS] Normalizadas a datetime')
    
    # 5. Limpiar precio
    df = limpiar_precio_flexible(df, campana)
    logger.info(f'[PRECIO]: convertido a float')
    
    # 6. Normalizar anónimos
    df = normalizar_anonimos(df, campana)
    n_anon = df['es_anonimo'].sum()
    logger.info(f'[ANONIMOS] {n_anon} ventas anónimas marcadas')
    
    # 7. Filtrar cantidad = 0
    antes = len(df)
    df = df[df['cantidad'] > 0]
    logger.info(f'[CANTIDAD] {antes - len(df)} filas con cantidad = 0 eliminadas')    
    
    return df
    
if __name__ == '__main__': 

    verano = pipeline_campana('data/raw/campana_verano_ventas.csv', 'verano')  
    primavera = pipeline_campana('data/raw/campana_primavera_ventas.csv', 'primavera')
    
    # Unificar: 
    unificado = pd.concat([verano, primavera], ignore_index=True)
    Path('output').mkdir(exist_ok=True)
    unificado.to_parquet('output/silver_ventas_unificado.parquet', index=False, engine='pyarrow')
    logger.info(f'\nTotal unificado: {len(unificado):,} filas - silver_ventas_unificado.csv')   