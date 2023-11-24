from rest_framework import viewsets, permissions
from .models import TipoDocumento, Empresas, Roles, Cargos, Colaboradores, Login, Modulos, Permisos
from .serializers import TipoDocumentoSlr, EmpresasSlr, RolesSlr, CargosSlr, ColaboradoresSlr, LoginSlr, ModulosSlr, PermisosSlr


class TipoDocumentoViewSet(viewsets.ModelViewSet):
    queryset = TipoDocumento.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = TipoDocumentoSlr


class EmpresasViewSet(viewsets.ModelViewSet):
    queryset = Empresas.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = EmpresasSlr


class RolesViewSet(viewsets.ModelViewSet):
    queryset = Roles.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = RolesSlr


class CargosViewSet(viewsets.ModelViewSet):
    queryset = Cargos.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = CargosSlr


class ColaboradoresViewSet(viewsets.ModelViewSet):
    queryset = Colaboradores.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = ColaboradoresSlr


class LoginViewSet(viewsets.ModelViewSet):
    queryset = Login.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = LoginSlr


class ModulosViewSet(viewsets.ModelViewSet):
    queryset = Modulos.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = ModulosSlr


class PermisosViewSet(viewsets.ModelViewSet):
    queryset = Permisos.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = PermisosSlr
