from copy import PyStringMap
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

class Consulta(models.Model):
    id_Consulta = models.AutoField(primary_key=True)
    id_Cita = models.ForeignKey(Cita, on_delete=models.CASCADE)
    Descripcion = models.CharField(max_length=255)
    MontoTotal = models.FloatField()
    id_Servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    def __str__(self):
        return self.id_Consulta + ' ' + self.id_Cita + ' ' +self.id_Servicio

class Laboratorio(models.Model):
    id_Lab = models.AutoField(primary_key=True)
    Nombres = models.CharField(max_length=255)
    def __str__(self):
        return self.id_Lab + ' ' +self.Nombres

class Rayos_X(models.Model):
    id_Rayos = models.AutoField(primary_key=True)
    Tipo = models.CharField(max_length=255)
    id_Consulta = models.ForeignKey(Consulta,on_delete=models.CASCADE)
    id_Lab = models.ForeignKey(Laboratorio,on_delete=models.CASCADE)
    def __str__(self):
        return self.id_Rayos + ' ' + self.id_Consulta + ' ' + self.id_Lab

class Consulta_Medicina_Receta(models.Model):
    id_Receta = models.AutoField(primary_key=True)
    id_Med = models.ForeignKey(Medicina,on_delete=models.CASCADE)
    Desc = models.CharField(max_length=255)
    id_Consulta = models.ForeignKey(Consulta,on_delete=models.CASCADE)
    def __str__(self):
        return self.id_Receta + ' ' + self.id_Med + ' ' +self.id_Consulta
    
class Servicio(models.Model):
    id_servicio = models.AutoField(primary_key=True)
    nombre_servicio = models.CharField(max_length=255)

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

class Medicina(models.Model):
    id_med = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    tipo = models.CharField(max_length=255)
    def __str__(self):
        return self.id_med + " " + self.nombre


class Cita(models.Model):
    id_cita = models.AutoField(primary_key=True)
    id_paciente = foreing_key=True
    id_doctor = foreign_key=True
    fecha_reserva = models.DateField()
    fecha_consulta = models.DateTimeField()
    def str(self) -> str:
        return self.id_cita + ' ' + self.id_paciente + ' ' + self.id_doctor

class Tarjeta(models.Model):
    id_tarjeta = models.AutoField(primary_key=True)
    fecha_caducidad = models.DateField()
    cvc = models.IntegerField()
    id_paciente = foreing_key=True
    def str(self) -> str:
        return self.id_tarjeta

class PagoReserva(models.Model):
    id_pago = models.AutoField(primary_key=True)
    monto = models.DecimalField(7,2)
    id_tarjeta = foreing_Key=True
    id_cita = foreing_Key=True
    def str(self) -> str:
        return self.id_pago + ' ' +self.monto
