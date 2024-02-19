
import pyodbc
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from AdminDBUtilsConn import ConexionDB


def send_email(identificacion, nombre, apellido, correo):

    # Configurar el correo electrónico
    email_origen = "asistemas@berlinasdelfonce.com"
    email_destino = correo
    ruta_img = "https://saas-cms-admin-sandbox.s3.us-west-2.amazonaws.com/sites/647e59513d04a300028afa72/assets/647e59b33d04a300028afa77/Logo_berlinas_blanco_fondo-transparente_DIGITAL.png"

    message = MIMEMultipart()
    message["From"] = email_origen
    message["To"] = email_destino
    message["Subject"] = "Portal Propietarios - Complemento de videotutoriales"

    body = f"""
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <title>Portal Propietarios - Envio Link de tutoriales</title>
        </head>
        <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px;">
            <div style="max-width: 700px; margin: 0 auto; padding: 20px; border: 1px solid #ccc; border-radius: 10px; background-color: #fff; box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.1);">
                <div style="text-align: center; background-color: #009944; border-radius: 10px;">
                    <img src="{ruta_img}" alt="Logo de la empresa" style="max-width: 150px; display: block; margin: 20px auto;">
                </div>
                <div style="margin-top: 20px; line-height: 1.6; color: #000;">
                    <p>Estimado(a) propietario(a) {nombre} {apellido},</p>
                    <p color: #000 !important;>Reciba un cordial saludo de Berlinas del Fonce S.A., Queremos complementar el correo que enviamos ayer, ya que hemos ampliado la variedad de videotutoriales, detallando cada una de las funcionalidades que ofrece nuestro Portal de Propietarios.</p>
                    <p color: #000 !important;>Acceda al portal a través del siguiente enlace: <a style="text-decoration: none; color: #4caf50;" href="gestor.berlinasdelfonce.com">gestor.berlinasdelfonce.com</a> con el usuario {identificacion}</p>
                    <p color: #000 !important;>Ingreso, Consulta y Descargas:
                    <a style="text-decoration: none; color: #4caf50;" href="https://drive.google.com/file/d/1NwbuLAv6IUCQgiXwTFZIdSg-Ujxh467M/view?usp=sharing">Ver Video</a><br>

                    Análisis Gráfico de Información:
                    <a style="text-decoration: none; color: #4caf50;" href="https://drive.google.com/file/d/1vqNq6L1DAMTQwlRXORve8HNlenJFoSR3/view?usp=sharing">Ver Video</a><br>

                    Procedimiento para Escalar PQR:
                    <a style="text-decoration: none; color: #4caf50;" href="https://drive.google.com/file/d/1tu4NZB6ues47SDn6TgvEYIBNzSxtlX5y/view?usp=sharing">Ver Video</a><br>
                    
                    <p color: #000 !important;>Además, si al digitar su número de documento no encuentra su información de contacto para el envío del token, por favor, comuníquese a las siguientes líneas para suministrar sus datos actualizados:<br>
                    318 7717171: Producidos Berlinas<br>
                    316 5265129: Producidos Colibertador</p>
                    <p color: #000 !important;>Para informar cualquier fallo o error en la plataforma, puede comunicarse al siguiente contacto <a style="text-decoration: none; color: #4caf50;" href="https://api.whatsapp.com/send?phone=+573168756931">3168756931</a> o escribiendo al correo <a style="text-decoration: none; color: #4caf50;" href="mailto:asistemas@berlinasdelfonce.com">asistemas@berlinasdelfonce.com</a>.</p>
                    <hr style="border: 0; border-top: 1px solid #ccc; margin: 20px 0;">
                    <p style="color: #009944;"><strong>Cordialmente,</strong></p>
                    <p color: #000 !important;>Jorge Eliecer Maluendas Bautista<br>Programador de Sistemas<br><a style="text-decoration: none; color: #009944;" href="mailto:asistemas@berlinasdelfonce.com">asistemas@berlinasdelfonce.com</a><br>Teléfono: <a style="text-decoration: none; color: #009944;" href="https://api.whatsapp.com/send?phone=+573168756931">3168756931</a><br>Cra. 68D No. 15 – 15<br>Bogotá D.C. - Colombia</p>
                </div>
                <div style="margin-top: 30px; font-style: italic; font-size: 10px; color: #888; text-align: center;">
                    <p>Berlinas del Fonce S.A.</p>
                </div>
            </div>
        </body>
        </html>
    """

    message.attach(MIMEText(body, "html"))

    try:
        smtp = smtplib.SMTP_SSL("mail.berlinasdelfonce.com")
        smtp.login(email_origen, "PRUEBA2023")
        smtp.sendmail(email_origen, email_destino, message.as_string())
        smtp.quit()
        print(f"Correo Enviado a {correo}")
    except Exception as e:
        print(f"No se pudo enviar el correo a {correo} {str(e)}")


# Conectarse a la base de datos y ejecutar la consulta SQL
conn = ConexionDB()
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
