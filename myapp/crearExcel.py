import os
import pandas as pd
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

@csrf_exempt
@require_http_methods(["POST"])
def generar_excel(request):
    if request.method == 'POST':
        # Verificar si hay datos en la solicitud
        if request.body:
            # Decodificar los datos JSON de la solicitud
            colaboradores = json.loads(request.body)
            # Aquí puedes procesar los datos de colaboradores como desees

            # Ejemplo de creación de un archivo Excel de prueba con Pandas
            ruta_descargas = os.path.join(os.path.expanduser("~"), "Downloads")
            ruta_excel = os.path.join(ruta_descargas, "5apps", "excel", "prueba.xlsx")
            ventas = {"descripción": ["Producto1", "Producto2", "Producto3"], "venta": ["3456", "5646", "7656"],}

            # Crear el archivo Excel en la ruta especificada
            dataframe = pd.DataFrame(colaboradores)
            dataframe.to_excel(ruta_excel)

            return JsonResponse({'message': 'Archivo Excel generado correctamente'})

        return JsonResponse({'error': 'No se recibieron datos de colaboradores en el cuerpo de la solicitud'})

    return JsonResponse({'error': 'Se esperaba una solicitud POST'})
