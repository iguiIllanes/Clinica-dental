from statistics import mode
from xml.parsers.expat import model
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
    #id_persona = PersonaSerializer(read_only=True)
    class Meta:
        model = Medico
        fields = ('id_persona','fecha_contrato','usuario', 'password','contratado','correo_institucional')
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['id_persona'] = PersonaSerializer(instance.id_persona).data
        return response     

class EspecialidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Especialidad
        fields = ('id_especialidad','especialidad')

class MedicoEspecialidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicoEspecialidad
        fields = ('id_med_esp','id_especialidad','fecha_titulo','medico_id_persona')
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['id_especialidad'] = EspecialidadSerializer(instance.id_especialidad).data
        response['medico_id_persona']= MedicoSerializer(instance.medico_id_persona).data
        return response   

class PacienteSerializer(serializers.ModelSerializer):
    #id_persona = PersonaSerializer()
    class Meta:
        model = Paciente
        fields = ('id_persona', 'correo_paciente', 'usuario', 'password', 'alergias', 'enfermedades_base')
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['id_persona'] = PersonaSerializer(instance.id_persona).data
        return response  

class CitaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cita
        fields = ('id_cita', 'id_paciente', 'id_doctor', 'fecha_reserva', 'fecha_consulta')
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['id_paciente'] = PacienteSerializer(instance.id_paciente).data
        response['id_doctor'] = MedicoSerializer(instance.id_doctor).data
        return response  
