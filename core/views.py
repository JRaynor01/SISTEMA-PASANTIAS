from django.views.generic import TemplateView, View
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.views.decorators.clickjacking import xframe_options_exempt
from pasantia.models import PostPasantias, Postulaciones
from django.db.models import Q
from datetime import date

@login_required
def HomeView(request):
    #View tiene dos funciones get y post 
    #para recibir informacion y get para obtenerla
    posts = PostPasantias.objects.filter(estado='REVISION')
    posts = posts.order_by('-body','fecha_limite')
    context={
        'posts':posts,
        'view':'home'
    }
    return render(request, 'pages/index.html', context)

class ViewInformation(View):
    def get(self, request, post,*args, **kwargs):
        post = PostPasantias.objects.get(body=post)
        
        context={
            'post':post,
        }
        return render(request, 'pages/informacion.html', context)

viewInformation = xframe_options_exempt(ViewInformation.as_view())

class PostRevisados(View):
    def get(self, request, *args, **kwargs):
        posts = PostPasantias.objects.filter(estado='REVISION')
        posts_acept = PostPasantias.objects.filter(~Q(pk__in=posts))
        context={
            'posts':posts_acept,
            'view':'finalizados'
        }
        return render(request, 'pages/finalizados.html', context)

postfinalizados = login_required(PostRevisados.as_view())

class Buscador(View):
    def post(self, request, *args, **kwargs):
        posts = PostPasantias.objects.all()
        if request.POST["nro"] != "":
            posts = posts.filter(body=request.POST["nro"])
        if request.POST["fecha_ini"] !="":
            posts = posts.filter(created_on=request.POST["fecha_ini"])
            #posts = posts.filter(created_on__range=[request.POST["fecha_ini"], date.today()])
        if request.POST["fecha_fin"] !="":
            posts = posts.filter(fecha_limite=request.POST["fecha_fin"])
            #posts = posts.filter(fecha_limite__range=["2019-01-01",request.POST["fecha_ini"]])
        if request.POST["estado"] != "":
            posts = posts.filter(estado=request.POST["estado"])
        posts = posts.order_by('-body','fecha_limite')
        context={
            'posts':posts,
            'view':'home'
        }
        return render(request, 'pages/index.html', context)

buscador = login_required(Buscador.as_view())