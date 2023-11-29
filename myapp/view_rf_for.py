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

        reference_images_list = ["100567890.jpg", "Marcela.jpg"]

        for image_name in reference_images_list:
            current_directory = os.path.dirname(os.path.realpath(__file__))
            image_path = os.path.join(current_directory, image_name)
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

                if correlation > 1:
                    recognized_user = recognized_user = os.path.splitext(image_name)[0]
                    return JsonResponse({'message': f'Usuario reconocido: {recognized_user}', 'user_id': recognized_user})

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
                recognized_user = os.path.splitext(image_name)[0]
                return JsonResponse({'message': f'Usuario reconocido: {recognized_user}', 'image_name': image_name})


        return JsonResponse({'message': 'Usuario no reconocido'}, status=403)