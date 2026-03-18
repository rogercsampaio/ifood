from PIL import Image


def validar_produto(categoria, foto, preco):

    erros = []

    if not categoria or categoria.strip() == "":
        erros.append("Categoria é obrigatória")

    if foto is None:
        erros.append("Foto do produto é obrigatória")

    else:
        try:
            img = Image.open(foto)

            if img.format not in ["JPEG", "PNG"]:
                erros.append("A foto deve ser PNG ou JPEG")

        except:
            erros.append("Arquivo enviado não é uma imagem válida")

    if preco is None or preco <= 0:
        erros.append("Preço deve ser maior que zero")

    return erros