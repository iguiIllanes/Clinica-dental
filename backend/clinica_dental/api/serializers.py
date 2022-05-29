from statistics import mode
from xml.parsers.expat import model
from rest_framework import serializers

from .models import Persona
from .models import Medico
from .models import Especialidad
from .models import MedicoEspecialidad
from .models import Cita, Persona, Paciente
from .models import Tarjeta, PagoReserva
from .models import Consulta,Servicio,PagosConsulta
from .models import Laboratorio,Rayos_X
from .models import Medicina,Consulta_Medicina_Receta

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
        response['id_especialidad'] = EspecialidadSerializer(instance.id_especialidad).data['id_persona']
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
        response['id_paciente'] = PacienteSerializer(instance.id_paciente).data['id_persona']
        response['id_doctor'] = MedicoSerializer(instance.id_doctor).data['id_persona']
        return response  

class TarjetaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tarjeta
        fields = ('id_tarjeta','fecha_caducidad','cvc','id_paciente') 
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['id_paciente'] = PacienteSerializer(instance.id_paciente).data['id_persona']
        return response  

class PagoReservaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PagoReserva
        fields = ('id_pago','monto','id_cita','id_tarjeta')
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['id_cita'] = CitaSerializer(instance.id_cita).data
        response['id_tarjeta'] = TarjetaSerializer(instance.id_tarjeta).data
        return response  

class ServicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servicio
        fields = ('id_servicio','nombre_servicio')

class ConsultaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consulta
        fields = ('id_Consulta','id_Cita','Descripcion','MontoTotal','id_Servicio')
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['id_Cita'] = CitaSerializer(instance.id_Cita).data
        response['id_Servicio'] = ServicioSerializer(instance.id_Servicio).data
        return response  

class PagosConsultaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PagosConsulta
        fields = ('id_pago_consulta','id_consulta','monto')
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['id_consulta'] = ConsultaSerializer(instance.id_consulta).data
        return response  

class LaboratorioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Laboratorio
        fields = ('id_Lab','Nombres')

class RayosXSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rayos_X
        fields = ('id_Rayos','Tipo','id_Consulta','id_Lab')
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['id_Consulta'] = ConsultaSerializer(instance.id_Consulta).data
        response['id_Lab'] = LaboratorioSerializer(instance.id_Lab).data
        return response  

class MedicinaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicina
        fields = ('id_med','nombre','tipo')

class RecetaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consulta_Medicina_Receta
        fields = ('id_Receta','id_Med','Desc','id_Consulta')
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['id_Med'] = MedicinaSerializer(instance.id_Med).data
        response['id_Consulta'] = ConsultaSerializer(instance.id_Consulta).data
        return response  

