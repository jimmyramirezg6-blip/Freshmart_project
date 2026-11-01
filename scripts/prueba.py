import pandas as pd

verano = pd.read_parquet('output/silver_ventas_unificado.parquet')

print(verano.head())