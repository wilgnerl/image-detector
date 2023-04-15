import cv2


def calcula_relacao_eixo_a_e_b(ellipse):
    a, b = ellipse[1][0]/2, ellipse[1][1]/2
    teste_a_b = a/b

    return teste_a_b


def calcula_diametro(comprimento_px, largura_real_cm, comprimento_obj):

    # mede o comprimento da imagem em pixels
    comprimento_px = comprimento_px

    # calcula a relação de pixels por centímetro (ppc)
    ppc = comprimento_px / largura_real_cm

    # mede o comprimento de um objeto na imagem em pixels
    comprimento_objeto_px = comprimento_obj

    # converte o comprimento em pixels para centímetros
    comprimento_objeto_cm = comprimento_objeto_px / ppc

    raio = comprimento_objeto_cm/10

    return raio


def fun_diametro(img):
    contagem_pixels = []

    # Percorre cada linha da imagem
    for y in range(img.shape[0]):
        # Conta o número de pixels 255 na linha atual
        contagem = cv2.countNonZero(img[y])
        # Adiciona o número de pixels contados à lista
        contagem_pixels.append(contagem)
    # Encontra a linha com o maior número de pixels 255
    linha_mais_pixels = max(contagem_pixels)
    return linha_mais_pixels
