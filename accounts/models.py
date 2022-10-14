from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
import os
from PIL import Image
from django.db.models.signals import post_save

def user_directory_path_ci(instance, filename):
    profile_picture_name = 'users/{0}/ci.pdf'.format(instance.user.username)
    full_path = os.path.join(settings.MEDIA_ROOT, profile_picture_name)
    
    if os.path.exists(full_path):
        os.remove(full_path)
        
    return profile_picture_name

def user_directory_path_hoja(instance, filename):
    profile_picture_name = 'users/{0}/hoja_vida.pdf'.format(instance.user.username)
    full_path = os.path.join(settings.MEDIA_ROOT, profile_picture_name)
    
    if os.path.exists(full_path):
        os.remove(full_path)
        
    return profile_picture_name

def user_directory_path_record(instance, filename):
    profile_picture_name = 'users/{0}/record.pdf'.format(instance.user.username)
    full_path = os.path.join(settings.MEDIA_ROOT, profile_picture_name)
    
    if os.path.exists(full_path):
        os.remove(full_path)
        
    return profile_picture_name

def user_directory_path_boleta(instance, filename):
    profile_picture_name = 'users/{0}/boleta.pdf'.format(instance.user.username)
    full_path = os.path.join(settings.MEDIA_ROOT, profile_picture_name)
    
    if os.path.exists(full_path):
        os.remove(full_path)
        
    return profile_picture_name

def user_directory_path_conc(instance, filename):
    profile_picture_name = 'users/{0}/conclusion_estudios.pdf'.format(instance.user.username)
    full_path = os.path.join(settings.MEDIA_ROOT, profile_picture_name)
    
    if os.path.exists(full_path):
        os.remove(full_path)
        
    return profile_picture_name

CARGO_OPTIONS = (
    ('administrador', 'administrador'),
    ('estudiante', 'estudiante'),
)

DOCUMENTS_OPTIONS = (
    ('aceptado', 'aceptado'),
    ('pendiente', 'pendiente'),
    ('rechazado', 'rechazado'),
)

class User(AbstractUser):
    second_last_name = models.CharField(max_length=150, blank=True)
    ci = models.CharField(max_length=10, null=True)
    tipo = models.CharField(max_length=15, choices=CARGO_OPTIONS, default='estudiante')
    
class Profile(models.Model):
    #User info
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    birthday = models.DateField(null=True, blank=True)
    puntaje_gral = models.DecimalField(max_digits=5, decimal_places=2,null=True, blank = True)
    celular = models.CharField(max_length=8, blank=True)
    grado = models.CharField(max_length=9, blank=True)
    
    #documentos necesarios
    ci_doc = models.FileField(upload_to=user_directory_path_ci, blank=True)
    est_ci = models.CharField(max_length=15, choices=DOCUMENTS_OPTIONS, default='rechazado')
    hoja_vida_doc = models.FileField(upload_to=user_directory_path_hoja, blank=True)
    est_hoja_vida = models.CharField(max_length=15, choices=DOCUMENTS_OPTIONS, default='rechazado')
    record_doc = models.FileField(upload_to=user_directory_path_record, blank=True)
    est_record_doc = models.CharField(max_length=15, choices=DOCUMENTS_OPTIONS, default='rechazado')
    bol_insc_doc = models.FileField(upload_to=user_directory_path_boleta, blank=True)
    est_bol_insc = models.CharField(max_length=15, choices=DOCUMENTS_OPTIONS, default='rechazado')
    conc_est_doc = models.FileField(upload_to=user_directory_path_conc, blank=True)
    est_conc_est = models.CharField(max_length=15, choices=DOCUMENTS_OPTIONS, default='rechazado')
    
    def __str__(self):
        return self.user.username
    
#a prueba
def create_user_profile(sender, instance, created, **kwargs):
    if created and instance.tipo == 'estudiante':
        Profile.objects.create(user=instance)
        
def save_user_profile(sender, instance, **kwargs):
    if instance.tipo == 'estudiante':
        instance.profile.save()
        
#create profile
post_save.connect(create_user_profile, sender=User)
#save profile
post_save.connect(save_user_profile, sender=User)