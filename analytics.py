import streamlit as st
from db import listar_feedbacks_com_produto, listar_produtos
from collections import Counter, defaultdict
import matplotlib.pyplot as plt
import json


SENTIMENT_MAP = {
    "Muito Negativo": 0,
    "Negativo": 2,
    "Neutro": 5,
    "Positivo": 8,
    "Muito Positivo": 10
}


# =========================
# 🔥 FUNÇÃO AUXILIAR
# =========================
def extrair_categorias(categoria_raw):
    try:
        categorias = json.loads(categoria_raw) if categoria_raw else []
    except:
        return []

    resultado = []

    for cat in categorias:
        if isinstance(cat, dict):
            resultado.append(cat.get("label"))
        elif isinstance(cat, (list, tuple)) and len(cat) == 2:
            resultado.append(cat[0])

    return resultado


def normalizar_sentimento(sent):
    if sent in ["Positivo", "Muito Positivo"]:
        return "Positivo"
    elif sent in ["Negativo", "Muito Negativo"]:
        return "Negativo"
    return "Neutro"


# =========================
# 📊 TELA ANALYTICS
# =========================
def tela_analytics_dashboard():

    st.title("📊 Analytics de Feedbacks de Produtos")

    feedbacks = listar_feedbacks_com_produto()

    if not feedbacks:
        st.info("Nenhum feedback disponível.")
        return

    produtos = listar_produtos()

    # =========================
    # 🔎 FILTROS
    # =========================
    st.subheader("🔎 Filtros")

    col_f1, col_f2 = st.columns(2)

    with col_f1:
        sentimento_filtro = st.selectbox(
            "Sentimento",
            ["Todos", "Positivo", "Negativo", "Neutro"]
        )

    with col_f2:
        nomes_produtos = ["Todos"] + sorted(list(set([fb["produto"] for fb in feedbacks])))
        produto_filtro = st.selectbox("Produto", nomes_produtos)

    # =========================
    # 🔥 FILTRAGEM
    # =========================
    feedbacks_filtrados = [
        fb for fb in feedbacks
        if (sentimento_filtro == "Todos" or normalizar_sentimento(fb["sentimento_final"]) == sentimento_filtro)
        and (produto_filtro == "Todos" or fb["produto"] == produto_filtro)
    ]

    if not feedbacks_filtrados:
        st.warning("Nenhum dado com os filtros aplicados.")
        return

    st.markdown("---")

    # =========================
    # ⭐ REPUTAÇÃO GERAL
    # =========================
    notas = [
        SENTIMENT_MAP[fb["sentimento_final"]]
        for fb in feedbacks_filtrados
        if fb["sentimento_final"] in SENTIMENT_MAP
    ]

    reputacao = round(sum(notas)/len(notas), 2) if notas else 0
    st.markdown(f"### ⭐ Reputação Geral: {reputacao}/10")

    # =========================
    # 📊 MÉTRICAS
    # =========================
    sentimentos_lista = [normalizar_sentimento(fb["sentimento_final"]) for fb in feedbacks_filtrados]
    contagem = Counter(sentimentos_lista)

    col1, col2, col3 = st.columns(3)
    col1.metric("👍 Positivos", contagem.get("Positivo", 0))
    col2.metric("👎 Negativos", contagem.get("Negativo", 0))
    col3.metric("😐 Neutros", contagem.get("Neutro", 0))

    st.markdown("---")

    # =========================
    # 📦 AGRUPAR POR PRODUTO
    # =========================
    produtos_dict = defaultdict(list)

    for fb in feedbacks_filtrados:
        produtos_dict[fb["produto"]].append(fb)

    st.subheader("📦 Análise por Produto")

    for produto, fbs in produtos_dict.items():

        st.markdown(f"## 🛒 {produto}")

        # ⭐ reputação
        notas_prod = [
            SENTIMENT_MAP[fb["sentimento_final"]]
            for fb in fbs
            if fb["sentimento_final"] in SENTIMENT_MAP
        ]

        reputacao_prod = round(sum(notas_prod)/len(notas_prod), 2) if notas_prod else 0

        colA, colB = st.columns(2)
        colA.metric("⭐ Reputação", f"{reputacao_prod}/10")
        colB.metric("📝 Total", len(fbs))

        # =========================
        # 📊 GRÁFICOS
        # =========================
        sentimentos = Counter([normalizar_sentimento(fb["sentimento_final"]) for fb in fbs])

        labels = ["Positivo", "Neutro", "Negativo"]
        valores = [sentimentos.get(l, 0) for l in labels]

        colG1, colG2 = st.columns(2)

        # 🔹 BARRA
        with colG1:
            fig, ax = plt.subplots(figsize=(2.5, 1.8))
            ax.bar(labels, valores)
            ax.set_title("Qtd", fontsize=7)
            ax.tick_params(axis='x', labelsize=7)
            ax.tick_params(axis='y', labelsize=7)
            st.pyplot(fig, use_container_width=False)

        # 🔹 PIZZA
        with colG2:
            fig2, ax2 = plt.subplots(figsize=(2.5, 1.8))

            if sum(valores) > 0:
                ax2.pie(valores, labels=labels, autopct='%1.0f%%', textprops={'fontsize': 7})
            else:
                ax2.text(0.5, 0.5, "Sem dados", ha='center')

            ax2.set_title("Distribuição", fontsize=7)
            st.pyplot(fig2, use_container_width=False)

        # =========================
        # 🏷️ CATEGORIAS
        # =========================
        todas_categorias = []

        for fb in fbs:
            todas_categorias.extend(extrair_categorias(fb["categoria"]))

        top_categorias = Counter(todas_categorias).most_common(5)

        st.markdown("**🏷️ Principais categorias:**")

        if top_categorias:
            for cat, qtd in top_categorias:
                st.markdown(f"- {cat} ({qtd})")
        else:
            st.write("Sem categorias")

        st.markdown("---")

    # =========================
    # 📝 ÚLTIMOS 3 FEEDBACKS
    # =========================
    st.subheader("📝 Últimos 3 Feedbacks")

    ult3 = sorted(feedbacks_filtrados, key=lambda x: x["data_hora"], reverse=True)[:3]

    for fb in ult3:
        with st.container():
            cols = st.columns([2, 5])

            # 🖼️ IMAGEM LOCAL (CORRIGIDO)
            with cols[0]:
                url_imagem = None
                for p in produtos:
                    if p["nome"] == fb["produto"]:
                        url_imagem = p["url_foto"]
                        break

                if url_imagem:
                    st.image(url_imagem, width = 150)
                else:
                    st.text("Sem imagem")

            # 📄 INFO
            with cols[1]:
                st.markdown(f"**Produto:** {fb['produto']}")
                st.markdown(f"**Cliente:** {fb['nome_cliente']}")
                st.markdown(f"**Sentimento:** {fb['sentimento_final']}")
                st.markdown(f"**Data:** {fb['data_hora']}")
                st.markdown(f"**Descrição:** {fb['descricao']}")

                categorias = extrair_categorias(fb["categoria"])[:3]

                if categorias:
                    st.markdown("**Categorias:**")
                    st.write(", ".join(categorias))
                else:
                    st.write("Sem categorias")

        st.markdown("---")