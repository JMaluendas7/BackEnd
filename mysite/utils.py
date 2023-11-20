import os
import django
from django.conf import settings
import smtplib
import ssl
import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.template.loader import render_to_string

# Establecer la configuración de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
django.setup()


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

    # Adjuntar el contenido HTML al mensaje
    # message.attach(MIMEText(html_content, "html"))

    body = f"""
    <p>Prueba de envio de correo</p>
    <br/>
    Esta es una prueba<br/>
    <br/>
    Fecha de Prueba: {dia_registro}<br/>
    <br/>
    Cordialmente,<br/>
    <br/>
    Prueba<br/>
    Prueba<br/>
    <a href="mailto:prueba@prueba.com">prueba@prueba.com</a><br/>
    <a href="http://www.prueba.com">www.prueba.com</a><br/>
    Teléfono: (11-1) 111111 Ext 1111<br/>
    Oficina Principal: Cra Direccion Prueba<br/>
    00000-0000<br/>
    """

    message.attach(MIMEText(body, "html"))

    context = ssl.create_default_context()

    # Establecer la conexión SMTP y enviar el correo electrónico
    context = ssl.create_default_context()
    smtp_host = 'sandbox.smtp.mailtrap.io'
    smtp_port = 2525

    # Configurar el mensaje y el servidor SMTP
    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.starttls(context=context)
        server.login('f412691b9c0ac6', 'efb888accbe956')
        server.send_message(message)

    # Reemplazar los datos de configuración por las variables del settings.py
    # smtp_host = EMAIL_HOST
    # smtp_port = EMAIL_PORT

    # with smtplib.SMTP(smtp_host, smtp_port) as server:
    #     server.starttls(context=context)
    #     server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
    #     server.send_message(message)

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
