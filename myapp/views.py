from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from .models import Colaboradores, Permisos, Login, TipoDocumento, Roles, Empresas, Token, Cargos
from django.contrib.auth import authenticate, logout
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods
import jwt


import hashlib
import base64
from django.utils import timezone

# En views.py
from .envioCorreos import send_email
import secrets
import string
import os


def subir_foto(request):
    imagen = request.FILES['imagen']
    destination = os.path.join('static', imagen.name)

    # Guardar la imagen en una carpeta específica
    with open(destination, 'wb+') as destination_file:
        for chunk in imagen.chunks():
            destination.write(chunk)

    # Aquí podrías guardar la ruta de la imagen en la base de datos si es necesario

    return JsonResponse({'mensaje': 'Imagen subida correctamente'})


def generate_token():
    characters = string.ascii_uppercase + string.digits
    token = ''.join(secrets.choice(characters) for i in range(6))
    return token


def generate_uidb64(num_documento):
    user = Login.objects.get(documento_num=num_documento)
    print(user.last_name)
    user_id_str = str(user.documento_num.num_documento)
    timestamp = str(int(timezone.now().timestamp()))
    num_documento = str(user.documento_num.num_documento)
    data_to_hash = f"{user_id_str}{timestamp}{num_documento}"
    # Crear el hash unico
    hash_object = hashlib.sha256(data_to_hash.encode())
    uidb64 = base64.urlsafe_b64encode(
        hash_object.digest()).decode().replace('=', '')
    return uidb64


@method_decorator(csrf_exempt, name='dispatch')
class ResetPass(ViewSet):
    def send_reset_email(self, request):
        email = request.data["email"]
        dni = request.data["dni"]
        print(email, dni)
        user = Login.objects.get(email=email, documento_num=dni)
        if user:
            token = generate_token()
            first_name = user.first_name
            last_name = user.last_name
            uidb64 = generate_uidb64(user.documento_num)
            send_email(email, first_name, last_name, uidb64, token)
            Token.objects.create(
                token=token, documento_num=dni, documento_num_cryp=uidb64)
            return Response({'message': 'EMail enviado'})

    def new_pass(self, request):
        uidb64 = request.data["uidb64"]
        token = request.data["token"]
        password = request.data["password"]
        password2 = request.data["password2"]
        tok = Token.objects.get(
            token=token, documento_num_cryp=uidb64, vencido=False)
        if tok:
            user = Login.objects.get(documento_num=tok.documento_num)
            make_pass = make_password(password)
            user.password = make_pass
            user.save()
            tok.vencido = True
            tok.save()
            return JsonResponse({'message': 'Contraseña cambiada con éxito'})
        return JsonResponse({'error': 'Hubo un problema al cambiar la contraseña'}, status=500)


class LoginView(APIView):
    # Vista para el inicio de sesion con Face Id
    def post(self, request):
        user = authenticate(
            username=request.data["username"], password=request.data["password"])
        if user:
            payload = {"username": user.username,
                       "nombre": user.first_name,
                       "apellido": user.last_name,
                       "rol_id": user.documento_num.rol_id.id_rol}
            token = jwt.encode(payload, 'your-secret-key',
                               algorithm='HS256')  # Genera un JWT

            return Response({"token": token,
                             "num_documento": user.documento_num.num_documento,
                             "username": user.username,
                             "nombre": user.first_name,
                             "apellido": user.last_name,
                             "rol_id": user.documento_num.rol_id.id_rol,
                             "message": user.first_name + " has iniciado sesion"
                             })
        else:
            return Response({"message": "Credenciales inválidas"}, status=400)


class LoginFaceView(APIView):
    def postFace(self, request):
        documento_num = request.data["documento_num"]
        user = Login.objects.get(documento_num=documento_num)
        userLogin = authenticate(
            username=user.username, password=user.password)
        if userLogin:
            payload = {"username": user.username,
                       "nombre": user.first_name,
                       "apellido": user.last_name,
                       "rol_id": user.documento_num.rol_id.id_rol}
            token = jwt.encode(payload, 'your-secret-key',
                               algorithm='HS256')  # Genera un JWT

            return Response({"token": token,
                             "num_documento": user.documento_num.num_documento,
                             "username": user.username,
                             "nombre": user.first_name,
                             "apellido": user.last_name,
                             "rol_id": user.documento_num.rol_id.id_rol,
                             "message": user.first_name + " has iniciado sesion de manera facial"
                             })
        else:
            return Response({"message": "Credenciales inválidas"}, status=400)


class ColaboradoresView(ViewSet):
    @action(detail=False, methods=['GET'])
    def get(self, request, num_Documento=None):
        if num_Documento is None:
            usuarios = Colaboradores.objects.all()
            data = []
            for usuario in usuarios:
                tipo_doc = usuario.tipo_documento_id.nombreDoc
                rol_id = usuario.rol_id.detalle_rol
                data.append({
                    'num_documento': usuario.num_documento,
                    'nombres': usuario.nombres,
                    'apellidos': usuario.apellidos,
                    'telefono': usuario.telefono,
                    'direccion': usuario.direccion,
                    'email': usuario.email,
                    'cargo_id': usuario.cargo_id.detalle_cargo,
                    'rol_id': rol_id,
                    'ciudad': usuario.ciudad,
                    'empresa_id': usuario.empresa_id.nombre_empresa,
                    'fecha_registro': usuario.fecha_registro,
                })

        else:
            try:
                usuario = Colaboradores.objects.get(
                    num_documento=num_Documento)
                data = {'num_documento': usuario.num_documento,
                        'nombres': usuario.nombres, 'apellidos': usuario.apellidos}
            except Colaboradores.DoesNotExist:
                return JsonResponse({'error': 'Usuario no encontrado'}, status=404)

        return JsonResponse(data, safe=False)

    @action(detail=True, methods=['POST'])
    def post(self, request, id_permiso, rol_id, format=None):
        permiso = Permisos.objects.get(id_permiso=id_permiso, rol_id=rol_id)
        if permiso.permiso_insertar:
            tipo_documento = request.POST.get('tipo_documento')
            num_documento = request.POST.get('numDocumento')
            nombres = request.POST.get('nombre')
            apellidos = request.POST.get('apellido')
            email = request.POST.get('email')
            direccion = request.POST.get('direccion')
            ciudad = request.POST.get('ciudad')
            telefono = request.POST.get('telefono')
            cargo_id = request.POST.get('cargo_id')
            empresa_id = request.POST.get('empresa_id')
            empresa_id = Empresas.objects.get(id_empresa=empresa_id)
            rol_id = request.POST.get('rol_id')
            tipo_documento_id = TipoDocumento.objects.get(
                id_tipodocumento=tipo_documento)
            id_rol = Roles.objects.get(id_rol=rol_id)
            Colaboradores.objects.create(num_documento=num_documento, nombres=nombres, apellidos=apellidos, telefono=telefono, direccion=direccion, email=email,
                                         cargo_id=cargo_id, ciudad=ciudad, tipo_documento_id=tipo_documento_id, rol_id=id_rol, empresa_id=empresa_id)
            response_data = {'mensaje': 'Colaborador creado con éxito'}
            return JsonResponse(response_data)

    @action(detail=True, methods=['PUT'])
    def put(self, request, id):
        try:
            colaborador = Colaboradores.objects.get(num_documento=id)

            data_to_update = request.data
            print(data_to_update)
            colaborador.nombres = data_to_update.get(
                'nombres', colaborador.nombres)
            colaborador.apellidos = data_to_update.get(
                'apellidos', colaborador.apellidos)
            colaborador.telefono = data_to_update.get(
                'telefono', colaborador.telefono)
            colaborador.email = data_to_update.get('email', colaborador.email)
            # colaborador.cargo_id = data_to_update.get(
            #     'cargo_id', colaborador.cargo_id)
            colaborador.direccion = data_to_update.get(
                'direccion', colaborador.direccion)
            colaborador.ciudad = data_to_update.get(
                'ciudad', colaborador.ciudad)
            # colaborador.rol_id = data_to_update.get(
            #     'rol_id', colaborador.rol_id)
            # colaborador.empresa_id = data_to_update.get(
            #     'empresa_id', colaborador.empresa_id)

            colaborador.save()

            return Response("Colaborador actualizado exitosamente", status=status.HTTP_200_OK)
        except colaborador.DoesNotExist:
            return Response("Colaborador no encontrado", status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(f"Error al actualizar el colaborador: {str(e)}", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['DELETE'])
    def delete(self, request, id):
        try:
            usuario = Colaboradores.objects.get(num_documento=id)
            usuario.delete()
            response_data = {'mensaje': 'Colaborador eliminado con éxito'}

        except Colaboradores.DoesNotExist:
            return JsonResponse({'error': 'Colaborador no encontrado'}, status=404)

        return JsonResponse(response_data)


class UsersView(ViewSet):
    @action(detail=True, methods=['POST'])
    def post(self, request, format=None):
        id_user = request.POST.get('id_user')
        username = request.POST.get('usuario')
        contrasena = request.POST.get('contrasena')
        passs = make_password(contrasena)
        superuserValue = request.POST.get('superuser')
        superuser = superuserValue == 'on'
        colaborador = Colaboradores.objects.get(num_documento=id_user)
        first_name = colaborador.nombres
        last_name = colaborador.apellidos
        email = colaborador.email

        Login.objects.create(password=passs, is_superuser=superuser, username=username, first_name=first_name,
                             last_name=last_name, email=email, is_staff=True, is_active=True, documento_num=colaborador)
        response_data = {'mensaje': 'Colaborador creado con éxito'}
        return JsonResponse(response_data)


@method_decorator(csrf_exempt, name='dispatch')
class MenuView(ViewSet):
    @action(detail=False, methods=['GET'])
    @method_decorator(require_http_methods(["GET"]))
    def get(self, request, rol):
        try:
            raiz_modulos = Permisos.objects.filter(
                modulo_id__id_modulo_padre=None, rol_id__id_rol=rol)
            print(raiz_modulos)
            data_menu = []
            for modulo in raiz_modulos:
                print(modulo)
                submodulos = Permisos.objects.filter(
                    modulo_id__id_modulo_padre=modulo.modulo_id.id_modulo, rol_id__id_rol=rol)
                data_sub_menu = []
                for submodulo in submodulos:
                    sub_mod = submodulo.modulo_id
                    data_sub_menu.append({
                        'id_modulo': sub_mod.id_modulo,
                        'id_permiso': submodulo.id_permiso,
                        'nom_modulo': sub_mod.nom_modulo,
                        'link': sub_mod.link,
                        'url_img': sub_mod.url_img,
                        'insertar': submodulo.permiso_insertar,
                        'eliminar': submodulo.permiso_eliminar,
                        'actualizar': submodulo.permiso_actualizar,
                        'consultar': submodulo.permiso_consultar,
                        'reportes': submodulo.permiso_reportes,
                    })

                mod = modulo.modulo_id
                data_menu.append({
                    'id_modulo': mod.id_modulo,
                    'id_permiso': modulo.id_permiso,
                    'nom_modulo': mod.nom_modulo,
                    'url_img': mod.url_img,
                    'isOpen': False,

                    'subItems': data_sub_menu,

                })

            return Response(data_menu)

        except Exception as e:
            print(str(e))
            return Response({'error': 'Ocurrió un error en el servidor'}, status=500)
