from django.contrib import admin

# Register your models here.

from .models import Persona
from .models import Paciente
from .models import Medico

admin.site.register(Persona)
admin.site.register(Paciente)
admin.site.register(Medico)
