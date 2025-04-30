import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import Lasso
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import mean_squared_error, r2_score
import os

# Criar pasta de saída, se necessário
os.makedirs('output/graficos', exist_ok=True)

# Carregar dados tratados
df = pd.read_csv('data/dados_tratados.csv')

# Variáveis
X = df[['ndvi_mean', 'ndvi_max', 'ndvi_min', 'ndvi_std', 'ndvi_mar_mai']]
y = df['producao']

# Separar treino e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Modelo
modelo = Lasso(alpha=0.1)
modelo.fit(X_train, y_train)

# Previsão
y_pred = modelo.predict(X_test)

# Avaliação
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)
print(f'✅ RMSE: {rmse:.2f}')
print(f'✅ R²: {r2:.2f}')

# Validação cruzada
cv_scores = cross_val_score(modelo, X, y, cv=5, scoring='r2')
print("✅ R² Cross-validation (5-fold):", np.mean(cv_scores))

# Exportar previsões
output = pd.DataFrame({'ano': df.loc[y_test.index, 'ano'], 'real': y_test.values, 'previsto': y_pred})
output.to_csv('../output/predicoes_lasso.csv', index=False)

# Gráficos
sns.heatmap(df.drop(columns='ano').corr(), annot=True, cmap='Blues')
plt.title('Correlação entre variáveis')
plt.tight_layout()
plt.savefig('output/graficos/heatmap_correlacao.png')
plt.clf()

sns.scatterplot(x='ndvi_mar_mai', y='producao', data=df)
plt.title("NDVI (mar-mai) vs Produção")
plt.savefig('output/graficos/scatter_ndvi_prod.png')
plt.clf()

from statsmodels.tsa.seasonal import seasonal_decompose
ndvi_df = pd.read_csv('../data/ndvi_data.csv')
ndvi_df['data'] = pd.to_datetime(ndvi_df['data'], dayfirst=True)
decomp = seasonal_decompose(ndvi_df.set_index('data')['ndvi'], model='additive', period=12)
decomp.plot()
plt.savefig('output/graficos/decomposicao_sazonal.png')
plt.clf()

# Real vs Previsto
plt.scatter(y_test, y_pred)
plt.plot([y.min(), y.max()], [y.min(), y.max()], 'k--')
plt.xlabel('Valor Real')
plt.ylabel('Valor Previsto')
plt.title('Produção Real vs Prevista')
plt.savefig('output/graficos/real_vs_previsto.png')
plt.clf()

print("✅ Gráficos salvos em output/graficos/")
