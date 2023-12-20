import pandas as pd
import numpy as np
import time
import plotly.express as px
import streamlit as st
import numpy as np
from scipy.optimize import minimize_scalar

def calcular_probabilidade(theta, a, b, c):
    return c + (1 - c) / (1 + np.exp(-a * (theta - b)))

def calcular_verossimilhanca(theta, a, b, c, x):
    if x.ndim == 1:
        x = np.expand_dims(x, axis=1)
    num_itens, num_candidatos = x.shape
    verossimilhanca = np.ones(num_candidatos)
    for i, item in enumerate(x):
        p = calcular_probabilidade(theta, a[i], b[i], c[i])
        verossimilhanca *= np.power(p, item) * np.power(1 - p, 1 - item)
    return np.prod(verossimilhanca)

def encontrar_theta_max(a, b, c, x):
    if len(a) != x.shape[0] or len(b) != x.shape[0] or len(c) != x.shape[0]:
        raise ValueError("O comprimento das listas de parâmetros a, b e c deve corresponder ao número de itens em x.")

    if x.ndim == 1:
        x = np.expand_dims(x, axis=1)

    theta_max_list = []
    for i in range(x.shape[1]):
        result = minimize_scalar(lambda theta: -calcular_verossimilhanca(theta, a, b, c, x[:, i]), bounds=(-3, 5), method='bounded')
        theta_max_list.append(result.x * 100 + 500)
    return theta_max_list

st.set_page_config(layout='wide', page_title='Enemaster.app', initial_sidebar_state="expanded", page_icon="🧊",    menu_items={
        'About': "# Feito por *enemaster.app*"
    })

st.sidebar.markdown(f'<img width="100%" src="https://raw.githubusercontent.com/NiedsonEmanoel/NiedsonEmanoel/main/enem/An%C3%A1lise%20de%20Itens/OrdenarPorTri/natureza/EneMaster.png">',unsafe_allow_html=True)
st.sidebar.markdown(f"<br><hr>",unsafe_allow_html=True)
Nome = st.sidebar.text_input('Nome')
email = st.sidebar.text_input('Email')

st.sidebar.markdown(f"<hr>",unsafe_allow_html=True)
uploaded_file = st.sidebar.file_uploader("Envie o arquivo do Simulado", type=['csv'])
if uploaded_file is not None:
    dItens = pd.read_csv(uploaded_file, encoding='utf-8', decimal=',')
    a, b, c = zip(*dItens[['NU_PARAM_A', 'NU_PARAM_B', 'NU_PARAM_C']].values.tolist())
    total = len(a)
    st.title("Simulado:")
else:
    st.title("Adicione o arquivo .csv do seu simulado ao lado.")

anwers = []

with st.form("form"):

    if uploaded_file is not None:
        for i in dItens.index:
            l = dItens.loc[i, "imagAPI"]
            st.markdown(f'<img src="{l}">',unsafe_allow_html=True)
            st.markdown(f"<br>",unsafe_allow_html=True)
            Resposta = st.radio('Resposta', ['A', 'B', 'C', 'D', 'E'], horizontal=True, key=dItens.loc[i, "CO_ITEM"])
            if dItens.loc[i, "TX_GABARITO"] == Resposta:
                anwers.append(1)
            else:
                anwers.append(0)
    
            st.markdown(f"<hr>",unsafe_allow_html=True)

        submitted = st.form_submit_button("Concluir!", type="primary")
        if submitted:
            x = np.array(anwers)
            with st.spinner("Estimando sua nota TRI..."):
                time.sleep(2)
                theta_max_list = encontrar_theta_max(a, b, c, x)
            tri = round(theta_max_list[0],2)
            st.success('Sua nota aproximada é: '+str(tri), icon="✅")
            st.balloons()
            
