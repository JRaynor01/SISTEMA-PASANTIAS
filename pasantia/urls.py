from django.urls import path

from .views import *

app_name = "pasantia"

urlpatterns = [
    path('create/post', HomeViewPostulacion, name="pasantia-edit"),
    path('create/postpasantia', Createpostpasantia, name='createpost'),
    path('modify/<pasantia>/', modificarPasantia, name="modpost"),
    path('create/registentidad',createEntidad, name="createntidad"),
    path('create/postulacion/<pasantia>', crearPostulacion, name='postulacion'),
    path('revpost/<pasantia>', revpost,name="rev_postulacion"),
    path('revdoc/<username>', revdoc, name="rev_doc"),
    path('postulacion/registro/',crearPostulacion, name='postulacionhecha'),
    path('sorteo/<pasantia>/', sorteo, name="sorteo"),
    path('<pasantia>/unidades', registrarunidades, name="registrounidades"),
    path('<pasantia>/unidades/<id>', registrarestudiantes, name="asignarestudiantes"),
    path('view/pdf/<body>/', pdfpasantia, name="verpdf"),
]

