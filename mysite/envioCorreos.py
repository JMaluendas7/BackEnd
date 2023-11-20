import smtplib
import ssl
import datetime

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.template.loader import render_to_string
from settings import EMAIL_HOST, EMAIL_PORT, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD


def send_email(option, description):
    email_origen = "jmaluendase@gmail.com"
    email_destino = "jmaluendasbautista@gmail.com"

    dia_envio = datetime.datetime.now()
    # dia_envio = datetime.datetime.now() - datetime.timedelta(days=5) Resta de fecha en dias
    dia_registro = dia_envio.strftime("%d-%m-%Y")

    # Carga del contenido del template HTML
    html_content = render_to_string(
        'templates/email.html', {'dia_registro': dia_registro})

    # Configurar el correo electrónico
    message = MIMEMultipart()
    message["From"] = email_origen
    message["To"] = email_destino
    message["Subject"] = "Prueba de envio de correo"

    # Configurar el correo electrónico
    message = MIMEMultipart()
    message["From"] = email_origen
    message["To"] = email_destino
    message["Subject"] = "Prueba de envio de correo"

    # Adjuntar el contenido HTML al mensaje
    message.attach(MIMEText(html_content, "html"))

    context = ssl.create_default_context()

    # Reemplazar los datos de configuración por las variables del settings.py
    smtp_host = EMAIL_HOST
    smtp_port = EMAIL_PORT

    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.starttls(context=context)
        server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
        server.send_message(message)

    print("Mensaje enviado")

    # # Establecer la conexión SMTP y enviar el correo electrónico
    # context = ssl.create_default_context()
    # smtp_host = "mail.berlinasdelfonce.com"
    # smtp_port = 465
    # with smtplib.SMTP_SSL(smtp_host, smtp_port, context=context) as server:
    #     server.login(email_origen, password)
    #     server.send_message(message)
    return True


if __name__ == "__main__":
    send_email("opcion", "descripcion")
