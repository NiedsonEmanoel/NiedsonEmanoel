import pandas as pd

dItens2015 = pd.read_csv("E_ITENS_PROVA_2015.csv", sep=";", encoding="latin-1")
dItens2015a = pd.read_csv("E_ITENS_PROVA_2015.csv", sep=";", encoding="latin-1")

ilai = pd.read_excel('lai2015process.xlsx')

dItens2015['CO_HABILIDADE'].fillna(31, inplace=True)

for i in dItens2015.index:
    if dItens2015.loc[i, 'CO_HABILIDADE'] == 31:
        qs = ilai[ilai['COD'] == dItens2015.loc[i, 'CO_ITEM']]
        if not qs.empty:
            habilidade = qs.iloc[0]['Hab']  # Pega o primeiro valor de 'Hab' se houver
            print((habilidade))
            dItens2015.loc[i, 'CO_HABILIDADE'] = habilidade

dItens2015.to_csv('ITENS_PROVA_2015.csv', index=False, sep=";", encoding="latin-1")
dItens2015['CO_HABILIDADE'].value_counts()
dItens2015.to_excel('ITENS_PROVA_2015.xlsx')
dItens2015 = pd.read_csv("ITENS_PROVA_2015.csv", sep=";", encoding="latin-1")

