from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from openpyxl.styles import Font, Alignment
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
def TiquetesCRM(request):
    try:
        if request.method == "POST":
            # server = 'd1.berlinasdelfonce.com'
            server = '172.16.0.25'
            database = 'Dynamix'
            username = 'Developer'
            password = '123456'

            conn = pyodbc.connect(
                'DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+password)

            fechaInicio = request.POST.get('startDate', None)
            fechaFinal = request.POST.get('endDate', None)
            fecTransaccion = request.POST.get('Date', None)
            Opcion = request.POST.get('Opcion', None)

            fechaInicio = datetime.strptime(
                fechaInicio, '%Y-%m-%dT%H:%M:%S.%f')
            fechaFinal = datetime.strptime(fechaFinal, '%Y-%m-%dT%H:%M:%S.%f')
            fecTransaccion = datetime.strptime(
                fecTransaccion, '%Y-%m-%dT%H:%M:%S.%f')

            print("fechaInicio = ", fechaInicio,
                  ", fechaFinal = ", fechaFinal,
                  ", fecTransaccion = ", fecTransaccion)

            cursor = conn.cursor()

            cursor.execute("{CALL Rp_CRM (?, ?, ?, ?)}",
                           (fechaInicio, fechaFinal, fecTransaccion, Opcion))

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
def PvuInactivate(request):
    try:
        if request.method == "POST":
            server = '172.16.0.25'
            # server = 'd1.berlinasdelfonce.com'
            database = 'Dynamix'
            username = 'Developer'
            password = '123456'

            conn = pyodbc.connect(
                'DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+password)

            cedula = request.POST.get('dni', None)
            op = 3

            cursor = conn.cursor()

            cursor.execute(
                "{CALL VO_ViajeroFrecuente (?, ?)}", (cedula, op))

            # columns = [column[0] for column in cursor.description]
            # results = cursor.fetchall()

            # rows_list = []
            # for row in results:
            #     row_dict = {}
            #     for index, value in enumerate(row):
            #         column_name = columns[index]
            #         if isinstance(value, datetime):
            #             value = value.strftime("%Y-%m-%d %H:%M:%S")
            #         elif isinstance(value, str):
            #             value = value.rstrip()  # Eliminar espacios al final de la cadena
            #         elif isinstance(value, Decimal):  # Verificar si el valor es Decimal
            #             value = float(value)  # Convertir Decimal a float
            #             value = round(value)  # Redondear si es necesario
            #         row_dict[column_name] = value
            #     rows_list.append(row_dict)

            # print(rows_list)

            cursor.close()
            conn.close()

            return JsonResponse({'results': "Correctamente"})
        else:
            print("error")
    except pyodbc.Error as ex:
        print("Error:", ex)


@csrf_exempt
@require_http_methods(["POST"])
def generarRptoPL(request):
    if request.method == 'POST':
        # Verificar si hay datos en la solicitud
        if request.body:
            # Decodificar los datos JSON de la solicitud
            results = json.loads(request.body)

            datos = results['results']
            Opcion = int(results['Opcion'])
            SubOpcion = int(results['SubOpcion'])
            empresa = int(results['empresa'])
            startDate = results['startDate']
            startDate = datetime.strptime(startDate, "%Y-%m-%dT%H:%M:%S.%fZ")
            year = startDate.year
            month = startDate.month
            # print(Opcion, SubOpcion)

            # Obtener la ruta absoluta de la plantilla Excel en el mismo directorio que el script
            script_dir = os.path.dirname(__file__)

            if Opcion == 9:
                if SubOpcion == 0:
                    plantilla_path = os.path.join(
                        script_dir, '../docs/Plantillas/Plantilla_Rpto_Planeacion_Ocupacion_Lineas_Consolidado.xlsx')
                if SubOpcion == 1:
                    plantilla_path = os.path.join(
                        script_dir, '../docs/Plantillas/Plantilla_Rpto_Planeacion_Ocupacion_Lineas_Detallado.xlsx')

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

                # Ubicación para el nombre de la empresa
                if Opcion == 9:
                    if SubOpcion == 0:
                        start_column_colEmp = 'K'
                        start_row_colEmp = 2
                    elif SubOpcion == 1:
                        start_column_colEmp = 'D'
                        start_row_colEmp = 2

                # Ubicación para month y year del reporte
                start_column_colMes = 'I'
                start_row_colMes = 6
                start_column_colYear = 'G'
                start_row_colYear = 6

                # Escribir Month and Year
                cell_colMonth = sheet[f'{start_column_colMes}{start_row_colMes}']
                cell_colMonth.value = month
                cell_colMonth.alignment = Alignment(horizontal="left")
                cell_colYear = sheet[f'{start_column_colYear}{start_row_colYear}']
                cell_colYear.value = year
                cell_colYear.alignment = Alignment(horizontal="left")

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

                if Opcion == 9:
                    if SubOpcion == 0 or SubOpcion == 1:
                        # Ubicación específica para la columnas
                        start_column_col1 = 'B'
                        start_row_col1 = 8

                        start_column_col2 = 'C'
                        start_row_col2 = 8

                        start_column_col3 = 'D'
                        start_row_col3 = 8

                        start_column_col4 = 'E'
                        start_row_col4 = 8

                        start_column_col5 = 'F'
                        start_row_col5 = 8

                        start_column_col6 = 'G'
                        start_row_col6 = 8

                        start_column_col7 = 'H'
                        start_row_col7 = 8

                        start_column_col8 = 'I'
                        start_row_col8 = 8

                        start_column_col9 = 'J'
                        start_row_col9 = 8

                        start_column_col10 = 'K'
                        start_row_col10 = 8

                        start_column_col11 = 'L'
                        start_row_col11 = 8

                        start_column_col12 = 'M'
                        start_row_col12 = 8

                        start_column_col13 = 'N'
                        start_row_col13 = 8

                        start_column_col14 = 'O'
                        start_row_col14 = 8

                        start_column_col15 = 'P'
                        start_row_col15 = 8

                        start_column_col16 = 'Q'
                        start_row_col16 = 8

                        start_column_col17 = 'R'
                        start_row_col17 = 8

                        # Escribir la fecha actual en la celda B6
                        cell_c6 = sheet['B6']
                        cell_c6.value = current_date

                        # Escribir la hora actual en la celda D6
                        cell_d6 = sheet['D6']
                        cell_d6.value = current_time

                        # Variables para almacenar las sumas de la columnas (flotante)
                        sum_col3 = 0.0
                        sum_col4 = 0.0
                        sum_col5 = 0.0
                        sum_col6 = 0.0
                        sum_col7 = 0.0
                        sum_col8 = 0.0
                        sum_col9 = 0.0
                        sum_col10 = 0.0
                        sum_col11 = 0.0

                        for index, colaborador in enumerate(datos, start=1):
                            for col_index, (col_name, col_value) in enumerate(colaborador.items(), start=1):
                                # Escribir en la columna 1
                                if col_index == 1:
                                    cell_col1 = sheet[f'{start_column_col1}{start_row_col1 + index}']
                                    cell_col1.value = col_value
                                    cell_col1.alignment = Alignment(
                                        horizontal='center')

                                # Escribir en la columna 2
                                elif col_index == 2:
                                    cell_col2 = sheet[f'{start_column_col2}{start_row_col2 + index}']
                                    cell_col2.value = col_value
                                    cell_col2.alignment = Alignment(
                                        horizontal='center')

                                # Escribir en la columna 3
                                elif col_index == 3:
                                    cell_col3 = sheet[f'{start_column_col3}{start_row_col3 + index}']
                                    cell_col3.value = col_value
                                    cell_col3.alignment = Alignment(
                                        horizontal='center')
                                    if Opcion == 1:
                                        if SubOpcion == 0:
                                            sum_col3 += float(col_value)

                                # Escribir en la columna 4
                                elif col_index == 4:
                                    cell_col4 = sheet[f'{start_column_col4}{start_row_col4 + index}']
                                    cell_col4.value = col_value
                                    cell_col4.alignment = Alignment(
                                        horizontal='center')
                                    if Opcion == 1:
                                        if SubOpcion == 0 or SubOpcion == 1:
                                            sum_col4 += float(col_value)

                                # Escribir en la columna 5
                                elif col_index == 5:
                                    cell_col5 = sheet[f'{start_column_col5}{start_row_col5 + index}']
                                    cell_col5.value = col_value
                                    cell_col5.alignment = Alignment(
                                        horizontal='center')
                                    if Opcion == 1:
                                        if SubOpcion == 0 or SubOpcion == 1 or SubOpcion == 2:
                                            sum_col5 += float(col_value)

                                # Escribir en la columna 6
                                elif col_index == 6:
                                    cell_col6 = sheet[f'{start_column_col6}{start_row_col6 + index}']
                                    cell_col6.value = col_value
                                    cell_col6.alignment = Alignment(
                                        horizontal='center')
                                    if Opcion == 9:
                                        if SubOpcion == 1:
                                            sum_col6 += float(col_value)

                                # Escribir en la columna 7
                                elif col_index == 7:
                                    cell_col7 = sheet[f'{start_column_col7}{start_row_col7 + index}']
                                    cell_col7.value = col_value
                                    cell_col7.alignment = Alignment(
                                        horizontal='center')
                                    if Opcion == 9:
                                        if SubOpcion == 1:
                                            sum_col7 += float(col_value)
                                            cell_col7.number_format = '#,###'

                                # Escribir en la columna 8
                                elif col_index == 8:
                                    cell_col8 = sheet[f'{start_column_col8}{start_row_col8 + index}']
                                    cell_col8.value = col_value
                                    cell_col8.alignment = Alignment(
                                        horizontal='center')
                                    if Opcion == 9:
                                        if SubOpcion == 1:
                                            sum_col8 += float(col_value)
                                            cell_col8.number_format = '#,###'

                                # Escribir en la columna 9
                                elif col_index == 9:
                                    cell_col9 = sheet[f'{start_column_col9}{start_row_col9 + index}']
                                    cell_col9.value = col_value
                                    cell_col9.alignment = Alignment(
                                        horizontal='center')
                                    if Opcion == 9:
                                        if SubOpcion == 1:
                                            sum_col9 += float(col_value)
                                            cell_col9.number_format = '#,###'

                                # Escribir en la columna 9
                                elif col_index == 10:
                                    cell_col10 = sheet[f'{start_column_col10}{start_row_col10 + index}']
                                    cell_col10.value = col_value
                                    cell_col10.alignment = Alignment(
                                        horizontal='center')
                                    if Opcion == 9:
                                        if SubOpcion == 1:
                                            sum_col10 += float(col_value)
                                            cell_col10.number_format = '#,###'

                                # Escribir en la columna 11
                                elif col_index == 11:
                                    cell_col11 = sheet[f'{start_column_col11}{start_row_col11 + index}']
                                    cell_col11.value = col_value
                                    cell_col11.alignment = Alignment(
                                        horizontal='center')
                                    if Opcion == 9:
                                        if SubOpcion == 1:
                                            sum_col11 += col_value
                                            cell_col11.number_format = '#,###'

                                # Escribir en la columna 12
                                elif col_index == 12:
                                    cell_col12 = sheet[f'{start_column_col12}{start_row_col12 + index}']
                                    cell_col12.value = col_value
                                    cell_col12.alignment = Alignment(
                                        horizontal='center')

                                # Escribir en la columna 13
                                elif col_index == 13:
                                    cell_col13 = sheet[f'{start_column_col13}{start_row_col13 + index}']
                                    cell_col13.value = col_value
                                    cell_col13.alignment = Alignment(
                                        horizontal='center')

                                # Escribir en la columna 14
                                elif col_index == 14:
                                    cell_col14 = sheet[f'{start_column_col14}{start_row_col14 + index}']
                                    cell_col14.value = col_value
                                    cell_col14.alignment = Alignment(
                                        horizontal='center')

                                # Escribir en la columna 15
                                elif col_index == 15:
                                    cell_col15 = sheet[f'{start_column_col15}{start_row_col15 + index}']
                                    cell_col15.value = col_value
                                    cell_col15.alignment = Alignment(
                                        horizontal='center')

                                # Escribir en la columna 16
                                elif col_index == 16:
                                    cell_col16 = sheet[f'{start_column_col16}{start_row_col16 + index}']
                                    cell_col16.value = col_value
                                    cell_col16.alignment = Alignment(
                                        horizontal='center')

                                # Escribir en la columna 17
                                elif col_index == 17:
                                    cell_col17 = sheet[f'{start_column_col17}{start_row_col17 + index}']
                                    cell_col17.value = col_value
                                    cell_col17.alignment = Alignment(
                                        horizontal='center')

                            if Opcion == 9:
                                if SubOpcion == 1:
                                    cell_sum_col6 = sheet[
                                        f'{start_column_col6}{start_row_col6 + len(datos) + 1}']
                                    cell_sum_col6.value = sum_col6
                                    cell_sum_col6.font = Font(bold=True)
                                    cell_sum_col6.number_format = "#,###"
                                    cell_sum_col6.alignment = Alignment(
                                        horizontal='center')

                                    cell_sum_col7 = sheet[
                                        f'{start_column_col7}{start_row_col7 + len(datos) + 1}']
                                    cell_sum_col7.value = sum_col7
                                    cell_sum_col7.font = Font(bold=True)
                                    cell_sum_col7.number_format = "#,###"
                                    cell_sum_col7.alignment = Alignment(
                                        horizontal='center')

                                    cell_sum_col8 = sheet[
                                        f'{start_column_col8}{start_row_col8 + len(datos) + 1}']
                                    cell_sum_col8.value = sum_col8
                                    cell_sum_col8.font = Font(bold=True)
                                    cell_sum_col8.number_format = '#,###'
                                    cell_sum_col8.alignment = Alignment(
                                        horizontal='center')

                                    cell_sum_col9 = sheet[
                                        f'{start_column_col9}{start_row_col9 + len(datos) + 1}']
                                    cell_sum_col9.value = sum_col9
                                    cell_sum_col9.font = Font(bold=True)
                                    cell_sum_col9.number_format = '#,###'
                                    cell_sum_col9.alignment = Alignment(
                                        horizontal='center')

                                    cell_sum_col10 = sheet[
                                        f'{start_column_col10}{start_row_col10 + len(datos) + 1}']
                                    cell_sum_col10.value = sum_col10
                                    cell_sum_col10.font = Font(bold=True)
                                    cell_sum_col10.number_format = '#,###'
                                    cell_sum_col10.alignment = Alignment(
                                        horizontal='center')

                                    # Escribir "Totales" en negrita
                                    cell_totals = sheet[
                                        f'{start_column_col1}{start_row_col1 + len(datos) + 1}']
                                    cell_totals.value = "Totales"
                                    cell_totals.font = Font(bold=True)
                                    cell_totals.alignment = Alignment(
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
