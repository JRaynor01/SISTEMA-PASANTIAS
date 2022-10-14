from django.shortcuts import render, get_object_or_404,redirect
from django.views.generic import TemplateView, View
from accounts.forms import EditProfileForm, DocumentUploadForm
from accounts.models import Profile
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from pasantia.models import Postulaciones
from django.utils import timezone

User = get_user_model()

#Modificar mis datos personales
@login_required
def EditProfile(request):
    user = request.user.id
    profile = Profile.objects.get(user__id=user)
    user_basic_info = User.objects.get(id=user)
    
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=profile)
        if form.is_valid():
            profile.celular = form.cleaned_data.get('celular')
            messages.success(request, 'Dato actualizado')
            profile.save()
            return redirect('users:edit')
    else:
        form = EditProfileForm(instance=profile)
    
    context={
        'form':form,
        'profile':profile,
        'view':'home',
    }    
    return render(request, 'users/edit.html', context)

@login_required
def DocumentUploadProfile(request):
    user = request.user.id
    profile = Profile.objects.get(user__id=user)
    try:
        postulacion = Postulaciones.objects.filter(estudiante__id=user)
        postulacion = postulacion.get(estadopas='REVISION')
    except (Postulaciones.DoesNotExist):
        estado='sincambios'
        postulacion=''
    else:
        estado='encurso'
        if postulacion.postpasantia.fecha_limite < timezone.now():
            estado='encalificacion'
    
    if request.method == 'POST':
        form = DocumentUploadForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            if form.cleaned_data.get('ci_doc') != None :
                profile.est_ci = 'pendiente'
            if form.cleaned_data.get('hoja_vida_doc') != None :
                profile.est_hoja_vida = 'pendiente'
            if form.cleaned_data.get('record_doc') != None :
                profile.est_record_doc = 'pendiente'
            if form.cleaned_data.get('bol_insc_doc') != None :
                profile.est_bol_insc = 'pendiente'
            if form.cleaned_data.get('conc_est_doc') != None :
                profile.est_conc_est = 'pendiente'
            profile.ci_doc = form.cleaned_data.get('ci_doc')
            profile.hoja_vida_doc = form.cleaned_data.get('hoja_vida_doc') 
            profile.record_doc = form.cleaned_data.get('record_doc') 
            profile.bol_insc_doc = form.cleaned_data.get('bol_insc_doc') 
            profile.conc_est_doc = form.cleaned_data.get('conc_est_doc') 
            messages.success(request, 'Documentos subido o actualizados correctamente')
            profile.save()
            return redirect('users:profile-document')
        else:
            messages.success(request, 'Ocurrio un error al actualizar los documetnos')
    else:
        form = DocumentUploadForm(instance=profile)
    
    context={
        'estado':estado,
        'postulacion':postulacion,
        'form':form,
        'profile':profile,
    }    
    return render(request, 'users/document.html', context)
