import pandas as pd
from pycaret.regression import *

# Carrega o arquivo CSV
dfENEM = pd.read_csv('mc.csv', sep=';', encoding='latin-1')

# Filtra apenas as linhas em que o aluno esteve presente (TP_PRESENCA_MT = 1), 
# a prova matemática (CO_PROVA_MT = 303) e a nota de matemática é maior que 1

for x in dfENEM.keys():
    if x == "TX_RESPOSTAS_MT":
        print('IGNORED')
    elif x == "NU_NOTA_MT":
        print('IGNORED')
    elif x == "TX_GABARITO_MT":
        print("IGNORED")

    elif x == "TX_RESPOSTAS_LC":
        print('IGNORED')    
    elif x == "NU_NOTA_LC":
        print('IGNORED')
    elif x == "TX_GABARITO_LC":
        print("IGNORED")

    elif x == "TX_RESPOSTAS_CH":
        print('IGNORED')    
    elif x == "NU_NOTA_CH":
        print('IGNORED')
    elif x == "TX_GABARITO_CH":
        print("IGNORED")

    elif x == "TX_RESPOSTAS_CN":
        print('IGNORED')    
    elif x == "NU_NOTA_CN":
        print('IGNORED')
    elif x == "TX_GABARITO_CN":
        print("IGNORED")    
    else:
        del dfENEM[x]

dfENEM = dfENEM[dfENEM['TP_PRESENCA_MT'] == 1]
dfENEM = dfENEM[dfENEM['NU_NOTA_MT'] > 1]

# Remove colunas que não serão utilizadas
for x in dfENEM.keys():
    if(x == "TX_RESPOSTAS_MT"):
        print('IGNORED')
    elif x== "NU_NOTA_MT":
        print('IGNORED')
    elif x == "TX_GABARITO_MT":
        print("IGNORED")
    else:
        del dfENEM[x]

# Função para calcular o número de acertos do aluno em cada questão
def CalculaAcerto(Disciplina, Df):
    campo_resp = 'TX_RESPOSTAS_'+Disciplina
    campo_gab = 'TX_GABARITO_'+Disciplina

    # Adiciona colunas para armazenar o número de acertos em cada questão
    for l in range(45):
            campo_destino = str("ACERTOS_"+Disciplina+"_"+str(l))
            Df[campo_destino] = 0
            print('Colunas feitas')

    # Percorre cada linha do DataFrame e compara as respostas com o gabarito
    for x in Df[campo_resp].keys():
        respostas = list(Df[campo_resp][x])
        gabarito = list(Df[campo_gab][x])
        print(x)
        for j in range(45):
            campo_destino = str("ACERTOS_"+Disciplina+"_"+str(j))

            if(respostas[j] == gabarito[j]):
                Df.loc[x, campo_destino]= 1
    return Df

# Chama a função CalculaAcerto para a disciplina de matemática (MT)
dfENEM = CalculaAcerto("MT", dfENEM)

# Remove as colunas de respostas e gabarito
del dfENEM['TX_RESPOSTAS_MT']
del dfENEM['TX_GABARITO_MT']

# ----------------------------------------------------- #

# Configurando o modelo de regressão
LingRegression = setup(dfENEM, target='NU_NOTA_MT', normalize=True, use_gpu=True)

# Criando um modelo de regressão básico
lrModel = create_model('br')

# Afinando o modelo criado
lrModel_Tunned = tune_model(lrModel)

# Finalizando o modelo
lrModelFinal = finalize_model(lrModel_Tunned)

# Convertendo o modelo para o código JavaScript
jsCode = convert_model(lrModel_Tunned, 'javascript')

# Salvando o código JavaScript em um arquivo
arquivoJS = open('MT_303_MODEL.js', 'a+')
arquivoJS.write('export '+jsCode)
arquivoJS.close()

# Salvando o modelo final
save_model(lrModelFinal, 'MT_303')

# Plotando vários gráficos de avaliação do modelo
plot_model(lrModel_Tunned, plot='residuals')
plot_model(lrModel_Tunned, plot='error')
plot_model(lrModel_Tunned, plot='cooks')
plot_model(lrModel_Tunned, plot='learning')
plot_model(lrModel_Tunned, plot='feature_all')

# Amostrando uma parte do conjunto de dados para previsão
dfEnem_sam = dfENEM.sample(frac=0.0001, random_state=9)

# Carregando o modelo salvo
dtLoad = load_model('MT_303')

# Fazendo previsões no conjunto de dados amostrado
predict_model(dtLoad, data=dfEnem_sam)