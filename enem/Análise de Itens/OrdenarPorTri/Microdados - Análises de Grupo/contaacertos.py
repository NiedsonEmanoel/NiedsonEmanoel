import pandas as pd
import numpy as np
import locale
Disciplina = "MT"

# Definir o locale para pt-BR
locale.setlocale(locale.LC_ALL, 'pt_BR.utf8')
# Carrega o arquivo CSV
dfENEM = pd.read_csv('MICRODADOS_ENEM_2021.csv', sep=';', encoding='latin-1')
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
    else:
        del dfENEM[x]

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
            + "\nEm porcentagem: "
            + str(percent)
            + "%"
            + "\nEm porcentagem (relativa): "
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
        if isinstance(respostas, str) and isinstance(gabarito, str):
            acertos = sum([1 for r, g in zip(respostas, gabarito) if r == g])
            return acertos
        else:
            return np.nan

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
    qtdAlunos = []

    for acertos in qtd_acertos:
        df_filtered = dfENEM.loc[dfENEM['T_ACERTOS_'+Disciplina] == acertos]
        notas_filtered = df_filtered['NU_NOTA_'+Disciplina].dropna()
        if len(notas_filtered) > 0:
            notas_min.append(notas_filtered.min())
            notas_max.append(notas_filtered.max())
            notas_mediana.append(notas_filtered.median())
            qtdAlunos.append(len(notas_filtered))
        else:
            notas_min.append(None)
            notas_max.append(None)
            notas_mediana.append(None)
            qtdAlunos.append(None)

    df_result = pd.DataFrame({'QTD_ACERTOS': qtd_acertos,
                            'NOTA_MIN': notas_min,
                            'NOTA_MEDIANA': notas_mediana,
                            'NOTA_MAX': notas_max,
                            'QTD_ALUNOS': qtdAlunos,
                            'Disciplina': Disciplina,
                            'ANO': Ano})
    return(df_result)

Quaest = TratamentoQuestoes(dfENEM, Disciplina)

frames = [Quaest]
dfTabelinhas = pd.concat(frames, ignore_index=True)
dfTabelinhas.to_excel('AcertosXTriEnem'+Disciplina+'_'+str(Ano)+'.xlsx')

salvar_em_txt(dcomplete, 'Percent_200to900_'+Disciplina+'_'+str(Ano)+'.txt')