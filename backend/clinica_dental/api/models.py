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

<<<<<<< HEAD
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
    




=======
class Servicio(models.Model):
    id_servicio = models.AutoField(primary_key=True)
    nombre_servicio = models.CharField(max_length=255)

    def __str__(self):
        return self.id_servicio

class PagosConsulta(models.Model):
    id_pago_consulta =  models.AutoField(primary_key=True)
    id_consulta = models.ForeignKey(Consulta)
    monto = models.FloatField()

    def __str__(self):
        return self.id_pago_consulta
class Medicina(models.Model):
    id_med = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    tipo = models.CharField(max_length=255)
    def __str__(self):
        return self.id_med
>>>>>>> c77c59e7604901e229fc5d80da1919bdbd1c1a87
