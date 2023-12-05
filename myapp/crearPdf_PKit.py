import pdfkit

config = pdfkit.configuration(
    wkhtmltopdf='C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe')
html_file_path = "formato_berli.html"
output_pdf = "salida.pdf"

pdfkit.from_file(html_file_path, output_pdf, configuration=config)
