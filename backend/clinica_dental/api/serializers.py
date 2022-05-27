from statistics import mode
from rest_framework import serializers

from .models import Persona
from .models import Medico
from .models import Especialidad
from .models import MedicoEspecialidad
from .models import Cita, Persona, Paciente

class PersonaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Persona
        fields = ('id_persona', 'ci', 'nombre', 'apellido', 'telefono', 'fecha_nacimiento')

class MedicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medico
        fields = ('id_persona','fecha_contrato','usuario', 'password','contratado','correo_institucional')

class EspecialidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Especialidad
        fields = ('id_especialidad','especialidad')

class MedicoEspecialidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicoEspecialidad
        fields = ('id_med_esp','id_especialidad','fecha_titulo','medico_id_persona')
class PacienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paciente
        fields = ('id_persona', 'correo_paciente', 'usuario', 'password', 'alergias', 'enfermedades_base')

class CitaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cita
        fields = ('id_cita', 'id_paciente', 'id_doctor', 'fecha_reserva', 'fecha_consulta')
