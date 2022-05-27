from rest_framework import viewsets

from .serializers import PersonaSerializer
from .models import Persona

class PersonaViewSet(viewsets.ModelViewSet):
    queryset = Persona.objects.all()
    serializer_class = PersonaSerializer
