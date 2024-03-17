from PIL import Image, ImageFilter
import cv2


def cortar_imagem(imagem, tamanho_corte_x, tamanho_corte_y):
    largura, altura = imagem.size
    cortes = []
    for y in range(0, altura, tamanho_corte_y):
        for x in range(0, largura, tamanho_corte_x):
            cortes.append(imagem.crop((x, y, x + tamanho_corte_x, y + tamanho_corte_y)))
    return cortes

# Carregar a imagem
imagem = Image.open("data/small/Bacteroides.fragilis/Bacteroides.fragilis_0001.jpg")
# imagem = Image.open("data/small/Lactobacillus.salivarius/Lactobacillus.salivarius_0001.jpg")

# # Cortar a imagem em várias partes
imagem_cinza = imagem.convert('L')

imagem_blur = imagem_cinza.filter(ImageFilter.GaussianBlur(radius=2))

# # Aplicar o algoritmo Canny para detecção de bordas
imagem_binaria = imagem_blur.point(lambda p: p > 190 and 255)
imagem_bordas = imagem_binaria.filter(ImageFilter.FIND_EDGES)
# # imagem_bordas.save("imagem_bordas.jpg")
# import cv2

# # Carregar a imagem
# imagem = cv2.imread("data/small/Bacteroides.fragilis/Bacteroides.fragilis_0001.jpg", cv2.IMREAD_GRAYSCALE)

# # # Aplicar filtro de blur
# imagem_blur = cv2.GaussianBlur(imagem, (5, 5), 0)

# # # Aplicar o algoritmo Canny para detecção de bordas
# imagem_bordas = cv2.Canny(imagem_blur, 30, 150, 3)

# # cv2.imshow("Imagem Original", imagem)
# # cv2.imshow("Imagem com Blur", imagem_blur)
# cv2.imshow("Detecção de Bordas (Canny)", imagem_bordas)

# # # Esperar até que uma tecla seja pressionada
# cv2.waitKey(0)
# cv2.destroyAllWindows()


# # imagem_limiarizada = imagem_cinza.point(lambda x: 255 if x > 200 else x//2)

# # Exibir a imagem original e a imagem após aplicar os filtros
# imagem.show()
# imagem_cinza.show()
# imagem_limiarizada.show()
# # Mostrar os cortes (exemplo para os primeiros 9 cortes)
# cortes = cortar_imagem(imagem_cinza, 256, 192)
# for i, corte in enumerate(cortes[:3]):
    # corte.show()


# import numpy as np

# # Lendo a imagem
# imagem = cv2.imread("data/small/Lactobacillus.salivarius/Lactobacillus.salivarius_0001.jpg")
# # imagem = Image.open("data/small/Bacteroides.fragilis/Bacteroides.fragilis_0001.jpg")
# # imagem = Image.open("data/small/Lactobacillus.salivarius/Lactobacillus.salivarius_0001.jpg")

# # Convertendo para tons de cinza
# imagem_cinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)

# # Definindo o limiar de binarização
# limiar = 127

# # Binarizando a imagem
# imagem_binaria = cv2.threshold(imagem_cinza, limiar, 255, cv2.THRESH_BINARY)[1]

# # Definindo parâmetros do Canny
# limiar1 = 100
# limiar2 = 200
# abertura = 3

# # Aplicando o detector de bordas Canny
# bordas_canny = cv2.Canny(imagem_binaria, limiar1, limiar2, apertureSize=abertura)

# # Exibindo as imagens
# cv2.imshow("Imagem Original", imagem)
# cv2.imshow("Imagem Binarizada", imagem_binaria)
# cv2.imshow("Bordas Canny", bordas_canny)

# cv2.waitKey(0)
# cv2.destroyAllWindows()