from django.db.models import Sum
from django.shortcuts import render

from ....utils.produse.specificatii import genereaza_specificatii_detaliate
from ....models import PlacaVideo
from ....utils.produse.listare_produse import COLOANE_SORTARE_PLACA_VIDEO, construieste_context_detaliu, proceseaza_listare_produse

def handler(request):
    context = proceseaza_listare_produse(
        request,
        PlacaVideo.objects.all(),
        COLOANE_SORTARE_PLACA_VIDEO,
    )
    context.update({
        'titlu_pagina': 'Plăci Video',
        'subtitlu_pagina': 'Performanță grafică pentru gaming, randare 3D și inteligență artificială.',
        'categorie': None,
    })
    return render(request, 'app/produse/lista_produse.html', context)


def detaliu(request, slug):
    produs = (
        PlacaVideo.objects.select_related('brand')
        .prefetch_related('categorii')
        .annotate(stoc_total=Sum('stocuri__cantitate', default=0))
        .filter(slug=slug)
        .first()
    )
    if produs is None:
        return render(
            request,
            'app/eroare.html',
            {
                'titlu_eroare': 'Placa video nu a fost găsită',
                'mesaj_eroare': f'Nu există nicio placă video cu identificatorul "{slug}".',
                'cod_eroare': 404,
            },
            status=404,
        )

    return render(
        request,
        'app/produse/detaliu_produs.html',
        construieste_context_detaliu(produs),
    )
