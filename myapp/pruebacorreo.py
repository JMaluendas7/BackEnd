from email.message import EmailMessage
import smtplib

remitente = "jmaluendasbautista@gmail.com"
destinatario = "jmaluendase@gmail.com"
mensaje = "¡Hola, mundo!"
email = EmailMessage()
email["From"] = remitente
email["To"] = destinatario
email["Subject"] = "Correo de prueba"
email.set_content(mensaje)
smtp = smtplib.SMTP_SSL("smtp.gmail.com")
smtp.login(remitente, "sdcruneulqpcroht")
smtp.sendmail(remitente, destinatario, email.as_string())
smtp.quit()
