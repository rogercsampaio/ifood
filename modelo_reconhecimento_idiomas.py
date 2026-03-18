from translate import Translator

translator = Translator(from_lang="en", to_lang="pt")

def traduzir_texto(texto: str) -> str:
    try:
        texto_traduzido = translator.translate(texto)
        return texto_traduzido
    except Exception as e:
        print(f"Erro ao traduzir: {e}")
        return texto