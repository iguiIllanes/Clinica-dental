from rest_framework import viewsets

from .serializers import PersonaSerializer
from .serializers import PacienteSerializer
from .serializers import CitaSerializer
from .models import Persona
from .models import Paciente
from .models import Cita

class PersonaViewSet(viewsets.ModelViewSet):
    queryset = Persona.objects.all()
    serializer_class = PersonaSerializer

class PacienteViewSet(viewsets.ModelViewSet):
    queryset = Paciente.objects.all()
    serializer_class = PacienteSerializer

class CitaViewSet(viewsets.ModelViewSet):
    queryset = Cita.objects.all()
    serializer_class = CitaSerializer