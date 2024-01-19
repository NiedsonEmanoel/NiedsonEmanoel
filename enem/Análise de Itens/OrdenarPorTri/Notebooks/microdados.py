

ANO = "2022" # @param ["2014", "2015", "2016", "2017", "2018", "2019", "2020", "2021", "2022", "2023"]
Disciplina = "MT" # @param ["CN", "MT", "LC", "CH"]

MICRODADOS_2014 = "https://download.inep.gov.br/microdados/microdados_enem_2014.zip" # @param {type:"string"}
MICRODADOS_2015 = "https://download.inep.gov.br/microdados/microdados_enem_2015.zip" # @param {type:"string"}
MICRODADOS_2016 = "https://download.inep.gov.br/microdados/microdados_enem_2016.zip" # @param {type:"string"}
MICRODADOS_2017 = "https://download.inep.gov.br/microdados/microdados_enem_2017.zip" # @param {type:"string"}
MICRODADOS_2018 = "https://download.inep.gov.br/microdados/microdados_enem_2018.zip" # @param {type:"string"}
MICRODADOS_2019 = "https://download.inep.gov.br/microdados/microdados_enem_2019.zip" # @param {type:"string"}
MICRODADOS_2020 = "https://download.inep.gov.br/microdados/microdados_enem_2020.zip" # @param {type:"string"}
MICRODADOS_2021 = "https://download.inep.gov.br/microdados/microdados_enem_2021.zip" # @param {type:"string"}
MICRODADOS_2022 = "https://download.inep.gov.br/microdados/microdados_enem_2022.zip" # @param {type:"string"}
MICRODADOS_2023 = "" # @param {type:"string"}


mcd = {
    '2014': {
        'link': MICRODADOS_2014
    },
    '2015': {
        'link': MICRODADOS_2015
    },
    '2016': {
        'link': MICRODADOS_2016
    },
    '2017': {
        'link': MICRODADOS_2017
    },
    '2018': {
        'link': MICRODADOS_2018
    },
    '2019': {
        'link': MICRODADOS_2019
    },
    '2020': {
        'link': MICRODADOS_2020
    },
    '2021': {
        'link': MICRODADOS_2021
    },
    '2022': {
        'link': MICRODADOS_2022
    },
    '2023': {
        'link': MICRODADOS_2023
    }
}

"""## Código"""

import os
import zipfile
import pandas as pd
import numpy as np

url = mcd[ANO]['link']
destino = "MICRODADOS_"+ANO+".zip"
!wget {url} -O {destino} --no-check-certificate
pasta_destino = 'microdados'
# Criar um objeto ZipFile
with zipfile.ZipFile(destino, 'r') as zip_ref:
    # Extrair todos os arquivos para a pasta de destino
    zip_ref.extractall(pasta_destino)

print(f'Arquivo ZIP descompactado em {pasta_destino}')
os.remove(destino)

dfENEM = pd.read_csv('microdados/DADOS/MICRODADOS_ENEM_'+ANO+'.csv', sep=';', encoding='latin-1')
totPart = dfENEM.shape[0]
Ano = dfENEM.loc[0, "NU_ANO"]

dfENEM = dfENEM[dfENEM['TP_PRESENCA_'+Disciplina] == 1]
dfENEM = dfENEM[dfENEM["NU_NOTA_"+Disciplina] != 0]

totPartRela = dfENEM.shape[0]

for x in dfENEM.keys():
    if x == "TX_RESPOSTAS_"+Disciplina:
        print('')
    elif x == "NU_NOTA_"+Disciplina:
        print('')
    elif x == "TX_GABARITO_"+Disciplina:
        print("")

    elif x == "TP_LINGUA":
        print('')

    else:
        del dfENEM[x]

import locale
def CalculaPercentNota(Df, Nota):
    Df = Df[Df["NU_NOTA_"+Disciplina] >= Nota]
    qtd = Df.shape[0]
    percent = (qtd/totPart)*100
    percentRel = (qtd/totPartRela)*100

    qtd = locale.format("%.0f", Df.shape[0], grouping=True)
    percent = locale.format("%.3f", percent, grouping=True)
    thisTot = locale.format("%.0f", totPart, grouping=True)
    thisTotRela = locale.format("%.3f", percentRel, grouping=True)

    return (
            str(qtd)
            + " Alunos tiraram "
            + str(Nota)
            + "+ em "
            + Disciplina
            + " no ENEM "
            + str(Ano)
            + ".\nTotal de participantes: "
            + str(thisTot)
            + "\nEm porcentagem (total participantes): "
            + str(percent)
            + "%"
            + "\nEm porcentagem (alunos válidos): "
            + str(thisTotRela)
            + "%\n\n"

        )

dcomplete = ""
for nota in range(900, 199, -100):
    d = CalculaPercentNota(dfENEM, nota)
    dcomplete += str(d)

def CalculaAcerto(Disciplina, Df):
    campo_resp = 'TX_RESPOSTAS_'+Disciplina
    campo_gab = 'TX_GABARITO_'+Disciplina

    def conta_acertos(row):
        respostas = row[campo_resp]
        gabarito = row[campo_gab]
        tp_lingua = row['TP_LINGUA']

        cont = 0

        for i in range(0, len(respostas)):
            if respostas[i] == gabarito[i]:
                # Se a resposta e o gabarito for o mesmo soma 1 na contagem
                cont += 1
        return cont
    # Aplica a função para contar os acertos em cada linha e armazena na nova coluna criada
    Df[f'T_ACERTOS_{Disciplina}'] = Df.apply(conta_acertos, axis=1)
    campDel = str('TX_RESPOSTAS_'+Disciplina)
    campDelT = str('TX_GABARITO_'+Disciplina)
    del Df[campDel]
    del Df[campDelT]
    return Df

# Chama a função CalculaAcerto
dfENEM = CalculaAcerto(Disciplina, dfENEM)

def salvar_em_txt(texto, nome_arquivo):
    with open(nome_arquivo, 'w') as arquivo:
        arquivo.write(texto)

def TratamentoQuestoes(dfENEM, Disciplina):
    qtd_acertos = list(range(int(dfENEM['T_ACERTOS_'+Disciplina].max()) + 1))
    notas_min = []
    notas_max = []
    notas_mediana = []

    for acertos in qtd_acertos:
        df_filtered = dfENEM.loc[dfENEM['T_ACERTOS_'+Disciplina] == acertos]
        notas_filtered = df_filtered['NU_NOTA_'+Disciplina].dropna()
        if len(notas_filtered) > 0:
            notas_min.append(notas_filtered.min())
            notas_max.append(notas_filtered.max())
            notas_mediana.append(notas_filtered.median())
        else:
            notas_min.append(None)
            notas_max.append(None)
            notas_mediana.append(None)

    df_result = pd.DataFrame({'QTD_ACERTOS': qtd_acertos,
                            'NOTA_MIN': notas_min,
                            'NOTA_MEDIANA': notas_mediana,
                            'NOTA_MAX': notas_max,
                            'Disciplina': Disciplina,
                            'ANO': Ano})
    return(df_result)

Quaest = TratamentoQuestoes(dfENEM, Disciplina)

frames = [Quaest]
dfTabelinhas = pd.concat(frames, ignore_index=True)
dfTabelinhas.to_excel('AcertosXTriEnem'+Disciplina+'_'+str(Ano)+'.xlsx')

salvar_em_txt(dcomplete, 'Percent_200to900_'+Disciplina+'_'+str(Ano)+'.txt')

from google.colab import files
files.download('AcertosXTriEnem'+Disciplina+'_'+str(Ano)+'.xlsx')