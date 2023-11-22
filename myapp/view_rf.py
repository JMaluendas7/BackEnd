# En tu archivo views.py

import cv2
from django.http import JsonResponse
from base64 import b64decode
import numpy as np


def reconocimiento_facial(request):
    if request.method == 'POST':
        # Recibe la foto en base64 desde el front
        data_url = request.POST.get('imageData')

        # Decodifica la imagen en base64
        header, encoded = data_url.split(",", 1)
        data = b64decode(encoded)
        np_data = np.frombuffer(data, dtype=np.uint8)

        # Convierte a imagen OpenCV
        img = cv2.imdecode(np_data, cv2.IMREAD_COLOR)

    # Carga el clasificador frontal de Haar para la detección de caras
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Carga una imagen de referencia del usuario (esto podría ser una base de datos de imágenes)
    reference_image = cv2.imread('ruta/a/imagen_de_referencia.jpg')
    reference_gray = cv2.cvtColor(reference_image, cv2.COLOR_BGR2GRAY)

    # Captura una imagen (en este caso, ya se ha capturado en la parte del frontend)
    # img = cv2.imread('ruta/a/imagen_capturada.jpg')  # Si la imagen se captura en el backend

    # Se convierte la imagen capturada a escala de grises
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Detecta caras en la imagen
    faces = face_cascade.detectMultiScale(
        gray, scaleFactor=1.1, minNeighbors=5)

    # Itera sobre las caras detectadas
    for (x, y, w, h) in faces:
        # Region of Interest (ROI) para la cara
        roi_gray = gray[y:y+h, x:x+w]

        # Redimensiona la cara detectada a un tamaño estándar (si se requiere)
        roi_gray_resized = cv2.resize(
            roi_gray, (ancho, alto))  # Ajusta 'ancho' y 'alto'

        # Realiza la comparación con la imagen de referencia
        # Aquí podrías utilizar algún método de comparación, como el reconocimiento de patrones, si tienes un conjunto de datos de referencia

        # Por ejemplo, puedes comparar histogramas de las imágenes
        hist_ref = cv2.calcHist([reference_gray], [0], None, [256], [0, 256])
        hist_roi = cv2.calcHist([roi_gray_resized], [0], None, [256], [0, 256])
        correlation = cv2.compareHist(hist_ref, hist_roi, cv2.HISTCMP_CORREL)

        # Establece un umbral para la coincidencia
        umbral = 0.9  # Ajusta este valor según sea necesario

        # Si la correlación es alta (la cara coincide con la referencia)
        if correlation > umbral:
            # Reconocimiento exitoso
            print("Usuario reconocido")

        # Simulación de reconocimiento facial exitoso
        recognized_user = "JMaluendas"  # Cambia esto por el nombre del usuario reconocido

        # Devolver una respuesta JSON con el resultado del reconocimiento
        return JsonResponse({'message': f'Usuario reconocido: {recognized_user}'})
    else:
        return JsonResponse({'message': 'Método no permitido'}, status=405)
