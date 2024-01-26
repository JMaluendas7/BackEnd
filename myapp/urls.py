from rest_framework import routers
from django.urls import path, include
from django.urls import path
from . import api, views, view_rf, view_rf_for
from . import crearExcel, rptoFuec, reportes, reporteAlcoholimetria, RptosOperaciones, RptosPlaneacion, RptosContabilidad, Pvu, Tiquetes, Dominicales, RptosConductores, RptosComercial, RptosMacarena, RptoHisFuec, RptosMigracion, RptosTaquillas
from . import RptosMicroseguros
from . import crearPdf_Wp
from django.conf import settings
from django.conf.urls.static import static
from django.views.decorators.csrf import csrf_exempt

router = routers.DefaultRouter()
router.register('rol', api.RolesViewSet, "Roles")
router.register('users', api.ColaboradoresViewSet, "Colaboradores")
router.register('login', api.LoginViewSet, "Login")
router.register('docsti', api.TipoDocumentoViewSet, "TipoDocumento")
router.register('Modulos', api.ModulosViewSet, "Modulos")
router.register('permisos', api.PermisosViewSet, "Permisos")
router.register('bussines', api.EmpresasViewSet, "Empresas")

urlpatterns = [
    path('api/', include(router.urls)),
    path('login/', views.LoginView.as_view(), name='Inicio de sesion'),
    path('loginface/', views.LoginFaceView.as_view(),
         name='Login con Face Id'),
    #     Crud Colaboradores
    path('colaboradores/',
         views.ColaboradoresView.as_view({'get': 'get'}), name='Lista de Colaboradores'),
    path('addColaboradores/<int:id_permiso>/<int:rol_id>/',
         views.ColaboradoresView.as_view({'post': 'post'}), name='Registro de Colaboradores'),
    path('colaboradoresput/<int:id>/',
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
    path('subir_fto/',
         csrf_exempt(view_rf_for.reconocimiento_facial), name='subir_fto'),
    path('generar_excel/', crearExcel.generar_excel, name='generar_excel'),
    path('callViajes/', rptoFuec.rptoFuec, name='Llamar Viajes'),
    path('callRptoViaje/', rptoFuec.rptoFuecPDF2,
         name='Llamar datos para el reporte'),
    path('saveRpto/', csrf_exempt(rptoFuec.saveRpto), name='Guardar el reporte'),
    #    Handle reportes WsDx
    path('rptoCuotaAdmin/', csrf_exempt(reportes.rptoCuotaAdmin),
         name='Reporte cuota de administracion'),
    #     path('generarRptoAdminCiudades/', csrf_exempt(reportes.generarRptoAdminCiudades),
    #          name='Generacion de excel en plantilla'),
    #     path('generarRptoAdminPropietarios/', csrf_exempt(reportes.generarRptoAdminPropietarios),
    #          name='Generacion de excel en plantilla'),
    path('generarRptoAdmin/', csrf_exempt(reportes.generarRptoAdmin),
         name='Generacion de excel en plantilla'),
    path('rptoAlcoholimetria/', csrf_exempt(reporteAlcoholimetria.rptoAlcoholimetria),
         name='Reporte de alcoholimetria'),
    path('generarRptoAlcoholimetria/', csrf_exempt(reporteAlcoholimetria.generarRptoAlcoholimetria),
         name='Generacion de reporte en excel de alcoholimetria'),
    path('rptoOperaciones/', csrf_exempt(RptosOperaciones.rptoOperaciones),
         name='Reportes-Datos Operaciones'),
    path('generarRptoOViajes/', csrf_exempt(RptosOperaciones.generarRptoOpeViajes),
         name='Generacion de reporte en excel de Viajes'),
    path('rptoPlaneacion/', csrf_exempt(RptosPlaneacion.rptoPlaneacion),
         name='Reportes-Datos Planeacion'),
    path('generarRptoPL/', csrf_exempt(RptosPlaneacion.generarRptoPL),
         name='Generacion de reporte en excel de Planeacion'),
    path('rptoContabilidad/', csrf_exempt(RptosContabilidad.rptoContabilidad),
         name='Reportes-Datos Contabilidad'),
    path('generarRptoPL/', csrf_exempt(RptosPlaneacion.generarRptoPL),
         name='Generacion de reporte en excel de Planeacion'),
    path('Pvu/', csrf_exempt(Pvu.Pvu), name='Pvu'),
    path('PvuInactivate/', csrf_exempt(Pvu.PvuInactivate), name='Pvu'),
    path('RptosDominicales/', csrf_exempt(Dominicales.RptosDominicales), name='Pvu'),
    path('TiquetesCRM/', csrf_exempt(Tiquetes.TiquetesCRM),
         name='Rpto Tiquetes CRM'),
    path('RptoConductores/', csrf_exempt(RptosConductores.RptoConductores), name=''),
    path('generarRptoConductores/', csrf_exempt(RptosConductores.generarRptoConductores),
         name='Generacion de reporte en excel de Conductores'),
    path('RptoComercialEst/', csrf_exempt(RptosComercial.rptoComercial),
         name='Reporte Estadistica Comercial'),
    path('rptoCertificados/', csrf_exempt(RptosComercial.rptoCertificados),
         name='Reporte Estadistica Certificados'),
    path('generarRptoComercial/', csrf_exempt(RptosComercial.generarRptosComercial),
         name='Generacion de reporte en excel de Comercial'),
    path('rptoDomicilios/', csrf_exempt(RptosComercial.rptoDomicilios),
         name='Reporte Domicilios'),
    path('RptosMacarena/', csrf_exempt(RptosMacarena.rptosMacarena),
         name='Reporte Macarena'),
    path('generarRptosMacarena/', csrf_exempt(RptosMacarena.generarRptosMacarena),
         name='Generacion de reporte en excel de Macarena'),
    path('rptoHistoricoFuec/', csrf_exempt(RptoHisFuec.rptoHistoricoFuec),
         name='Reporte Historico del Fuec'),
    path('generarRptoFuec/', csrf_exempt(RptoHisFuec.generarRptoFuec),
         name='Generacion de reporte en excel del FUEC'),
    path('rptosMigracion/', csrf_exempt(RptosMigracion.rptosMigracion),
         name='Reporte Historico de Migracion'),
    path('generarRptosMigracion/', csrf_exempt(RptosMigracion.generarRptosMigracion),
         name='Generacion de reporte en excel de Migracion'),
    path('RptoTaquillas/', csrf_exempt(RptosTaquillas.RptoTaquillas),
         name='Reporte Taquillas Bogota'),
    path('generarRptoTaquillas/', csrf_exempt(RptosTaquillas.generarRptoTaquillas),
         name='Reporte Excel Taquillas Bogota'),
    path('RptoMicroSeguros/', csrf_exempt(RptosMicroseguros.RptoMicroSeguros),
         name='Reporte MicroSeguros'),
    path('RptoTiquetesMicroSeguros/', csrf_exempt(RptosMicroseguros.RptoTiquetesMicroSeguros),
         name='Reporte Tiquetes con MicroSeguros'),
    path('generarRptoMicroseguros/', csrf_exempt(RptosMicroseguros.generarRptoMicroseguros),
         name='Reporte Excel de Tiquetes con Microseguros'),
    #     path('export/', crearPdf_Wp.export_pdf, name="export-pdf")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
