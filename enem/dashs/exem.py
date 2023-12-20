ANO = st.sidebar.selectbox("Prova", dItens['ANO'].unique())

dItens_filtered = dItens[dItens['ANO'] == ANO]
col1, col2 = st.columns(2)

frequencia_sg_area = dItens_filtered['SG_AREA'].value_counts().reset_index()
fig = px.bar(frequencia_sg_area, x='SG_AREA', color='SG_AREA', y='count', title='Itens por área')
col1.plotly_chart(fig)

frequencia_sg_area = dItens_filtered['TX_GABARITO'].value_counts().reset_index()
fig = px.pie(frequencia_sg_area, names='TX_GABARITO', values='count', color='TX_GABARITO', title='Porcentagem de Gabarito')
col2.plotly_chart(fig)

dItens

frequencia_sg_area