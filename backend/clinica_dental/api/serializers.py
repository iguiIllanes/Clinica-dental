from statistics import mode
from rest_framework import serializers

from .models import Persona

class PersonaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Persona
        fields = ('id_persona', 'ci', 'nombre', 'apellido', 'telefono', 'fecha_nacimiento')