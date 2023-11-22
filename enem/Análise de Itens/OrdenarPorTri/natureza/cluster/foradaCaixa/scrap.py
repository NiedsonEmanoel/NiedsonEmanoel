import pandas as pd
import requests
from io import StringIO

# URL do CSV
csv_url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vS4n98EfpV-7c4TIjLsPp39UTc2_XnNOtdzzboo9Cqn8kPeS21m4_J9Vg68dIH6wVx82iT6O3nRAjXJ/pub?gid=428127161&single=true&output=csv'
local_csv_filename = 'taltas.csv'

# Função para baixar o CSV da URL
def download_csv(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        return None

def done():
    # Verifique se o arquivo CSV já existe localmente
    try:
        df_existing = pd.read_csv(local_csv_filename, encoding='utf-8')
    except FileNotFoundError:
        df_existing = pd.DataFrame()

    # Baixe o CSV atual da URL
    csv_data = download_csv(csv_url)

    if csv_data is not None:
        # Crie um DataFrame com o CSV baixado
        df_new = pd.read_csv(StringIO(csv_data))

        # Concatene o DataFrame existente com o novo DataFrame
        df_combined = pd.concat([df_existing, df_new])

        # Remova linhas duplicadas com base em uma coluna de identificação (se aplicável)
        # Substitua 'coluna_identificacao' pelo nome da coluna que você deseja usar para identificação
        df_combined.drop_duplicates(subset='Prazo', keep='first', inplace=True)

        # Salve o DataFrame combinado com o nome 'selmas.csv' localmente
        df_combined.to_csv(local_csv_filename, index=False, encoding='utf-8')

        print("Dados atualizados e salvos como 'taltas.csv' com sucesso.")
    else:
        print("Falha ao baixar o CSV.")

done()