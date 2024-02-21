from . import XlsxRptos, StoredProcedures, api, views, view_rf, view_rf_for
from . import crearExcel, rptoFuec, reporteAlcoholimetria, RptosConductores
from django.views.decorators.csrf import csrf_exempt
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework import routers
from django.conf import settings

router = routers.DefaultRouter()
router.register('roles', api.RolesViewSet, "Roles")
router.register('login', api.LoginViewSet, "Login")
router.register('users', api.ColaboradoresViewSet, "Colaboradores")
router.register('docsti', api.TipoDocumentoViewSet, "TipoDocumento")
router.register('modulos', api.ModulosViewSet, "Modulos")
router.register('permisos', api.PermisosViewSet, "Permisos")
router.register('empresas', api.EmpresasViewSet, "Empresas")

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
    path('callRptoViaje/', rptoFuec.rptoFuecPDF,
         name='Llamar datos para el reporte'),
    path('saveRpto/', csrf_exempt(rptoFuec.saveRpto), name='Guardar el reporte'),
    #    Handle reportes WsDx
    path('RP_consultas01/', csrf_exempt(StoredProcedures.RP_consultas01),
         name='Reporte Estadistica Comercial'),
    path('XlsxRP_consultas01/', csrf_exempt(XlsxRptos.XlsxRP_consultas01),
         name='Generacion de reporte en excel de Comercial'),
    path('RP_Consultas05/', csrf_exempt(StoredProcedures.RP_Consultas05),
         name='Reporte Domicilios'),
    path('XlsxRP_Consultas05/', csrf_exempt(XlsxRptos.XlsxRP_Consultas05),
         name='Generacion de reporte en excel'),
    path('RP_CuotaAdmon/', csrf_exempt(StoredProcedures.RP_CuotaAdmon),
         name='Reporte cuota de administracion'),
    path('XlsxRP_CuotaAdmon/', csrf_exempt(XlsxRptos.XlsxRP_CuotaAdmon),
         name='Generacion de excel en plantilla'),
    path('Rp_certificaciones/', csrf_exempt(StoredProcedures.Rp_certificaciones),
         name='Reporte Estadistica Certificados'),
    path('RP_Macarena/', csrf_exempt(StoredProcedures.RP_Macarena),
         name='Reporte Macarena'),
    path('XlxsRP_Macarena/', csrf_exempt(XlsxRptos.XlxsRP_Macarena),
         name='Generacion de reporte en excel de Macarena'),
    path('Sp_RptHistoFuec/', csrf_exempt(StoredProcedures.Sp_RptHistoFuec),
         name='Reporte Historico del Fuec'),
    path('XlsxSp_RptHistoFuec/', csrf_exempt(XlsxRptos.XlsxSp_RptHistoFuec),
         name='Generacion de reporte en excel del FUEC'),
    path('RP_Prueba_Alcoholimetria/', csrf_exempt(StoredProcedures.RP_Prueba_Alcoholimetria),
         name='Reporte de alcoholimetria'),
    path('XlsxFics_MicroSegurosGET/', csrf_exempt(XlsxRptos.XlsxFics_MicroSegurosGET),
         name='Reporte Excel de Tiquetes con Microseguros'),
    path('generarRptoAlcoholimetria/', csrf_exempt(reporteAlcoholimetria.generarRptoAlcoholimetria),
         name='Generacion de reporte en excel de alcoholimetria'),
    path('UsuarioFrecuente/',
         csrf_exempt(StoredProcedures.UsuarioFrecuente), name='Pvu'),
    path('VO_ViajeroFrecuente/',
         csrf_exempt(StoredProcedures.VO_ViajeroFrecuente), name='Pvu'),
    path('RP_Dominicales/', csrf_exempt(StoredProcedures.RP_Dominicales), name='Pvu'),
    path('Rp_CRM/', csrf_exempt(StoredProcedures.Rp_CRM),
         name='Rpto Tiquetes CRM'),
    path('RP_CondvigFICS/', csrf_exempt(StoredProcedures.RP_CondvigFICS), name=''),
    path('generarRptoConductores/', csrf_exempt(RptosConductores.generarRptoConductores),
         name='Generacion de reporte en excel de Conductores'),
    path('RP_MIGRACION/', csrf_exempt(StoredProcedures.RP_MIGRACION),
         name='Reporte Historico de Migracion'),
    path('XlsxRP_MIGRACION/', csrf_exempt(XlsxRptos.XlsxRP_MIGRACION),
         name='Generacion de reporte en excel de Migracion'),
    path('RPT_EstadisticaXTaquilla/', csrf_exempt(StoredProcedures.RPT_EstadisticaXTaquilla),
         name='Reporte Taquillas Bogota'),
    path('XlsxRPT_EstadisticaXTaquilla/', csrf_exempt(XlsxRptos.XlsxRPT_EstadisticaXTaquilla),
         name='Reporte Excel Taquillas Bogota'),
    path('Fics_MicroSegurosGET/', csrf_exempt(StoredProcedures.Fics_MicroSegurosGET),
         name='Reporte MicroSeguros'),
    path('RP_Consultas04/', csrf_exempt(StoredProcedures.RP_Consultas04),
         name='Reporte Tiquetes con MicroSeguros'),
    path('Rp_VF3/', csrf_exempt(StoredProcedures.Rp_VF3),
         name='Reporte Turismo'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
