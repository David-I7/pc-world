from django.urls import path, re_path
from .views import info, log, accesare, test
from .views.app import contact, cos, despre, index, istoric, promotii, favorite, categorii
from .views.app.produse import laptopuri, procesoare, placi_video
from django.conf import settings

urlpatterns = [
    path('info/', info.handler, name='info'),
    path('log/', log.handler, name='log'),
    re_path(r'accesare/(?P<id>\d+)/', accesare.handler, name='accesare'),
    path('test/', test.handler, name='test'),
    
    # App URLs
    path('', index.handler, name='index'),
    path('istoric/', istoric.handler, name='istoric'),
    path('despre/', despre.handler, name='despre'),
    path('cos/', cos.handler, name='cos'),
    path('contact/', contact.handler, name='contact'),
    path('promotii/', promotii.handler, name='promotii'),
    path('favorite/', favorite.handler, name='favorite'),
    
    # Produse URLs
    path('laptopuri/', laptopuri.handler, name='laptopuri'),
    path('laptopuri/<slug:slug>/', laptopuri.detaliu, name='laptop_detaliu'),
    path('procesoare/', procesoare.handler, name='procesoare'),
    path('procesoare/<slug:slug>/', procesoare.detaliu, name='procesor_detaliu'),
    path('placi-video/', placi_video.handler, name='placi_video'),
    path('placi-video/<slug:slug>/', placi_video.detaliu, name='placa_video_detaliu'),
    path('categorii/<str:nume_categorie>/', categorii.handler, name='categorie'),
]

if settings.DEBUG:
    urlpatterns += [
        path('test/<int:id>/<path:subpath>/', test.handler, name='test'),
        re_path(r'^test2/(?P<id>\d+)/(?P<subpath>.+)/$', test.handler, name='test'),
    ]
