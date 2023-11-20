
import pyodbc
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


# Función para enviar correo electrónico
def send_email(identificacion, nombre, apellido, correo):
    # Configurar el correo electrónico
    email_origen = "jmaluendase@gmail.com"
    email_destino = 'jmaluendasbautista@gmail.com'
    ruta_img = "https://saas-cms-admin-sandbox.s3.us-west-2.amazonaws.com/sites/647e59513d04a300028afa72/assets/647e59b33d04a300028afa77/Logo_berlinas_blanco_fondo-transparente_DIGITAL.png"
    ruta_img2 = "http://gestor.berlinasdelfonce.com/img/iconlogobus.83dc07f2.png"

    message = MIMEMultipart()
    message["From"] = email_origen
    message["To"] = email_destino
    message["Subject"] = "Portal Propietarios - Envio Link de tutoriales"

    body = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Portal Propietarios - Envio Link de tutoriales</title>
        </head>
        <body style="font-family: Arial, sans-serif;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ccc; border-radius: 10px; background-color: #fff; box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.1);">
                <div style="display: flex; justify-content: space-around; background-color: #009944; height: auto; width: 100%; border-bottom-left-radius: 1rem; border-bottom-right-radius: 1rem;">
                    <img src={ruta_img} alt="Logo de la empresa" style="max-width: 150px; display: block; ">
                    <img src={ruta_img} alt="Logo de la empresa" style="max-width: 150px; display: block; ">
                </div>
                <div style="margin-top: 20px; line-height: 1.6;">
                    <p>Estimado/a {nombre} {apellido},</p>
                    <p>Esperamos que este mensaje le encuentre bien. En Berlinas del Fonce S.A., nos complace presentarle nuestros video tutoriales diseñados especialmente para quienes hacen uso de nuestro sistema de información, el Portal de Propietarios.</p>
                    <p>Estos tutoriales están diseñados específicamente para guiarle a través de las diversas funciones del Portal. Desde cómo acceder al sistema hasta la consulta de extractos, análisis detallado de las estadísticas de sus buses y la descarga de certificados cruciales para su gestión, estos recursos están creados para brindarle la orientación necesaria en cada paso.</p>
                    <p>Puede acceder a los video tutoriales siguiendo este <a style="text-decoration: none; color: #4caf50;" href="https://drive.google.com/file/d/1NwbuLAv6IUCQgiXwTFZIdSg-Ujxh467M/view">enlace</a>, donde encontrará información detallada sobre cómo aprovechar al máximo las funcionalidades que el sistema Portal tiene para usted.</p>
                    <p>Si tiene alguna pregunta o necesita asistencia adicional, no dude en ponerse en contacto con nuestro equipo de soporte técnico al </a><br>Teléfono: <a style="text-decoration: none;" href="https://api.whatsapp.com/send?phone=+573168756931">3168756931</a> o <a style="text-decoration: none;" href="mailto:asistemas@berlinasdelfonce.com">asistemas@berlinasdelfonce.com</a>.</p>

                    <hr style="border: 0; border-top: 1px solid #ccc; margin: 20px 0;">
                    <p style="color: #333;"><strong>Cordialmente,</strong></p>
                    <p>Jorge Eliecer Maluendas Bautista<br>Programador de Sistemas<br><a style="text-decoration: none; color: #000;" href="mailto:asistemas@berlinasdelfonce.com">asistemas@berlinasdelfonce.com</a><br>Teléfono: <a style="text-decoration: none; color: #000;" href="https://api.whatsapp.com/send?phone=+573168756931">3168756931</a><br>Cra. 68D No. 15 – 15<br>Bogotá D.C. - Colombia</p>
                </div>
                <div style="margin-top: 30px; font-style: italic; font-size:10px; color: #888;">
                    <p>Berlinas del Fonce S.A.</p>
                </div>
            </div>
        </body>
        </html>
    """
    # Sustituir los placeholders {nombre} y {apellido} en el cuerpo del correo
    body = body.replace("{nombre}", nombre)
    body = body.replace("{apellido}", apellido)

    message.attach(MIMEText(body, "html"))

    # Conexión SMTP y enviar el correo electrónico
    context = ssl.create_default_context()
    smtp_host = 'sandbox.smtp.mailtrap.io'
    smtp_port = 2525

    # Configurar el mensaje y el servidor SMTP
    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.starttls(context=context)
        server.login('9b86b787587574', 'b087222934202f')
        server.send_message(message)
    print(f"Correo enviado a {email_destino}")


# Parámetros de conexión a la base de datos
server = '172.16.0.25'
database = 'DynamiX'
username = 'developer'
password = '123456'

# Conectarse a la base de datos y ejecutar la consulta SQL
conn = pyodbc.connect('DRIVER={SQL Server};SERVER=' + server +
                      ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
cursor = conn.cursor()

query = """
WITH CTE AS (
    SELECT bus, documento1, nombre1, ROW_NUMBER() OVER (PARTITION BY documento1 ORDER BY nombre1) AS RowNum
    FROM PAS_PRODUCIDOSFIRMAS
    WHERE (year = 2023) AND (mes = 10)
)

SELECT TP_PROPIETARIOS.identificacion, TP_PROPIETARIOS.nombre, TP_PROPIETARIOS.apellido, TP_PROPIETARIOS.correo
FROM CTE
JOIN gestor.dbo.TP_PROPIETARIOS ON CTE.documento1 = TP_PROPIETARIOS.identificacion
WHERE CTE.RowNum = 1 AND TP_PROPIETARIOS.estado = 'True' AND TP_PROPIETARIOS.correo IS NOT NULL
ORDER BY TP_PROPIETARIOS.nombre;
"""
cursor.execute(query)
for row in cursor.fetchall():
    send_email(row.identificacion, row.nombre, row.apellido, row.correo)

cursor.close()
conn.close()
