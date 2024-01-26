from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from openpyxl.styles import Font, Alignment
from openpyxl import load_workbook
from datetime import datetime
from dateutil import parser
from decimal import Decimal
import pyodbc
import json
import pytz
import os
import io


@csrf_exempt
@require_http_methods(["POST"])
def rptoContabilidad(request):
    try:
        if request.method == "POST":

            server = 'd1.berlinasdelfonce.com'
            database = 'Dynamix'
            username = 'Developer'
            password = '123456'

            conn = pyodbc.connect(
                'DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+password)

            EmpiD = request.POST.get('empresa', None)
            fechaInicio = request.POST.get('startDate', None)
            fechaFinal = request.POST.get('endDate', None)
            Opcion = request.POST.get('Opcion', None)
            SubOpcion = request.POST.get('SubOpcion', None)
            Cadena01 = "VACIO"
            Cadena02 = "VACIO"
            if int(Opcion) == 22:
                if int(SubOpcion) == 0:
                    Cadena01 = "65"
                    Cadena02 = "VACIO"
                elif int(SubOpcion) == 1:
                    Cadena01 = "VACIO"
                    Cadena02 = "1"
            valor01 = 100
            print(Cadena01, Cadena02)

            cursor = conn.cursor()

            cursor.execute("{CALL RP_Consultas05 (?, ?, ?, ?, ?, ?, ?, ?)}",
                           (EmpiD, fechaInicio, fechaFinal, Opcion, SubOpcion, Cadena01, Cadena02, valor01))

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
def generarRptoOpeViajes(request):
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

            if Opcion == 0:
                if SubOpcion == 0:
                    plantilla_path = os.path.join(
                        script_dir, '../docs/Plantillas/Plantilla_Rpto_Operaciones_Viajes.xlsx')
            elif Opcion == 1:
                if SubOpcion == 0:
                    plantilla_path = os.path.join(
                        script_dir, '../docs/Plantillas/Plantilla_Rpto_Operaciones_InformeConsolidadoPM0.xlsx')
                elif SubOpcion == 1:
                    plantilla_path = os.path.join(
                        script_dir, '../docs/Plantillas/Plantilla_Rpto_Operaciones_InformeConsolidadoPM1.xlsx')
                elif SubOpcion == 2:
                    if empresa == 277 or empresa == 278:
                        plantilla_path = os.path.join(
                            script_dir, '../docs/Plantillas/Plantilla_Rpto_Operaciones_InformePorFechaPM.xlsx')
                    elif empresa == 9001 or empresa == 310 or empresa == 320:
                        plantilla_path = os.path.join(
                            script_dir, '../docs/Plantillas/Plantilla_Rpto_Operaciones_InformePorFechaSP.xlsx')
            elif Opcion == 20:
                if SubOpcion == 0:
                    plantilla_path = os.path.join(
                        script_dir, '../docs/Plantillas/Plantilla_Rpto_Operaciones_InfoEstadisticasConsolidadoPLC.xlsx')
                elif SubOpcion == 1:
                    plantilla_path = os.path.join(
                        script_dir, '../docs/Plantillas/Plantilla_Rpto_Operaciones_InfoEstadisticaConsolidadoPLC.xlsx')
            elif Opcion == 26:
                if SubOpcion == 0:
                    plantilla_path = os.path.join(
                        script_dir, '../docs/Plantillas/Plantilla_Rpto_Operaciones_InfoEstadisticasConsolidadoPLEA.xlsx')
                elif SubOpcion == 1:
                    plantilla_path = os.path.join(
                        script_dir, '../docs/Plantillas/Plantilla_Rpto_Operaciones_InfoEstadisticasDetalladoPLEA.xlsx')
            elif Opcion == 29:
                if SubOpcion == 0:
                    plantilla_path = os.path.join(
                        script_dir, '../docs/Plantillas/Plantilla_Rpto_Operaciones_InformeConsolidadoCombustible.xlsx')
                elif SubOpcion == 1:
                    plantilla_path = os.path.join(
                        script_dir, '../docs/Plantillas/Plantilla_Rpto_Operaciones_InformeDetalladoCombustible.xlsx')

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
                timezone = pytz.timezone('America/Bogota')
                current_datetime_bogota = current_datetime_utc.astimezone(
                    timezone)

                # Formatear la fecha y hora
                current_date = current_datetime_bogota.strftime('%Y-%m-%d')
                current_time = current_datetime_bogota.strftime('%H:%M:%S')

                # Ubicación para el nombre de la empresa
                if Opcion != 29:
                    start_column_colEmp = 'D'
                    start_row_colEmp = 2
                else:
                    start_column_colEmp = 'C'
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
                cell_colEmp.font = Font(bold=True)

                if Opcion == 0 or Opcion == 1 or Opcion == 20 or Opcion == 26 or Opcion == 29:
                    if SubOpcion == 0 or SubOpcion == 1 or SubOpcion == 2:
                        # Ubicación específica para la columna 1 en la celda B9
                        start_column_col1 = 'B'
                        start_row_col1 = 8

                        # Ubicación específica para la columna 2 en la celda C9
                        start_column_col2 = 'C'
                        start_row_col2 = 8

                        # Ubicación específica para la columna 3 en la celda D9
                        start_column_col3 = 'D'
                        start_row_col3 = 8

                        # Ubicación específica para la columna 4 en la celda E9
                        start_column_col4 = 'E'
                        start_row_col4 = 8

                        # Ubicación específica para la columna 5 en la celda E9
                        start_column_col5 = 'F'
                        start_row_col5 = 8

                        # Ubicación específica para la columna 6 en la celda E9
                        start_column_col6 = 'G'
                        start_row_col6 = 8

                        # Ubicación específica para la columna 7 en la celda E9
                        start_column_col7 = 'H'
                        start_row_col7 = 8

                        # Ubicación específica para la columna 8 en la celda E9
                        start_column_col8 = 'I'
                        start_row_col8 = 8

                        # Ubicación específica para la columna 9 en la celda E9
                        start_column_col9 = 'J'
                        start_row_col9 = 8

                        # Escribir la fecha actual en la celda B6
                        cell_c6 = sheet['B6']
                        cell_c6.value = current_date

                        # Escribir la hora actual en la celda D6
                        cell_d6 = sheet['D6']
                        cell_d6.value = current_time

                        # Variable para almacenar la suma de la columna 3 (flotante)
                        sum_col3 = 0.0
                        # Variable para almacenar la suma de la columna 4 (flotante)
                        sum_col4 = 0.0
                        # Variable para almacenar la suma de la columna 5 (flotante)
                        sum_col5 = 0.0
                        # Variable para almacenar la suma de la columna 6 (flotante)
                        sum_col6 = 0.0
                        # Variable para almacenar la suma de la columna 7 (flotante)
                        sum_col7 = 0.0
                        # Variable para almacenar la suma de la columna 8 (flotante)
                        sum_col8 = 0.0

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
                                    if Opcion == 1:
                                        if SubOpcion == 0 or SubOpcion == 1 or SubOpcion == 2:
                                            sum_col6 += float(col_value)
                                    elif Opcion == 29:
                                        if SubOpcion == 0:
                                            sum_col6 += float(col_value)
                                            cell_col6.number_format = "#,###"

                                # Escribir en la columna 7
                                elif col_index == 7:
                                    cell_col7 = sheet[f'{start_column_col7}{start_row_col7 + index}']
                                    cell_col7.value = col_value
                                    cell_col7.alignment = Alignment(
                                        horizontal='center')
                                    if Opcion != 20 and Opcion != 26 and Opcion != 29:
                                        sum_col7 += float(col_value)
                                    if Opcion == 1:
                                        if SubOpcion == 2:
                                            if empresa == 9001 or empresa == 310 or empresa == 320:
                                                cell_col7.number_format = "#,###"

                                # Escribir en la columna 8
                                elif col_index == 8:
                                    cell_col8 = sheet[f'{start_column_col8}{start_row_col8 + index}']
                                    cell_col8.value = col_value
                                    cell_col8.alignment = Alignment(
                                        horizontal='center')
                                    if Opcion == 1:
                                        if SubOpcion == 1:
                                            sum_col8 += float(col_value)
                                        elif SubOpcion == 2:
                                            if empresa == 277 or empresa == 278:
                                                sum_col8 += float(col_value)
                                                cell_col8.number_format = "#,###"
                                    elif Opcion == 29:
                                        if SubOpcion == 1:
                                            sum_col8 += float(col_value)
                                            cell_col8.number_format = "#,###"

                                # Escribir en la columna 9
                                elif col_index == 9:
                                    cell_col9 = sheet[f'{start_column_col9}{start_row_col9 + index}']
                                    cell_col9.value = col_value
                                    cell_col9.alignment = Alignment(
                                        horizontal='center')

                            if Opcion == 1:
                                if SubOpcion == 0:
                                    # Escribir las sumas al final de las filas de resultados y aplicar el estilo en negrita
                                    cell_sum_col3 = sheet[
                                        f'{start_column_col3}{start_row_col3 + len(datos) + 1}']
                                    cell_sum_col3.value = sum_col3
                                    cell_sum_col3.font = Font(bold=True)
                                    cell_sum_col3.alignment = Alignment(
                                        horizontal='center')

                                    cell_sum_col4 = sheet[
                                        f'{start_column_col4}{start_row_col4 + len(datos) + 1}']
                                    cell_sum_col4.value = sum_col4
                                    cell_sum_col4.font = Font(bold=True)
                                    cell_sum_col4.alignment = Alignment(
                                        horizontal='center')

                                    cell_sum_col5 = sheet[
                                        f'{start_column_col5}{start_row_col5 + len(datos) + 1}']
                                    cell_sum_col5.value = sum_col5
                                    cell_sum_col5.font = Font(bold=True)
                                    cell_sum_col5.alignment = Alignment(
                                        horizontal='center')

                                    cell_sum_col6 = sheet[
                                        f'{start_column_col6}{start_row_col6 + len(datos) + 1}']
                                    cell_sum_col6.value = sum_col6
                                    cell_sum_col6.font = Font(bold=True)
                                    cell_sum_col6.alignment = Alignment(
                                        horizontal='center')

                                    cell_sum_col7 = sheet[
                                        f'{start_column_col7}{start_row_col7 + len(datos) + 1}']
                                    cell_sum_col7.value = sum_col7
                                    cell_sum_col7.font = Font(bold=True)
                                    cell_sum_col7.alignment = Alignment(
                                        horizontal='center')
                                    if empresa == 9001 or empresa == 310 or empresa == 320:
                                        cell_sum_col7.number_format = "#,###"
                                    elif empresa == 277 or empresa == 278:
                                        cell_sum_col8 = sheet[
                                            f'{start_column_col8}{start_row_col8 + len(datos) + 1}']
                                        cell_sum_col8.value = sum_col8
                                        cell_sum_col8.number_format = "#,###"
                                    if Opcion == 1:
                                        if SubOpcion == 0:
                                            porcentaje = round((
                                                100 * sum_col5) / sum_col4, 2)
                                            cell_sum_col7.value = porcentaje

                                    cell_sum_col8 = sheet[
                                        f'{start_column_col8}{start_row_col8 + len(datos) + 1}']
                                    cell_sum_col8.value = sum_col8
                                    cell_sum_col8.font = Font(bold=True)
                                    cell_sum_col8.alignment = Alignment(
                                        horizontal='center')

                                    # Escribir "Totales" en negrita
                                    cell_totals = sheet[
                                        f'{start_column_col1}{start_row_col1 + len(datos) + 1}']
                                    cell_totals.value = "Totales"
                                    cell_totals.font = Font(bold=True)
                                    cell_totals.alignment = Alignment(
                                        horizontal='center')
                                elif SubOpcion == 1:
                                    # Escribir las sumas al final de las filas de resultados y aplicar el estilo en negrita
                                    cell_sum_col4 = sheet[
                                        f'{start_column_col4}{start_row_col4 + len(datos) + 1}']
                                    cell_sum_col4.value = sum_col4
                                    cell_sum_col4.font = Font(bold=True)
                                    cell_sum_col4.alignment = Alignment(
                                        horizontal='center')

                                    cell_sum_col5 = sheet[
                                        f'{start_column_col5}{start_row_col5 + len(datos) + 1}']
                                    cell_sum_col5.value = sum_col5
                                    cell_sum_col5.font = Font(bold=True)
                                    cell_sum_col5.alignment = Alignment(
                                        horizontal='center')

                                    cell_sum_col6 = sheet[
                                        f'{start_column_col6}{start_row_col6 + len(datos) + 1}']
                                    cell_sum_col6.value = sum_col6
                                    cell_sum_col6.font = Font(bold=True)
                                    cell_sum_col6.alignment = Alignment(
                                        horizontal='center')

                                    cell_sum_col7 = sheet[
                                        f'{start_column_col7}{start_row_col7 + len(datos) + 1}']
                                    cell_sum_col7.value = sum_col7
                                    cell_sum_col7.font = Font(bold=True)
                                    cell_sum_col7.alignment = Alignment(
                                        horizontal='center')
                                    cell_sum_col7.number_format = "#,###"

                                    cell_sum_col8 = sheet[
                                        f'{start_column_col8}{start_row_col8 + len(datos) + 1}']
                                    cell_sum_col8.value = sum_col8
                                    cell_sum_col8.font = Font(bold=True)
                                    cell_sum_col8.alignment = Alignment(
                                        horizontal='center')
                                    if SubOpcion == 1:
                                        porcentaje = round((
                                            100 * sum_col6) / sum_col5, 2)
                                        cell_sum_col8.value = porcentaje

                                    # Escribir "Totales" en negrita
                                    cell_totals = sheet[
                                        f'{start_column_col1}{start_row_col1 + len(datos) + 1}']
                                    cell_totals.value = "Totales"
                                    cell_totals.font = Font(bold=True)
                                    cell_totals.alignment = Alignment(
                                        horizontal='center')
                                elif SubOpcion == 2:
                                    # Escribir las sumas al final de las filas de resultados y aplicar el estilo en negrita
                                    cell_sum_col5 = sheet[
                                        f'{start_column_col5}{start_row_col5 + len(datos) + 1}']
                                    cell_sum_col5.value = sum_col5
                                    cell_sum_col5.font = Font(bold=True)
                                    cell_sum_col5.alignment = Alignment(
                                        horizontal='center')

                                    cell_sum_col6 = sheet[
                                        f'{start_column_col6}{start_row_col6 + len(datos) + 1}']
                                    cell_sum_col6.value = sum_col6
                                    cell_sum_col6.font = Font(bold=True)
                                    cell_sum_col6.alignment = Alignment(
                                        horizontal='center')

                                    cell_sum_col7 = sheet[
                                        f'{start_column_col7}{start_row_col7 + len(datos) + 1}']
                                    cell_sum_col7.value = sum_col7
                                    cell_sum_col7.font = Font(bold=True)
                                    cell_sum_col7.alignment = Alignment(
                                        horizontal='center')
                                    if empresa == 9001 or empresa == 310 or empresa == 320:
                                        cell_sum_col7.number_format = "#,###"
                                    elif empresa == 277 or empresa == 278:
                                        cell_sum_col8 = sheet[
                                            f'{start_column_col8}{start_row_col8 + len(datos) + 1}']
                                        cell_sum_col8.value = sum_col8
                                        cell_sum_col8.number_format = "#,###"
                                        cell_sum_col8.alignment = Alignment(
                                            horizontal='center')
                                        cell_sum_col8.font = Font(bold=True)

                                    cell_sum_col9 = sheet[
                                        f'{start_column_col9}{start_row_col9 + len(datos) + 1}']
                                    porcentaje = round(
                                        (100 * sum_col7) / sum_col6, 2)
                                    cell_sum_col9.value = porcentaje
                                    cell_sum_col9.font = Font(bold=True)
                                    cell_sum_col9.alignment = Alignment(
                                        horizontal='center')

                                    # Escribir "Totales" en negrita
                                    cell_totals = sheet[
                                        f'{start_column_col1}{start_row_col1 + len(datos) + 1}']
                                    cell_totals.value = "Totales"
                                    cell_totals.font = Font(bold=True)
                                    cell_totals.alignment = Alignment(
                                        horizontal='center')
                            elif Opcion == 29:
                                if SubOpcion == 0:
                                    # Escribir las sumas al final de las filas de resultados y aplicar el estilo en negrita
                                    cell_sum_col6 = sheet[
                                        f'{start_column_col6}{start_row_col6 + len(datos) + 1}']
                                    cell_sum_col6.value = sum_col6
                                    cell_sum_col6.font = Font(bold=True)
                                    cell_sum_col6.alignment = Alignment(
                                        horizontal='center')
                                    cell_sum_col6.number_format = "#,###"

                                    # Escribir "Totales" en negrita
                                    cell_totals = sheet[
                                        f'{start_column_col1}{start_row_col1 + len(datos) + 1}']
                                    cell_totals.value = "Totales"
                                    cell_totals.font = Font(bold=True)
                                    cell_totals.alignment = Alignment(
                                        horizontal='center')
                                elif SubOpcion == 1:
                                    # Escribir las sumas al final de las filas de resultados y aplicar el estilo en negrita
                                    cell_sum_col8 = sheet[
                                        f'{start_column_col8}{start_row_col8 + len(datos) + 1}']
                                    cell_sum_col8.value = sum_col8
                                    cell_sum_col8.font = Font(bold=True)
                                    cell_sum_col8.alignment = Alignment(
                                        horizontal='center')
                                    cell_sum_col8.number_format = "#,###"

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
