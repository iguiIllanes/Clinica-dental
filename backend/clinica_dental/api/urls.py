from django.urls import include, path
from rest_framework import routers
from . import views

from .views import (
    PersonasListApiView,
    PersonasDetailApiView,

    PacientesListApiView,
    PacientesIdDetailApiView,
    PacientesUsuarioDetailApiView,

    MedicosListApiView,
    MedicosDetailApiView,

    EspecialidadesListApiView,
    EspecialidadesDetailApiView,

    MedicosEspecialidadesListApiView,
    MedicosEspecialidadesDetailApiView,

    CitasListApiView,
    CitasDetailApiView,

    MedicoCitasApiView,

    PacienteCitasApiView,

    TarjetasListApiView,
    TarjetasDetailApiView,

    PagosReservasListApiView,
    PagosReservasDetailApiView,

    ServiciosListApiView,
    ServiciosDetailApiView,

    ConsultasListApiView,
    ConsultasDetailApiView,
    ConsultasUsuarioDetailApiView,
    ConsultasCitasDetailApiView,

    PagosConsultasListApiView,
    PagosConsultasDetailApiView,

    LaboratoriosListApiView,
    LaboratoriosDetailApiView,

    RayosXListApiView,
    RayosXDetailApiView,

    MedicinasListApiView,
    MedicinasDetailApiView,

    RecetasListApiView,
    RecetasDetailApiView,

  #  CitasPorMedicoApiView,
)

router = routers.DefaultRouter()

urlpatterns = [
    
    path ('', include(router.urls)),
    path ('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    path ('personas/', PersonasListApiView.as_view()),
    path ('personas/<int:persona_id>/', PersonasDetailApiView.as_view()),

    path ('pacientes/', PacientesListApiView.as_view()),
    path ('pacientes/<int:id_persona>', PacientesIdDetailApiView.as_view()),
    path ('pacientes/<str:usuario>/', PacientesUsuarioDetailApiView.as_view()),

    path ('medicos/',MedicosListApiView.as_view()),
    path ('medicos/<str:usuario>/',MedicosDetailApiView.as_view()),

    path ('medicos_especialidades/',MedicosEspecialidadesListApiView.as_view()),
    path ('medicos_especialidades/<int:id_med_esp>/',MedicosEspecialidadesDetailApiView.as_view()),

    path ('especialidades/',EspecialidadesListApiView.as_view()),
    path ('especialidades/<int:id_especialidad>/',EspecialidadesDetailApiView.as_view()),

    path ('citas/',CitasListApiView.as_view()),
    path ('citas/<int:id_cita>/',CitasDetailApiView.as_view()),

    path ('citas/medico/<int:id_medico>/',MedicoCitasApiView.as_view()),

    path ('citas/paciente/<int:id_paciente>', PacienteCitasApiView.as_view()),
    
    path ('tarjetas/',TarjetasListApiView.as_view()),
    path ('tarjetas/<int:id_tarjeta>/',TarjetasDetailApiView.as_view()),

    path ('pagos_reservas/', PagosReservasListApiView.as_view()),
    path ('pagos_reservas/<int:id_pago>/', PagosReservasDetailApiView.as_view()),

    path ('servicios/',ServiciosListApiView.as_view()),
    path ('servicios/<int:id_servicio>/',ServiciosDetailApiView.as_view()),

    path ('consultas/',ConsultasListApiView.as_view()),
    path ('consultas/<int:id_consulta>/',ConsultasDetailApiView.as_view()),
    path ('consultas/paciente/<int:id_paciente>', ConsultasUsuarioDetailApiView.as_view()),
    path ('consultas/paciente/<int:id_doctor>/<int:id_paciente>',ConsultasCitasDetailApiView.as_view()),

    path ('pagos_consultas/',PagosConsultasListApiView.as_view()),
    path ('pagos_consultas/<int:id_pago_consulta>/',PagosConsultasDetailApiView.as_view()),

    path ('laboratorios/',LaboratoriosListApiView.as_view()),
    path ('laboratorios/<int:id_lab>/',LaboratoriosDetailApiView.as_view()),

    path ('rayosx/',RayosXListApiView.as_view()),
    path ('rayosx/<int:id_rayos>/',RayosXDetailApiView.as_view()),

    path ('medicinas/',MedicinasListApiView.as_view()),
    path ('medicinas/<int:id_med>/',MedicinasDetailApiView.as_view()),

    path ('recetas/',RecetasListApiView.as_view()),
    path ('recetas/<int:id_receta>/',RecetasDetailApiView.as_view()),

   # path ('citas/medico/<int:id_doctor>/', CitasPorMedicoApiView.as_view()),
]