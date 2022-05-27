from django.urls import include, path
from rest_framework import routers
from . import views
from .views import (
    MedicosListApiView,
)
router = routers.DefaultRouter()
# router.register(r'personas', views.PersonaViewSet)
# router.register(r'medicos',views.MedicoViewSet)
# router.register(r'especialidades',views.EspecialidadViewSet)
# router.register(r'medicosespecialidades',views.MedicoEspecialidadViewSet)
# router.register(r'pacientes', views.PacienteViewSet)
# router.register(r'citas', views.CitaViewSet)
# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path ('medicos/',MedicosListApiView.as_view())
]