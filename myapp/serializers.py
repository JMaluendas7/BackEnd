from rest_framework import serializers
from .models import TipoDocumento, Empresas, Roles, Cargos, Colaboradores, Login, Modulos, Permisos


class TipoDocumentoSlr(serializers.ModelSerializer):
    class Meta:
        model = TipoDocumento
        fields = serializers.ALL_FIELDS


class EmpresasSlr(serializers.ModelSerializer):
    class Meta:
        model = Empresas
        fields = serializers.ALL_FIELDS


class RolesSlr(serializers.ModelSerializer):
    class Meta:
        model = Roles
        fields = serializers.ALL_FIELDS


class CargosSlr(serializers.ModelSerializer):
    class Meta:
        model = Cargos
        fields = serializers.ALL_FIELDS


class ColaboradoresSlr(serializers.ModelSerializer):
    class Meta:
        model = Colaboradores
        fields = serializers.ALL_FIELDS


class LoginSlr(serializers.ModelSerializer):
    class Meta:
        model = Login
        fields = serializers.ALL_FIELDS


class ModulosSlr(serializers.ModelSerializer):
    class Meta:
        model = Modulos
        fields = serializers.ALL_FIELDS


class PermisosSlr(serializers.ModelSerializer):
    class Meta:
        model = Permisos
        fields = serializers.ALL_FIELDS
