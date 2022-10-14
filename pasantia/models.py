from email.policy import default
from django.db import models
from django.utils import timezone
import os
from django.conf import settings
from django.contrib.auth import get_user_model
User = get_user_model()

OPTIONS = (
    ('REVISION','REVISION'),
    ('FINALIZADO','FINALIZADO'),
)

OPTIONS_UNIDAD = (
    ('REVISION','REVISION'),
    ('ASIGNADO','ASIGNADO'),
)

OPTIONS_ESTADO = (
    ('REVISION','REVISION'),
    ('FINALIZADO','FINALIZADO'),
    ('ASIGNADO', 'ASIGNADO')
)

OPTIONS_EST = (
    ('RECHAZADO','RECHAZADO'),
    ('PENDIENTE','PENDIENTE'),
    ('ACEPTADO','ACEPTADO'),
    ('ASIGNADO','ASIGNADO'),
)

def user_directory_path_file(instance, filename):
    profile_picture_name = 'postpasantias/{0}.pdf'.format(instance.body)
    full_path = os.path.join(settings.MEDIA_ROOT, profile_picture_name)
    
    if os.path.exists(full_path):
        os.remove(full_path)
        
    return profile_picture_name

def entidad_directory_path(instance, filename):
    profile_picture_name = 'entidades/{0}.jpg'.format(instance.nombre)
    full_path = os.path.join(settings.MEDIA_ROOT, profile_picture_name)
    
    if os.path.exists(full_path):
        os.remove(full_path)
        
    return profile_picture_name

class Entidad(models.Model):
    nombre = models.CharField(max_length=100, blank=True, unique=True)
    image = models.ImageField(upload_to=entidad_directory_path, blank=True, null=True)
    
    def __str__(self):
        return self.nombre

class PostPasantias(models.Model):
    body=models.CharField(max_length=50, unique=True)
    cantidad = models.PositiveIntegerField(default=1)
    fecha_limite = models.DateTimeField()
    created_on = models.DateTimeField(default=timezone.now, blank=True)
    file = models.FileField(upload_to=user_directory_path_file)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_author')
    cantidad_insc = models.PositiveIntegerField(default=0)
    entidad_pert = models.ForeignKey(Entidad, on_delete=models.CASCADE, related_name='post')
    estado = models.CharField(max_length=20, choices=OPTIONS_ESTADO, default='REVISION')


    def __str__(self):
        return self.body

class Unidad(models.Model):
    nombre = models.CharField(max_length=100, blank=True)
    cantidad = models.PositiveIntegerField(default=1)
    entidad_pert = models.ForeignKey(Entidad, on_delete=models.CASCADE, related_name='unidad')
    pasantia_pert = models.ForeignKey(PostPasantias, on_delete=models.CASCADE, related_name='unidad')
    estado = models.CharField(max_length=20, choices=OPTIONS_UNIDAD, default='REVISION')
    
    def __str__(self):
        return f'{self.nombre} {self.pasantia_pert}'        
         
class Postulaciones(models.Model):
    estudiante = models.ForeignKey(User, on_delete=models.CASCADE)
    postpasantia = models.ForeignKey(PostPasantias, on_delete=models.DO_NOTHING)
    estadopas = models.CharField(max_length=20, choices=OPTIONS, default='REVISION')
    estadoest = models.CharField(max_length=20, choices=OPTIONS_EST, default='PENDIENTE')
    
    def __str__(self):
        return f'{self.postpasantia} {self.estudiante}'
    
    
class Postulantes_Unidad(models.Model):
    estudiante = models.ForeignKey(User, on_delete=models.CASCADE)
    unidad = models.ForeignKey(Unidad, on_delete=models.CASCADE)
    fecha_finalizacion = models.DateTimeField(default=timezone.now, blank=True)
    
    def __str__(self):
        return f'{self.estudiante} a la unidad {self.unidad}'