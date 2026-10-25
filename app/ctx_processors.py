from datetime import datetime

def footer_context(request):
    return {
        'email_suport': 'suport@pcworld.com',
        'copyright': f'© {datetime.now().year} PC World. Toate drepturile rezervate.',
        'an_infiintare': 2025,
        'nume_firma': 'PC World',
        'numar_telefon': '+40 123 456 789',
        'adresa': 'Str. Florilor, nr. 1, București',
        'numar_sedii': 10,
        'numar_angajati': 10,
    }