import json
import re

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from urllib import request
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
        data = {
            "id_persona": request.data.get("id_persona"),
            "correo_paciente": request.data.get("correo_paciente"),
            "usuario": request.data.get("usuario"),
            "password": request.data.get("password"),
            "alergias": request.data.get("alergias"),
            "enfermedades_base": request.data.get("enfermedades_base"),
        }

        serializer = PacienteSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    

class PacientesDetailApiView(APIView):
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

