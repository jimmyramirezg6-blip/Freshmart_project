import pandas as pd

# Cargar los 3 archivos
clientes = pd.read_csv('data/raw/campana_verano_clientes.csv')
ventas = pd.read_csv('data/raw/campana_verano_ventas.csv')
productos = pd.read_csv('data/raw/productos_promo_verano.csv')


print(clientes['canal_contacto'].unique())
