import cv2
import numpy as np
import pandas as pd
from keras.models import load_model


# --------------- Neural network setup ---------------
np.set_printoptions(suppress=True)

# Load the trained model
model = load_model("./keras_model.h5", compile=False)


# ---------------- Funcoes Auxiliares ----------------
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


def img_filtering(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # Split the HSV channels of the image
    h, s, v = cv2.split(hsv)
    # Defines the channels threshholds
    hsv_min = np.array([120, 0, 0])
    hsv_max = np.array([255, 150, 95])
    # Mask to extract information of the contour
    mask = cv2.inRange(img, hsv_min, hsv_max)
    result = cv2.bitwise_and(img, img, mask=~mask)
    gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
    # Get the white object on black background (only caries the information of contour)
    _, fig_gray = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)
    blur = cv2.medianBlur(fig_gray, 5)
    return blur





def crit_teste_superficie(img):
    # Resize the raw image into (224-height,224-width) pixels
    image = cv2.resize(img, (224, 224),
                        interpolation=cv2.INTER_AREA)

    # Make the image a numpy array and reshape it to the models input shape.
    image = np.asarray(image, dtype=np.float32).reshape(1, 224, 224, 3)

    # Normalize the image array
    image = (image / 127.5) - 1

    # Predicts the model
    prediction = model.predict(image)
    index = np.argmax(prediction)
    return index


