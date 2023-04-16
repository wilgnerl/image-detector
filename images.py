import cv2
import os 
import numpy as np
import pandas as pd
from funcoes_aux import *

# ------------------- Listas das imagens --------------------
lista_nok_borda = os.listdir("./assets/NOK_borda/")
lista_nok_superficie = os.listdir("./assets/NOK_superficie/")
lista_nok_tamanho_forma = os.listdir("./assets/NOK_tamanho_forma/")
lista_ok = os.listdir("./assets/OK/")

lista_nok_borda = [f"./assets/NOK_borda/{filename}" for filename in lista_nok_borda]
lista_nok_superficie = [f"./assets/NOK_superficie/{filename}" for filename in lista_nok_superficie]
lista_nok_tamanho_forma = [f"./assets/NOK_tamanho_forma/{filename}" for filename in lista_nok_tamanho_forma]
lista_ok = [f"./assets/OK/{filename}" for filename in lista_ok]

lista_total = []
lista_total.extend(lista_nok_borda)
lista_total.extend(lista_nok_superficie)
lista_total.extend(lista_nok_tamanho_forma)
lista_total.extend(lista_ok)


df = pd.DataFrame(
    columns=["FILENAME", "TESTE - BORDA", "TESTE - SUPERFICIE", "DIAMETRO", "STATUS - DIAMETRO", "A/B", "STATUS - A/B"]
)

# --------------------- Analysis loop ------------------------
for path in lista_total:
    TESTE_BORDA = "-"
    TESTE_SUPERFICIE = "-"
    DIAMETRO = "-"
    AB = "-"
    STATUS_DIAMETRO = "-"
    STATUS_AB = "-"
    FILENAME = path
    
    fig_borda = cv2.imread(path)

    # ------------- Main image filtering ------------------
    blur = img_filtering(fig_borda)

    # ------- Logic to get the frame for analysis ---------
    contours, _ = cv2.findContours(
        blur, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    if len(contours) > 0:
        cnt = max(contours, key=cv2.contourArea)

        cv2.drawContours(fig_borda, [cnt], -1, (0, 255, 0), 2)

    frame_width = fig_borda.shape[0]
    frame_height = fig_borda.shape[1]

    # Coordenates to get the frame for analysis
    transition_x = int(frame_width / 2)
    transition_y = int(frame_height / 2) + 80
    transition_px = blur[transition_y, transition_x]


    # -------------- Criterios para o teste de borda --------------
    contours, _ = cv2.findContours(blur, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    cnt = max(contours, key=cv2.contourArea)
    ellipse = cv2.fitEllipse(cnt)

    _, radius = cv2.minEnclosingCircle(cnt)

    area_contour = cv2.contourArea(cnt)
    area_ellipse = np.pi * ellipse[1][0] * ellipse[1][1] / 4.0
    diff = area_ellipse - area_contour

    # ------------------- Teste de borda -------------------------
    if (diff > 20):
        TESTE_BORDA = "Reprovado"
        data = {
            "FILENAME": [FILENAME],
            "TESTE - BORDA": [TESTE_BORDA],
            "TESTE - SUPERFICIE": ["-"],
            "DIAMETRO": ["-"],
            "STATUS - DIAMETRO": ["-"],
            "A/B": ["-"],
            "STATUS - A/B": ["-"]

        }
        data = pd.DataFrame(data)
        df = pd.concat([df, data], ignore_index=True)
        # print(conta_imagem)
        continue
    else:
        TESTE_BORDA = "Aprovado"


    #----------- Criterios para o teste de superficie -------------
    index = crit_teste_superficie(fig_borda)


    #-------------------- Teste de superficie ---------------------
    if (index == 1):
        TESTE_SUPERFICIE = "Reprovado"
        data = {
            "FILENAME": [FILENAME],
            "TESTE - BORDA": [TESTE_BORDA],
            "TESTE - SUPERFICIE": [TESTE_SUPERFICIE],
            "DIAMETRO": ["-"],
            "STATUS - DIAMETRO": ["-"],
            "A/B": ["-"],
            "STATUS - A/B": ["-"]
        }
        data = pd.DataFrame(data)
        df = pd.concat([df, data], ignore_index=True)

        continue
    else:
        TESTE_SUPERFICIE = "Aprovado"


    #--------------- Criterios para o teste de diametro -------------
    linha_mais_pixels = fun_diametro(blur)
    diametro = calcula_diametro(508, 650, linha_mais_pixels)
    
    #---------------------- Teste de diametro -----------------------
    if (diametro > 49.5 and diametro < 50.5):
        STATUS_DIAMETRO = "Aprovado"
        DIAMETRO = round(diametro, 2)
    else:
        STATUS_DIAMETRO = "Reprovado"
        DIAMETRO = round(diametro, 2)

    #----------- Criterios para o teste de circularidade ------------
    ab = calcula_relacao_eixo_a_e_b(ellipse)
    #------------------ Teste de circularidade ----------------------
    if (ab > 0.95 and ab < 1.05):
        AB = round(ab, 2)
        STATUS_AB = "Aprovado"
    else:
        AB = round(ab, 2)
        STATUS_AB = "Reprovado"

    data = {
        "FILENAME": [FILENAME],
        "TESTE - BORDA": [TESTE_BORDA],
        "TESTE - SUPERFICIE": [TESTE_SUPERFICIE],
        "DIAMETRO": [DIAMETRO],
        "STATUS - DIAMETRO": [STATUS_DIAMETRO],
        "A/B": [AB],
        "STATUS - A/B": [STATUS_AB],
    }
    data = pd.DataFrame(data)
    df = pd.concat([df, data], ignore_index=True)

# Saves the Data frame on a CSV file
df.to_csv('./image_result.csv') 
