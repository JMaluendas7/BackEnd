from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from datetime import datetime
from decimal import Decimal
import pyodbc
import json
# import django.db import Database


@csrf_exempt
@require_http_methods(["POST"])
def rptoFuec(request):
    # server = 'd1.berlinasdelfonce.com'
    # database = 'Dynamix'
    # username = 'Developer'
    # password = '123456'

    try:
        if request.method == "POST":

            server = 'd1.berlinasdelfonce.com'
            database = 'Dynamix'
            username = 'Developer'
            password = '123456'

            conn = pyodbc.connect(
                'DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+password)

            # conne =

            data = json.loads(request.body)
            fecha = data.get('fecha')

            # Verificar si la fecha está presente y reconocible, si no, usar la fecha del equipo
            if fecha:
                try:
                    fecha = datetime.strptime(fecha, '%Y-%m-%d %H:%M:%S')
                except ValueError:
                    print(fecha)
            else:
                fecha = datetime.now()

            print(fecha)
            bus = data.get('searchV')

            cursor = conn.cursor()
            print(bus)

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


def decimal_default(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError


def convert_to_dict(row, columns):
    converted_row = []
    for value, column in zip(row, columns):
        if isinstance(value, datetime):
            value = value.strftime("%Y-%m-%d %H:%M:%S")
        converted_row.append(value)
    return converted_row


@csrf_exempt
@require_http_methods(["POST"])
def rptoFuecPDF2(request):
    try:
        if request.method == "POST":
            data = request.body
            Nviaje = json.loads(data).get('viaje')
            Motivo = 'TRANSPORTE DE PARTICULARES (GRUPO - PERSONA NATURAL)'
            Cliente = 860015624
            op = 1
            server = 'd1.berlinasdelfonce.com'
            database = 'Dynamix'
            username = 'Developer'
            password = '123456'
            conn = pyodbc.connect(
                'DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+password)

            cursor = conn.cursor()
            cursor.execute(
                "{CALL RP_Formato_ServicioEspecial (?, ?, ?, ?)}", (Nviaje, Motivo, Cliente, op))

            cursor.execute("SELECT [Viaje], [FechaPartida], [Bus], [Placa], [Descripcion_Clase], [Descripcion_Marca], [Modelo], [Origen], [Destino], [Empresa_Registrado], [Nit_Emp], [dir_Emp], [tel_emp], [tel_emp1], [ema_emp], [Ciudad_Empresa], [Num_Tarjeta_Operacion], [Nombre_Conductor1], [Apellido_Conductor1], [Cedula_Conductor1], [Pase1_Conductor1], [fechavencimiento1_Conductor1], [Nombre_Conductor2], [Apellido_Conductor2], [Cedula_Conductor2], [Pase1_Conductor2], [fechavencimiento1_Conductor2], [NIT_Cliente], [Nombre_Cliente], [Direccion_Cliente], [Ciudad_Cliente], [Telefono_Cliente], [Objeto_Contrato], [Rep_cedula], [Rep_Apellidos], [Rep_Nombres], [Rep_Telefono], [Consecutivo_FUEC], [Modificar], [Talonario], [Usuario], [Fechasistema] FROM [DynamiX].[dbo].[FUEC_Transaccion] WHERE Viaje = ?", Nviaje)
            row = cursor.fetchone()
            columns = [column[0] for column in cursor.description]
            converted_row = convert_to_dict(row, columns)

            # Conversion a diccionario
            resultss = dict(zip(columns, converted_row))
            results = {key: value.rstrip() if isinstance(
                value, str) else value for key, value in resultss.items()}

            conn.commit()
            conn.close()

            return JsonResponse({'data': results})
        else:
            print("error")
    except pyodbc.Error as ex:
        print("Error:", ex)
