import pandas as pd
import requests
import os
import time

ano = '2019'
adit = '/'
#adit = '-2/'
#adit = '/digital/'
#adit = '/presencial/'

df = pd.read_csv('ITENS_PROVA_'+ano+'.csv', sep=";", encoding="latin-1")
ano = str(ano)+str(adit)

provas = [512, 508, 504, 516]

df = df[df.CO_PROVA.isin(provas)]
df = df.query("IN_ITEM_ABAN == 0 and TP_LINGUA not in [0, 1]")
#df = df.query("TP_VERSAO_DIGITAL not in [1]")

output_directory = 'ComentadaCorrecao'
os.makedirs(output_directory, exist_ok=True)


for i in df.index:
#    time.sleep(10)
    li = str(df.loc[i, 'CO_POSICAO']).zfill(3) + str(df.loc[i, 'TX_GABARITO']).lower()
    lo = '.'
    nameIten = str(df.loc[i, 'CO_ITEM'])+ '.gif'
    if df.loc[i, 'SG_AREA'] == 'LC':
        lo = '1dia'
    elif df.loc[i, 'SG_AREA'] == 'CH':
        lo = '1dia'
    else:
        lo = '2dia'
    po = 'https://www.curso-objetivo.br/vestibular/resolucao_comentada/enem/'+ano+lo+'/'+li+'.gif?v1'
    print(po)
    # Obter o nome do arquivo a partir da URL
    filename = os.path.join(output_directory, nameIten)

    # Verificar se a imagem já existe localmente
    if os.path.exists(filename):
        print(f'A imagem para o item {nameIten} já existe localmente.')
    else:
        # Se a imagem não existe, fazer o download
        response = requests.get(po, verify=False)
        with open(filename, 'wb') as file:
            file.write(response.content)
        print(f'Imagem salva em: {filename}')


#doesngetbeen = []
#df = df[df.CO_ITEM.isin(doesngetbeen)]
