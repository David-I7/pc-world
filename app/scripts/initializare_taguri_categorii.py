from ..utils.produse.tags import genereaza_taguri_laptop, genereaza_taguri_placa_video, genereaza_taguri_procesor

from ..models import Categorie, Laptop, PlacaVideo, Procesor, Produs


def run():
    for laptop in Laptop.objects.select_related('brand').all():
        genereaza_taguri_laptop(laptop)
        laptop.taguri = genereaza_taguri_laptop(laptop)
        laptop.save(update_fields=['taguri'])

    for gpu in PlacaVideo.objects.select_related('brand').all():
        gpu.taguri = genereaza_taguri_placa_video(gpu)
        gpu.save(update_fields=['taguri'])

    for cpu in Procesor.objects.select_related('brand').all():
        cpu.taguri = genereaza_taguri_procesor(cpu)
        cpu.save(update_fields=['taguri'])

    Categorie.objects.get_or_create(
        nume='Categorie Fara Produse',
        defaults={
            'descriere': 'Categorie goala folosita exclusiv pentru testarea meniului dinamic.',
            'culoare': '#64748b',
            'sigla': 'sigle_categorii/categorie-fara-produse.svg',
        },
    )

    print(
        f"Taguri actualizate pentru {Produs.objects.count()} produse si categorie goala de test verificata."
    )
