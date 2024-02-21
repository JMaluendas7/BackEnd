# 5Apps BackEnd

## Introducción

5Apps es un aplicativo de reportes para el área administrativa y operativa de la empresa. Hasta el momento, consulta información en la base de datos y genera reportes en Excel y PDF, los cuales son archivos necesarios para las estadísticas y operatividad de la empresa. Un documento importante es el FUEC (Formato Único de Entrega y Control), ya que todo vehículo al salir debe llevarlo impreso, por lo cual se debe tener como prioridad y no detener su generación.

El BackEnd de 5Apps tiene ap

## Tabla de Contenidos

- [Instalación](#instalación)
- [Uso](#uso)
- [Contribución](#contribución)
- [Licencia](#licencia)

## Instalación

El ambiente de desarrollo de 5Apps se debe guardar en una carpeta (`5Apps`).

1. Desde la consola de Git Bash, accede a la carpeta `5Apps` identificate y clona el repositorio con las siguientes instrucciónes:
   ```bash
   git config --global user.name "Nombre"
   git config --global user.email "correo@dominio.com"
   git clone https://github.com/JMaluendas7/BackEnd.git
2. Acceder a la carpeta BackEnd en la cual queda alojado el proyecto clonado.
   ```bash
   cd BackEnd
3. Crear el entorno virtual
   ```bash
   virtualenv venv
4. Activacion del entorno virtual
   ```bash
   venv\Scripts\activate
5. Intalamos todas las librerias que requiere el proyecto.
   ```bash
   pip install -r requirements.txt
6. Despleglamos el BackEnd.
   ```bash
   python manage.py runserver 0.0.0.0:9000

## Uso

5Apps actualmente cuenta con generacion de reportes para el area administrativa y operativa del grupo empresarial de Berlinas.

## Contribucion

¡Para contribuir a mejorar 5Apps! Si tienes ideas para nuevas características, mejoras en el código o soluciones para problemas, Simplemente sigue estos pasos:

Haz un fork del repositorio.
1. Crea una nueva rama
   ```bash
   git checkout -b feature/mejora
2. Realiza tus cambios y haz commit de ellos.
   ```bash
   git commit -am 'Añade una mejora'
4. Sube tus cambios a la rama.
   ```bash
   git push origin feature/mejora
Abre un pull request.

## Licencia

© Transporte y Turismo Berlinas del Fonce - JMaluendas 2024. Todos los derechos reservados.
