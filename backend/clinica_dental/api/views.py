from rest_framework import viewsets

from .serializers import PersonaSerializer,MedicoSerializer, EspecialidadSerializer,MedicoEspecialidadSerializer
from .models import Persona
from .models import Medico
from .models import Especialidad
from .models import MedicoEspecialidad

from .serializers import PersonaSerializer
from .serializers import PacienteSerializer
from .serializers import CitaSerializer
from .models import Persona
from .models import Paciente
from .models import Cita

class PersonaViewSet(viewsets.ModelViewSet):
    queryset = Persona.objects.all()
    serializer_class = PersonaSerializer

class MedicoViewSet(viewsets.ModelViewSet):
    queryset = Medico.objects.all()
    serializer_class = MedicoSerializer

class EspecialidadViewSet(viewsets.ModelViewSet):
    queryset = Especialidad.objects.all()
    serializer_class = EspecialidadSerializer

class MedicoEspecialidadViewSet(viewsets.ModelViewSet):
    queryset = MedicoEspecialidad.objects.all()
    serializer_class = MedicoEspecialidadSerializer
class PacienteViewSet(viewsets.ModelViewSet):
    queryset = Paciente.objects.all()
    serializer_class = PacienteSerializer

class CitaViewSet(viewsets.ModelViewSet):
    queryset = Cita.objects.all()
    serializer_class = CitaSerializer
