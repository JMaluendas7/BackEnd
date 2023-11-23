from rest_framework import routers
from django.urls import path, include
from django.contrib.auth.views import LoginView as login_view
from django.urls import path
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)
from django.contrib.auth import views as auth_views
from djoser import views as djoser_views

from . import api
from . import views
from django.conf import settings
from django.conf.urls.static import static

router = routers.DefaultRouter()
router.register('docsti', api.TipoDocumentoViewSet, "TipoDocumento")
router.register('bussines', api.EmpresasViewSet, "Empresas")
router.register('rol', api.RolesViewSet, "Roles")
router.register('contrato', api.ContratosViewSet, "Contratos")
router.register('users', api.ColaboradoresViewSet, "Colaboradores")
router.register('login', api.LoginViewSet, "Login")
router.register('Modulos', api.ModulosViewSet, "Modulos")
router.register('permisos', api.PermisosViewSet, "Permisos")

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='Inicio de sesion'),
    path('api/', include(router.urls)),
    #     path('', views.index, name='Login'),
    #     path('salir/', views.salir, name='salir'),
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
    path('reset_password/',
         views.ResetPass.as_view({'post': 'send_reset_email'}), name='send_reset_email'),
     path('subir_foto/', views.subir_foto, name='subir_foto'),
    #     path('reset_password/<uidb64>/<token>/',
    #          views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    #     path('api/reset_password/', views.reset_password_request,
    #          name='reset_password_request'),

    #     path('password/reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    #     path('password/reset/confirm/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
