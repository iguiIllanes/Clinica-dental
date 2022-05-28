from django.urls import include, path
from rest_framework import routers
from . import views

from .views import (
    MedicosEspecialidadesListApiView,
    PersonasListApiView,
    PersonasDetailApiView,

    PacientesListApiView,
    PacientesDetailApiView,


    MedicosListApiView,
    MedicosDetailApiView,

    EspecialidadesListApiView,
    EspecialidadesDetailApiView,

    MedicosEspecialidadesListApiView,
    MedicosEspecialidadesDetailApiView,

    CitasListApiView,
    CitasDetailApiView,
    MedicoCitasApiView
)

router = routers.DefaultRouter()

urlpatterns = [
    
    path ('', include(router.urls)),
    path ('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    path ('personas/', PersonasListApiView.as_view()),
    path ('personas/<int:persona_id>/', PersonasDetailApiView.as_view()),

    path ('pacientes/', PacientesListApiView.as_view()),
    path ('pacientes/<str:usuario>/', PacientesDetailApiView.as_view()),

    path ('medicos/',MedicosListApiView.as_view()),
    path ('medicos/<str:usuario>/',MedicosDetailApiView.as_view()),

    path ('medicos_especialidades/',MedicosEspecialidadesListApiView.as_view()),
    path ('medicos_especialidades/<int:id_med_esp>/',MedicosEspecialidadesDetailApiView.as_view()),

    path ('especialidades/',EspecialidadesListApiView.as_view()),
    path ('especialidades/<int:id_especialidad>/',EspecialidadesDetailApiView.as_view()),

    path ('citas/',CitasListApiView.as_view()),
    path ('citas/<int:id_cita>/',CitasDetailApiView.as_view()),

    path ('citas/medico/<int:id_medico>/',MedicoCitasApiView.as_view()),
    
]