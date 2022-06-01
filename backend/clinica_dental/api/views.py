import json
import re

from datetime import datetime

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from urllib import request, response
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

from .serializers import TarjetaSerializer,PagoReservaSerializer,ServicioSerializer,ConsultaSerializer
from .serializers import PagosConsultaSerializer,LaboratorioSerializer,RayosXSerializer
from .serializers import RecetaSerializer,MedicinaSerializer

from . models import Tarjeta,PagoReserva,Servicio,Consulta,PagosConsulta,Laboratorio,Rayos_X,Consulta_Medicina_Receta,Medicina


class PersonasListApiView(APIView):
    def get(self, request, *args, **kwargs):
        personas = Persona.objects.all()
        serializer = PersonaSerializer(personas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = {
            "ci": request.data.get("ci"),
            "nombre":request.data.get("nombre"),
            "apellido":request.data.get("apellido"),
            "telefono":request.data.get("telefono"),
            "fecha_nacimiento":request.data.get("fecha_nacimiento")
        }
        serializer = PersonaSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class PersonasDetailApiView(APIView):
    def get_persona(self, persona_id):
        try:
            return Persona.objects.get(id_persona=persona_id)
        except Persona.DoesNotExist:
            return None

    def get(self, request, persona_id, *args, **kwargs):
        persona = self.get_persona(persona_id)
        if not persona:
            return Response(
                {"res":"No existe una persona con ese id"},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = PersonaSerializer(persona)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, persona_id, *args, **kwargs):
        persona = self.get_persona(persona_id)

    def delete(self, request, persona_id, *args, **kwargs):
        persona_instance = self.get_persona(persona_id)
        if not persona_instance:
            return Response(
                {"res": "Object with todo id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        persona_instance.delete()
        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )


class PacientesListApiView(APIView):
    def get(self, request, *args, **kwargs):
        pacientes = Paciente.objects.all()
        serializer = PacienteSerializer(pacientes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):

        persona = {
            "ci":request.data.get("ci"),
            "nombre": request.data.get("nombre"),
            "apellido": request.data.get("apellido"),
            "telefono": request.data.get("telefono"),
            "fecha_nacimiento": request.data.get("fecha_nacimiento")
        }

        persona_serializer = PersonaSerializer(data=persona)
        if persona_serializer.is_valid():
            persona_serializer.save()
            data = {
                "id_persona": persona_serializer.data["id_persona"],
                "correo_paciente": request.data.get("correo_paciente"),
                "usuario": request.data.get("usuario"),
                "password": request.data.get("password"),
                "alergias": request.data.get("alergias"),
                "enfermedades_base": request.data.get("enfermedades_base"),
            }

            paciente_serializer = PacienteSerializer(data=data)        
            if paciente_serializer.is_valid():
                paciente_serializer.save()
                return Response(paciente_serializer.data, status=status.HTTP_201_CREATED)
            return Response(paciente_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
        return Response(persona_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   

class PacientesUsuarioDetailApiView(APIView):
    def get_paciente(self, usuario):
        try:
            return Paciente.objects.get(usuario = usuario)
        except Paciente.DoesNotExist:
            return None
    
    def get(self, request, usuario, *args, **kwargs):
        paciente_instance = self.get_paciente(usuario)
        if not paciente_instance:
            return Response(
                {"res": "Object with that id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = PacienteSerializer(paciente_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

class PacientesIdDetailApiView(APIView):
    def get_paciente(self, id_persona):
        try:
            return Paciente.objects.get(id_persona = id_persona)
        except Paciente.DoesNotExist:
            return None
    
    def get(self, request, id_persona, *args, **kwargs):
        paciente_instance = self.get_paciente(id_persona)
        if not paciente_instance:
            return Response(
                {"res": "Object with that id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = PacienteSerializer(paciente_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

        
class MedicosListApiView(APIView):
    def get(self, request, *args, **kwargs):
        medicos = Medico.objects.all()
        serializer = MedicoSerializer(medicos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = {
            'id_persona': request.data.get('id_persona'),
            'fecha_contrato': request.data.get('fecha_contrato'), 
            'usuario': request.data.get('usuario'), 
            'password': request.data.get('password'), 
            'contratado': request.data.get('contratado'), 
            'correo_institucional': request.data.get('correo_institucional'),    
        }
        serializer = MedicoSerializer(data=data)
        if serializer.is_valid():
             serializer.save()
             return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MedicosDetailApiView(APIView):

    def get_object(self, usuario):
        try:
            return Medico.objects.get(usuario = usuario)
        except Medico.DoesNotExist:
            return None

    def get(self, request, usuario, *args, **kwargs):
        medico_instance = self.get_object(usuario)
        if not medico_instance:
            return Response(
                {"res": "Object with that id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = MedicoSerializer(medico_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request,id_medico, *args, **kwargs):
        medico_instance = self.get_object(id_medico)
        if not medico_instance:
            return Response(
                {"res": "Object with that id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        data = {
            'fecha_contrato': request.data.get('fecha_contrato'), 
            'usuario': request.data.get('usuario'), 
            'password': request.data.get('password'), 
            'contratado': request.data.get('contratado'), 
            'correo_institucional': request.data.get('correo_institucional'), 
        }
        serializer = MedicoSerializer(instance = medico_instance, data=data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id_medico, *args, **kwargs):

        medico_instance = self.get_object(id_medico)
        if not medico_instance:
            return Response(
                {"res": "Object with that id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        medico_instance.delete()
        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )

class EspecialidadesListApiView(APIView):
    def get(self, request, *args, **kwargs):
        especialidades = Especialidad.objects.all()
        serializer = EspecialidadSerializer(especialidades, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = {
            'especialidad': request.data.get('especialidad'),
        }
        serializer = EspecialidadSerializer(data=data)
        if serializer.is_valid():
             serializer.save()
             return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EspecialidadesDetailApiView(APIView):

    def get_object(self, id_especialidad):
        try:
            return Especialidad.objects.get(id_especialidad=id_especialidad)
        except Especialidad.DoesNotExist:
            return None

    def get(self, request, id_especialidad, *args, **kwargs):
        especialidad_instance = self.get_object(id_especialidad)
        if not especialidad_instance:
            return Response(
                {"res": "Object with that id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = EspecialidadSerializer(especialidad_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def put(self, request,id_especialidad, *args, **kwargs):
        especialidad_instance = self.get_object(id_especialidad)
        if not especialidad_instance:
            return Response(
                {"res": "Object with that id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        data = {
            'especialidad': request.data.get('especialidad'), 
        }
        serializer = EspecialidadSerializer(instance = especialidad_instance, data=data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id_especialidad, *args, **kwargs):

        especialidad_instance = self.get_object(id_especialidad)
        if not especialidad_instance:
            return Response(
                {"res": "Object with that id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        especialidad_instance.delete()
        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )

class  MedicosEspecialidadesListApiView(APIView):
    def get(self, request, *args, **kwargs):
        medicos_especialidades = MedicoEspecialidad.objects.all()
        serializer = MedicoEspecialidadSerializer(medicos_especialidades, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = {
            'id_especialidad': request.data.get('id_especialidad'),
            'fecha_titulo': request.data.get('fecha_titulo'),
            'medico_id_persona': request.data.get('medico_id_persona'),
        }
        serializer = MedicoEspecialidadSerializer(data=data)
        if serializer.is_valid():
             serializer.save()
             return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MedicosEspecialidadesDetailApiView(APIView):

    def get_object(self, id_med_esp):
        try:
            return MedicoEspecialidad.objects.get(id_med_esp=id_med_esp)
        except MedicoEspecialidad.DoesNotExist:
            return None

    def get(self, request, id_med_esp, *args, **kwargs):
        medico_especialidad_instance = self.get_object(id_med_esp)
        if not medico_especialidad_instance:
            return Response(
                {"res": "Object with that id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = MedicoEspecialidadSerializer(medico_especialidad_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def put(self, request,id_med_esp, *args, **kwargs):
        medico_especialidad_instance = self.get_object(id_med_esp)
        if not medico_especialidad_instance:
            return Response(
                {"res": "Object with that id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        data = {
            'id_especialidad': request.data.get('id_especialidad'),
            'fecha_titulo': request.data.get('fecha_titulo'),
            'medico_id_persona': request.data.get('medico_id_persona'),
        }
        serializer = MedicoEspecialidadSerializer(instance = medico_especialidad_instance, data=data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id_med_esp, *args, **kwargs):

        medico_especialidad_instance = self.get_object(id_med_esp)
        if not medico_especialidad_instance:
            return Response(
                {"res": "Object with that id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        medico_especialidad_instance.delete()
        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )

class  CitasListApiView(APIView):
    def get(self, request, *args, **kwargs):
        citas = Cita.objects.all()
        serializer = CitaSerializer(citas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = {
            'id_paciente': request.data.get('id_paciente'),
            'id_doctor': request.data.get('id_doctor'),
            'fecha_reserva': request.data.get('fecha_reserva'),
            'fecha_consulta': request.data.get('fecha_consulta'),
        }
        serializer = CitaSerializer(data=data)
        if serializer.is_valid():
             serializer.save()
             return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class CitasDetailApiView(APIView):

    def get_object(self, id_cita):
        try:
            return Cita.objects.get(id_cita=id_cita)
        except Cita.DoesNotExist:
            return None

    def get(self, request, id_cita, *args, **kwargs):
        cita_instance = self.get_object(id_cita)
        if not cita_instance:
            return Response(
                {"res": "Object with that id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = CitaSerializer(cita_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def put(self, request,id_cita, *args, **kwargs):
        cita_instance = self.get_object(id_cita)
        if not cita_instance:
            return Response(
                {"res": "Object with that id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        data = {
            'id_paciente': request.data.get('id_paciente'),
            'id_doctor': request.data.get('id_doctor'),
            'fecha_reserva': request.data.get('fecha_reserva'),
            'fecha_consulta': request.data.get('fecha_consulta'),
        }
        serializer = CitaSerializer(instance = cita_instance, data=data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id_cita, *args, **kwargs):

        cita_instance = self.get_object(id_cita)
        if not cita_instance:
            return Response(
                {"res": "Object with that id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        cita_instance.delete()
        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )

class MedicoCitasApiView(APIView):

    def get_object(self, id_medico):
        try:
            return Cita.objects.filter(id_doctor=id_medico)
        except Cita.DoesNotExist:
            return None

    def get(self, request, id_medico, *args, **kwargs):
        cita_instance = self.get_object(id_medico)
        if not cita_instance:
            return Response(
                {"res": "Object with that id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = CitaSerializer(cita_instance, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class PacienteCitasApiView(APIView):
    def get_citas(self, id_paciente):
        try:
            return Cita.objects.filter(id_paciente = id_paciente)
        except Cita.DoesNotExist:
            return None

    def get(self, request, id_paciente, *args, **kwargs):
        citas_instance = self.get_citas(id_paciente)
        if not citas_instance:
            return Response(
                {"res": "Object with that id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
 
        citas_serializer = CitaSerializer(citas_instance, many=True)
        return Response(citas_serializer.data, status=status.HTTP_200_OK)

class  TarjetasListApiView(APIView):
    def get(self, request, *args, **kwargs):
        tarjetas = Tarjeta.objects.all()
        serializer = TarjetaSerializer(tarjetas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = {
            'fecha_caducidad': request.data.get('fecha_caducidad'),
            'cvc': request.data.get('cvc'),
            'id_paciente': request.data.get('id_paciente'),
        }

        serializer = TarjetaSerializer(data=data)
        if serializer.is_valid():
             serializer.save()
             return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TarjetasDetailApiView(APIView):

    def get_object(self, id_tarjeta):
        try:
            return Tarjeta.objects.get(id_tarjeta=id_tarjeta)
        except Tarjeta.DoesNotExist:
            return None

    def get(self, request, id_tarjeta, *args, **kwargs):
        tarjeta_instance = self.get_object(id_tarjeta)
        if not tarjeta_instance:
            return Response(
                {"res": "Object with that id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = TarjetaSerializer(tarjeta_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request,id_tarjeta, *args, **kwargs):
        tarjeta_instance = self.get_object(id_tarjeta)
        if not tarjeta_instance:
            return Response(
                {"res": "Object with that id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        data = {
            'fecha_caducidad': request.data.get('fecha_caducidad'),
            'cvc': request.data.get('cvc'),
            'id_paciente': request.data.get('id_paciente'),
        }
        serializer = TarjetaSerializer(instance = tarjeta_instance, data=data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id_tarjeta, *args, **kwargs):
        tarjeta_instance = self.get_object(id_tarjeta)
        if not tarjeta_instance:
            return Response(
                {"res": "Object with that id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        tarjeta_instance.delete()
        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )

class  PagosReservasListApiView(APIView):
    def get(self, request, *args, **kwargs):
        pagos_reservas = PagoReserva.objects.all()
        serializer = PagoReservaSerializer(pagos_reservas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = {
            'monto': request.data.get('monto'),
            'id_tarjeta': request.data.get('id_tarjeta'),
            'id_cita': request.data.get('id_cita'),
        }

        serializer = PagoReservaSerializer(data=data)
        if serializer.is_valid():
             serializer.save()
             return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PagosReservasDetailApiView(APIView):

    def get_object(self, id_pago):
        try:
            return PagoReserva.objects.get(id_pago=id_pago)
        except PagoReserva.DoesNotExist:
            return None

    def get(self, request, id_pago, *args, **kwargs):
        pago_reserva_instance = self.get_object(id_pago)
        if not pago_reserva_instance:
            return Response(
                {"res": "Object with that id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = PagoReservaSerializer(pago_reserva_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request,id_pago, *args, **kwargs):
        pago_reserva_instance = self.get_object(id_pago)
        if not pago_reserva_instance:
            return Response(
                {"res": "Object with that id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        data = {
            'monto': request.data.get('monto'),
            'id_tarjeta': request.data.get('id_tarjeta'),
            'id_cita': request.data.get('id_cita'),
        }
        serializer = PagoReservaSerializer(instance = pago_reserva_instance, data=data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id_pago, *args, **kwargs):
        pago_reserva_instance = self.get_object(id_pago)
        if not pago_reserva_instance:
            return Response(
                {"res": "Object with that id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        pago_reserva_instance.delete()
        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )

class  ServiciosListApiView(APIView):
    def get(self, request, *args, **kwargs):
        servicios = Servicio.objects.all()
        serializer = ServicioSerializer(servicios, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = {
            'nombre_servicio': request.data.get('nombre_servicio'),
        }

        serializer = ServicioSerializer(data=data)
        if serializer.is_valid():
             serializer.save()
             return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ServiciosDetailApiView(APIView):

    def get_object(self, id_servicio):
        try:
            return Servicio.objects.get(id_servicio=id_servicio)
        except Servicio.DoesNotExist:
            return None

    def get(self, request, id_servicio, *args, **kwargs):
        servicio_instance = self.get_object(id_servicio)
        if not servicio_instance:
            return Response(
                {"res": "Object with that id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = ServicioSerializer(servicio_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request,id_servicio, *args, **kwargs):
        servicio_instance = self.get_object(id_servicio)
        if not servicio_instance:
            return Response(
                {"res": "Object with that id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        data = {
            'nombre_servicio': request.data.get('nombre_servicio'),
        }
        serializer = ServicioSerializer(instance = servicio_instance, data=data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id_servicio, *args, **kwargs):
        servicio_instance = self.get_object(id_servicio)
        if not servicio_instance:
            return Response(
                {"res": "Object with that id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        servicio_instance.delete()
        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )

class  ConsultasListApiView(APIView):
    def get(self, request, *args, **kwargs):
        consultas = Consulta.objects.all()
        serializer = ConsultaSerializer(consultas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = {
            'id_Cita': request.data.get('id_Cita'),
            'Descripcion': request.data.get('Descripcion'),
            'MontoTotal': request.data.get('MontoTotal'),
            'id_Servicio': request.data.get('id_Servicio'),
        }

        serializer = ConsultaSerializer(data=data)
        if serializer.is_valid():
             serializer.save()
             return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ConsultasDetailApiView(APIView):

    def get_object(self, id_Consulta):
        try:
            return Consulta.objects.get(id_Consulta=id_Consulta)
        except Consulta.DoesNotExist:
            return None

    def get(self, request, id_consulta, *args, **kwargs):
        consulta_instance = self.get_object(id_consulta)
        if not consulta_instance:
            return Response(
                {"res": "Object with that id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = ConsultaSerializer(consulta_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request,id_consulta, *args, **kwargs):
        consulta_instance = self.get_object(id_consulta)
        if not consulta_instance:
            return Response(
                {"res": "Object with that id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        data = {
            'id_Cita': request.data.get('id_Cita'),
            'Descripcion': request.data.get('Descripcion'),
            'MontoTotal': request.data.get('MontoTotal'),
            'id_Servicio': request.data.get('id_Servicio'),
        }
        serializer = ConsultaSerializer(instance = consulta_instance, data=data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id_consulta, *args, **kwargs):
        consulta_instance = self.get_object(id_consulta)
        if not consulta_instance:
            return Response(
                {"res": "Object with that id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        consulta_instance.delete()
        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )

class ConsultasUsuarioDetailApiView(APIView): #TODO corregir esto para poder hacer get en historial-paciente
    def get_citas(self, id_paciente):
        try:
            return Cita.objects.filter(id_paciente=id_paciente).values_list('id_cita',flat=True)
        except Cita.DoesNotExist:
            return None

    def get_consultas(self, citas):
        try:
            return Consulta.objects.filter(id_Cita__in=citas)
        except Cita.DoesNotExist:
            return None

    def get(self, request, id_paciente, *args, **kwargs):
        citas_instance = self.get_citas(id_paciente)        
        if not citas_instance:
            return Response(
                {"res": "Object with that id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        consultas_instance = self.get_consultas(citas_instance)
        if not consultas_instance:
            return Response(
                {"res": "Object with that id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        Serializer = ConsultaSerializer(consultas_instance, many=True)
        return Response(Serializer.data, status=status.HTTP_200_OK)

class ConsultasCitasDetailApiView(APIView): #TODO corregir esto para poder hacer get en historial-paciente
    def get_citas(self, id_paciente, id_doctor):
        try:
            return Cita.objects.filter(id_paciente=id_paciente).filter(id_doctor=id_doctor).filter(fecha_consulta__date=datetime.today().strftime('%Y-%m-%d'))
        except Cita.DoesNotExist:
            return None

    def get(self, request, id_paciente,id_doctor, *args, **kwargs):
        citas_instance = self.get_citas(id_paciente,id_doctor)        
        if not citas_instance:
            return Response(
                {"res": "Object with that id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )    
        Serializer = CitaSerializer(citas_instance, many=True)
        return Response(Serializer.data, status=status.HTTP_200_OK)

class  PagosConsultasListApiView(APIView):
    def get(self, request, *args, **kwargs):
        pagos_consultas = PagosConsulta.objects.all()
        serializer = PagosConsultaSerializer(pagos_consultas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = {
            'id_consulta': request.data.get('id_consulta'),
            'monto': request.data.get('monto'),
        }

        serializer = PagosConsultaSerializer(data=data)
        if serializer.is_valid():
             serializer.save()
             return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PagosConsultasDetailApiView(APIView):

    def get_object(self, id_pago_consulta):
        try:
            return PagosConsulta.objects.get(id_pago_consulta=id_pago_consulta)
        except PagosConsulta.DoesNotExist:
            return None

    def get(self, request, id_pago_consulta, *args, **kwargs):
        pago_consuta_instance = self.get_object(id_pago_consulta)
        if not pago_consuta_instance:
            return Response(
                {"res": "Object with that id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = PagosConsultaSerializer(pago_consuta_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request,id_pago_consulta, *args, **kwargs):
        pago_consuta_instance = self.get_object(id_pago_consulta)
        if not pago_consuta_instance:
            return Response(
                {"res": "Object with that id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        data = {
            'id_consulta': request.data.get('id_consulta'),
            'monto': request.data.get('monto'),
        }
        serializer = PagosConsultaSerializer(instance = pago_consuta_instance, data=data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id_pago_consulta, *args, **kwargs):
        pago_consuta_instance = self.get_object(id_pago_consulta)
        if not pago_consuta_instance:
            return Response(
                {"res": "Object with that id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        pago_consuta_instance.delete()
        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )

class  LaboratoriosListApiView(APIView):
    def get(self, request, *args, **kwargs):
        laboratorios = Laboratorio.objects.all()
        serializer = LaboratorioSerializer(laboratorios, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = {
            'Nombres': request.data.get('Nombres'),
        }

        serializer = LaboratorioSerializer(data=data)
        if serializer.is_valid():
             serializer.save()
             return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LaboratoriosDetailApiView(APIView):

    def get_object(self, id_lab):
        try:
            return Laboratorio.objects.get(id_Lab=id_lab)
        except Laboratorio.DoesNotExist:
            return None

    def get(self, request, id_lab, *args, **kwargs):
        laboratorio_instance = self.get_object(id_lab)
        if not laboratorio_instance:
            return Response(
                {"res": "Object with that id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = LaboratorioSerializer(laboratorio_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request,id_lab, *args, **kwargs):
        laboratorio_instance = self.get_object(id_lab)
        if not laboratorio_instance:
            return Response(
                {"res": "Object with that id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        data = {
            'Nombres': request.data.get('Nombres'),
        }
        serializer = LaboratorioSerializer(instance = laboratorio_instance, data=data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id_lab, *args, **kwargs):
        laboratorio_instance = self.get_object(id_lab)
        if not laboratorio_instance:
            return Response(
                {"res": "Object with that id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        laboratorio_instance.delete()
        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )

class  RayosXListApiView(APIView):
    def get(self, request, *args, **kwargs):
        rayosx = Rayos_X.objects.all()
        serializer = RayosXSerializer(rayosx, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = {
            'Tipo': request.data.get('Tipo'),
            'id_Consulta': request.data.get('id_Consulta'),
            'id_Lab': request.data.get('id_Lab'),
        }

        serializer = RayosXSerializer(data=data)
        if serializer.is_valid():
             serializer.save()
             return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RayosXDetailApiView(APIView):

    def get_object(self, id_rayos):
        try:
            return Rayos_X.objects.get(id_Rayos=id_rayos)
        except Rayos_X.DoesNotExist:
            return None

    def get(self, request, id_rayos, *args, **kwargs):
        rayosx_instance = self.get_object(id_rayos)
        if not rayosx_instance:
            return Response(
                {"res": "Object with that id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = RayosXSerializer(rayosx_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request,id_rayos, *args, **kwargs):
        rayosx_instance = self.get_object(id_rayos)
        if not rayosx_instance:
            return Response(
                {"res": "Object with that id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        data = {
            'Tipo': request.data.get('Tipo'),
            'id_Consulta': request.data.get('id_Consulta'),
            'id_Lab': request.data.get('id_Lab'),
        }
        serializer = RayosXSerializer(instance = rayosx_instance, data=data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id_rayos, *args, **kwargs):
        rayosx_instance = self.get_object(id_rayos)
        if not rayosx_instance:
            return Response(
                {"res": "Object with that id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        rayosx_instance.delete()
        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )

class  MedicinasListApiView(APIView):
    def get(self, request, *args, **kwargs):
        medicinas = Medicina.objects.all()
        serializer = MedicinaSerializer(medicinas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = {
            'nombre': request.data.get('nombre'),
            'tipo': request.data.get('tipo'),
        }

        serializer = MedicinaSerializer(data=data)
        if serializer.is_valid():
             serializer.save()
             return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MedicinasDetailApiView(APIView):

    def get_object(self, id_med):
        try:
            return Medicina.objects.get(id_med=id_med)
        except Medicina.DoesNotExist:
            return None

    def get(self, request, id_med, *args, **kwargs):
        medicina_instance = self.get_object(id_med)
        if not medicina_instance:
            return Response(
                {"res": "Object with that id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = MedicinaSerializer(medicina_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request,id_med, *args, **kwargs):
        medicina_instance = self.get_object(id_med)
        if not medicina_instance:
            return Response(
                {"res": "Object with that id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        data = {
            'nombre': request.data.get('nombre'),
            'tipo': request.data.get('tipo'),
        }
        serializer = MedicinaSerializer(instance = medicina_instance, data=data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id_med, *args, **kwargs):
        medicina_instance = self.get_object(id_med)
        if not medicina_instance:
            return Response(
                {"res": "Object with that id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        medicina_instance.delete()
        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )

class  RecetasListApiView(APIView):
    def get(self, request, *args, **kwargs):
        recetas = Consulta_Medicina_Receta.objects.all()
        serializer = RecetaSerializer(recetas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = {
            'id_Med': request.data.get('id_Med'),
            'Desc': request.data.get('Desc'),
            'id_Consulta': request.data.get('id_Consulta'),
        }

        serializer = RecetaSerializer(data=data)
        if serializer.is_valid():
             serializer.save()
             return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RecetasDetailApiView(APIView):

    def get_object(self, id_receta):
        try:
            return Consulta_Medicina_Receta.objects.get(id_Receta=id_receta)
        except Consulta_Medicina_Receta.DoesNotExist:
            return None

    def get(self, request, id_receta, *args, **kwargs):
        medicina_instance = self.get_object(id_receta)
        if not medicina_instance:
            return Response(
                {"res": "Object with that id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = RecetaSerializer(medicina_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request,id_receta, *args, **kwargs):
        receta_instance = self.get_object(id_receta)
        if not receta_instance:
            return Response(
                {"res": "Object with that id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        data = {
            'id_Med': request.data.get('id_Med'),
            'Desc': request.data.get('Desc'),
            'id_Consulta': request.data.get('id_Consulta'),
        }
        serializer = RecetaSerializer(instance = receta_instance, data=data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id_receta, *args, **kwargs):
        receta_instance = self.get_object(id_receta)
        if not receta_instance:
            return Response(
                {"res": "Object with that id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        receta_instance.delete()
        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )