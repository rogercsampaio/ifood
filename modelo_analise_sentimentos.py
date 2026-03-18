from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import streamlit as st


@st.cache_resource
def carregar_modelo():
    model_name = "tabularisai/multilingual-sentiment-analysis"

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name)

    model.eval()

    print("Modelo e tokenizador carregados")

    return tokenizer, model


def predict_sentiment(texts, threshold=0.5):

    tokenizer, model = carregar_modelo()

    if isinstance(texts, str):
        texts = [texts]

    inputs = tokenizer(
        texts,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=512
    )

    with torch.no_grad():
        outputs = model(**inputs)

    probabilities = torch.nn.functional.softmax(outputs.logits, dim=-1)

    sentiment_map = {
        0: "Muito Negativo",
        1: "Negativo",
        2: "Neutro",
        3: "Positivo",
        4: "Muito Positivo",
        5: "Incerto (Desconhecido)"
    }

    results = []

    for probs in probabilities:

        probs_list = probs.tolist()

        all_scores = {
            sentiment_map[i]: round(probs_list[i], 4)
            for i in range(5)
        }

        best_index = int(torch.argmax(probs))
        best_score = round(probs_list[best_index], 4)

        if best_score < threshold:
            final_label = sentiment_map[5]
        else:
            final_label = sentiment_map[best_index]

        results.append({
            "predicted_label": final_label,
            "confidence": best_score,
            "all_probabilities": all_scores
        })

    return results