import pandas as pd

resultado = pd.read_csv('output/segmentacion.csv')

# Filtrar clientes sin pedido

sin_pedidos = resultado[resultado['pedidos_3m'] == 0].copy()
print(f'Clientes sin pedidos: {len(sin_pedidos)}')

# Convertir fecha_registro a datetime
sin_pedidos['fecha_registro'] = pd.to_datetime(sin_pedidos['fecha_registro'])

# ¿Cuántos se registraron desde el 2024-06-15, arranque de la campaña?
fecha_captacion  = pd.Timestamp('2024-06-15')
recientes = sin_pedidos[sin_pedidos['fecha_registro'] >= fecha_captacion]
antiguos = sin_pedidos[sin_pedidos['fecha_registro'] < fecha_captacion]

print(f'\nRegistros recientes (desde el 15 jun 2024): {len(recientes)}')
print(f'\nRegistro antiguos (antes del 15 jun 2025): {len(antiguos)}')
print(f'\n% Captación reciente: {round(100.0 * len(recientes) / len(sin_pedidos),1)} % ')

print(f'\n% antiguos que dejaron de comprar: {round(100.0 * len(antiguos) / len(sin_pedidos), 1)} %')

# Conclusiones

print(f'\n---- Conclusión -----')
print('Solo 292 (4.4%) de los 6.607 son capacitación reciente.  ')
print('Los otros 6.315 (95.6%) son clientes antiguos que han dejado de comprar')
print('No es un problema de captación, es de retención')
