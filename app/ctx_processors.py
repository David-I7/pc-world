from datetime import datetime
from django.db.models import Count
from .models import Categorie

def footer(request):
    return {
        'email_suport': 'suport@pcworld.com',
        'copyright': f'© {datetime.now().year} PC World. Toate drepturile rezervate.',
        'an_infiintare': 2025,
        'nume_firma': 'PC World',
        'numar_telefon': '+40 123 456 789',
        'adresa': 'Str. Florilor, nr. 1, Sector 1, București',
        'numar_sedii': 10,
        'numar_angajati': 87,
    }

def categorii_meniu(request):
    categorii = (
        Categorie.objects.annotate(numar_produse=Count('produse'))
        .filter(numar_produse__gt=0)
        .order_by('nume')
    )
    return {
        'categorii_meniu': categorii,
    }