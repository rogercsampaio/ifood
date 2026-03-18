'''
Dado um determinado feedback do produto, reconhece as principais categorias de reclamação, como qualidade, entrega, atendimento, etc. 
Isso ajuda a identificar áreas específicas de melhoria e a direcionar esforços para resolver os problemas mais comuns enfrentados pelos clientes.
Utilizaremos um modelo pré-treinado e zero-short. Modelo usado: MoritzLaurer/mDeBERTa-v3-base-mnli-xnli
'''
import streamlit as st
from transformers import pipeline

# Labels
LABELS = [
    "produto de baixa qualidade, estragado ou amassado",
    "produto fresco, bonito ou saboroso",
    "produto muito verde ou muito maduro",
    "entrega atrasada",
    "produto faltando no pedido",
    "pedido entregue errado",
    "preço alto",
    "bom custo benefício",
    "embalagem ruim ou danificada",
    "embalagem boa",
    "experiência positiva",
    "experiência negativa"
]

# 🔥 Carrega uma única vez
@st.cache_resource
def load_model():
    return pipeline(
        "zero-shot-classification",
        model="MoritzLaurer/mDeBERTa-v3-base-mnli-xnli"
    )

# 🔮 Inferência
def predict(text, top_k=3):
    classifier = load_model()
    
    result = classifier(
        text,
        candidate_labels=LABELS,
        multi_label=True
    )

    top_labels = sorted(
        zip(result["labels"], result["scores"]),
        key=lambda x: x[1],
        reverse=True
    )[:top_k]

    return top_labels