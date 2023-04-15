# contours, _ = cv2.findContours(
#     blur, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

# cnt = max(contours, key=cv2.contourArea)
# ellipse = cv2.fitEllipse(cnt)

# _, radius = cv2.minEnclosingCircle(cnt)

# area_contour = cv2.contourArea(cnt)
# area_ellipse = np.pi * ellipse[1][0] * ellipse[1][1] / 4.0
# diff = area_ellipse - area_contour

# if (diff > 20):
#     TESTE_BORDA = "Reprovado"
#     data = {
#         "FILENAME": [FILENAME],
#         "TESTE - BORDA": [TESTE_BORDA],
#         "TESTE - SUPERFICIE": ["-"],
#         "DIAMETRO": ["-"],
#         "STATUS - DIAMETRO": ["-"],
#         "A/B": ["-"],
#         "STATUS - A/B": ["-"]

#     }
#     data = pd.DataFrame(data)
#     df = pd.concat([df, data], ignore_index=True)
#     flag_image = True
#     conta_imagem += 1
#     # print(conta_imagem)
#     continue
# else:
#     TESTE_BORDA = "Aprovado"

# # teste de superficie

# # Resize the raw image into (224-height,224-width) pixels
# image = cv2.resize(fig_borda, (224, 224),
#                    interpolation=cv2.INTER_AREA)

# # Make the image a numpy array and reshape it to the models input shape.
# image = np.asarray(image, dtype=np.float32).reshape(1, 224, 224, 3)

# # Normalize the image array
# image = (image / 127.5) - 1

# # Predicts the model
# prediction = model.predict(image)
# index = np.argmax(prediction)
# confidence_score = prediction[0][index]

# if (index == 1):
#     TESTE_SUPERFICIE = "Reprovado"
#     data = {
#         "FILENAME": [FILENAME],
#         "TESTE - BORDA": [TESTE_BORDA],
#         "TESTE - SUPERFICIE": [TESTE_SUPERFICIE],
#         "DIAMETRO": ["-"],
#         "STATUS - DIAMETRO": ["-"],
#         "A/B": ["-"],
#         "STATUS - A/B": ["-"]
#     }
#     data = pd.DataFrame(data)
#     df = pd.concat([df, data], ignore_index=True)
#     flag_image = True
#     conta_imagem += 1
#     # print(conta_imagem)
#     continue
# else:
#     TESTE_SUPERFICIE = "Aprovado"

# linha_mais_pixels = fun_diametro(blur)
# diametro = calcula_diametro(
#     fig_borda.shape[0], 756, linha_mais_pixels)

# if (diametro > 49.5 and diametro < 50.5):
#     STATUS_DIAMETRO = "Aprovado"
#     DIAMETRO = diametro
# else:
#     STATUS_DIAMETRO = "Reprovado"
#     DIAMETRO = diametro

# ab = calcula_relacao_eixo_a_e_b(ellipse)
# if (ab > 0.95 and ab < 1.05):
#     AB = ab
#     STATUS_AB = "Aprovado"
# else:
#     AB = ab
#     STATUS_AB = "Reprovado"

# data = {
#     "FILENAME": [FILENAME],
#     "TESTE - BORDA": [TESTE_BORDA],
#     "TESTE - SUPERFICIE": [TESTE_SUPERFICIE],
#     "DIAMETRO": [DIAMETRO],
#     "STATUS - DIAMETRO": [STATUS_DIAMETRO],
#     "A/B": [AB],
#     "STATUS - A/B": [STATUS_AB],
# }
# data = pd.DataFrame(data)
# df = pd.concat([df, data], ignore_index=True)
