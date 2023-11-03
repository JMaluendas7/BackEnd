from rest_framework import routers
from django.urls import path, include
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
    path('api/', include(router.urls)),
    path('', views.index, name='Login'),
    path('salir/', views.salir, name='salir'),
    path('colaboradores/',
         views.ColaboradoresView.as_view({'get': 'get'}), name='Lista de Colaboradores'),
    path('menu/<rol>',
         views.MenuView.as_view({'get': 'get'}), name='Lista Menu'),
]
