import cv2
from django.http import JsonResponse
import os
import face_recognition
import io
import numpy as np  # Agregamos la importación de numpy

def reconocimiento_facial(request):
    print("Origen de la solicitud:", request.headers.get('Origin'))
    if request.method == 'POST':
        # Recibe la foto en base64 desde el front
        image_data = request.FILES.get('imageData')

        current_directory = os.path.dirname(os.path.realpath(__file__))
        image_path = os.path.join(current_directory, 'jm.jpg')
        reference_image = cv2.imread(image_path, 0)  # Lee la imagen de referencia con OpenCV

        # Convertir la imagen a un formato utilizable por OpenCV
        nparr = np.frombuffer(image_data.read(), np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # Carga el clasificador frontal de Haar para la detección de caras
        face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

        for (x, y, w, h) in faces:
            roi_gray = gray[y:y+h, x:x+w]
            roi_gray_resized = cv2.resize(roi_gray, (100, 100))

            hist_ref = cv2.calcHist([reference_image], [0], None, [256], [0, 256])
            hist_roi = cv2.calcHist([roi_gray_resized], [0], None, [256], [0, 256])
            correlation = cv2.compareHist(hist_ref, hist_roi, cv2.HISTCMP_CORREL)

            if correlation > 0.9:
                recognized_user = "JMaluendas (OpenCV)"
                return JsonResponse({'message': f'Usuario reconocido: {recognized_user}'})

        # Método con face_recognition
        image_data.seek(0)  # Reiniciar el cursor de lectura del archivo
        current_image = face_recognition.load_image_file(io.BytesIO(image_data.read()))
        current_image = cv2.cvtColor(current_image, cv2.COLOR_BGR2RGB)  # Convertir a formato RGB

        current_encoding = face_recognition.face_encodings(current_image)

        if not current_encoding:
            return JsonResponse({'message': 'No se encontró ningún rostro en la imagen'}, status=400)

        # Convertir la imagen de referencia a formato RGB
        reference_image = cv2.cvtColor(reference_image, cv2.COLOR_BGR2RGB)
        reference_encoding = face_recognition.face_encodings(reference_image)[0]

        current_encoding = current_encoding[0]
        distance = face_recognition.face_distance([reference_encoding], current_encoding)[0]
        umbral = 0.6

        if distance < umbral:
            recognized_user = "JMaluendas"
            return JsonResponse({'message': f'Usuario reconocido: {recognized_user}'})

        return JsonResponse({'message': 'Usuario no reconocido'}, status=403)


    # # Carga una imagen de referencia del usuario (esto podría ser una base de datos de imágenes)
    # try:
    #     current_directory = os.path.dirname(os.path.realpath(__file__))
    #     image_path = os.path.join(current_directory, 'jm.jpg')
    #     print(image_data)
    #     reference_image = cv2.imread(image_path)
    #     if reference_image is None:
    #         return JsonResponse({'message': 'No se pudo cargar la imagen de referencia'}, status=500)
    # except Exception as e:
    #     return JsonResponse({'message': f'Error al cargar la imagen: {str(e)}'}, status=500)


    # reference_gray = cv2.cvtColor(reference_image, cv2.COLOR_BGR2GRAY)

    # # Captura una imagen (en este caso, ya se ha capturado en la parte del frontend)
    # # img = cv2.imread('ruta/a/imagen_capturada.jpg')  # Si la imagen se captura en el backend

    # # Se convierte la imagen capturada a escala de grises
    # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # ancho = 100
    # alto = 100
    # # Detecta caras en la imagen
    # faces = face_cascade.detectMultiScale(
    #     gray, scaleFactor=1.1, minNeighbors=5)

    # # Itera sobre las caras detectadas
    # for (x, y, w, h) in faces:
    #     # Region of Interest (ROI) para la cara
    #     roi_gray = gray[y:y+h, x:x+w]

    #     # Redimensiona la cara detectada a un tamaño estándar (si se requiere)
    #     roi_gray_resized = cv2.resize(
    #         roi_gray, (ancho, alto))  # Ajusta 'ancho' y 'alto'

    #     # Realiza la comparación con la imagen de referencia
    #     # Aquí podrías utilizar algún método de comparación, como el reconocimiento de patrones, si tienes un conjunto de datos de referencia

    #     # Por ejemplo, puedes comparar histogramas de las imágenes
    #     hist_ref = cv2.calcHist([reference_gray], [0], None, [256], [0, 256])
    #     hist_roi = cv2.calcHist([roi_gray_resized], [0], None, [256], [0, 256])
    #     correlation = cv2.compareHist(hist_ref, hist_roi, cv2.HISTCMP_CORREL)

    #     # Establece un umbral para la coincidencia
    #     umbral = 0.9  # Ajusta este valor según sea necesario

    #     # Si la correlación es alta (la cara coincide con la referencia)
    #     if correlation > umbral:
    #         # Reconocimiento exitoso
    #         print("Usuario reconocido")

    #     # Simulación de reconocimiento facial exitoso
    #     recognized_user = "JMaluendas"  # Cambia esto por el nombre del usuario reconocido

    #     # Devolver una respuesta JSON con el resultado del reconocimiento
    #     return JsonResponse({'message': f'Usuario reconocido: {recognized_user}'})
    # else:
    #     return JsonResponse({'message': 'Método no permitido'}, status=405)
