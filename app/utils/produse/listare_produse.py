from typing import Any
from urllib.parse import urlencode
from pc_world.settings import PROD_PER_PAG, PRODUSE_DISPLAY_K, PRODUSE_SIMILARE_K, STOC_MIN
from django.core.paginator import Paginator
from django.db.models import Sum
from django.utils import timezone

from .promotii import (
    prefetch_promotii_active,
    ataseaza_cea_mai_buna_promotie,
    obtine_promotii_active_queryset,
    sorteaza_produse_dupa_pret_efectiv,
)
from .specificatii import genereaza_specificatii_cheie, genereaza_specificatii_detaliate
from ...models import Produs

COLOANE_SORTARE_COMUNE = [
    ('nume', 'Nume'),
    ('pret', 'Preț'),
    ('data_lansare', 'Dată lansare'),
    ('stoc', 'Stoc'),
]

COLOANE_SORTARE_LAPTOP = COLOANE_SORTARE_COMUNE + [
    ('capacitate_ram', 'Memorie RAM'),
    ('capacitate_stocare', 'Stocare'),
    ('dimensiune_ecran', 'Dimensiune ecran'),
]

COLOANE_SORTARE_PLACA_VIDEO = COLOANE_SORTARE_COMUNE + [
    ('memorie', 'Memorie VRAM'),
    ('frecventa', 'Frecvență'),
]

COLOANE_SORTARE_PROCESOR = COLOANE_SORTARE_COMUNE + [
    ('numar_nuclee', 'Număr nuclee'),
    ('frecventa', 'Frecvență'),
]


def construieste_url_query(base_path, col='', sort_dir='', tags=None, page=None):
    params = []
    if col:
        params.append(('col', col))
    if sort_dir:
        params.append(('sort', sort_dir))
    if tags:
        for tag in tags:
            params.append(('tag', tag))
    if page is not None:
        params.append(('page', str(page)))
    if not params:
        return base_path
    return f"{base_path}?{urlencode(params)}"


def formateaza_garantie(duration):
    if not duration:
        return '-'
    days = duration.days
    if days >= 365 and days % 365 == 0:
        ani = days // 365
        return f"{ani} {'an' if ani == 1 else 'ani'}"
    if days >= 30 and days % 30 == 0:
        luni = days // 30
        return f"{luni} {'lună' if luni == 1 else 'luni'}"
    return f"{days} {'zi' if days == 1 else 'zile'}"


def proceseaza_listare_produse(request, queryset, coloane_sortare):
    now = timezone.now()
    qs = (
        queryset.select_related('brand')
        .prefetch_related('categorii', prefetch_promotii_active(now))
        .annotate(stoc_total=Sum('stocuri__cantitate', default=0))
    )

    active_tags = []
    for tag in request.GET.getlist('tag'):
        if tag not in active_tags:
            active_tags.append(tag)

    if active_tags:
        qs = qs.filter(taguri__contains=active_tags)

    allowed_cols = {col_key for col_key, _ in coloane_sortare}
    current_col = request.GET.get('col', '').strip()
    current_sort = request.GET.get('sort', '').strip().lower()

    if current_col not in allowed_cols:
        current_col = 'data_lansare'
    if current_sort not in ('a', 'd'):
        current_sort = 'a'

    per_page = PROD_PER_PAG
    if current_col == 'pret':
        produse_cu_promotii = ataseaza_cea_mai_buna_promotie(qs)
        produse_sortate = sorteaza_produse_dupa_pret_efectiv(
            produse_cu_promotii,
            descrescator=(current_sort == 'd'),
        )
        paginator = Paginator(produse_sortate, per_page)
        page_obj = paginator.get_page(request.GET.get('page', 1))
        produse_list = list(page_obj.object_list)
    else:  
        order_field = 'stoc_total' if current_col == 'stoc' else current_col
        if current_sort == 'd':
            qs = qs.order_by(f'-{order_field}', 'id')
        else:
            current_sort = 'a'
            qs = qs.order_by(order_field, 'id')

        paginator = Paginator(qs, per_page)
        page_obj = paginator.get_page(request.GET.get('page', 1))
        produse_list = ataseaza_cea_mai_buna_promotie(list(page_obj.object_list))

    total_count = paginator.count
    start_index = page_obj.start_index() if total_count > 0 else 0
    end_index = page_obj.end_index() if total_count > 0 else 0

    base_path = request.path
    for produs in produse_list:
        produs.listare = "DETALIATA" #type: ignore
        produs.specificatii_scurte = genereaza_specificatii_cheie(produs) # type: ignore
        produs.taguri_linkuri = [] # type: ignore
        for tag in produs.taguri or []:
            next_tags = active_tags if tag in active_tags else active_tags + [tag]
            produs.taguri_linkuri.append({ #type: ignore
                'nume': tag,
                'activ': tag in active_tags,
                'url': construieste_url_query(
                    base_path,
                    col=current_col,
                    sort_dir=current_sort,
                    tags=next_tags,
                ),
            })

    active_tags_links = [
        {
            'nume': tag,
            'url_elimina': construieste_url_query(
                base_path,
                col=current_col,
                sort_dir=current_sort,
                tags=[t for t in active_tags if t != tag],
            ),
        }
        for tag in active_tags
    ]

    url_pagina_anterioara = (
        construieste_url_query(
            base_path,
            col=current_col,
            sort_dir=current_sort,
            tags=active_tags,
            page=page_obj.previous_page_number(),
        )
        if page_obj.has_previous()
        else None
    )
    url_pagina_urmatoare = (
        construieste_url_query(
            base_path,
            col=current_col,
            sort_dir=current_sort,
            tags=active_tags,
            page=page_obj.next_page_number(),
        )
        if page_obj.has_next()
        else None
    )
    url_reset_sortare = construieste_url_query(base_path, tags=active_tags)

    return {
        'page_obj': page_obj,
        'produse': produse_list,
        'total_count': total_count,
        'start_index': start_index,
        'end_index': end_index,
        'active_tags': active_tags,
        'active_tags_links': active_tags_links,
        'current_col': current_col,
        'current_sort': current_sort,
        'coloane_sortare': coloane_sortare,
        'url_pagina_anterioara': url_pagina_anterioara,
        'url_pagina_urmatoare': url_pagina_urmatoare,
        'url_reset_sortare': url_reset_sortare,
        'stoc_min': STOC_MIN,
    }
 

def obtine_produse_similare(produs, k=None):
    if k is None:
        k = PRODUSE_SIMILARE_K

    categorii_ids = list(produs.categorii.values_list('id', flat=True))
    if not categorii_ids:
        return []

    now = timezone.now()
    produse: list[Any] = list(
        Produs.objects.filter(categorii__id__in=categorii_ids)
        .exclude(pk=produs.pk)
        .select_related('brand')
        .prefetch_related(prefetch_promotii_active(now))
        .distinct()
        .order_by('?')[:k]
    )

    ataseaza_cea_mai_buna_promotie(produse)
    for p in produse:
        p.listare = "COMPACTA"

    return produse


def obtine_produse_display(tip_produs: Produs.TipProdus, k=None):
    if k is None:
        k = PRODUSE_DISPLAY_K

    now = timezone.now()
    produse_cu_promotii: list[Any] = list(
        Produs.objects.filter(tip_produs=tip_produs)
        .select_related('brand')
        .prefetch_related(prefetch_promotii_active(now))
        .order_by('?')[:k]
    )

    ataseaza_cea_mai_buna_promotie(produse_cu_promotii)
    for p in produse_cu_promotii:
        p.listare = "COMPACTA"

    return produse_cu_promotii


def obtine_produse_promotii(k=None):
    if k is None:
        k = PRODUSE_DISPLAY_K

    now = timezone.now()
    promotii_active = obtine_promotii_active_queryset(now).order_by('data_sfarsit')
    produse_cu_promotii: list[Any] = []
    seen_ids: set[int] = set()

    for promotie in promotii_active:
        limit = k - len(produse_cu_promotii)
        if limit <= 0:
            break
        batch = (
            promotie.produse.exclude(pk__in=seen_ids)
            .select_related('brand')
            .prefetch_related(prefetch_promotii_active(now))
            .order_by('?')[:limit]
        )
        for p in batch:
            seen_ids.add(p.pk)
            produse_cu_promotii.append(p)

    ataseaza_cea_mai_buna_promotie(produse_cu_promotii)
    for p in produse_cu_promotii:
        p.listare = "COMPACTA"

    return produse_cu_promotii


def construieste_context_detaliu(produs):
    ataseaza_cea_mai_buna_promotie([produs])
    return {
        'produs': produs,
        'specificatii': genereaza_specificatii_detaliate(produs),
        'garantie_formatata': formateaza_garantie(produs.durata_garantie),
        'produse_similare': obtine_produse_similare(produs),
        'stoc_min': STOC_MIN,
    }
