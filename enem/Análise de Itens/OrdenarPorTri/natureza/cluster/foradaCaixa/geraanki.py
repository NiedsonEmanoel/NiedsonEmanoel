import pandas as pd
from fpdf import FPDF
from PIL import Image
import random
import time
import genanki
import os
pd.options.mode.chained_assignment = None

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib

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

    nota_CNMaior = nota_CN + 150
    nota_CNMenor = nota_CN - 25

    dfResult = dfResult.query("IN_ITEM_ABAN == 0 and TP_LINGUA not in [0, 1]")

    cols_to_drop = ['TP_LINGUA', 'TX_MOTIVO_ABAN', 'IN_ITEM_ABAN', 'IN_ITEM_ADAPTADO', 'NU_PARAM_A', 'NU_PARAM_B', 'NU_PARAM_C']
    dfResult.drop(cols_to_drop, axis=1, inplace=True)

    # Para a área de Natureza (CN)
    dfResult_CN = dfResult[dfResult['SG_AREA'] == 'CN']
    dfResult_CN = dfResult_CN[dfResult_CN['theta_065'] <= nota_CNMaior]
    dfResult_CN = dfResult_CN[dfResult_CN['theta_065'] >= nota_CNMenor]
    dfResult_CN.sort_values('theta_065', ascending=True, inplace=True)
    dfResult_CN['indexacao'] = dfResult_CN.reset_index().index + 1

    # Criar um baralho para armazenar os flashcards
    baralho = genanki.Deck(
        generate_random_number(), # Um número aleatório que identifica o baralho
        str('TRI::Treino::Natureza') # O nome do baralho
    )

    # Criar uma lista para armazenar as informações dos flashcards
    flashcards = []

    # Percorrer as linhas do dataframe dfResult_CN
    for i in dfResult_CN.index:
        # Obter o nome do arquivo de imagem da questão
        imagem = str(dfResult_CN.loc[i, "CO_ITEM"]) + '.png'
        
        # Obter a resposta da questão
        resposta =str('Gabarito: ')+ str(dfResult_CN.loc[i, 'TX_GABARITO'])+str('<br><br>Licenciado para Selma Calgaroto, uso sob cortesia para: '+name) + str('<br>A distribuição indevida desse material é facilmente identificável. O autor reserva-se ao direito de processar criminalmente/civilmente quem usurpar o uso justo desse material.')
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

    pacote.write_to_file('Saidas/Flashcards/Natureza_'+name+'_065.apkg')
    return 'Saidas/Flashcards/Natureza_'+name+'_065.apkg'

def questionBalance_99(name, nota_CN, dfResult):

    nota_CNMaior = nota_CN + 100
    nota_CNMenor = nota_CN 

    dfResult = dfResult[dfResult['IN_ITEM_ABAN'] == 0]
    dfResult = dfResult[dfResult['TP_LINGUA'] != 0]
    dfResult = dfResult[dfResult['TP_LINGUA'] != 1]

    cols_to_drop = ['TP_LINGUA', 'TX_MOTIVO_ABAN', 'IN_ITEM_ABAN', 'IN_ITEM_ADAPTADO', 'NU_PARAM_A', 'NU_PARAM_B', 'NU_PARAM_C']
    dfResult.drop(cols_to_drop, axis=1, inplace=True)

    dfResult_CN = dfResult[dfResult['SG_AREA'] == 'CN']
    dfResultInterc = dfResult_CN[dfResult_CN['theta_065'] <= nota_CN+150]
    dfResultInterc = dfResult_CN[dfResult_CN['theta_065'] >= nota_CN-25]
    dfResult_CN = dfResult_CN[dfResult_CN['theta_099'] <= nota_CNMaior]
    dfResult_CN = dfResult_CN[dfResult_CN['theta_099'] >= nota_CNMenor]
    dfResult_CN = dfResult_CN[~dfResult_CN['theta_065'].isin(dfResultInterc['theta_065'])]
    dfResult_CN.sort_values('theta_065', ascending=True, inplace=True)
    dfResult_CN['indexacao'] = dfResult_CN.reset_index().index + 1

    baralho = genanki.Deck(
        generate_random_number(), # Um número aleatório que identifica o baralho
        str('TRI::Revisão::Natureza') # O nome do baralho
    )

    # Criar uma lista para armazenar as informações dos flashcards
    flashcards = []

    # Percorrer as linhas do dataframe dfResult_CN
    for i in dfResult_CN.index:
        # Obter o nome do arquivo de imagem da questão
        imagem = str(dfResult_CN.loc[i, "CO_ITEM"]) + '.png'
        
        # Obter a resposta da questão
        resposta =str('Gabarito: ')+ str(dfResult_CN.loc[i, 'TX_GABARITO'])+str('<br><br>Licenciado para Selma Calgaroto, uso sob cortesia para: '+name) + str('<br>A distribuição indevida desse material é facilmente identificável. O autor reserva-se ao direito de processar criminalmente/civilmente quem usurpar o uso justo desse material.')
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

    pacote.write_to_file('Saidas/Flashcards/Natureza_'+name+'_099.apkg')
    return 'Saidas/Flashcards/Natureza_'+name+'_099.apkg'

def enviar_email(receiver_email, files):

    subject = 'Flashcards'

    smtp_server='smtp.gmail.com'
    smtp_port=587
    smtp_username='smtp.niedson@gmail.com'
    smtp_password='hpvepsdpvtstsjiz'

    filename = files

    body = 'Olá seguem os flashcards solicitados. - NÃO RESPONDA ESSE E-MAIL.'
    # Criação da mensagem de email
    message = MIMEMultipart()
    sender_email = smtp_username
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject

    # Adiciona o corpo do email
    message.attach(MIMEText(body, 'plain'))

    # Anexa o arquivo PDF
    attachment = open(filename, 'rb')

    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment', filename=filename)

    message.attach(part)

    # Conecta-se ao servidor SMTP e envia o email
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        text = message.as_string()
        server.sendmail(sender_email, receiver_email, text)
        server.quit()
        print('Email enviado com sucesso!')
    except Exception as e:
        print('Ocorreu um erro ao enviar o email:', str(e))

