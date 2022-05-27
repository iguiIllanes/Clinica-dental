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

from django.shortcuts import render
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse

from django.views.decorators.csrf import csrf_exempt

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions

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

