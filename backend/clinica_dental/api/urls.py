from django.urls import include, path
from rest_framework import routers
from . import views

from .views import (
    PersonasListApiView,
    PersonasDetailApiView,

    PacientesListApiView,
    MedicosListApiView,
)

router = routers.DefaultRouter()

router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('personas/', PersonasListApiView.as_view()),
    path('personas/<int:persona_id>/', PersonasDetailApiView.as_view()),
    path('pacientes/', PacientesListApiView.as_view()),
    path ('medicos/',MedicosListApiView.as_view())
]