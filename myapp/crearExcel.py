import io
import json
import pandas as pd
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods


@csrf_exempt
@require_http_methods(["POST"])
def generar_excel(request):
    if request.method == 'POST':
        # Verifica si hay datos en la solicitud
        if request.body:
            # Decodifica los datos JSON de la solicitud
            JsonData = json.loads(request.body)

            if isinstance(JsonData.get("results"), str):
                JsonData = json.loads(JsonData["results"])

            # Crea el archivo Excel en memoria
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                # Itera sobre cada conjunto de datos
                for idx, data in enumerate(JsonData, start=1):
                    # Verifica si los datos son una lista
                    if isinstance(data, list):
                        # Si es una lista, crea un DataFrame con la lista
                        dataframe = pd.DataFrame(data)
                    elif isinstance(data, dict):
                        # Si se un diccionario, crea un DataFrame solo si es la primera iteración
                        if idx == 1:
                            dataframe = pd.DataFrame(JsonData)
                        else:
                            # Si no es la primera iteración, sigue con la siguiente iteración
                            continue
                    else:
                        return JsonResponse({'error': 'Los datos deben ser una lista o un diccionario'})

                    # Escribe los datos en una hoja de cálculo
                    dataframe.to_excel(
                        writer, index=False, sheet_name=f'Sheet{idx}')

                    worksheet = writer.sheets[f'Sheet{idx}']

                    # Ajusta ancho de las columnas de acuerdo a contenido
                    for column in worksheet.columns:
                        max_length = 0
                        column = [cell for cell in column]
                        try:
                            max_length = max(len(str(cell.value))
                                             for cell in column)
                        except:
                            pass
                        adjusted_width = (max_length + 2)
                        worksheet.column_dimensions[column[0]
                                                    .column_letter].width = adjusted_width

            output.seek(0)

            response = HttpResponse(output.getvalue(),
                                    content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename=JsonData.xlsx'

            return response

        return JsonResponse({'error': 'No se recibieron datos de JsonData en el cuerpo de la solicitud'})
    return JsonResponse({'error': 'Se esperaba una solicitud POST'})
