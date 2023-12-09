import pyodbc
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
import json
from django.db import connection


@csrf_exempt
@require_http_methods(["POST"])
def rptoFuec(request):
    server = '172.16.0.25'
    database = 'Dynamix'
    username = 'Developer'
    password = '123456'

    try:
        if request.method == "POST":  # Verificar el método de la solicitud
            conn = pyodbc.connect(
                'DRIVER={SQL Server};SERVER='+server + ';DATABASE='+database+';UID='+username+';PWD='+password)

            data = json.loads(request.body)
            fecha = data.get('fecha')
            print(fecha)
            bus = data.get('searchV')

            cursor = conn.cursor()

            cursor.execute("{CALL RP_FS_BUS (?, ?)}", (bus, fecha))

            results = cursor.fetchall()
            print(results)

            rows_list = []
            for row in results:
                rows_list.append({
                    'viaje': row[0],
                    'fecha': row[1].strftime('%Y-%m-%d %H:%M:%S'),
                    'origen': row[2],
                    'destino': row[3]
                })

            cursor.close()
            conn.close()

            return JsonResponse({'results': rows_list})
        else:
            print("error")
    except pyodbc.Error as ex:
        print("Error:", ex)
