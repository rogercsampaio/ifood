import streamlit as st
from db import listar_feedbacks_com_produto, listar_produtos
from sentence_transformers import SentenceTransformer, util
import torch

# --- Mapas para emojis de sentimento ---
SENTIMENT_EMOJI = {
    "Muito Negativo": "👎",
    "Negativo": "😞",
    "Neutro": "😐",
    "Positivo": "🙂",
    "Muito Positivo": "👍",
    "": "❓"
}

# --- carregar modelo embeddings (cache) ---
@st.cache_resource
def carregar_modelo_embeddings():
    model = SentenceTransformer('all-MiniLM-L6-v2')
    return model

# --- gerar embeddings para todos os feedbacks ---
def gerar_embeddings(feedbacks, model):
    if not feedbacks:
        return [], []
    descricoes = [fb["descricao"] for fb in feedbacks]
    embeddings = model.encode(descricoes, convert_to_tensor=True)
    return embeddings, descricoes

# --- função RAG simples ---
def recuperar_feedbacks_pergunta(pergunta, embeddings, descricoes, feedbacks, model, top_k=3):
    if len(embeddings) == 0:
        return []
    pergunta_emb = model.encode(pergunta, convert_to_tensor=True)
    cos_scores = util.cos_sim(pergunta_emb, embeddings)[0]
    top_results = torch.topk(cos_scores, k=min(top_k, len(cos_scores)))

    resultados = []
    for idx, score in zip(top_results.indices, top_results.values):
        fb = feedbacks[idx]
        resultados.append({
            "produto": fb["produto"] if "produto" in fb else "",
            "nome_cliente": fb["nome_cliente"] if "nome_cliente" in fb else "",
            "descricao": fb["descricao"] if "descricao" in fb else "",
            "sentimento": fb["sentimento_final"] if "sentimento_final" in fb else "",
            "similaridade": round(score.item(), 3)
        })
    return resultados

# --- Função principal para a aba RAG ---
def tela_rag():
    st.title("🤖 RAG - Recuperação Inteligente de Feedbacks")

    # carregar modelo
    model = carregar_modelo_embeddings()

    # carregar feedbacks e produtos do banco e converter em dict
    feedbacks = [dict(fb) for fb in listar_feedbacks_com_produto()]
    produtos = [dict(p) for p in listar_produtos()]

    st.write(f"Total de feedbacks encontrados: {len(feedbacks)}")

    # botão para gerar embeddings
    if st.button("Gerar Embeddings"):
        embeddings, descricoes = gerar_embeddings(feedbacks, model)
        st.session_state['embeddings'] = embeddings
        st.session_state['descricoes'] = descricoes
        st.success("✅ Embeddings gerados com sucesso!")

    # input da pergunta
    pergunta = st.text_input("Digite sua pergunta sobre os feedbacks:")

    # botão para buscar
    if st.button("Buscar Feedbacks Relevantes"):
        if 'embeddings' not in st.session_state:
            st.warning("Primeiro clique em 'Gerar Embeddings'!")
        elif not pergunta.strip():
            st.warning("Digite uma pergunta.")
        else:
            resultados = recuperar_feedbacks_pergunta(
                pergunta,
                st.session_state['embeddings'],
                st.session_state['descricoes'],
                feedbacks,
                model,
                top_k=3
            )
            if resultados:
                st.markdown("### 💡 Feedbacks mais relevantes:")
                for r in resultados:
                    with st.container():
                        cols = st.columns([1, 4])
                        # imagem do produto
                        with cols[0]:
                            url_img = None
                            for p in produtos:
                                if p.get("nome") == r["produto"]:
                                    url_img = p.get("url_foto", None)
                                    break
                            if url_img:
                                st.image(url_img, width=80)
                            else:
                                st.text("Sem imagem")
                        # informações
                        with cols[1]:
                            emoji = SENTIMENT_EMOJI.get(r["sentimento"], "❓")
                            st.markdown(f"**Produto:** {r['produto']}")
                            st.markdown(f"**Cliente:** {r['nome_cliente']}")
                            st.markdown(f"**Sentimento:** {r['sentimento']} {emoji}")
                            st.markdown(f"**Similaridade:** {r['similaridade']}")
                            st.markdown(f"**Descrição:** {r['descricao']}")
                    st.markdown("---")
            else:
                st.info("Nenhum feedback relevante encontrado.")