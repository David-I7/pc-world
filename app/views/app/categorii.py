from django.shortcuts import render
from ...models import Categorie
from ...utils.produse.listare_produse import COLOANE_SORTARE_COMUNE, proceseaza_listare_produse


def handler(request, nume_categorie):
    categorie = Categorie.objects.filter(nume=nume_categorie).first()
    if categorie is None:
        return render(
            request,
            'app/eroare.html',
            {
                'titlu_eroare': 'Categoria nu a fost găsită',
                'mesaj_eroare': f'Categoria "{nume_categorie}" nu există în catalogul nostru.',
                'cod_eroare': 404,
            },
            status=404,
        )

    queryset = categorie.produse.select_related('laptop', 'procesor', 'placavideo')

    context = proceseaza_listare_produse(
        request,
        queryset,
        COLOANE_SORTARE_COMUNE,
    )
    context.update({
        'titlu_pagina': categorie.nume,
        'categorie': categorie,
    })
    return render(request, 'app/produse/lista_produse.html', context)
