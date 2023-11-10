from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from django.http import JsonResponse
from .models import Colaboradores, Permisos, Login, TipoDocumento, Roles, Empresas

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.hashers import make_password

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework import status
import json
import jwt

# Create your Views here.


# @login_required
# def index(request):
#     return (render(request, 'home.html'))


def salir(request):
    logout(request)
    return redirect('/')

class LoginView(APIView):
    def post(self, request):
        user = authenticate(username=request.data["username"], password=request.data["password"])
        if user:         # Genera un JWT
            payload = {"user_id": user.colaborador_id,
                       "username": user.username,
                       "nombre": user.first_name,
                       "apellido": user.last_name}
            token = jwt.encode(payload, 'your-secret-key', algorithm='HS256')
            return Response({"token": token, "username": user.username, "nombre": user.first_name, "apellido": user.last_name})
        else:
            return Response({"error": "Credenciales inválidas"}, status=400)
        

class ColaboradoresView(ViewSet):
    @login_required
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
    @login_required
    @action(detail=True, methods=['POST'])
    def post(self, request, format=None):
        tipo_documento = request.POST.get('tipo_documento')
        num_documento = request.POST.get('numDocumento')
        nombres = request.POST.get('nombre')
        apellidos = request.POST.get('apellido')
        email = request.POST.get('email')
        direccion = request.POST.get('direccion')
        ciudad = request.POST.get('ciudad')
        telefono = request.POST.get('telefono')
        contrato_id = request.POST.get('contrato_id')
        empresa_id = request.POST.get('empresa_id')
        empresa_id = Empresas.objects.get(id_empresa=empresa_id)
        rol_id = request.POST.get('rol_id')
        tipo_documento_id = TipoDocumento.objects.get(
            id_tipodocumento=tipo_documento)
        id_rol = Roles.objects.get(id_rol=rol_id)
        Colaboradores.objects.create(num_documento=num_documento, nombres=nombres, apellidos=apellidos, telefono=telefono, direccion=direccion, email=email,
                                     contrato_id=contrato_id, ciudad=ciudad, tipo_documento_id=tipo_documento_id, rol_id=id_rol, empresa_id=empresa_id)
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
            # colaborador.contrato_id = data_to_update.get(
            #     'contrato_id', colaborador.contrato_id)
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
                             last_name=last_name, email=email, is_staff=True, is_active=True, colaborador_id=id_user)
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
                        'nom_modulo': sub_mod.nom_modulo,
                        'link': sub_mod.link,
                    })

                mod = modulo.modulo_id
                data_menu.append({
                    'id_modulo': mod.id_modulo,
                    'nom_modulo': mod.nom_modulo,
                    'url_img': mod.url_img,
                    'isOpen': False,
                    'subItems': data_sub_menu,
                })

            return Response(data_menu)

        except Exception as e:
            print(str(e))
            return Response({'error': 'Ocurrió un error en el servidor'}, status=500)
