import pandas as pd
from pycaret.clustering import *
Disciplina = 'MT'

# Carregar os dados
dItens = pd.read_csv('../provasOrdernadasPorTri.csv', encoding='utf-8', decimal=',')
dItens = dItens[dItens['SG_AREA'] == Disciplina]
# Especificar a coluna para o clustering
column_for_clustering = 'theta_065'  # Substitua 'nome_da_coluna' pelo nome da sua coluna

# Selecionar a coluna desejada
selected_column = dItens[[column_for_clustering]]  # Converta em DataFrame

# Configurar o clustering usando a coluna específica
clusterA = setup(selected_column, normalize=True)

# Criar o modelo K-Means
model = create_model('kmeans')

# Avaliar o modelo
evaluate_model(model)

# Atribuir os clusters a cada item
assigned_clusters = assign_model(model)

# Adicionar as atribuições de cluster ao DataFrame original
del assigned_clusters[column_for_clustering]
dItens_with_clusters = pd.concat([dItens, assigned_clusters], axis=1)

# Exportar itens de cada cluster para arquivos CSV separados
unique_clusters = dItens_with_clusters['Cluster'].unique()
for cluster in unique_clusters:
    cluster_items = dItens_with_clusters[dItens_with_clusters['Cluster'] == cluster]
    cluster_csv_name = f'{Disciplina}_{column_for_clustering}_{cluster}.csv'
    cluster_items.to_csv(cluster_csv_name, index=False, encoding='utf-8', decimal=',')
    print(f"Arquivo CSV para o cluster {cluster} foi exportado como {cluster_csv_name}")

dItens_with_clusters.to_csv('provasOrdernadasPorTri'+'_'+Disciplina+'_CLUSTERED.csv', index=False, encoding='utf-8', decimal=',')
