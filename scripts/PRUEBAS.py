import pandas as pd

# Cargar los 3 archivos
clientes = pd.read_csv('data/raw/campana_verano_clientes.csv')
ventas = pd.read_csv('data/raw/campana_verano_ventas.csv')
productos = pd.read_csv('data/raw/productos_promo_verano.csv')



ventas = [1200.50, 980.00, 1540.75, 0.0, 2100.30, 1750.00, 640.25]
dias   = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]

for i in range(7): 
    venta = ventas[i]
    print(venta)
    
    