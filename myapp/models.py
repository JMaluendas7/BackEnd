from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission


class TipoDocumento(models.Model):
    id_tipoDocumento = models.AutoField(primary_key=True)
    nombreDoc = models.CharField(max_length=99, null=False)
    denominacion = models.CharField(max_length=5, null=False, unique=True)
    estado = models.BooleanField(default=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)


class Empresas(models.Model):
    id_empresa = models.AutoField(primary_key=True)
    nombre_empresa = models.CharField(max_length=150, null=False, unique=True)
    nit = models.CharField(max_length=12, null=False, unique=True)
    direccion = models.CharField(max_length=150)
    estado = models.BooleanField(default=True)
    telefono1 = models.PositiveIntegerField(null=False)
    telefono2 = models.PositiveIntegerField(null=True)
    email = models.EmailField(max_length=150, null=False)
    fecha_registro = models.DateTimeField(auto_now_add=True)


class Roles(models.Model):
    id_rol = models.SmallAutoField(primary_key=True)
    detalle_rol = models.CharField(max_length=100, null=False)
    empresa_id = models.ForeignKey(
        Empresas, on_delete=models.CASCADE)


class Contratos(models.Model):
    id_contrato = models.AutoField(primary_key=True)
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()


class Colaboradores(models.Model):
    id_colaborador = models.AutoField(primary_key=True),
    tipo_documento_id = models.ForeignKey(
        TipoDocumento, on_delete=models.CASCADE)
    num_documento = models.IntegerField(null=False, unique=True)
    nombres = models.CharField(max_length=99, null=False)
    apellidos = models.CharField(max_length=99, null=False)
    telefono = models.IntegerField(null=False)
    direccion = models.CharField(max_length=150, null=False)
    email = models.EmailField(max_length=150, null=False)
    rol_id = models.ForeignKey(Roles, on_delete=models.CASCADE)
    empresa_id = models.ForeignKey(
        Empresas, on_delete=models.CASCADE)
    contrato_id = models.IntegerField(unique=True)
    ciudad = models.CharField(max_length=100)
    departamento = models.CharField(max_length=100)
    fecha_registro = models.DateTimeField(auto_now_add=True)


class Login(AbstractUser):
    id_login = models.AutoField(primary_key=True)
    colaborador_id = models.IntegerField(default=7)
    groups = models.ManyToManyField(Group, related_name='logins', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='logins', blank=True)


class Modulos(models.Model):
    id_modulo = models.AutoField(primary_key=True)
    nom_modulo = models.CharField(max_length=150, null=False)
    id_modulo_padre = models.ForeignKey(
        'self', null=True, blank=True, related_name='submenus', on_delete=models.CASCADE)
    link = models.CharField(max_length=200, null=True)
    url_img = models.CharField(max_length=200, null=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)


class Permisos(models.Model):
    id_permiso = models.AutoField(primary_key=True)
    rol_id = models.ForeignKey(
        Roles, on_delete=models.CASCADE)
    modulo_id = models.ForeignKey(
        Modulos, on_delete=models.CASCADE)
    permiso_insertar = models.BooleanField(default=True)
    permiso_eliminar = models.BooleanField(default=True)
    permiso_actualizar = models.BooleanField(default=True)
    permiso_consultar = models.BooleanField(default=True)
    permiso_reportes = models.BooleanField(default=True)
    estado_permiso = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
