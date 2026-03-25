import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Visualização NUOPA", layout="wide")

st.title("📊 Visualização de Dados – NUOPA")

# --- Upload ---
st.sidebar.header("Configurações")
arquivo = st.sidebar.file_uploader("Envie o Excel (.xlsx)", type=["xlsx"])
opcao = st.sidebar.selectbox("Modo", ["Normal", "Invertido"])

if arquivo:
    try:
        df = pd.read_excel(arquivo)
        st.success("Dados carregados!")
    except Exception as e:
        st.error(f"Erro: {e}")
        st.stop()

    # 🔁 Define qual DataFrame será usado
    df_base = df if opcao == "Normal" else df.T.reset_index()

    # --- TABELA ---
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.subheader("📄 Tabela")

        fig_tabela = go.Figure(data=[
            go.Table(
                header=dict(
                    values=list(df_base.columns),
                    fill_color="lightgreen",
                    align="center",font=dict(color="black", size=12)
                ),
                cells=dict(
                    values=[df_base[c] for c in df_base.columns],
                    fill_color="gray",
                    align="center",font=dict(color="white", size=14)
                )
            )
        ])

        st.plotly_chart(fig_tabela, use_container_width=True)

    # --- GRÁFICO ---
    st.subheader("📊 Gráfico de Barras")

    col_nome_x = st.sidebar.selectbox("Eixo X", df_base.columns)
    col_nome_y = st.sidebar.selectbox("Eixo Y", df_base.columns)

    fig_barra = px.bar(
        df_base,
        x=col_nome_x,
        y=col_nome_y,
        color=col_nome_x,
        text_auto=True,
        title=f"{col_nome_y} por {col_nome_x}"
    )

    st.plotly_chart(fig_barra, use_container_width=True)

else:
    st.info("Envie um arquivo Excel para começar.")
