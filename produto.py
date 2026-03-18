from modelo_reconhecimento_imgs import pipeline_prever_nome_produto
from validacoes import validar_produto
import streamlit as st
from db import criar_produto
import os


def tela_produto():

    st.title("Cadastro de Produto")

    categoria = st.selectbox(
        "Categoria",
        ["frutas", "vegetais"]
    )

    foto = st.file_uploader(
        "Foto do produto",
        type=["png", "jpg", "jpeg"]
    )

    nome_produto = ""

    # 🔹 Assim que a foto é enviada o modelo roda
    if foto is not None:

        os.makedirs("imagens", exist_ok=True)
        caminho = f"imagens/{foto.name}"

        with open(caminho, "wb") as f:
            f.write(foto.getbuffer())

        # 🔹 Loading enquanto o modelo roda
        with st.spinner("🔎 IDENTIFICANDO O PRODUTO COM INTELIGÊNCIA ARTIFICIAL, AGUARDE..."):
            nome_produto = pipeline_prever_nome_produto(caminho)

    with st.form("form_produto"):

        nome = st.text_input(
            "Nome do produto",
            value=nome_produto
        )

        preco = st.number_input(
            "Preço",
            min_value=0.0,
            step=0.01
        )

        submitted = st.form_submit_button("Cadastrar produto")

        if submitted:

            erros = validar_produto(categoria, foto, preco)

            if erros:
                for erro in erros:
                    st.error(erro)

            else:

                criar_produto(nome, categoria, caminho, preco)
                st.success("Produto cadastrado com sucesso!")