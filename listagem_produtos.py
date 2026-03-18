import streamlit as st
import db


def tela_listagem_produtos():

    st.title("Produtos cadastrados")

    produtos = db.listar_produtos()

    if not produtos:
        st.info("Nenhum produto cadastrado.")
        return

    # grid com 3 colunas
    cols = st.columns(3)

    for i, produto in enumerate(produtos):

        with cols[i % 3]:

            st.image(produto["url_foto"], width=300)

            st.markdown(f"### {produto['nome']}")

            st.write(f"Categoria: {produto['categoria']}")

            st.write(f"💰 R$ {produto['preco']:.2f}")