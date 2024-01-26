from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from openpyxl.styles import Alignment, Font
from openpyxl import load_workbook
from datetime import datetime
from decimal import Decimal
import pyodbc
import json
import pytz
import os
import io


@csrf_exempt
@require_http_methods(["POST"])
def RptoMicroSeguros(request):
    try:
        if request.method == "POST":

            # server = 'd1.berlinasdelfonce.com'
            server = '172.16.0.25'
            database = 'Dynamix'
            username = 'Developer'
            password = '123456'

            conn = pyodbc.connect(
                'DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+password)
            cursor = conn.cursor()

            Desde = request.POST.get('startDate', None)
            Hasta = request.POST.get('endDate', None)
            Tipo = 1

            print(Desde, Hasta)

            cursor.execute(
                "{CALL Fics_MicroSegurosGET (?, ?, ?)}", (Desde, Hasta, Tipo))

            columns = [column[0] for column in cursor.description]
            results = cursor.fetchall()

            rows_list = []
            for row in results:
                row_dict = {}
                for index, value in enumerate(row):
                    column_name = columns[index]
                    if isinstance(value, datetime):
                        value = value.strftime("%Y-%m-%d %H:%M:%S")
                    elif isinstance(value, str):
                        value = value.rstrip()  # Eliminar espacios al final de la cadena
                    elif isinstance(value, Decimal):  # Verificar si el valor es Decimal
                        value = float(value)  # Convertir Decimal a float
                        value = round(value)  # Redondear si es necesario
                    row_dict[column_name] = value
                rows_list.append(row_dict)

            print(rows_list)

            cursor.close()
            conn.close()

            return JsonResponse({'results': rows_list})
        else:
            print("error")
    except pyodbc.Error as ex:
        print("Error:", ex)


@csrf_exempt
@require_http_methods(["POST"])
def RptoTiquetesMicroSeguros(request):
    try:
        if request.method == "POST":

            server = 'd1.berlinasdelfonce.com'
            # server = '172.16.0.25'
            database = 'Dynamix'
            username = 'Developer'
            password = '123456'

            conn = pyodbc.connect(
                'DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+password)
            cursor = conn.cursor()

            EmpiD = request.POST.get('empresa', None)
            fechaInicio = request.POST.get('startDate', None)
            fechaFinal = request.POST.get('endDate', None)
            Opcion = request.POST.get('Opcion', None)
            SubOpcion = request.POST.get('SubOpcion', None)
            Cadena01 = "VACIO"
            Cadena02 = "VACIO"
            valor01 = 100

            cursor.execute(
                "{CALL RP_Consultas04 (?, ?, ?, ?, ?, ?, ?, ?)}", (EmpiD, fechaInicio, fechaFinal, Opcion, SubOpcion, Cadena01, Cadena02, valor01))

            columns = [column[0] for column in cursor.description]
            results = cursor.fetchall()

            rows_list = []
            for row in results:
                row_dict = {}
                for index, value in enumerate(row):
                    column_name = columns[index]
                    if isinstance(value, datetime):
                        value = value.strftime("%Y-%m-%d %H:%M:%S")
                    elif isinstance(value, str):
                        value = value.rstrip()  # Eliminar espacios al final de la cadena
                    elif isinstance(value, Decimal):  # Verificar si el valor es Decimal
                        value = float(value)  # Convertir Decimal a float
                        value = round(value)  # Redondear si es necesario
                    row_dict[column_name] = value
                rows_list.append(row_dict)

            print(rows_list)

            cursor.close()
            conn.close()

            return JsonResponse({'results': rows_list})
        else:
            print("error")
    except pyodbc.Error as ex:
        print("Error:", ex)


@csrf_exempt
@require_http_methods(["POST"])
def generarRptoMicroseguros(request):
    if request.method == 'POST':
        # Verificar si hay datos en la solicitud
        if request.body:
            # Decodificar los datos JSON de la solicitud
            results = json.loads(request.body)

            datos = results['results']
            empresa = int(results['empresa'])
            startDate = results['startDate']
            startDate = datetime.strptime(startDate, "%Y-%m-%dT%H:%M:%S.%fZ")

            print(empresa)
            # Obtener la ruta absoluta de la plantilla Excel en el mismo directorio que el script
            script_dir = os.path.dirname(__file__)

            plantilla_path = os.path.join(
                script_dir, '../docs/Plantillas/Plantilla_Rpto_MicroSeguros_TiquetesVendidosConMicroSeguros.xlsx')

            # Verificar si existe el archivo
            if os.path.exists(plantilla_path):
                try:
                    # Carga de la plantilla Excel
                    workbook = load_workbook(plantilla_path)
                except Exception as e:
                    print(f"Error al cargar la plantilla: {e}")
                    return JsonResponse({'error': f"Error al cargar la plantilla: {e}"})

                sheet = workbook.active

                # Obtener la fecha y hora actual en UTC
                current_datetime_utc = datetime.now(pytz.utc)

                # Convertir la hora a la zona horaria deseada
                # timezone = pytz.timezone('America/Bogota')
                current_datetime_bogota = current_datetime_utc.astimezone(
                    pytz.timezone('America/Bogota'))

                # Formatear la fecha y hora
                current_date = current_datetime_bogota.strftime('%Y-%m-%d')
                current_time = current_datetime_bogota.strftime('%H:%M:%S')

                # Ubicación para month y year del reporte
                start_column_colMes = 'I'
                start_row_colMes = 6
                start_column_colYear = 'G'
                start_row_colYear = 6

                cell_colMonth = sheet[f'{start_column_colMes}{start_row_colMes}']
                cell_colMonth.value = startDate.year
                cell_colMonth.alignment = Alignment(horizontal="left")
                cell_colYear = sheet[f'{start_column_colYear}{start_row_colYear}']
                cell_colYear.value = startDate.month
                cell_colYear.alignment = Alignment(horizontal="left")

                start_column_colEmp = 'C'
                start_row_colEmp = 2
                # Escribir nombre de Empresa
                cell_colEmp = sheet[f'{start_column_colEmp}{start_row_colEmp}']
                if empresa == 277:
                    cell_colEmp.value = "Berlinas del Fonce S.A."
                elif empresa == 278:
                    cell_colEmp.value = "Berlitur S.A.S"
                elif empresa == 300:
                    cell_colEmp.value = "Compañia Libertador S.A."
                elif empresa == 310:
                    cell_colEmp.value = "Cartagena International Travels S.A.S"
                elif empresa == 9001:
                    cell_colEmp.value = "Servicio Especial"
                elif empresa == 320:
                    cell_colEmp.value = "Tourline Express S.A.S"

                cell_colEmp.alignment = Alignment(
                    horizontal='center')
                cell_colEmp.font = Font(bold=True)

                # Ubicación específica para la columnas
                start_row_col = 8
                start_column_col1 = 'B'
                start_column_col2 = 'C'
                start_column_col3 = 'D'
                start_column_col4 = 'E'
                start_column_col5 = 'F'
                start_column_col6 = 'G'
                start_column_col7 = 'H'

                # Escribir la fecha actual en la celda B6
                cell_c6 = sheet['B6']
                cell_c6.value = current_date

                # Escribir la hora actual en la celda D6
                cell_d6 = sheet['D6']
                cell_d6.value = current_time

                for index, colaborador in enumerate(datos, start=1):
                    for col_index, (col_name, col_value) in enumerate(colaborador.items(), start=1):
                        # Escribir en la columna 1
                        if col_index == 1:
                            cell_col1 = sheet[f'{start_column_col1}{start_row_col + index}']
                            cell_col1.value = col_value
                            cell_col1.alignment = Alignment(
                                horizontal='center')

                        # Escribir en la columna 2
                        elif col_index == 2:
                            cell_col2 = sheet[f'{start_column_col2}{start_row_col + index}']
                            cell_col2.value = col_value
                            cell_col2.alignment = Alignment(
                                horizontal='center')

                        # Escribir en la columna 3
                        elif col_index == 3:
                            cell_col3 = sheet[f'{start_column_col3}{start_row_col + index}']
                            cell_col3.value = col_value
                            cell_col3.number_format = '#,###'
                            cell_col3.alignment = Alignment(
                                horizontal='center')

                        # Escribir en la columna 4
                        elif col_index == 4:
                            cell_col4 = sheet[f'{start_column_col4}{start_row_col + index}']
                            cell_col4.value = col_value
                            cell_col4.number_format = "#,###"
                            cell_col4.alignment = Alignment(
                                horizontal='center')

                        # Escribir en la columna 5
                        elif col_index == 5:
                            cell_col5 = sheet[f'{start_column_col5}{start_row_col + index}']
                            cell_col5.value = col_value
                            cell_col5.number_format = "#,###"
                            cell_col5.alignment = Alignment(
                                horizontal='center')

                        # Escribir en la columna 6
                        elif col_index == 6:
                            cell_col6 = sheet[f'{start_column_col6}{start_row_col + index}']
                            cell_col6.value = col_value
                            cell_col6.alignment = Alignment(
                                horizontal='center')

                        # Escribir en la columna 6
                        elif col_index == 7:
                            cell_col7 = sheet[f'{start_column_col7}{start_row_col + index}']
                            cell_col7.value = col_value
                            cell_col7.alignment = Alignment(
                                horizontal='center')

                # Crear un objeto BytesIO para guardar temporalmente el archivo Excel
                buffer = io.BytesIO()
                workbook.save(buffer)
                buffer.seek(0)

                # Crear la respuesta con el nuevo archivo Excel
                response = HttpResponse(
                    buffer.getvalue(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                response['Content-Disposition'] = 'attachment; filename=Plantilla_Rpto_CuotaAdmin.xlsx'

                return response
            else:
                return JsonResponse({'error': 'El archivo de la plantilla no fue encontrado'})

        else:
            return JsonResponse({'error': 'Se esperaba una solicitud POST'})

    else:
        return JsonResponse({'error': 'Se esperaba una solicitud POST'})
