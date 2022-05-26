from django.db import models

class Persona(models.Model):
    id_persona = models.AutoField(primary_key=True)
    ci = models.IntegerField()
    nombre = models.CharField(max_length=255)
    apellido = models.CharField(max_length=255)
    telefono = models.IntegerField()
    fecha_nacimiento = models.DateField()
    def __str__(self):
        return self.id_persona + ' ' + self.nombre


class Paciente(models.Model):
    id_persona = models.ForeignKey(primary_key=True)
    correo_paciente = models.CharField(max_length=255)
    usuario = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    alergias = models.CharField(max_length=255)
    enfermedades_base = models.CharField(max_length=255)
    def __str__(self):
        return self.id_persona + ' ' + self.usuario
    

class Medico(models.Model):
    id_persona = models.ForeignKey(primary_key=True)
    fecha_contrato = models.DateTimeField()
    usuario = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    contratado = models.BooleanField()
    correo_institucional = models.CharField(max_length=255)
    def __str__(self):
        return self.id_persona + ' ' + self.usuario

class MedicoEspecialidad(models.Model):
    id_med_esp = models.AutoField(primary_key=True)
    id_especialidad = models.ForeignKey()
    fecha_titulo = models.DateTimeField()
    medico_id_persona = models.ForeignKey()
    def __str__(self):
        return self.id_med_esp

class Especialidad(models.Model):
    id_especialidad = models.AutoField(primary_key=True)
    especialidad = models.CharField(max_length=255)
    def __str__(self):
        return self.id_especialidad + " " + self.especialidad


    
