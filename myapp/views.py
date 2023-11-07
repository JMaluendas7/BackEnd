from django.shortcuts import render
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from django.http import JsonResponse
from .models import Colaboradores, Permisos, Login, TipoDocumento
from .serializers import ColaboradoresSlr

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework import status
# Create your Views here.


# @login_required
# def index(request):
#     return (render(request, 'home.html'))


# def salir(request):
#     logout(request)
#     return redirect('/')


class ColaboradoresView(ViewSet):
    # @login_required
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
                    'tipo_doc': tipo_doc,
                    'telefono': usuario.telefono,
                    'direccion': usuario.telefono,
                    'email': usuario.email,
                    'rol_id': rol_id,
                    'ciudad': usuario.ciudad,
                    'departamento': usuario.departamento,
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
    def post(self, request, format=None):
        serializer = ColaboradoresSlr(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # num_DocumentoR = request.POST.get('numDocumento')
        # num_Documento = TipoDocumento.objects.get(id_tipodocumento=1)
        # nombres = request.POST.get('nombre')
        # apellidos = request.POST.get('apellido')
        # telefono = request.POST.get('telefono')
        # direccion = request.POST.get('direccion')
        # email = request.POST.get('email')
        # contrato_id = request.POST.get('contrato_id')
        # ciudad = request.POST.get('ciudad')
        # departamento = request.POST.get('departamento')
        # tipo_documento_id = request.POST.get('tipo_documento')
        # rol_id = request.POST.get('rol_id')
        # empresa_id = request.POST.get('empresa')
        # Colaboradores.objects.create(num_Documento=num_Documento, nombres=nombres, apellidos=apellidos, telefono=telefono, direccion=direccion, email=email,
        #                              contrato_id=contrato_id, ciudad=ciudad, departamento=departamento, tipo_documento_id=tipo_documento_id, rol_id=int(rol_id), empresa_id=int(empresa_id))
        # response_data = {'mensaje': 'Colaborador creado con éxito'}
        # return JsonResponse(response_data)

    @action(detail=True, methods=['PUT'])
    def put(self, request, num_Doc=1234):
        try:
            num_documento = request.POST.get('numDocumento')
            nombres = request.POST.get('nombres')
            apellidos = request.POST.get('apellidos')
            telefono = request.POST.get('telefono')
            direccion = request.POST.get('direccion')
            email = request.POST.get('email')
            contrato_id = request.POST.get('contrato_id')
            ciudad = request.POST.get('ciudad')
            departamento = request.POST.get('departamento')
            tipo_documento_id = request.POST.get('tipo_documento')
            rol_id = request.POST.get('rol_id')
            empresa_id = request.POST.get('empresa')
            Colaboradores.objects.filter(num_documento=num_Doc).update(num_documento=num_documento, nombres=nombres, apellidos=apellidos, telefono=telefono, direccion=direccion,
                                                                       email=email, contrato_id=contrato_id, ciudad=ciudad, departamento=departamento, tipo_documento_id=tipo_documento_id, rol_id=rol_id, empresa_id=empresa_id)
            response_data = {'mensaje': 'Colaborador actualizado con éxito'}
        except Colaboradores.DoesNotExist:
            return JsonResponse({'error': 'Colaborador no encontrado'}, status=404)

        return JsonResponse(response_data)

    @action(detail=True, methods=['DELETE'])
    def delete(self, request, num_Doc=1234):
        try:
            usuario = Colaboradores.objects.get(num_documento=num_Doc)
            usuario.delete()
            response_data = {'mensaje': 'Colaborador eliminado con éxito'}

        except Colaboradores.DoesNotExist:
            return JsonResponse({'error': 'Colaborador no encontrado'}, status=404)

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
