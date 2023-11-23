from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission


class TipoDocumento(models.Model):
    id_tipodocumento = models.AutoField(primary_key=True)
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
    telefono1 = models.IntegerField(null=False)
    telefono2 = models.IntegerField(null=True)
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
    num_documento = models.IntegerField(primary_key=True)
    tipo_documento_id = models.ForeignKey(
        TipoDocumento, on_delete=models.CASCADE)
    nombres = models.CharField(max_length=99, null=False)
    apellidos = models.CharField(max_length=99, null=False)
    telefono = models.IntegerField(null=False)
    direccion = models.CharField(max_length=150, null=False)
    email = models.EmailField(max_length=150, null=False)
    rol_id = models.ForeignKey(Roles, on_delete=models.CASCADE)
    empresa_id = models.ForeignKey(
        Empresas, on_delete=models.CASCADE)
    contrato_id = models.IntegerField(unique=True)
    ciudad = models.CharField(max_length=100, null=False)
    fecha_registro = models.DateTimeField(auto_now_add=True)


class Login(AbstractUser):
    documento_num = models.OneToOneField(
        Colaboradores, on_delete=models.CASCADE, primary_key=True)
    groups = models.ManyToManyField(Group, related_name='logins', blank=True)
    user_permissions = models.ManyToManyField(
        Permission, related_name='logins', blank=True)


class Token(models.Model):
    token = models.CharField(max_length=6, null=False)
    fecha = models.DateField(auto_now_add=True)
    hora = models.DateTimeField(auto_now_add=True)
    vencido = models.BooleanField(default=False)
    documento_num = models.IntegerField(null=False)
    documento_num_cryp = models.CharField(null=False, max_length=60)


class ImagenUsuario(models.Model):
    num_documento = models.ForeignKey(Login, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='imagenes_usuarios/')


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
