import cv2
import numpy as np
from blob import detector
import pandas as pd
from keras.models import load_model
from funcoes_aux import *
import time


# --------------- Neural network setup ---------------
np.set_printoptions(suppress=True)

# Load the trained model
model = load_model("./keras_model.h5", compile=False)

# Load the labels
class_names = open("./labels.txt", "r").readlines()



# ------- Data frame and video capture setup ----------
df = pd.DataFrame(
    columns=["FILENAME", "TESTE - BORDA", "TESTE - SUPERFICIE",
             "DIAMETRO", "STATUS - DIAMETRO", "A/B", "STATUS - A/B"]
)

cap = cv2.VideoCapture('./assets/Video2_Vedacao.mp4')

num_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

frame_atual = 1

flag_image = False
conta_imagem = 0

contador_de_frames = 0
autoriza_contagem_de_frames = False

TESTE_BORDA = "-"
TESTE_SUPERFICIE = "-"
STATUS_DIAMETRO = "-"
STATUS_AB = "-"
DIAMETRO = "-"
AB = "-"
FILENAME = ""


# ----------------------------- Video analysis loop -----------------------------------
while (frame_atual < num_frames-1):
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_atual)

    ret, frame = cap.read()

    if not ret:
        break

    fig_borda = frame


    # ------------- Main image filtering ------------------
    hsv = cv2.cvtColor(fig_borda, cv2.COLOR_BGR2HSV)
    # Split the HSV channels of the image
    h, s, v = cv2.split(hsv)
    # Defines the channels threshholds
    hsv_min = np.array([120, 0, 0])
    hsv_max = np.array([255, 150, 95])
    # Mask to extract information of the contour
    mask = cv2.inRange(fig_borda, hsv_min, hsv_max)
    result = cv2.bitwise_and(fig_borda, fig_borda, mask=~mask)
    gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
    # Get the white object on black background (only caries the information of contour)
    _, fig_gray = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)
    blur = cv2.medianBlur(fig_gray, 5)

    # ------- Logic to get the frame for analysis ---------
    contours, _ = cv2.findContours(
        blur, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    if len(contours) > 0:
        cnt = max(contours, key=cv2.contourArea)

        cv2.drawContours(frame, [cnt], -1, (0, 255, 0), 2)

    frame_width = fig_borda.shape[0]
    frame_height = fig_borda.shape[1]

    # Coordenates to get the frame for analysis
    transition_x = int(frame_width / 2)
    transition_y = int(frame_height / 2) + 80
    transition_px = blur[transition_y, transition_x]

    # Condition for updating the frame to be analysed
    if(autoriza_contagem_de_frames):
        contador_de_frames += 10
        if(contador_de_frames == 250):
            autoriza_contagem_de_frames = False
            contador_de_frames = 0

    # -------------------- Condition for analysing the frame --------------------
    if (transition_px == 255 and flag_image and not autoriza_contagem_de_frames):


        # -------------- Criterios para o teste de borda --------------
        flag_image = False
        conta_imagem += 1
        autoriza_contagem_de_frames = True
        print(conta_imagem)
        
        contours, _ = cv2.findContours(
            blur, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

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

        # Resize the raw image into (224-height,224-width) pixels
        image = cv2.resize(fig_borda, (224, 224),
                           interpolation=cv2.INTER_AREA)

        # Make the image a numpy array and reshape it to the models input shape.
        image = np.asarray(image, dtype=np.float32).reshape(1, 224, 224, 3)

        # Normalize the image array
        image = (image / 127.5) - 1

        # Predicts the model
        prediction = model.predict(image)
        index = np.argmax(prediction)
        confidence_score = prediction[0][index]

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
        diametro = calcula_diametro(
            fig_borda.shape[0], 756, linha_mais_pixels)
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

    if (transition_px == 0 and not flag_image):
        flag_image = True

    circleColor = (0, 255, 0)  # Vermelho
    circleRadius = 10
    circleThickness = -1  # Preencher a bola
    cv2.circle(frame, (transition_x, transition_y), circleRadius,
               circleColor, circleThickness)

    cv2.imshow('Video', frame)
    key = cv2.waitKey(25)  # Espera 25ms antes de exibir o próximo quadro
    if key == ord('q'):  # Verifica se a tecla "q" foi pressionada
        break

    frame_atual = frame_atual + 10
cap.release()
cv2.destroyAllWindows()

print(df)
# Saves the Data frame on a CSV file
df.to_csv('./out.csv') 
