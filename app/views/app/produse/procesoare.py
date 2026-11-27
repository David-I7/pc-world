from django.db.models import Sum
from django.shortcuts import render
from django.utils import timezone

from app.models import Procesor
from app.utils.produse.listare_produse import COLOANE_SORTARE_PROCESOR, construieste_context_detaliu, proceseaza_listare_produse
from app.utils.produse.promotii import prefetch_promotii_active

def handler(request):
    context = proceseaza_listare_produse(
        request,
        Procesor.objects.all(),
        COLOANE_SORTARE_PROCESOR,
    )
    context.update({
        'titlu_pagina': 'Procesoare',
        'subtitlu_pagina': 'Procesoare multi-core de ultimă generație pentru desktopuri performante.',
        'categorie': None,
    })
    return render(request, 'app/produse/lista_produse.html', context)


def detaliu(request, slug):
    produs = (
        Procesor.objects.select_related('brand')
        .prefetch_related('categorii', prefetch_promotii_active(timezone.now()))
        .annotate(stoc_total=Sum('stocuri__cantitate', default=0))
        .filter(slug=slug)
        .first()
    )
    if produs is None:
        return render(
            request,
            'app/eroare.html',
            {
                'titlu_eroare': 'Procesorul nu a fost găsit',
                'mesaj_eroare': f'Nu există niciun procesor cu identificatorul "{slug}".',
                'cod_eroare': 404,
            },
            status=404,
        )
    
    return render(
        request,
        'app/produse/detaliu_produs.html',
        construieste_context_detaliu(produs),
    )
