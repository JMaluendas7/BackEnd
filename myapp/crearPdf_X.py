from xhtml2pdf import pisa


def convert_html_to_pdf(html_file, output_pdf):
    with open(html_file, 'r', encoding='utf-8') as f:
        source_html = f.read()

    result_file = open(output_pdf, "w+b")

    pisa.CreatePDF(
        source_html,
        dest=result_file,
        encoding='utf-8'
    )

    result_file.close()


convert_html_to_pdf('formato_berli.html', 'output.pdf')
