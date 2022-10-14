from email import message
from multiprocessing import context
from accounts.models import Profile, User
from django.utils import timezone
from django.http import HttpResponse
from django.views.generic import TemplateView, View
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .forms import PasantiaPostForm, EntidadRegisterForm
from .models import Entidad, PostPasantias, Postulaciones, Postulantes_Unidad, Unidad
from django.contrib import messages
from accounts.forms import DocumentUploadForm
from django.db.models import Q

import os
from django.conf import settings
from django.template.loader import get_template
from xhtml2pdf import pisa

#ES ADMIN
def esadmin(request, user, plantilla, context):
    if user.tipo == "administrador":
        return render(request, plantilla, context)
    else:
        messages.error(request, "Acceso denegado")
        return redirect('home')
    
def modecha(fecha):
    if fecha.month<10:
        if fecha.day<10:
            return f'{fecha.year}-0{fecha.month}-0{fecha.day}'
        else:
            return f'{fecha.year}-0{fecha.month}-{fecha.day}'
    else:
        if fecha.day<10:
            return f'{fecha.year}-{fecha.month}-0{fecha.day}'
        else:
            return f'{fecha.year}-{fecha.month}-{fecha.day}'
#CREAR DICCIONARIO
def pasantia_dic(pasantia):
    output={}
    output["body"]=pasantia.body
    output["cantidad"]=pasantia.cantidad
    output["entidad"]=pasantia.entidad.nombre
    
    return output
    
def estudiantes_post(estudiantes):
    output=[]
    for estudiante in estudiantes:
        output_int={}
        output_int["id"] = estudiante.id
        output_int["first_name"] = estudiante.first_name
        output_int["last_name"] = estudiante.last_name
        output_int["second_last_name"] = estudiante.second_last_name
        output_int["ci"] = estudiante.ci
        
        output.append(output_int)
    
    return output
#Estudiantes designados
def asignados(postulaciones):
    output=[]
    for postulante in postulaciones:
        output.append(postulante.estudiante)
    return output
    
#DATOS
@login_required
def HomeViewPostulacion(request):
    #View tiene dos funciones get y post 
    #para recibir informacion y get para obtenerla
    logged_in_user = request.user
    if logged_in_user.tipo == 'administrador':  
        return render(request, 'pasantia/agregar.html')
    else:
        messages.error(request, 'No tiene acceso a la pagina')
        return redirect('home')
    
class CreatePostPasantia(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        
        logged_in_user = request.user
        
        if logged_in_user.tipo == 'administrador':
        
            form = PasantiaPostForm()
            entidad = Entidad.objects.all()
            
            context={
                'entidad':entidad,
                'form':form,
            }
            return render(request, 'pasantia/createpost.html', context)
        else:
            messages.error(request, 'No tiene acceso a la pagina')
            return redirect('home')
        
    def post(self, request, *args, **kwargs):
        
        logged_in_user = request.user
        entidad = Entidad.objects.get(nombre=request.POST['entidad'])
        cantidad_unidades = request.POST['num_label']  
            
        form = PasantiaPostForm(request.POST, request.FILES)    
        
        if form.is_valid() and logged_in_user.tipo == 'administrador':
            new_post = form.save(commit=False)
            new_post.entidad_pert = entidad
            new_post.author = logged_in_user
            new_post.save()
            cantidad_total = 0
            for i in range(int(cantidad_unidades)):
                cantidad = request.POST[f'cantidad{i}']
                cantidad_total += int(cantidad)
                unidad = Unidad(nombre=request.POST[f'unidad{i}'].upper(), cantidad=cantidad, entidad_pert=entidad, pasantia_pert=new_post)
                unidad.save()
            new_post.cantidad = cantidad_total
            new_post.save()
          
            messages.success(request, 'Exito en la publicacion')
        else:
            messages.error(request, 'Ocurrio un problema intente de nuevo')
        
        return redirect('pasantia:pasantia-edit')
    
Createpostpasantia = login_required(CreatePostPasantia.as_view())

class CreateEntidad(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        
        logged_in_user = request.user
        
        if logged_in_user.tipo == 'administrador':
        
            form = EntidadRegisterForm()
            
            context={
                'form':form,
            }
            return render(request, 'pasantia/createunit.html', context)
        else:
            messages.error(request, 'No tiene acceso a la pagina')
            return redirect('home')
        
    def post(self, request, *args, **kwargs):
        
        logged_in_user = request.user
        
        form = EntidadRegisterForm(request.POST, request.FILES)
        
        if form.is_valid() and logged_in_user.tipo == 'administrador':
            nombre = form.cleaned_data.get('name')
            nombre = nombre.upper()
            imagen = form.cleaned_data.get('image')
            try:
                Entidad.objects.create(nombre=nombre, image=imagen)
                messages.success(request, 'Entidad añadida exitosamente')
            except:
                messages.error(request, f'La entidad {nombre} ya se encuentra en la BD')
                return redirect('pasantia:createntidad')
        else:
            messages.error(request, 'Ocurrio un error intente nuevamente')
        
        return redirect('pasantia:pasantia-edit')
    
createEntidad = login_required(CreateEntidad.as_view())

class ModificarPasantia(LoginRequiredMixin,View):
    def get(self, request, pasantia, *args, **kwargs):
        entidad = Entidad.objects.all()
        pasantia = PostPasantias.objects.get(body=pasantia)
        fecha_lim = modecha(pasantia.fecha_limite)
        fecha_pub =modecha(pasantia.created_on)
        context={
            'post':pasantia,
            'fecha_lim':fecha_lim,
            'fecha_cre':fecha_pub,
            'entidad':entidad,
        }
        plantilla = 'pasantia/modificarpost.html'
        representacion = esadmin(request, request.user, plantilla, context)
        return representacion
    
    def post(self, request, pasantia, *args, **kwargs):
        pasantia = PostPasantias.objects.get(body=pasantia)
        entidad = Entidad.objects.get(nombre=request.POST['entidad'])
        pasantia.entidad_pert=entidad
        unidades = Unidad.objects.filter(pasantia_pert=pasantia)
        unidades.delete()
        cantidad_unidades = request.POST['num_label']
        cantidad_total = 0
        for i in range(int(cantidad_unidades)):
            cantidad = request.POST[f'cantidad{i}']
            cantidad_total += int(cantidad)
            unidad = Unidad(nombre=request.POST[f'unidad{i}'].upper(), cantidad=cantidad, entidad_pert=entidad, pasantia_pert=pasantia)
            unidad.save()
        pasantia.cantidad = cantidad_total
        pasantia.fecha_limite=request.POST['fecha_limite']
        pasantia.created_on=request.POST['created_on']
        if request.POST['file'] != '':
            pasantia.file=request.POST['file']
        pasantia.save()
        messages.success(request, 'Modifica exitosamente')
        return redirect('home')
        
modificarPasantia = login_required(ModificarPasantia.as_view())

class CrearPostulacion(View):
    def get(self, request, pasantia,*args, **kwargs):
        
        post = PostPasantias.objects.get(body=pasantia)
        
        try:
            postulacion = Postulaciones.objects.filter(estudiante__id=request.user.id)
            postulacion = postulacion.get(estadopas='REVISION')
        except (Postulaciones.DoesNotExist):
            estado='sincambios'
            postulacion=''
        else:
            estado='encurso'
            if postulacion.postpasantia.fecha_limite < timezone.now():
                 estado='encalificacion'
        
        form = DocumentUploadForm()
        
        context={
            'postulacion':postulacion,
            'estado':estado,
            'pasantia':post,
            'form':form,
        }
         
        return render(request, 'pasantia/postulacion.html', context)
    
    def post(self, request, pasantia,*args, **kwargs):
        
        post = PostPasantias.objects.get(body=pasantia)
        
        if post.fecha_limite < timezone.now():
            messages.error(request, 'La postulacion ya llego a su dia limite')
            return redirect('home')
        
        logged_in_user = request.user
        try:
            postulacion = Postulaciones.objects.filter(estudiante__id=logged_in_user.id)
            postulacion = postulacion.get(estadopas='REVISION')
        except (Postulaciones.DoesNotExist):
            new_postulacion = Postulaciones(estudiante=logged_in_user, postpasantia=post)
            post.cantidad_insc += 1
            post.save()
            new_postulacion.save()
            messages.success(request, 'Registro Aceptado')
            return redirect('home')
        else:
            
            messages.success(request, f'Ya te encuentras Postulando a una pasantia {postulacion.postpasantia}')
        
            return redirect('home')

crearPostulacion = login_required(CrearPostulacion.as_view())  

#PARA TRABAJO DIRIGIDO
class Sorteo(View):
    def get(self, request, pasantia,*args, **kwargs):
        estudiantes = User.objects.filter(tipo="estudiante")
        post_est_acep = asignados(Postulaciones.objects.filter(estadoest='ACEPTADO'))
        estudiantes_res = estudiantes.filter(~Q(username__in=post_est_acep))
        pasanti =PostPasantias.objects.get(body=pasantia)
        formu = {}
        for i in range(pasanti.cantidad):
            formu[i]=i
        context={
            'formu':formu,
            'estudiantes':estudiantes_res,
            'pasantia':pasanti,
            'valor':len(estudiantes_res)
        }
        plantilla = 'pasantia/verposts.html'
        representacion = esadmin(request, request.user, plantilla, context)
        return representacion
        #return JsonResponse(datos)
        
    def post(self, request, pasantia,*args, **kwargs):
        pasanti =PostPasantias.objects.get(body=pasantia)
        for i in range(pasanti.cantidad):
            username=request.POST[f'form{i}']
            user=User.objects.get(username=username)
            postulaciones=Postulaciones(estudiante=user, postpasantia = pasanti, estadoest='ACEPTADO')
            postulaciones.save()
        messages.success(request, 'Pasantes registrados')
        
        return redirect('home')
        
sorteo = login_required(Sorteo.as_view())   

#Revision de Postulantes
class RevPost(View):
    def get(self, request, pasantia, *args, **kwargs):
        pasantia = PostPasantias.objects.get(body=pasantia)
        fecha_lim = modecha(pasantia.fecha_limite)
        fecha_pub =modecha(pasantia.created_on)
        
        
        #Estudiantes matriculados en la pasantia
        estudiantes_insc = Postulaciones.objects.filter(postpasantia=pasantia)
        if pasantia.fecha_limite<=timezone.now():
            value=True
        else:
            value =False
                
        plantilla = 'pasantia/verpostulantes.html'
        context = {
            'post':pasantia,
            'fecha_lim':fecha_lim,
            'fecha_cre':fecha_pub,
            'estudiantes_insc':estudiantes_insc,
            'value':value,
        }
        representacion = esadmin(request, request.user, plantilla, context)
        return representacion
    
    def post(self, request, pasantia, *args, **kwargs):
        pasantia = PostPasantias.objects.get(body=pasantia)
        pasantia.estado='FINALIZADO'
        pasantia.save()
        cantidad = pasantia.cantidad
        for i in range(1,cantidad+1):
            postulante = Postulaciones.objects.get(estudiante__ci=request.POST[f'{i}'])
            postulante.estadoest = 'ACEPTADO'
            postulante.save()
        postulantes = Postulaciones.objects.filter(postpasantia=pasantia)
        postulantes.filter(estadoest='PENDIENTE').update(estadoest='RECHAZADO')
        postulantes.update(estadopas='FINALIZADO')
        messages.success(request, f'Estudiantes Registrados en la pasantia {pasantia.body}')
        return redirect('home')
        
    
revpost = login_required(RevPost.as_view())

class RevDoc(View):
    def get(self, request, username, *args, **kwargs):
        profile = Profile.objects.get(user__username = username)
        
        plantilla = 'pasantia/verdoc.html'
        context = {
            'profile':profile,
            
        }
        representacion = esadmin(request, request.user, plantilla, context)
        return representacion
    
    def post(self, request, username,*args, **kwargs):
        profile = Profile.objects.get(user__username = username)
        
        if 'casoci' in request.POST:
            profile.est_ci = request.POST["casoci"]
            messages.success(request, f'Archivo {request.POST["casoci"]}')
        if 'casohv' in request.POST:
            profile.est_hoja_vida = request.POST["casohv"]
            messages.success(request, f'Archivo {request.POST["casohv"]}')
        if 'casora' in request.POST:
            profile.est_record_doc = request.POST["casora"]
            messages.success(request, f'Archivo {request.POST["casora"]}')
        if 'casofm' in request.POST:
            profile.est_bol_insc = request.POST["casofm"]
            messages.success(request, f'Archivo {request.POST["casofm"]}')
        if 'casoce' in request.POST:
            profile.est_conc_est = request.POST["casoce"]
            messages.success(request, f'Archivo {request.POST["casoce"]}')
        
        profile.save()
        
        return redirect('pasantia:rev_doc', username)
        
revdoc = login_required(RevDoc.as_view()) 

class RegistroUnidades(View):
    def get(self, request, pasantia, *args, **kwargs):
        posts = PostPasantias.objects.filter(estado='REVISION')
        posts_acept = PostPasantias.objects.filter(~Q(pk__in=posts))
        post = PostPasantias.objects.get(body=pasantia)
        unidades = Unidad.objects.filter(pasantia_pert=post)
        postulantes_aceptados = Postulaciones.objects.filter(postpasantia=post).filter(estadoest='ACEPTADO')
        
        context={
            'posts':posts_acept,
            'postulantes':postulantes_aceptados,
            'view':'finalizados',
            'pasantia':post,
            'unidades':unidades,
        }
        return render(request, 'pages/finalizadosespecifico.html', context)
registrarunidades = login_required(RegistroUnidades.as_view())

class RegistrarEstudiantes(View):
    def get(self, request, pasantia, id,*args, **kwargs):
        posts = PostPasantias.objects.filter(estado='REVISION')
        posts_acept = PostPasantias.objects.filter(~Q(pk__in=posts))
        post = PostPasantias.objects.get(body=pasantia)
        unidades = Unidad.objects.filter(pasantia_pert=post)
        postulantes_aceptados = Postulaciones.objects.filter(postpasantia=post).filter(estadoest='ACEPTADO')
        unidad = unidades.get(pk=int(id))
        context={
            'posts':posts_acept,
            'postulantes':postulantes_aceptados,
            'view':'finalizados',
            'pasantia':post,
            'unidades':unidades,
            'unidad':unidad,
        }
        return render(request, 'pages/finalizadosespecificounidad.html', context)
    def post(self, request, pasantia, id,*args, **kwargs):
        post = PostPasantias.objects.get(body=pasantia)
        unidades = Unidad.objects.filter(pasantia_pert=post)
        unidad = unidades.get(pk=int(id))
        
        for i in range(unidad.cantidad):
            est_acep = Postulaciones.objects.get(estudiante__username=request.POST[f'{i}'])
            Postulantes_Unidad.objects.create(estudiante = est_acep.estudiante, unidad=unidad)
        messages.success(request, f'Estudiantes añadidos exitosamente a la unidad {unidad} de la pasantia {post}')
        unidad.estado='ASIGNADO'
        unidad.save()
        if len(Postulantes_Unidad.objects.filter(unidad__pasantia_pert=post))==post.cantidad:
            post.estado="ASIGNADO"
            post.save()
        return redirect('postfinalizados')
    
registrarestudiantes = login_required(RegistrarEstudiantes.as_view())

class GenerarPDF(View):
    def link_callback(self, uri, rel):
        """
        Convert HTML URIs to absolute system paths so xhtml2pdf can access those
        resources
        """
        # use short variable names
        sUrl = settings.STATIC_URL  # Typically /static/
        sRoot = settings.STATIC_ROOT  # Typically /home/userX/project_static/
        mUrl = settings.MEDIA_URL  # Typically /static/media/
        mRoot = settings.MEDIA_ROOT  # Typically /home/userX/project_static/media/

        # convert URIs to absolute system paths
        if uri.startswith(mUrl):
            path = os.path.join(mRoot, uri.replace(mUrl, ""))
        elif uri.startswith(sUrl):
            path = os.path.join(sRoot, uri.replace(sUrl, ""))
        else:
            return uri  # handle absolute uri (ie: http://some.tld/foo.png)

        # make sure that file exists
        if not os.path.isfile(path):
            raise Exception(
                'media URI must start with %s or %s' % (sUrl, mUrl)
            )
        return path
    
    def get(self, request, body,*args, **kwargs):
    
        pasantia = PostPasantias.objects.get(body=body)
        unidades = Unidad.objects.filter(pasantia_pert=pasantia)
        postulantes_acep = Postulantes_Unidad.objects.filter(unidad__in=unidades) 
        postulantes_rech = Postulaciones.objects.filter(postpasantia=pasantia).filter(estadoest='RECHAZADO')
        template = get_template('pasantia/reporteP.html')
        context= {
            'post':pasantia,
            'unidades':unidades,
            'postulantes_acep':postulantes_acep,
            'postulantes_rech':postulantes_rech,
            'logo':'{}{}'.format(settings.STATIC_URL, 'images/encabezado2.jpg')
        }
        html = template.render(context)
        response = HttpResponse(content_type='application/pdf')
            #response['Content-Disposition'] = 'attachment; filename="report.pdf"'
            #response['Content-Disposition'] = 'attachment; filename="report.pdf"'
        pisaStatus = pisa.CreatePDF(
            html, dest=response,
            link_callback=self.link_callback
        )
        return response

pdfpasantia = login_required(GenerarPDF.as_view())