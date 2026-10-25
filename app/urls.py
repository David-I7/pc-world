from django.urls import path, re_path
from .views import info, log, accesare
from .views.app import contact, cos, despre, index, istoric, produse, promotii, favorite

urlpatterns = [
    path('', index.handler, name='index'),
    path('info/', info.handler, name='info'),
    path('log/', log.handler, name='log'),
    path('istoric/', istoric.handler, name='istoric'),
    path('despre/', despre.handler, name='despre'),
    re_path(r'accesare/(?P<id>\d+)/', accesare.handler, name='accesare'),
    path('produse/', produse.handler, name='produse'),
    path('cos/', cos.handler, name='cos'),
    path('contact/', contact.handler, name='contact'),
    path('promotii/', promotii.handler, name='promotii'),
    path('favorite/', favorite.handler, name='favorite')
]
