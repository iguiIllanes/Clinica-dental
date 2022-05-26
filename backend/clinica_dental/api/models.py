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