from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from datetime import datetime
from decimal import Decimal
import pyodbc
import json


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

            conn = pyodbc.connect(
                'DRIVER={SQL Server};SERVER=172.16.0.25;DATABASE=Dynamix;UID=Developer;PWD=123456')

            cursor = conn.cursor()
            cursor.execute(
                "{CALL RP_Formato_ServicioEspecial (?, ?, ?, ?)}", (Nviaje, Motivo, Cliente, op))

            cursor.execute("SELECT [Viaje], [FechaPartida], [Bus], [Placa], [Descripcion_Clase], [Descripcion_Marca], [Modelo], [Origen], [Destino], [Empresa_Registrado], [Nit_Emp], [dir_Emp], [tel_emp], [tel_emp1], [ema_emp], [Ciudad_Empresa], [Num_Tarjeta_Operacion], [Nombre_Conductor1], [Apellido_Conductor1], [Cedula_Conductor1], [Pase1_Conductor1], [fechavencimiento1_Conductor1], [Nombre_Conductor2], [Apellido_Conductor2], [Cedula_Conductor2], [Pase1_Conductor2], [fechavencimiento1_Conductor2], [NIT_Cliente], [Nombre_Cliente], [Direccion_Cliente], [Ciudad_Cliente], [Telefono_Cliente], [Objeto_Contrato], [Rep_cedula], [Rep_Apellidos], [Rep_Nombres], [Rep_Telefono], [Consecutivo_FUEC], [Modificar], [Talonario], [Usuario], [Fechasistema] FROM [DynamiX].[dbo].[FUEC_Transaccion] WHERE Viaje = ?", Nviaje)
            row = cursor.fetchone()
            columns = [column[0] for column in cursor.description]
            converted_row = convert_to_dict(row, columns)

            # Conversion a diccionario
            results = dict(zip(columns, converted_row))
            print(results)
            conn.commit()
            conn.close()

            return JsonResponse({'data': results})
        else:
            print("error")
    except pyodbc.Error as ex:
        print("Error:", ex)
