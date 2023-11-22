from scrap import *
import numpy as np

done()

from geraanki import *
import pandas as pd


dItens = pd.read_csv('provasOrdernadasPorTri.csv', encoding='utf-8', decimal=',')
dTaltas = pd.read_csv('taltas.csv', encoding='utf-8', decimal=',')
dfNtaltas = dTaltas[dTaltas['OK']=='Y']  # Crie o DataFrame dfNtaltas vazio

for index, row in dTaltas.iterrows():
    if row['OK'] != 'Y':
        if row['Flashcards'] == 'Flashcards de RevisÃ£o, Flashcards de Treino':
            locaONE = questionBalance_65(row['Email'], float(row['TRI']), dItens)
            locaTwo = questionBalance_99(row['Email'], float(row['TRI']), dItens)
            enviar_email(row['Email'], locaONE)
            enviar_email(row['Email'], locaTwo)
        elif row['Flashcards'] == 'Flashcards de RevisÃ£o':
            locaONE = questionBalance_99(row['Email'], float(row['TRI']), dItens)
            enviar_email(row['Email'], locaONE)
        else:
           locaONE = questionBalance_65(row['Email'], float(row['TRI']), dItens)
           enviar_email(row['Email'], locaONE)

        row['OK'] = 'Y'
        dfNtaltas = dfNtaltas.append(row)  # Adicione a linha ao DataFrame dfNtaltas
        dfNtaltas.to_csv('taltas.csv', index=False, encoding='utf-8')
