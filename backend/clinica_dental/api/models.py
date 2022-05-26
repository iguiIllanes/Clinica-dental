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
