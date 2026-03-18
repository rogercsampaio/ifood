import streamlit as st
import json
from db import listar_feedbacks_com_produto, listar_produtos


emotion_map = {
    "Very Positive": "🤩",
    "Positive": "😊",
    "Neutral": "😐",
    "Negative": "😞",
    "Very Negative": "😡",
    "Incerto (Desconhecido)": "🤔"
}


def tela_listagem_feedbacks():

    st.title("Listagem de Feedbacks")

    feedbacks = listar_feedbacks_com_produto()

    if not feedbacks:
        st.info("Nenhum feedback cadastrado ainda.")
        return

    produtos = listar_produtos()

    for fb in feedbacks:
        with st.container():
            col1, col2 = st.columns([1, 5])

            # 🖼️ IMAGEM
            with col1:
                url_imagem = None
                for p in produtos:
                    if p["nome"] == fb["produto"]:
                        url_imagem = p["url_foto"]
                        break

                if url_imagem:
                    st.image(url_imagem, width=100)
                else:
                    st.text("Sem imagem")

            # 📄 INFORMAÇÕES
            with col2:
                emoji = emotion_map.get(fb["sentimento_final"], "🤔")

                st.markdown(f"**Produto:** {fb['produto']}")
                st.markdown(f"**Cliente:** {fb['nome_cliente']}")
                st.markdown(f"**Descrição:** {fb['descricao']}")
                st.markdown(f"**Sentimento:** {emoji} {fb['sentimento_final']}")

                # 🔥 CATEGORIAS (ROBUSTO)
                st.markdown("**Categorias identificadas:**")

                categorias_raw = fb.get("categoria")

                try:
                    categorias = json.loads(categorias_raw) if categorias_raw else []
                except:
                    categorias = []

                if categorias:
                    for cat in categorias:

                        # ✅ Caso 1: dict (formato ideal)
                        if isinstance(cat, dict):
                            label = cat.get("label")
                            score = float(cat.get("score", 0))

                        # ✅ Caso 2: tuple/lista (legado)
                        elif isinstance(cat, (list, tuple)) and len(cat) == 2:
                            label, score = cat
                            score = float(score)

                        else:
                            continue  # ignora lixo

                        st.write(f"• **{label}** — {score:.2f}")
                        st.progress(score)

                else:
                    st.write("Sem categorias")

                st.markdown(f"**Data/Hora:** {fb['data_hora']}")

            st.markdown("---")