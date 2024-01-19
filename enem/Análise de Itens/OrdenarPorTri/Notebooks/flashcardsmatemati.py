

# @markdown ##Insira seu nome
nome = "Niedson" # @param {type:"string"}

# @markdown ##Insira sua nota em Matemática
nota = 850 # @param {type:"number"}
nota = float(nota)

"""## Aperte Ctrl+F9 ou Ambiente de execução -> executar tudo
### O seu download iniciará em alguns segundos.

## **Ajustes de Sensibilidade do Algoritmo**
"""

prova = "MT" # @param ["CN", "MT", "LC", "CH"]
flashname = ''
if prova=='MT':
  flashname = 'Matemática'
elif prova == 'CN':
  flashname = 'Natureza'
elif prova == 'LC':
  flashname == 'Linguagens'
else:
  flashname = 'Humanas'

aj165 = 200 # @param {type:"slider", min:10, max:200, step:5}

aj265 = 30 # @param {type:"slider", min:10, max:100, step:5}

aj399 = 130 # @param {type:"slider", min:10, max:200, step:5}

aj499 = 10 # @param {type:"slider", min:10, max:100, step:5}

"""## Código"""

!pip install genanki
urlItens = "https://github.com/NiedsonEmanoel/NiedsonEmanoel/raw/main/enem/An%C3%A1lise%20de%20Itens/OrdenarPorTri/gerador/provasOrdernadasPorTri.csv"

import pandas as pd
import random
import time
import genanki
import os

dItens = pd.read_csv(urlItens, encoding='utf-8', decimal=',')

def generate_random_number():
    # Obter o timestamp atual em segundos
    timestamp = int(time.time())

    # Definir o timestamp como semente para a função random
    random.seed(timestamp)

    # Gerar um número inteiro aleatório entre 0 e 100000
    return random.randint(0, 100000)

# Criar um modelo para os flashcards
modelo = genanki.Model(
    generate_random_number(),
    str(generate_random_number()),
    fields=[
        {'name': 'MyMedia'},
        {'name': 'Questão'},
        {'name': 'Resposta'}
    ],
    templates=[
        {
            'name': 'Cartão 1',
            'qfmt': '<b>{{Questão}}</b><hr>{{MyMedia}}',
            'afmt': '{{FrontSide}}<br><hr><b>{{Resposta}}</b>',
        },
    ])

def questionBalance_65(name, nota_CN, dfResult):

    nota_CNMaior = nota_CN + aj165
    nota_CNMenor = nota_CN - aj265

    dfResult = dfResult.query("IN_ITEM_ABAN == 0 and TP_LINGUA not in [0, 1]")

    cols_to_drop = ['TP_LINGUA', 'TX_MOTIVO_ABAN', 'IN_ITEM_ABAN', 'IN_ITEM_ADAPTADO', 'NU_PARAM_A', 'NU_PARAM_B', 'NU_PARAM_C']
    dfResult.drop(cols_to_drop, axis=1, inplace=True)

    # Para a área de Natureza (CN)
    dfResult_CN = dfResult[dfResult['SG_AREA'] == prova]
    dfResult_CN = dfResult_CN[dfResult_CN['theta_065'] <= nota_CNMaior]
    dfResult_CN = dfResult_CN[dfResult_CN['theta_065'] >= nota_CNMenor]
    dfResult_CN.sort_values('theta_065', ascending=True, inplace=True)
    dfResult_CN['indexacao'] = dfResult_CN.reset_index().index + 1

    # Criar um baralho para armazenar os flashcards
    baralho = genanki.Deck(
        generate_random_number(), # Um número aleatório que identifica o baralho
        str('TRI::Treino::'+str(flashname)) # O nome do baralho
    )

    # Criar uma lista para armazenar as informações dos flashcards
    flashcards = []

    # Percorrer as linhas do dataframe dfResult_CN
    for i in dfResult_CN.index:
        # Obter o nome do arquivo de imagem da questão
        imagem = str(dfResult_CN.loc[i, "CO_ITEM"]) + '.png'

        # Obter a resposta da questão
        resposta =str('Gabarito: ')+ str(dfResult_CN.loc[i, 'TX_GABARITO'])
        inic = "Q" + str(dfResult_CN.loc[i, "CO_POSICAO"]) + ':' + str(dfResult_CN.loc[i, "ANO"]) + ' - H' + str(dfResult_CN.loc[i, "CO_HABILIDADE"].astype(int)) + " - Proficiência: " + str(dfResult_CN.loc[i, "theta_065"].round(2))

        # Criar um flashcard com a imagem e a resposta
        flashcard = genanki.Note(
            model=modelo,
            fields=[inic,'<img src="https://niedsonemanoel.com.br/enem/An%C3%A1lise%20de%20Itens/OrdenarPorTri/1.%20Itens%20BNI_/' + imagem + '"]', resposta]
        )

        # Adicionar o flashcard à lista de flashcards
        flashcards.append(flashcard)

    for flashcard in flashcards:
        baralho.add_note(flashcard)

    # Criar um pacote com o baralho e as imagens
    pacote = genanki.Package(baralho)

    pacote.write_to_file(name+'_'+str(flashname)+'_065.apkg')
    return name+'_'+str(flashname)+'_065.apkg'

def questionBalance_99(name, nota_CN, dfResult):

    nota_CNMaior = nota_CN + aj399
    nota_CNMenor = nota_CN - aj499

    dfResult = dfResult[dfResult['IN_ITEM_ABAN'] == 0]
    dfResult = dfResult[dfResult['TP_LINGUA'] != 0]
    dfResult = dfResult[dfResult['TP_LINGUA'] != 1]

    cols_to_drop = ['TP_LINGUA', 'TX_MOTIVO_ABAN', 'IN_ITEM_ABAN', 'IN_ITEM_ADAPTADO', 'NU_PARAM_A', 'NU_PARAM_B', 'NU_PARAM_C']
    dfResult.drop(cols_to_drop, axis=1, inplace=True)

    dfResult_CN = dfResult[dfResult['SG_AREA'] == prova]
    dfResultInterc = dfResult_CN[dfResult_CN['theta_065'] <= nota_CN+aj165]
    dfResultInterc = dfResult_CN[dfResult_CN['theta_065'] >= nota_CN-aj265]
    dfResult_CN = dfResult_CN[dfResult_CN['theta_099'] <= nota_CNMaior]
    dfResult_CN = dfResult_CN[dfResult_CN['theta_099'] >= nota_CNMenor]
    dfResult_CN = dfResult_CN[~dfResult_CN['theta_065'].isin(dfResultInterc['theta_065'])]
    dfResult_CN.sort_values('theta_065', ascending=True, inplace=True)
    dfResult_CN['indexacao'] = dfResult_CN.reset_index().index + 1

    baralho = genanki.Deck(
        generate_random_number(), # Um número aleatório que identifica o baralho
        str('TRI::Revisão::'+str(flashname)) # O nome do baralho
    )

    # Criar uma lista para armazenar as informações dos flashcards
    flashcards = []

    # Percorrer as linhas do dataframe dfResult_CN
    for i in dfResult_CN.index:
        # Obter o nome do arquivo de imagem da questão
        imagem = str(dfResult_CN.loc[i, "CO_ITEM"]) + '.png'

        # Obter a resposta da questão
        resposta =str('Gabarito: ')+ str(dfResult_CN.loc[i, 'TX_GABARITO'])
        inic = "Q" + str(dfResult_CN.loc[i, "CO_POSICAO"]) + ':' + str(dfResult_CN.loc[i, "ANO"]) + ' - H' + str(dfResult_CN.loc[i, "CO_HABILIDADE"].astype(int)) + " - Proficiência: " + str(dfResult_CN.loc[i, "theta_065"].round(2))

        # Criar um flashcard com a imagem e a resposta
        flashcard = genanki.Note(
            model=modelo,
            fields=[inic,'<img src="https://niedsonemanoel.com.br/enem/An%C3%A1lise%20de%20Itens/OrdenarPorTri/1.%20Itens%20BNI_/' + imagem + '"]', resposta]
        )

        # Adicionar o flashcard à lista de flashcards
        flashcards.append(flashcard)

    for flashcard in flashcards:
        baralho.add_note(flashcard)

    # Criar um pacote com o baralho e as imagens
    pacote = genanki.Package(baralho)

    pacote.write_to_file(name+'_'+str(flashname)+'_099.apkg')
    return name+'_'+str(flashname)+'_099.apkg'

loc65 = questionBalance_65(nome, nota, dItens)


loc99 = questionBalance_99(nome, nota, dItens)
