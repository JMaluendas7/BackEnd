from rest_framework import routers
from django.urls import path, include
from django.urls import path
from . import api
from . import views
from . import view_rf
from django.conf import settings
from django.conf.urls.static import static
from django.views.decorators.csrf import csrf_exempt

router = routers.DefaultRouter()
router.register('docsti', api.TipoDocumentoViewSet, "TipoDocumento")
router.register('bussines', api.EmpresasViewSet, "Empresas")
router.register('rol', api.RolesViewSet, "Roles")
router.register('cargos', api.CargosViewSet, "Cargos")
router.register('users', api.ColaboradoresViewSet, "Colaboradores")
router.register('login', api.LoginViewSet, "Login")
router.register('Modulos', api.ModulosViewSet, "Modulos")
router.register('permisos', api.PermisosViewSet, "Permisos")

urlpatterns = [
    path('api/', include(router.urls)),
    path('login/', views.LoginView.as_view(), name='Inicio de sesion'),
    # Crud Colaboradores
    path('colaboradores/',
         views.ColaboradoresView.as_view({'get': 'get'}), name='Lista de Colaboradores'),
    path('addColaboradores/',
         views.ColaboradoresView.as_view({'post': 'post'}), name='Registro de Colaboradores'),
    path('colaboradoresput/<id>/',
         views.ColaboradoresView.as_view({'put': 'put'}), name="Editar Colaborador"),
    path('colaboradoresdel/<id>/', views.ColaboradoresView.as_view(
        {'delete': 'delete'}), name="Eliminar Colaborador"),
    # Crud Usuarios
    path('addUsers/', views.UsersView.as_view({'post': 'post'}),
         name='Registro de Usuarios que se logean'),
    # Lectura de menu
    path('menu/<rol>/',
         views.MenuView.as_view({'get': 'get'}), name='Lista Menu'),
    # Cambio de contraseña con correo de verificacion
    path('reset_password/',
         views.ResetPass.as_view({'post': 'send_reset_email'}), name='send_reset_email'),
    path('reset_password/change/',
         views.ResetPass.as_view({'post': 'new_pass'}), name='change pass'),
    path('subir_foto/',
         views.subir_foto, name='subir_foto'),
    path('subir_ft/',
         csrf_exempt(view_rf.reconocimiento_facial), name='subir_ft'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
