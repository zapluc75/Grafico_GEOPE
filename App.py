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
        plan = pd.read_excel(arquivo)
        plan_t = plan.T
        st.success("Dados carregados com sucesso!")
    except Exception as e:
        st.error(f"Erro ao carregar o arquivo: {e}")
        st.stop()

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.subheader("📄 Tabela Completa")
        fig_tabela = go.Figure(
            data=[
                go.Table(
                    header=dict(
                        values=list(plan.columns),
                        fill_color="lightgreen",
                        align="center",
                        font=dict(color="black", size=12)
                    ),
                    cells=dict(
                        values=[plan[c].tolist() for c in plan.columns],
                        fill_color="gray",
                        align="center",
                        font=dict(color="white", size=14)
                    )
                )
            ]
        )
     st.plotly_chart(fig_tabela, use_container_width=True)      
        st.subheader("📄 Tabela Invertida")
        fig_tabela_t = go.Figure(
            data=[
                go.Table(
                    header=dict(
                        values=list(plan_t.columns),
                        fill_color="lightgreen",
                        align="center",
                        font=dict(color="black", size=12)
                    ),
                    cells=dict(
                        values=[plan_t[c].tolist() for c in plan_t.columns],
                        fill_color="gray",
                        align="center",
                        font=dict(color="white", size=14)
                    )
                )
            ]
        )
    
    st.plotly_chart(fig_tabela_t, use_container_width=True)

    # --- Configuração do Gráfico ---
    cl1, cl2, cl3 = st.columns([1, 2, 1])

    with cl2:
        st.subheader("📊 Gráfico de Barras")

    # 🔁 NOVO: opção dinâmica
    modo = st.sidebar.selectbox("Modo do gráfico", ["Normal", "Invertido"])

    if modo == "Normal":
        col_nome_x = st.sidebar.selectbox("Coluna para eixo X", plan.columns)
        col_nome_y = st.sidebar.selectbox("Coluna para eixo Y", plan.columns)

        fig_barra = px.bar(
            plan,
            x=col_nome_x,
            y=col_nome_y,
            title=f"{col_nome_y} por {col_nome_x}",
            labels={col_nome_x: "Categoria", col_nome_y: "Valor"},
            hover_data={col_nome_x: True, col_nome_y: True},
            color=col_nome_x,
            text_auto=True
        )

    else:
        # 🔄 Inversão (transposição)
        try:
            # 🔁 Usuário escolhe a coluna que vira índice
            col_nome_x = st.sidebar.selectbox("Coluna para eixo X", plan_t.columns)
            col_nome_y = st.sidebar.selectbox("Coluna para eixo Y", plan_t.columns)
                                  
            fig_barra = px.bar(
                plan_t,
                x=col_nome_x,
                y=col_nome_y,
                title=f"{col_nome_y} por {col_nome_x}",
                labels={col_nome_x: "Categoria", col_nome_y: "Valor"},
                hover_data={col_nome_x: True, col_nome_y: True},
                color=col_nome_x,
                text_auto=True
            )
                   
        except Exception as e:
            st.error(f"Erro ao inverter os dados: {e}")
            st.stop()

    st.plotly_chart(fig_barra, use_container_width=True)
   
else:
    st.info("Envie um arquivo Excel na barra lateral para começar.")
