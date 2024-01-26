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
def rptoComercial(request):
    try:
        if request.method == "POST":
            server = 'd1.berlinasdelfonce.com'
            database = 'Dynamix'
            username = 'Developer'
            password = '123456'
            conn = pyodbc.connect(
                'DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+password)

            EmpID = request.POST.get('empresa', None)
            Fechainicio = request.POST.get('startDate', None)
            FechaFinal = request.POST.get('endDate', None)
            Opcion = request.POST.get('Opcion', None)
            datocontrol = '0'

            cursor = conn.cursor()

            cursor.execute("{CALL RP_consultas01 (?, ?, ?, ?, ?)}",
                           (EmpID, Fechainicio, FechaFinal, datocontrol, Opcion))

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
def rptoCertificados(request):
    try:
        if request.method == "POST":
            server = 'd1.berlinasdelfonce.com'
            database = 'Dynamix'
            username = 'Developer'
            password = '123456'
            conn = pyodbc.connect(
                'DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+password)

            documento = request.POST.get('documento', None)

            cursor = conn.cursor()

            cursor.execute("{CALL Rp_certificaciones (?)}",
                           (documento))

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
def rptoDomicilios(request):
    try:
        if request.method == "POST":
            server = 'd1.berlinasdelfonce.com'
            database = 'Dynamix'
            username = 'Developer'
            password = '123456'
            conn = pyodbc.connect(
                'DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+password)

            Empid = request.POST.get('empresa', None)
            fechaInicio = request.POST.get('startDate', None)
            fechaFinal = request.POST.get('endDate', None)
            Opcion = int(request.POST.get('Opcion', None))
            SubOpcion = request.POST.get('SubOpcion', None)
            Cadena01 = request.POST.get('Cadena01', None)

            if Opcion == 12:
                Cadena01 = request.POST.get('documento', None)
            elif Cadena01 == None and (Opcion == 13 or Opcion == 14):
                Cadena01 = "24445"

            if Opcion == 22:
                Cadena02 = '1'
            elif Opcion == 28:
                Cadena02 = '65'
            else:
                Cadena02 = "VACIO"

            valor = 100
            print(Empid, fechaInicio, fechaFinal, Opcion,
                  SubOpcion, Cadena01, Cadena02, valor)

            cursor = conn.cursor()

            cursor.execute("{CALL RP_Consultas05 (?, ?, ?, ?, ?, ?, ?, ?)}",
                           (Empid, fechaInicio, fechaFinal, Opcion, SubOpcion, Cadena01, Cadena02, valor))

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

            # print(rows_list)

            cursor.close()
            conn.close()

            return JsonResponse({'results': rows_list})
        else:
            print("error")
    except pyodbc.Error as ex:
        print("Error:", ex)


@csrf_exempt
@require_http_methods(["POST"])
def generarRptosComercial(request):
    if request.method == 'POST':
        # Verificar si hay datos en la solicitud
        if request.body:
            # Decodificar los datos JSON de la solicitud
            results = json.loads(request.body)

            datos = results['results']
            Opcion = int(results['Opcion'])
            try:
                Opcion2 = int(results['Opcion2'])
            except:
                Opcion2 = None
            empresa = int(results['empresa'])
            if Opcion != 12 and Opcion != 99:
                startDate = results['startDate']
                startDate = datetime.strptime(
                    startDate, "%Y-%m-%dT%H:%M:%S.%fZ")
                year = startDate.year
                month = startDate.month
            try:
                SubOpcion = int(results['SubOpcion'])
            except:
                SubOpcion = None

            print(Opcion, SubOpcion)

            # Obtener la ruta absoluta de la plantilla Excel en el mismo directorio que el script
            script_dir = os.path.dirname(__file__)

            if Opcion == 6:
                plantilla_path = os.path.join(
                    script_dir, '../docs/Plantillas/Plantilla_Rpto_Estadisticas_PlanilladosPasajerosXRutas.xlsx')
            elif Opcion == 7:
                plantilla_path = os.path.join(
                    script_dir, '../docs/Plantillas/Plantilla_Rpto_Estadisticas_PlanilladosPasajerosXTrayectos.xlsx')
            elif Opcion == 8:
                plantilla_path = os.path.join(
                    script_dir, '../docs/Plantillas/Plantilla_Rpto_Estadisticas_PlanilladosPasajerosOrigen-Destino.xlsx')
            elif Opcion == 11:
                plantilla_path = os.path.join(
                    script_dir, '../docs/Plantillas/Plantilla_Rpto_Comercial_EstadisticasDomiciliosPorLinea.xlsx')
            elif Opcion == 12:
                plantilla_path = os.path.join(
                    script_dir, '../docs/Plantillas/Plantilla_Rpto_Estadisticas_ViajesXPasajero.xlsx')
            elif Opcion == 13:
                plantilla_path = os.path.join(
                    script_dir, '../docs/Plantillas/Plantilla_Rpto_PuntosVenta_PaxVentaCucuta.xlsx')
                if Opcion2 == 2:
                    plantilla_path = os.path.join(
                        script_dir, '../docs/Plantillas/Plantilla_Rpto_PuntosVenta_PaxVendidosEnBogota.xlsx')
            elif Opcion == 14:
                plantilla_path = os.path.join(
                    script_dir, '../docs/Plantillas/Plantilla_Rpto_PuntosVenta_PaxMovilizadosXCiudad.xlsx')
                if Opcion2 == 2:
                    plantilla_path = os.path.join(
                        script_dir, '../docs/Plantillas/Plantilla_Rpto_PuntosVenta_PaxDespachadosEnBogota.xlsx')
            elif Opcion == 28:
                plantilla_path = os.path.join(
                    script_dir, '../docs/Plantillas/Plantilla_Rpto_ComercialTrazabilidadVentas.xlsx')
            elif Opcion == 33:
                if SubOpcion == 0:
                    plantilla_path = os.path.join(
                        script_dir, '../docs/Plantillas/Plantilla_Rpto_Biometricos_RptoXFecha.xlsx')
                elif SubOpcion == 1:
                    plantilla_path = os.path.join(
                        script_dir, '../docs/Plantillas/Plantilla_Rpto_TesoreriaTiquetesMacarena.xlsx')
                elif SubOpcion == 2:
                    plantilla_path = os.path.join(
                        script_dir, '../docs/Plantillas/Plantilla_Rpto_MicroSegurosRptoMicroSeguros.xlsx')
            elif Opcion == 34:
                if SubOpcion == 0:
                    plantilla_path = os.path.join(
                        script_dir, '../docs/Plantillas/Plantilla_Rpto_SeguridadSalud_NumeroDespachosXDia_Consolidado.xlsx')
                elif SubOpcion == 1:
                    plantilla_path = os.path.join(
                        script_dir, '../docs/Plantillas/Plantilla_Rpto_SeguridadSalud_NumeroDespachosXDia_Detallado.xlsx')
                elif SubOpcion == 2:
                    plantilla_path = os.path.join(
                        script_dir, '../docs/Plantillas/Plantilla_Rpto_SeguridadSalud_CantidadVehiculosTrabajaronXDia_Consolidado.xlsx')
                elif SubOpcion == 3:
                    plantilla_path = os.path.join(
                        script_dir, '../docs/Plantillas/Plantilla_Rpto_SeguridadSalud_CantidadVehiculosTrabajaronXDia_Detallado.xlsx')
                elif SubOpcion == 4:
                    plantilla_path = os.path.join(
                        script_dir, '../docs/Plantillas/Plantilla_Rpto_SeguridadSalud_HorasEfectivasConductores_Consolidado.xlsx')
                elif SubOpcion == 5:
                    plantilla_path = os.path.join(
                        script_dir, '../docs/Plantillas/Plantilla_Rpto_SeguridadSalud_HorasEfectivasConductores_Detallado.xlsx')
            elif Opcion == 99:
                plantilla_path = os.path.join(
                    script_dir, '../docs/Plantillas/Plantilla_Rpto_Estadisticas_Certificaciones.xlsx')

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
                if Opcion == 6 or Opcion == 7 or Opcion == 8 or Opcion == 12 or Opcion == 13 or Opcion == 14 or Opcion == 33 or Opcion == 34 or Opcion == 99 or Opcion == 11 or Opcion == 28:
                    start_column_colEmp = 'C'
                    start_row_colEmp = 2
                elif Opcion == 1:
                    start_column_colEmp = 'D'
                    start_row_colEmp = 2

                # Ubicación para month y year del reporte
                start_column_colMes = 'I'
                start_row_colMes = 6
                start_column_colYear = 'G'
                start_row_colYear = 6

                # Escribir Month and Year
                if Opcion != 12 and Opcion != 99:
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

                if Opcion == 6 or Opcion == 7 or Opcion == 8 or Opcion == 12 or Opcion == 13 or Opcion == 14 or Opcion == 33 or Opcion == 34 or Opcion == 99 or Opcion == 11 or Opcion == 28:
                    # Ubicación para la columnas
                    start_row_col = 8
                    start_column_col1 = 'B'
                    start_column_col2 = 'C'
                    start_column_col3 = 'D'
                    start_column_col4 = 'E'
                    start_column_col5 = 'F'
                    start_column_col6 = 'G'
                    start_column_col7 = 'H'
                    start_column_col8 = 'I'
                    start_column_col9 = 'J'
                    start_column_col10 = 'K'
                    start_column_col11 = 'L'
                    start_column_col12 = 'M'
                    start_column_col13 = 'N'
                    start_column_col14 = 'O'
                    start_column_col15 = 'P'
                    start_column_col16 = 'Q'
                    start_column_col17 = 'R'
                    start_column_col18 = 'S'

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
                                cell_col3.alignment = Alignment(
                                    horizontal='center')
                                if Opcion == 6 or Opcion == 8:
                                    cell_col3.number_format = '#,###'
                                    sum_col3 += float(col_value)

                            # Escribir en la columna 4
                            elif col_index == 4:
                                cell_col4 = sheet[f'{start_column_col4}{start_row_col + index}']
                                cell_col4.value = col_value
                                cell_col4.alignment = Alignment(
                                    horizontal='center')
                                if Opcion == 6 or Opcion == 7 or Opcion == 8 or Opcion == 11 or (Opcion == 34 and (SubOpcion == 0 or SubOpcion == 2)):
                                    cell_col4.number_format = '#,###'
                                    sum_col4 += float(col_value)

                            # Escribir en la columna 5
                            elif col_index == 5:
                                cell_col5 = sheet[f'{start_column_col5}{start_row_col + index}']
                                cell_col5.value = col_value
                                cell_col5.alignment = Alignment(
                                    horizontal='center')
                                if Opcion == 6 or Opcion == 7 or Opcion == 11 or (Opcion == 34 and SubOpcion == 0):
                                    cell_col5.number_format = '#,###'
                                    sum_col5 += float(col_value)

                            # Escribir en la columna 6
                            elif col_index == 6:
                                cell_col6 = sheet[f'{start_column_col6}{start_row_col + index}']
                                cell_col6.value = col_value
                                cell_col6.alignment = Alignment(
                                    horizontal='center')
                                if Opcion == 6 or (Opcion == 34 and SubOpcion == 0):
                                    cell_col6.number_format = '#,###'
                                    sum_col6 += float(col_value)

                            # Escribir en la columna 7
                            elif col_index == 7:
                                cell_col7 = sheet[f'{start_column_col7}{start_row_col + index}']
                                cell_col7.value = col_value
                                cell_col7.alignment = Alignment(
                                    horizontal='center')
                                if Opcion2 == None and (Opcion == 9 or Opcion == 8 or Opcion == 28 or Opcion == 14):
                                    sum_col7 += float(col_value)
                                    cell_col7.number_format = '#,###'

                            # Escribir en la columna 8
                            elif col_index == 8:
                                cell_col8 = sheet[f'{start_column_col8}{start_row_col + index}']
                                cell_col8.value = col_value
                                cell_col8.alignment = Alignment(
                                    horizontal='center')
                                if Opcion == 9 or Opcion == 8 or Opcion == 28 or (Opcion == 33 and SubOpcion == 1):
                                    sum_col8 += float(col_value)
                                    cell_col8.number_format = '#,###'

                            # Escribir en la columna 9
                            elif col_index == 9:
                                cell_col9 = sheet[f'{start_column_col9}{start_row_col + index}']
                                cell_col9.value = col_value
                                cell_col9.alignment = Alignment(
                                    horizontal='center')
                                if Opcion == 8 or Opcion == 28:
                                    sum_col9 += float(col_value)
                                    cell_col9.number_format = '#,###'

                            # Escribir en la columna 10
                            elif col_index == 10:
                                cell_col10 = sheet[f'{start_column_col10}{start_row_col + index}']
                                cell_col10.value = col_value
                                cell_col10.alignment = Alignment(
                                    horizontal='center')
                                if Opcion == 8:
                                    sum_col10 += float(col_value)
                                    cell_col10.number_format = '#,###'

                            # Escribir en la columna 11
                            elif col_index == 11:
                                cell_col11 = sheet[f'{start_column_col11}{start_row_col + index}']
                                cell_col11.value = col_value
                                cell_col11.alignment = Alignment(
                                    horizontal='center')
                                if Opcion == 8:
                                    sum_col10 += float(col_value)
                                    cell_col10.number_format = '#,###'

                            # Escribir en la columna 12
                            elif col_index == 12:
                                cell_col12 = sheet[f'{start_column_col12}{start_row_col + index}']
                                cell_col12.value = col_value
                                cell_col12.alignment = Alignment(
                                    horizontal='center')
                                if Opcion == 8:
                                    sum_col10 += float(col_value)
                                    cell_col10.number_format = '#,###'

                            # Escribir en la columna 13
                            elif col_index == 13:
                                cell_col13 = sheet[f'{start_column_col13}{start_row_col + index}']
                                cell_col13.value = col_value
                                cell_col13.alignment = Alignment(
                                    horizontal='center')

                            # Escribir en la columna 14
                            elif col_index == 14:
                                cell_col14 = sheet[f'{start_column_col14}{start_row_col + index}']
                                cell_col14.value = col_value
                                cell_col14.alignment = Alignment(
                                    horizontal='center')

                            # Escribir en la columna 15
                            elif col_index == 15:
                                cell_col15 = sheet[f'{start_column_col15}{start_row_col + index}']
                                cell_col15.value = col_value
                                cell_col15.alignment = Alignment(
                                    horizontal='center')

                            # Escribir en la columna 16
                            elif col_index == 16:
                                cell_col16 = sheet[f'{start_column_col16}{start_row_col + index}']
                                cell_col16.value = col_value
                                cell_col16.alignment = Alignment(
                                    horizontal='center')

                            # Escribir en la columna 17
                            elif col_index == 17:
                                cell_col17 = sheet[f'{start_column_col17}{start_row_col + index}']
                                cell_col17.value = col_value
                                cell_col17.alignment = Alignment(
                                    horizontal='center')

                            # Escribir en la columna 18
                            elif col_index == 18:
                                cell_col18 = sheet[f'{start_column_col18}{start_row_col + index}']
                                cell_col18.value = col_value
                                cell_col18.alignment = Alignment(
                                    horizontal='center')

                            if Opcion == 6:
                                cell_sum_col3 = sheet[
                                    f'{start_column_col3}{start_row_col + len(datos) + 1}']
                                cell_sum_col3.value = sum_col3
                                cell_sum_col3.font = Font(bold=True)
                                cell_sum_col3.number_format = "#,###"
                                cell_sum_col3.alignment = Alignment(
                                    horizontal='center')

                                cell_sum_col6 = sheet[
                                    f'{start_column_col6}{start_row_col + len(datos) + 1}']
                                cell_sum_col6.value = sum_col6
                                cell_sum_col6.font = Font(bold=True)
                                cell_sum_col6.number_format = "#,###"
                                cell_sum_col6.alignment = Alignment(
                                    horizontal='center')

                            if Opcion == 6 or Opcion == 7 or Opcion == 11 or (Opcion == 34 and (SubOpcion == 0 or SubOpcion == 2)):
                                if Opcion == 11:
                                    cell_sum_col3 = sheet[
                                        f'{start_column_col3}{start_row_col + len(datos) + 1}']
                                    cell_sum_col3.value = sum_col3
                                    cell_sum_col3.font = Font(bold=True)
                                    cell_sum_col3.number_format = "#,###"
                                    cell_sum_col3.alignment = Alignment(
                                        horizontal='center')

                                cell_sum_col4 = sheet[
                                    f'{start_column_col4}{start_row_col + len(datos) + 1}']
                                cell_sum_col4.value = sum_col4
                                cell_sum_col4.font = Font(bold=True)
                                cell_sum_col4.number_format = "#,###"
                                cell_sum_col4.alignment = Alignment(
                                    horizontal='center')

                                cell_sum_col5 = sheet[
                                    f'{start_column_col5}{start_row_col + len(datos) + 1}']
                                cell_sum_col5.value = sum_col5
                                cell_sum_col5.font = Font(bold=True)
                                cell_sum_col5.number_format = "#,###"
                                cell_sum_col5.alignment = Alignment(
                                    horizontal='center')
                                if (Opcion == 34 and SubOpcion == 0):
                                    cell_sum_col6 = sheet[
                                        f'{start_column_col6}{start_row_col + len(datos) + 1}']
                                    cell_sum_col6.value = sum_col6
                                    cell_sum_col6.font = Font(bold=True)
                                    cell_sum_col6.number_format = "#,###"
                                    cell_sum_col6.alignment = Alignment(
                                        horizontal='center')
                            elif Opcion == 8:
                                cell_sum_col3 = sheet[
                                    f'{start_column_col3}{start_row_col + len(datos) + 1}']
                                cell_sum_col3.value = sum_col3
                                cell_sum_col3.font = Font(bold=True)
                                cell_sum_col3.number_format = "#,###"
                                cell_sum_col3.alignment = Alignment(
                                    horizontal='center')

                                cell_sum_col4 = sheet[
                                    f'{start_column_col4}{start_row_col + len(datos) + 1}']
                                cell_sum_col4.value = sum_col4
                                cell_sum_col4.font = Font(bold=True)
                                cell_sum_col4.number_format = "#,###"
                                cell_sum_col4.alignment = Alignment(
                                    horizontal='center')

                                cell_sum_col7 = sheet[
                                    f'{start_column_col7}{start_row_col + len(datos) + 1}']
                                cell_sum_col7.value = sum_col7
                                cell_sum_col7.font = Font(bold=True)
                                cell_sum_col7.number_format = "#,###"
                                cell_sum_col7.alignment = Alignment(
                                    horizontal='center')

                                cell_sum_col8 = sheet[
                                    f'{start_column_col8}{start_row_col + len(datos) + 1}']
                                cell_sum_col8.value = sum_col8
                                cell_sum_col8.font = Font(bold=True)
                                cell_sum_col8.number_format = "#,###"
                                cell_sum_col8.alignment = Alignment(
                                    horizontal='center')

                                cell_sum_col9 = sheet[
                                    f'{start_column_col9}{start_row_col + len(datos) + 1}']
                                cell_sum_col9.value = sum_col9
                                cell_sum_col9.font = Font(bold=True)
                                cell_sum_col9.number_format = "#,###"
                                cell_sum_col9.alignment = Alignment(
                                    horizontal='center')

                                cell_sum_col10 = sheet[
                                    f'{start_column_col10}{start_row_col + len(datos) + 1}']
                                cell_sum_col10.value = sum_col10
                                cell_sum_col10.font = Font(bold=True)
                                cell_sum_col10.number_format = "#,###"
                                cell_sum_col10.alignment = Alignment(
                                    horizontal='center')

                            elif Opcion == 14:
                                cell_sum_col7 = sheet[
                                    f'{start_column_col7}{start_row_col + len(datos) + 1}']
                                cell_sum_col7.value = sum_col7
                                cell_sum_col7.font = Font(bold=True)
                                cell_sum_col7.number_format = "#,###"
                                cell_sum_col7.alignment = Alignment(
                                    horizontal='center')

                            elif Opcion == 28:
                                cell_sum_col7 = sheet[
                                    f'{start_column_col7}{start_row_col + len(datos) + 1}']
                                cell_sum_col7.value = sum_col7
                                cell_sum_col7.font = Font(bold=True)
                                cell_sum_col7.number_format = "#,###"
                                cell_sum_col7.alignment = Alignment(
                                    horizontal='center')

                                cell_sum_col8 = sheet[
                                    f'{start_column_col8}{start_row_col + len(datos) + 1}']
                                cell_sum_col8.value = sum_col8
                                cell_sum_col8.font = Font(bold=True)
                                cell_sum_col8.number_format = "#,###"
                                cell_sum_col8.alignment = Alignment(
                                    horizontal='center')

                                cell_sum_col9 = sheet[
                                    f'{start_column_col9}{start_row_col + len(datos) + 1}']
                                cell_sum_col9.value = sum_col9
                                cell_sum_col9.font = Font(bold=True)
                                cell_sum_col9.number_format = "#,###"
                                cell_sum_col9.alignment = Alignment(
                                    horizontal='center')

                            elif Opcion == 33 and SubOpcion == 1:
                                cell_sum_col8 = sheet[
                                    f'{start_column_col8}{start_row_col + len(datos) + 1}']
                                cell_sum_col8.value = sum_col8
                                cell_sum_col8.font = Font(bold=True)
                                cell_sum_col8.number_format = "#,###"
                                cell_sum_col8.alignment = Alignment(
                                    horizontal='center')

                            # Escribir "Totales" en negrita
                            if Opcion != 12 and Opcion != 99:
                                cell_totals = sheet[
                                    f'{start_column_col1}{start_row_col + len(datos) + 1}']
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
                response['Content-Disposition'] = 'attachment; filename=Comercial.xlsx'

                return response
            else:
                return JsonResponse({'error': 'El archivo de la plantilla no fue encontrado'})

        else:
            return JsonResponse({'error': 'Se esperaba una solicitud POST'})

    else:
        return JsonResponse({'error': 'Se esperaba una solicitud POST'})
