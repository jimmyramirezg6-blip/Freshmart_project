import pandas as pd
from config import COLUMN_MAPPING, COLUMNAS_OBLIGATORIAS, CAMPANA_CONFIG

def aplicar_mappging(df: pd.DataFrame, campana:str) -> pd.DataFrame: 
    """
    Renombra columnas según el mapping de la campaña. 
    VAlida que todas las columnas obligatorios exiten después. 
    """
    
    mapping = COLUMN_MAPPING.get(campana, {})
    
    if mapping: 
        df= df.rename(columns=mapping)
    
    # Validar que tenemos todas las columnas obligatorias. 
    
    faltantes = set(COLUMNAS_OBLIGATORIAS) - set(df.columns)
    if faltantes: 
        raise ValueError(
            f'Campaña "{campana}" : faltan columnas después de mapping: {faltantes}'
        )
    return df

def normalizar_anonimos(df:pd.DataFrame, campana: str) -> pd.DataFrame: 
    """
    Unifica la represetnación de clietnes anónimos. 
    Verano: NULL = anónnimo. Primavera: -1 = anónimo. 
    Resultado: siempre NULL +  columna 'es_anonimo'
    """
    config = CAMPANA_CONFIG[campana]
    
    if not config['anonimo_es_null']: 
        df.loc[df['cliente_id'] == -1, 'cliente_id'] = None
    
    df['es_anonimo'] = df['cliente_id'].isna()
    
    return df


df = pd.read_csv()