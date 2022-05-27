from django.db import models

class Persona(models.Model):
    id_persona = models.AutoField(primary_key=True)
    ci = models.IntegerField()
    nombre = models.CharField(max_length=255)
    apellido = models.CharField(max_length=255)
    telefono = models.IntegerField()
    fecha_nacimiento = models.DateField()
    class Meta:
        unique_together = ["ci","nombre", "apellido", "fecha_nacimiento"]
    def __str__(self):
        return str(self.id_persona) + " " + self.nombre +  " " + self.apellido

class Laboratorio(models.Model):
    id_Lab = models.AutoField(primary_key=True)
    Nombres = models.CharField(max_length=255)
    def __str__(self):
        return self.id_Lab + ' ' +self.Nombres


    
class Servicio(models.Model):
    id_servicio = models.AutoField(primary_key=True)
    nombre_servicio = models.CharField(max_length=255)

class Paciente(models.Model):
    id_persona = models.OneToOneField(Persona, primary_key=True, on_delete=models.CASCADE)
    correo_paciente = models.CharField(max_length=255)
    usuario = models.CharField(max_length=255,unique=True)
    password = models.CharField(max_length=255)
    alergias = models.CharField(max_length=255)
    enfermedades_base = models.CharField(max_length=255)
    def __str__(self):
        return str(self.id_persona) + ' ' + self.usuario
    

class Medico(models.Model):
    id_persona = models.OneToOneField(Persona, primary_key=True, on_delete=models.CASCADE)
    fecha_contrato = models.DateTimeField()
    usuario = models.CharField(max_length=255,unique=True)
    password = models.CharField(max_length=255)
    contratado = models.BooleanField()
    correo_institucional = models.CharField(max_length=255)
    def __str__(self):
        return str(self.id_persona) + ' ' + self.usuario

class Especialidad(models.Model):
    id_especialidad = models.AutoField(primary_key=True)
    especialidad = models.CharField(max_length=255)
    def __str__(self):
        return self.id_especialidad + " " + self.especialidad

class MedicoEspecialidad(models.Model):
    id_med_esp = models.AutoField(primary_key=True)
    id_especialidad = models.ForeignKey(Especialidad, on_delete=models.CASCADE)
    fecha_titulo = models.DateTimeField()
    medico_id_persona = models.ForeignKey(Medico, on_delete=models.CASCADE)
    def __str__(self):
        return self.id_med_esp

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
    monto = models.FloatField()
    id_tarjeta = models.ForeignKey(Tarjeta, on_delete=models.CASCADE)
    id_cita = models.ForeignKey(Cita, on_delete=models.CASCADE)
    def str(self) -> str:
        return self.id_pago + ' ' +self.monto

class Consulta(models.Model):
    id_Consulta = models.AutoField(primary_key=True)
    id_Cita = models.ForeignKey(Cita, on_delete=models.CASCADE)
    Descripcion = models.CharField(max_length=255)
    MontoTotal = models.FloatField()
    id_Servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    def __str__(self):
        return self.id_Consulta + ' ' + self.id_Cita + ' ' +self.id_Servicio

class PagosConsulta(models.Model):
    id_pago_consulta = models.AutoField(primary_key=True)
    id_consulta = models.ForeignKey(Consulta, on_delete=models.CASCADE)
    monto = models.FloatField()
    def __str__(self):
        return self.id_pago_consulta

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