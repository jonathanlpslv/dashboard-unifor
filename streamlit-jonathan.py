import numpy as np
import pandas as pd
import plotly.express as px

import streamlit as st

df_ibyte=pd.read_csv('RECLAMEAQUI_IBYTE.csv')
df_hapivida=pd.read_csv('RECLAMEAQUI_HAPVIDA.csv')
df_nagem=pd.read_csv('RECLAMEAQUI_NAGEM.csv')

df_ibyte['EMPRESA'] = 'IBYTE'
df_hapivida['EMPRESA'] = 'HAPVIDA'
df_nagem['EMPRESA'] = 'NAGEM'

df = pd.concat([df_ibyte, df_hapivida, df_nagem])

df['TEMPO']=pd.to_datetime(df['TEMPO'])

estado_lista=[]
for i in range(len(df)):
    estado_lista.append(df['LOCAL'].iloc[i][-2:].strip())

df['ESTADO']=estado_lista

df['TOTAL_PALAVRAS'] = df['DESCRICAO'].apply(lambda x: len(x.split(" ")))

empresas = df['EMPRESA'].unique()
empresas = np.insert(empresas, 0, "Todas")

statuses = df["STATUS"].unique()
statuses = np.insert(statuses, 0, "Todas")

estados = df["ESTADO"].unique()
estados = np.insert(estados, 0, "Todos")

st.set_page_config(
   page_title = "Real-Time Reclame Aqui Dashboard",
   layout="wide"
)

st.session_state['total_experimentos']=len(df)

data = df

with st.sidebar:
    empresas_selected = st.selectbox("Seleção das Empresas", empresas)

    status_filter = st.selectbox("Selecione o Status", statuses)

    estado_filter = st.selectbox("Selecione o estado", estados)

if empresas_selected != "Todas":
    data = df[df['EMPRESA'] == empresas_selected]

if status_filter != "Todas":
    data = data[data["STATUS"] == status_filter]

if estado_filter != "Todos":
    data = data[data["ESTADO"] == estado_filter]

tab1, tab2 = st.tabs(["Dados", "Gráficos"])

with tab1:
    st.write("### Tabela de Dados do Reclame Aqui", data.sort_index())


with tab2:    
    df_serie = data[['EMPRESA', 'TEMPO', 'TOTAL_PALAVRAS']].set_index(['EMPRESA', 'TEMPO']).groupby(['EMPRESA', 'TEMPO'])['TOTAL_PALAVRAS'].count().reset_index()

    fig_hapvida = px.line(df_serie,
                            x = 'TEMPO',
                            y = 'TOTAL_PALAVRAS',
                            line_group = 'EMPRESA',
                            markers=True,
                            range_y=(0, df_serie.max()),
                            color = 'EMPRESA',
                            title= 'Série temporal do número de reclamações'
                    ).update_layout(
                       xaxis_title="Tempo", yaxis_title="Total"
                    )                            

    st.plotly_chart(fig_hapvida, use_container_width=True)    

    df_serie = data[['EMPRESA', 'TEMPO', 'TOTAL_PALAVRAS']].set_index(['EMPRESA', 'TEMPO']).groupby(['EMPRESA', 'TEMPO'])['TOTAL_PALAVRAS'].sum().reset_index()
    fig_hapvida = px.line(df_serie,
                            x = 'TEMPO',
                            y = 'TOTAL_PALAVRAS',
                            line_group = 'EMPRESA',
                            markers=True,
                            range_y=(0, df_serie.max()),
                            color = 'EMPRESA',
                            title= 'Distribuição do tamanho do texto'
                    ).update_layout(
                       xaxis_title="Tempo", yaxis_title="Total"
                    )

    st.plotly_chart(fig_hapvida, use_container_width=True)    
   
