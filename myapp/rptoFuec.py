import pyodbc
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
import json
from django.db import connection


@csrf_exempt
@require_http_methods(["POST"])
def rptoFuec(request):
    # Conexión a la base de datos
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

            # Llamado al procedimiento con 2 parametros
            cursor.execute("{CALL RP_FS_BUS (?, ?)}", (bus, fecha))

            # Obtener los resultados
            results = cursor.fetchall()
            print(results)

            # Construir una lista de diccionarios a partir de las filas
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

            # Devolver los resultados como JsonResponse
            return JsonResponse({'results': rows_list})
        else:
            print("error")
    except pyodbc.Error as ex:
        print("Error:", ex)


def rptoFuecPDF():
    # Conexión a la base de datos
    server = '172.16.0.25'
    database = 'Dynamix'
    username = 'Developer'
    password = '123456'

    try:
        # if request.method == "POST":  # Verificar el método de la solicitud
        conn = pyodbc.connect(
            'DRIVER={SQL Server};SERVER='+server + ';DATABASE='+database+';UID='+username+';PWD='+password)

        # data = json.loads(request.body)
        Nviaje = 621975
        # Nviaje = data.get('nviaje')
        Motivo = 'TRANSPORTE DE PARTICULARES (GRUPO - PERSONA NATURAL)'
        Cliente = 860015624
        op = 1

        cursor = conn.cursor()

        # Llamado al procedimiento con 2 parametros
        cursor.execute("{CALL RP_Formato_ServicioEspecial (?, ?, ?, ?)}",
                       (Nviaje, Motivo, Cliente, op))
        # cursor.execute("{CALL RP_FS_BUS (?, ?)}", (bus, fecha))
        print("paso")
        # Obtener los resultados
        results = cursor.fetchall()
        print("paso")
        print(results)
        print("paso")

        # Construir una lista de diccionarios a partir de las filas
        # rows_list = []
        # for row in results:
        #     rows_list.append({
        #         'viaje': row[0],
        #         'fecha': row[1].strftime('%Y-%m-%d %H:%M:%S'),
        #         'origen': row[2],
        #         'destino': row[3]
        #     })

        cursor.close()
        conn.close()

        # Devolver los resultados como JsonResponse
        return JsonResponse({'results': "rows_list"})
        # else:
        #     print("error")

    except pyodbc.Error as ex:
        print("Error:", ex)


def rptoFuecPDF():
    # Conexión a la base de datos
    server = '172.16.0.25'
    database = 'Dynamix'
    username = 'Developer'
    password = '123456'

    try:
        conn = pyodbc.connect(
            'DRIVER={SQL Server};SERVER='+server + ';DATABASE='+database+';UID='+username+';PWD='+password)

        # data = json.loads(request.body)
        Nviaje = 621975
        # Nviaje = data.get('nviaje')
        Motivo = 'TRANSPORTE DE PARTICULARES (GRUPO - PERSONA NATURAL)'
        Cliente = 860015624
        op = 1

        cursor = conn.cursor()

        # Llamado al procedimiento con 2 parametros
        cursor.execute("{CALL RP_Formato_ServicioEspecial (?, ?, ?, ?)}",
                       (Nviaje, Motivo, Cliente, op))
        # cursor.execute("{CALL RP_FS_BUS (?, ?)}", (bus, fecha))
        print("paso")
        # Obtener los resultados
        results = cursor.fetchall()
        print("paso")
        print(results)
        print("paso")

        cursor.close()
        conn.close()

        # Devolver los resultados como JsonResponse
        return JsonResponse({'results': "rows_list"})
        # else:
        #     print("error")

    except pyodbc.Error as ex:
        print("Error:", ex)


def llamar_procedimiento():
    # Conexión a la base de datos
    server = '172.16.0.25'
    database = 'Dynamix'
    username = 'Developer'
    password = '123456'
    # Configura tu conexión a la base de datos SQL Server
    conn = pyodbc.connect('DRIVER={SQL Server};SERVER='+server +
                          ';DATABASE='+database+';UID='+username+';PWD='+password)
    # Crea un cursor para ejecutar comandos SQL
    parametros = {'Nviaje': 544928,
                  'Motivo': 'TRANSPORTE DE PARTICULARES (GRUPO - PERSONA NATURAL)', 'Cliente': 860015624, 'op': 1}
    cursor = connection.cursor()
    cursor.callproc('RP_Formato_ServicioEspecial', parametros)

    # Obtener los resultados
    resultados = cursor.fetchall()

    # Trabajar con los resultados aquí
    for resultado in resultados:
        # Procesar cada fila de resultado
        print(resultado)

    # Cerrar el cursor
    cursor.close()


# Llama a la función con los valores deseados
llamar_procedimiento()
