from reportlab.pdfgen import canvas

# Crear un archivo PDF
output_pdf = "../docs/output_reportlab.pdf"

# Inicializar documento
pdf_canvas = canvas.Canvas(output_pdf)

# Agregar texto en psocision especifica (x, y)
pdf_canvas.drawString(
    100, 750, "Prueba de creacion de pdf con ReportLab version Open Source")

# Guardar el PDF generado
pdf_canvas.save()
