import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def tri_3pl_enem(theta, a, b, c):
    return c + (1 - c) * (1 / (1 + np.exp(-1.7 * a * (theta - b))))

# Encontrando o valor de theta que resulta em targ (padrão 0.65)
def find_theta(a, b, c, targ):
    left = -100
    right = 100
    tol = 1e-5
    target = targ
    while (right - left) / 2 > tol:
        theta = (left + right) / 2
        value = tri_3pl_enem(theta, a, b, c)
        if value > target:
            right = theta
        else:
            left = theta
    return theta * 100 + 500

def get_prova_string(ano, co_prova):
    if ano == 2016:
        if co_prova in [303]:
            return 'PROVA AZUL'
    if ano == 2017:
        if co_prova in [400, 396]:
            return 'PROVA AMARELA'
        elif co_prova in [406, 393]:
            return 'PROVA CINZA'
        elif co_prova in [436, 440]:
            return 'PROVA AMARELA PPL REAPLICACAO'
        else:
            return 'PROVA CINZA PPL REAPLICACAO'    
    if ano == 2018:
        if co_prova in [456, 452]:
            return 'PROVA AMARELA'
        elif co_prova in [449, 462]:
            return 'PROVA CINZA'
        elif co_prova in [496, 492]:
            return 'PROVA AMARELA PPL REAPLICACAO'
        else:
            return 'PROVA CINZA PPL REAPLICACAO'
    if ano == 2019:
        if co_prova in [512, 508]:
            return 'PROVA AMARELA'
        elif co_prova in [505, 518]:
            return 'PROVA CINZA'
        elif co_prova in [552, 548]:
            return 'PROVA AMARELA PPL REAPLICACAO'
        else:
            return 'PROVA CINZA PPL REAPLICACAO'
    elif ano == 2020:
        if co_prova in [578, 568]:
            return 'PROVA AMARELA'
        elif co_prova in [599, 590]:
            return 'PROVA CINZA'
        elif co_prova in [658, 648]:
            return 'PROVA AMARELA PPL REAPLICACAO'
        else:
            return 'PROVA CINZA PPL REAPLICACAO'
    if ano == 2022:
        if co_prova in [1056, 1066]:
            return 'PROVA AMARELA'
        elif co_prova in [1078, 1087]:
            return 'PROVA CINZA'
        elif co_prova in [1136, 1146]:
            return 'PROVA AMARELA PPL REAPLICACAO'
        else:
            return 'PROVA CINZA PPL REAPLICACAO'
    else: #2021
        if co_prova in [890, 880]:
            return 'PROVA AMARELA'
        elif co_prova in [902, 911]:
            return 'PROVA CINZA'
        elif co_prova in [960, 970]:
            return 'PROVA AMARELA PPL REAPLICACAO'
        else:
            return 'PROVA CINZA PPL REAPLICACAO' 
   

def thetaToCsv(provas, dfItens):
    dfItens = dfItens[dfItens.CO_PROVA.isin(provas)]

    dfItens["theta_065"] = 0
    dfItens["theta_080"] = 0
    dfItens["theta_099"] = 0
    dfItens['CO_PROVA'] = dfItens.apply(lambda row: get_prova_string(row['ANO'], row['CO_PROVA']), axis=1)

    for i in dfItens.index:    
        dfItens.loc[i, "theta_065"] = find_theta(
            dfItens.loc[i, "NU_PARAM_A"],
            dfItens.loc[i, "NU_PARAM_B"],
            dfItens.loc[i, "NU_PARAM_C"],
            0.65,
        )
        dfItens.loc[i, "theta_080"] = find_theta(
            dfItens.loc[i, "NU_PARAM_A"],
            dfItens.loc[i, "NU_PARAM_B"],
            dfItens.loc[i, "NU_PARAM_C"],
            0.80,
        )
        dfItens.loc[i, "theta_099"] = find_theta(
            dfItens.loc[i, "NU_PARAM_A"],
            dfItens.loc[i, "NU_PARAM_B"],
            dfItens.loc[i, "NU_PARAM_C"],
            0.99,
        )
    return dfItens

def Make():
    #Leitura dos dados de 2016 e Escolha da Prova [303 - MT 2 dia]
    dItens2016 = pd.read_csv("itens_prova_2016.csv", sep=";", encoding="latin-1")
    dItens2017 = pd.read_csv("ITENS_PROVA_2017.csv", sep=";", encoding="latin-1")
    dItens2018 = pd.read_csv("ITENS_PROVA_2018.csv", sep=";", encoding="latin-1")
    dItens2019 = pd.read_csv("ITENS_PROVA_2019.csv", sep=";", encoding="latin-1")
    dItens2020 = pd.read_csv("ITENS_PROVA_2020.csv", sep=";", encoding="latin-1")
    dItens2021 = pd.read_csv("ITENS_PROVA_2021.csv", sep=";", encoding="latin-1")
    dItens2022 = pd.read_csv("ITENS_PROVA_2022.csv", sep=";", encoding="latin-1")

    provas2016 = [303]
    provas2017 = [393,432,396,436,400,440,406,444]
    provas2018 = [449, 488, 452, 492, 456, 496, 462, 500]
    provas2019 = [512, 552, 508, 548, 505, 544, 518, 556]
    provas2020 = [599, 679, 568, 648, 578, 658, 590, 670]
    provas2021 = [911, 991, 880, 960, 890, 970, 902, 982] 
    provas2022 = [1087, 1167, 1056, 1136, 1066, 1146, 1078, 1158] 


    dItens2016['ANO'] = 2016
    dItens2017['ANO'] = 2017      
    dItens2018['ANO'] = 2018    
    dItens2019['ANO'] = 2019
    dItens2020['ANO'] = 2020
    dItens2021['ANO'] = 2021
    dItens2022['ANO'] = 2022


    #Colocando as proficiências nas provas e nos dataframes indicados
    dItens2016 = thetaToCsv(provas2016, dItens2016)
    dItens2017 = thetaToCsv(provas2017, dItens2017)
    dItens2018 = thetaToCsv(provas2018, dItens2018)
    dItens2019 = thetaToCsv(provas2019, dItens2019)
    dItens2020 = thetaToCsv(provas2020, dItens2020)
    dItens2021 = thetaToCsv(provas2021, dItens2021)
    dItens2022 = thetaToCsv(provas2022, dItens2022)
    del dItens2020['TP_VERSAO_DIGITAL']

    result = pd.concat([dItens2016,dItens2017, dItens2018, dItens2019, dItens2020, dItens2021, dItens2022])
    result.to_csv('provasOrdernadasPorTri16-22.csv', index=False, encoding='utf-8', decimal=',')

    return result

# Ler os dados do arquivo CSV
dfItens = Make()
dfItens = dfItens[dfItens["IN_ITEM_ABAN"] == 0]
dfItens = dfItens[dfItens["ANO"] == 2022]
dfItens = dfItens[dfItens["SG_AREA"] == "MT"]

# Definir limites aceitáveis para theta_065
limite_inferior = dfItens['theta_065'].quantile(0.05)
limite_superior = dfItens['theta_065'].quantile(0.99)

# Filtrar o dataframe com base nos limites aceitáveis
dfItens = dfItens[(dfItens['theta_065'] >= limite_inferior) & (dfItens['theta_065'] <= limite_superior)]

# Crie um gráfico de barras com habilidade no eixo x e theta_065 no eixo y
plt.bar(dfItens['CO_HABILIDADE'], dfItens['theta_065'], color='blue', width=0.8)

# Adicione rótulos aos eixos x e y e título do gráfico
plt.xlabel('Habilidade')
plt.ylabel('Proficiência')
plt.title('Proficiência x Habilidades - Matemática')

limite_superior = 1000 if limite_superior >= 1000 else limite_superior

# Definir intervalo do eixo y
plt.ylim([limite_inferior, limite_superior])
plt.xticks(dfItens['CO_HABILIDADE'])

# Definir estilo da grade
plt.grid(True, linestyle='--', alpha=0.5)

# Definir tamanho da fonte dos rótulos dos eixos e do título
plt.xticks(fontsize=7)
plt.yticks(fontsize=10)
plt.title(fontsize=12)

# Exiba o gráfico
plt.show()

