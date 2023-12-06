# import os
# import pdfkit
# import jinja2

# # Obtener y mostrar la ubicación actual de trabajo
# current_directory = os.getcwd()
# print("La ubicación actual de trabajo es:", current_directory)

# # Configuración con la ruta predeterminada de wkhtmltopdf
# config = pdfkit.configuration(wkhtmltopdf='C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe')

# output_pdf = "salida.pdf"

# # Cargar el archivo HTML desde el directorio actual
# html_file_name = 'formato_berli.html'
# html_file_path = os.path.join(current_directory, html_file_name)
# print(html_file_path)

# # Renderizar la plantilla HTML con Jinja2
# with open(html_file_path, 'r', encoding='utf-8') as file:
#     template = jinja2.Template(file.read())
#     rendered_html = template.render()
# # Generar el PDF a partir del HTML renderizado
# options = {
#     'no-images': None,
#     'quiet': '',
#     'disable-local-file-access': None
# }
# # Generar el PDF a partir del HTML renderizado
# try:
#     pdfkit.from_file(html_file_path, output_pdf, configuration=config, options=options)
#     # pdfkit.from_string(rendered_html, output_pdf, configuration=config, options=options)
# except Exception as e:
#     print("Error al generar el PDF:", e)


import pdfkit

# Configuración con la ruta predeterminada de wkhtmltopdf
config = pdfkit.configuration(wkhtmltopdf='C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe')  # Reemplaza con tu ruta correcta

output_pdf = "salida.pdf"

# URL de la página web que deseas convertir
url = "https://www.google.com"

# Generar el PDF a partir de la página web
pdfkit.from_url(url, output_pdf, configuration=config)
