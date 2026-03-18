from transformers import ViTImageProcessor, ViTForImageClassification
import modelo_reconhecimento_idiomas as traducoes
import torch
from PIL import Image
import streamlit as st

@st.cache_resource
def carregar_modelo():
    try:
        model_name = "google/vit-base-patch16-224"
        
        processor = ViTImageProcessor.from_pretrained(model_name)
        model = ViTForImageClassification.from_pretrained(model_name)
        
        print(f"Modelo carregado com sucesso: {model_name}")
        print(f"Total de categorias do modelo: {model.config.num_labels}")
        #print("Categorias disponíveis:", model.config.id2label)
    except Exception as e:
        print(f"Erro ao carregar o modelo: {e}")
        return None, None
    else:
        return processor, model
    
    

def processar_imagem(processor, image_path):
    image = Image.open(image_path)
    inputs = processor(images=image, return_tensors="pt")
    return inputs, image


def prever_nome_produto(model, inputs):
    with torch.no_grad():
        outputs = model(**inputs)
    
    logits = outputs.logits
    predicted_class_idx = logits.argmax(-1).item()
    predicted_label = model.config.id2label[predicted_class_idx]
    
    print("Índice da classe:", predicted_class_idx)
    print("Classe prevista:", predicted_label)
    
    return predicted_label

# Função principal para carregar o modelo, processar a imagem e prever a categoria
def pipeline_prever_nome_produto(image_path):
    processor, model = carregar_modelo()
    if processor is None or model is None:
        return
    
    inputs, image = processar_imagem(processor, image_path)
    nome_produto_previsto = prever_nome_produto(model, inputs)
    nome_produto_previsto_traduzido = traducoes.traduzir_texto(nome_produto_previsto)
    return nome_produto_previsto_traduzido


