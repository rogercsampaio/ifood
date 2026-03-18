from listagem_feedbacks import tela_listagem_feedbacks
import streamlit as st

from produto import tela_produto
from listagem_produtos import tela_listagem_produtos
from pedido import tela_pedido
from feedback import tela_feedback
from analytics import tela_analytics_dashboard
from rag import tela_rag



st.set_page_config(page_title="Sistema Loja", layout="wide")

st.title("Sistema de Gestão")

abas = st.tabs([
    "Cadastrar Produto",
    "Lista de Produtos",
    "Feedback",
    "Listagem Feedbacks",
    "Analytics",
    "RAG"
])


with abas[0]:
    tela_produto()

with abas[1]:
    tela_listagem_produtos()

with abas[2]:
    tela_feedback()

with abas[3]:
    tela_listagem_feedbacks()

with abas[4]:
    tela_analytics_dashboard()
 
with abas[5]:
    tela_rag()
  

    