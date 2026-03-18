import streamlit as st
import json
from db import listar_produtos, criar_feedback
from modelo_analise_sentimentos import predict_sentiment
from modelo_reconhecimento_categorias_feedback import predict


emotion_map = {
    "Very Positive": "🤩",
    "Positive": "😊",
    "Neutral": "😐",
    "Negative": "😞",
    "Very Negative": "😡",
    "Incerto (Desconhecido)": "🤔"
}


def tela_feedback():

    st.title("Cadastro de Feedback")

    produtos = listar_produtos()

    if not produtos:
        st.warning("Nenhum produto cadastrado. Cadastre um produto antes de registrar feedback.")
        return

    nomes_produtos = [produto["nome"] for produto in produtos]

    # SELECTBOX FORA DO FORM
    produto_nome = st.selectbox("Produto", nomes_produtos)

    produto_selecionado = next(
        (p for p in produtos if p["nome"] == produto_nome),
        None
    )

    # imagem do produto
    if produto_selecionado and produto_selecionado["url_foto"]:
        st.image(produto_selecionado["url_foto"], width=120)

    # FORM
    with st.form("form_feedback"):
        nome_cliente = st.text_input("Nome do cliente")
        descricao = st.text_area("Descrição do feedback")
        submitted = st.form_submit_button("Cadastrar feedback")

    # PROCESSAMENTO
    if submitted:

        if not descricao:
            st.error("A descrição do feedback é obrigatória.")
            return

        with st.spinner("🧠 IA analisando feedback..."):

            # sentimento
            resultado = predict_sentiment(descricao)
            sentimento_final = resultado[0]["predicted_label"]

            # categorias (top 3)
            categoria_feedback = predict(descricao)

        # salvar no banco (JSON)
        criar_feedback(
            nome_cliente,
            descricao,
            sentimento_final,
            json.dumps(categoria_feedback),
            produto_selecionado["id"]
        )

        # 🎯 POPUP DE RESULTADO
        popup = st.empty()

        with popup.container():

            emoji = emotion_map.get(sentimento_final, "🤔")

            st.markdown(f"""
                ## {emoji} Emoção detectada
                **Sentimento identificado pela IA:**  
                ### {sentimento_final}
            """)

            # 📊 Categorias
            st.markdown("### 📊 Principais categorias identificadas:")

            for label, score in categoria_feedback:
                score = float(score)
                st.write(f"• **{label}** — {score:.2f}")
                st.progress(score)

            # botão OK
            if st.button("OK"):
                popup.empty()
                st.success("Feedback cadastrado com sucesso!")