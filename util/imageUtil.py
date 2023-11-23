from PIL import Image, ImageDraw


def transformar_em_circulo(imagem_original, tamanho_maximo=120):
    # Redimensiona a imagem original para um quadrado de 120x120 pixels
    tamanho_quadrado = tamanho_maximo
    imagem_redimensionada = imagem_original.resize(
        (tamanho_quadrado, tamanho_quadrado), Image.Resampling.LANCZOS
    )

    # Cria uma máscara circular
    mascara = Image.new("L", (tamanho_quadrado, tamanho_quadrado), 0)
    draw = ImageDraw.Draw(mascara)
    draw.ellipse((0, 0, tamanho_quadrado, tamanho_quadrado), fill=255)

    # Aplica a máscara na imagem redimensionada
    imagem_final = Image.new(
        "RGB", (tamanho_quadrado, tamanho_quadrado), (255, 255, 255)
    )
    imagem_final.paste(imagem_redimensionada, (0, 0), mask=mascara)

    return imagem_final
