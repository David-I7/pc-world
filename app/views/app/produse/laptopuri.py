from django.db.models import Sum
from django.shortcuts import render

from ....utils.produse.specificatii import genereaza_specificatii_detaliate
from ....models import Laptop
from ....utils.produse.listare_produse import COLOANE_SORTARE_LAPTOP,construieste_context_detaliu, proceseaza_listare_produse

def handler(request):
    context = proceseaza_listare_produse(
        request,
        Laptop.objects.all(),
        COLOANE_SORTARE_LAPTOP,
    )
    context.update({
        'titlu_pagina': 'Laptopuri',
        'subtitlu_pagina': 'Descoperă gama noastră de laptopuri pentru gaming, business și uz zilnic.',
        'categorie': None,
    })
    return render(request, 'app/produse/lista_produse.html', context)


def detaliu(request, slug):
    produs = (
        Laptop.objects.select_related('brand')
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
                'titlu_eroare': 'Laptopul nu a fost găsit',
                'mesaj_eroare': f'Nu există niciun laptop cu identificatorul "{slug}".',
                'cod_eroare': 404,
            },
            status=404,
        )

    return render(
        request,
        'app/produse/detaliu_produs.html',
        construieste_context_detaliu(produs),
    )
