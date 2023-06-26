import pandas as pd
import numpy as np

Disciplina = 'MT'

dItens = pd.read_csv('provasOrdernadasPorTri.csv', encoding='utf-8', decimal=',')

dItens = dItens[dItens['SG_AREA'] == Disciplina]
dItens = dItens[dItens['CO_HABILIDADE'].between(1, 30)]
dItens = dItens[dItens['IN_ITEM_ABAN'] == 0]

dItens.sort_values('theta_065', ascending=True, inplace=True)

if Disciplina == 'LC':
    dItens = dItens[~dItens['CO_HABILIDADE'].isin([5, 6, 7, 8])]


# Selecionar um item de cada habilidade de 1 a 30
habilidades_unicas = dItens.groupby('CO_HABILIDADE').sample(1)

# Selecionar os 12 itens restantes permitindo repetições, mas no máximo 3 repetições por habilidade
habilidades_repetidas = dItens.groupby('CO_HABILIDADE').apply(lambda x: x.sample(min(len(x), 3)))
habilidades_repetidas = habilidades_repetidas.sample(n=12, replace=True)

# Combinar os dataframes resultantes
resultado = pd.concat([habilidades_unicas, habilidades_repetidas])

# Obter as habilidades presentes no resultado atual
habilidades_presentes = resultado['CO_HABILIDADE'].unique()

# Verificar se todas as 30 habilidades estão presentes
if Disciplina != 'LC':
    if len(habilidades_presentes) < 30:
        # Calcular o número de habilidades faltantes
        habilidades_faltantes = np.setdiff1d(range(1, 31), habilidades_presentes)
        num_faltantes = 30 - len(habilidades_presentes)

        # Selecionar itens adicionais para as habilidades faltantes
        itens_faltantes = dItens[dItens['CO_HABILIDADE'].isin(habilidades_faltantes)].sample(n=num_faltantes, replace=True)

        # Combinar os itens faltantes com os resultados atuais
        resultado = pd.concat([resultado, itens_faltantes])

# Verificar o número de itens atual
num_itens = len(resultado)

# Remover itens extras se o número atual for maior que 45
if num_itens > 45:
    resultado = resultado.sample(n=45)

# Preencher com itens adicionais se o número atual for menor que 45
if num_itens < 45:
    num_adicionais = 45 - num_itens
    itens_adicionais = dItens.sample(n=num_adicionais, replace=True)
    resultado = pd.concat([resultado, itens_adicionais])

# Exibir o resultado
print(resultado.max())
print('')
print(resultado.min())


resultado = resultado.sample(frac=1)
resultado.to_csv('Simulados/simulado'+Disciplina+'.csv', index=False, encoding='utf-8', decimal=',')

