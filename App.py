import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Visualização NUOPA", layout="wide")

st.title("📊 Visualização de Dados – NUOPA")

# --- Upload do arquivo ---
st.sidebar.header("Configurações")
arquivo = st.sidebar.file_uploader("Envie o arquivo Excel (.xlsx)", type=["xlsx"])

if arquivo:
    try:
        df = pd.read_excel(arquivo)
        st.success("Dados carregados com sucesso!")
    except Exception as e:
        st.error(f"Erro ao carregar o arquivo: {e}")
        st.stop()

    st.subheader("📄 Tabela Completa")
    fig_tabela = go.Figure(
        data=[
            go.Table(
                header=dict(
                    values=list(df.columns),
                    fill_color="lightgreen",
                    align="center",font=dict(color="black", size=12)
                ),
                cells=dict(
                    values=[df[c].tolist() for c in df.columns],
                    fill_color="gray",
                    align="center",font=dict(color="white", size=14)
                )
            )
        ]
    )

    st.plotly_chart(fig_tabela, use_container_width=True)
    
    # --- Configuração do Gráfico ---
    st.subheader("📊 Gráfico de Barras")

    col_nome_x = st.selectbox("Coluna para eixo X", df.columns)
    col_nome_y = st.selectbox("Coluna para eixo Y", df.columns)

    fig_barra = px.bar(
        df,
        x=col_nome_x,
        y=col_nome_y,
        title=f"Gráfico de Barras de {col_nome_y} por {col_nome_x}",
        labels={col_nome_x: "Categoria", col_nome_y: "Valor"},
        hover_data={col_nome_x: True, col_nome_y: True},
        color=col_nome_x,
        text_auto=True
    )

    st.plotly_chart(fig_barra, use_container_width=True)
  

else:
    st.info("Envie um arquivo Excel na barra lateral para começar.")
