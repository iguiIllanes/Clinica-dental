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


class PersonasApiView(APIView):
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
    

class PersonaApiView(APIView):
    def get_persona(self, persona_id):
        try:
            return Persona.objects.get(id_persona=persona_id);
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


class PacientesApiView(APIView):
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
        
class MedicosListApiView(APIView):
    # add permission to check if user is authenticated
    #permission_classes = [permissions.IsAuthenticated]

    # 1. List all
    def get(self, request, *args, **kwargs):
        '''
        List all the todo items for given requested user
        '''
        medicos = Medico.objects.all()#filter(user = request)
        serializer = MedicoSerializer(medicos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 2. Create
    def post(self, request, *args, **kwargs):
        '''
        Create the Todo with given todo data
        '''
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

