import io
import pandas as pd
import json
from django.http import JsonResponse, HttpResponse
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

            # Crear el archivo Excel en memoria
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                dataframe = pd.DataFrame(colaboradores)
                dataframe.to_excel(writer, index=False, sheet_name='Sheet1')

            output.seek(0)

            # Enviar el archivo Excel como una respuesta al frontend
            response = HttpResponse(output.getvalue(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename=colaboradores.xlsx'

            return response

        return JsonResponse({'error': 'No se recibieron datos de colaboradores en el cuerpo de la solicitud'})

    return JsonResponse({'error': 'Se esperaba una solicitud POST'})
