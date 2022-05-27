from django.urls import include, path
from rest_framework import routers
from . import views

from .views import (
    PersonasApiView,
    PersonaApiView,

    PacientesApiView,
)

router = routers.DefaultRouter()

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('personas/', PersonasApiView.as_view()),
    path('personas/<int:persona_id>/', PersonaApiView.as_view()),
    path('pacientes/', PacientesApiView.as_view()),
]