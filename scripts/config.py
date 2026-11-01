# config.py -- Configuración centralizada de pipeline de camapañas

COLUMNAS_OBLIGATORIAS = [
    'venta_id', 'cliente_id', 'producto_id', 'fecha_compra', 
    'cantidad', 'precio', 'descuento_pct', 'tienda_id', 'campana'
]

COLUMN_MAPPING = {
    'verano': {
        
    },
    'primavera': {
        'id_transaccion': 'venta_id', 
        'id_cliente': 'cliente_id', 
        'id_producto': 'producto_id', 
        'fecha_venta': 'fecha_compra',
        'unidades': 'cantidad', 
        'importe': 'precio', 
        'descuento': 'descuento_pct', 
        'almacen': 'tienda_id', 
        'promocion': 'campana', 
    }, 
}

# Particularidades por campaña
CAMPANA_CONFIG = {
    'verano': {
        'precio_es_string': True, 
        'fechas_mixtas': True, 
        'anonimo_es_null': True
    }, 
    'primavera': {
        'precio_es_string': False, 
        'fechas_mixtas': False, 
        'anonimo_es_null': False
    }
}
