from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import render_to_string

# from weasyprint import HTML
# from weasyprint.fonts import FontConfiguration


def export_pdf():

    context = {}
    html = render_to_string("formato_berli2.html", context)

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = "inline; report.pdf"

    font_config = FontConfiguration()
    HTML(string=html).write_pdf(response, font_config=font_config)

    return response
