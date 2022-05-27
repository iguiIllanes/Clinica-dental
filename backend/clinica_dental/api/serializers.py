from statistics import mode
from rest_framework import serializers

from .models import Cita, Persona, Paciente

class PersonaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Persona
        fields = ('id_persona', 'ci', 'nombre', 'apellido', 'telefono', 'fecha_nacimiento')

class PacienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paciente
        fields = ('id_persona', 'correo_paciente', 'usuario', 'password', 'alergias', 'enfermedades_base')

class CitaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cita
        fields = ('id_cita', 'id_paciente', 'id_doctor', 'fecha_reserva', 'fecha_consulta')