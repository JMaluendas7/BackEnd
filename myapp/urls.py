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

from . import api
from . import views

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
    #     path('reset_password/', PasswordResetView.as_view(), name='password_reset'),
    #     path('reset_password/done/', PasswordResetDoneView.as_view(),
    #          name='password_reset_done'),
    #     path('reset_password/<uidb64>/<token>/',
    #          PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    #     path('reset_password/complete/', PasswordResetCompleteView.as_view(),
    #          name='password_reset_complete'),
    path('reset_password/', views.PassResetView.as_view(), name='password_reset'),
    path('reset_password/<uidb64>/<token>/',
         views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('api/reset_password/', views.reset_password_request,
         name='reset_password_request'),
]
