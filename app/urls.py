from django.urls import path, re_path
from .views import info, log, accesare
from .views.app import contact, cos, despre, index, istoric, promotii, favorite
from .views.app.produse import laptopuri, procesoare, placi_video
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', index.handler, name='index'),
    path('info/', info.handler, name='info'),
    path('log/', log.handler, name='log'),
    path('istoric/', istoric.handler, name='istoric'),
    path('despre/', despre.handler, name='despre'),
    re_path(r'accesare/(?P<id>\d+)/', accesare.handler, name='accesare'),
    path('laptopuri/', laptopuri.handler, name='laptopuri'),
    path('procesoare/', procesoare.handler, name='procesoare'),
    path('placi-video/', placi_video.handler, name='placi_video'),
    path('cos/', cos.handler, name='cos'),
    path('contact/', contact.handler, name='contact'),
    path('promotii/', promotii.handler, name='promotii'),
    path('favorite/', favorite.handler, name='favorite'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
