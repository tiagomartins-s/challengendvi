import pandas as pd
import numpy as np
from scipy.stats import zscore

# Carregar dados
ndvi_df = pd.read_csv('data/ndvi_data.csv')
milho_df = pd.read_csv('data/milho_producao.csv')

# Conversão de datas
ndvi_df['data'] = pd.to_datetime(ndvi_df['data'], dayfirst=True)
ndvi_df['ano'] = ndvi_df['data'].dt.year
ndvi_df['mes'] = ndvi_df['data'].dt.month
milho_df['ano'] = milho_df['ano'].astype(int)

# Limpeza de nulos
ndvi_df.dropna(subset=['ndvi'], inplace=True)
milho_df.dropna(subset=['producao'], inplace=True)

# Remoção de outliers (Z-score)
ndvi_df = ndvi_df[(np.abs(zscore(ndvi_df['ndvi'])) < 3)]

# Agregações NDVI por ano
ndvi_agg = ndvi_df.groupby('ano').agg({
    'ndvi': ['mean', 'max', 'min', 'std']
})
ndvi_agg.columns = ['ndvi_mean', 'ndvi_max', 'ndvi_min', 'ndvi_std']
ndvi_agg = ndvi_agg.reset_index()

# NDVI médio no período crítico (março a maio)
ndvi_critico = ndvi_df[ndvi_df['mes'].isin([3, 4, 5])]
ndvi_mar_mai = ndvi_critico.groupby('ano')['ndvi'].mean().reset_index()
ndvi_mar_mai.columns = ['ano', 'ndvi_mar_mai']

# Unir todos os dados
ndvi_final = pd.merge(ndvi_agg, ndvi_mar_mai, on='ano', how='left')
df_final = pd.merge(milho_df, ndvi_final, on='ano', how='inner')

# Exportar CSV final
df_final.to_csv('data/dados_tratados.csv', index=False)
print("✅ Pré-processamento finalizado e salvo em 'data/dados_tratados.csv'")
