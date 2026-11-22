import random
from ..models import Depozit, Produs, Stoc


def run():
    produse = Produs.objects.all()
    depozite = Depozit.objects.all()
    
    if not produse.exists() or not depozite.exists():
        print("Nu există produse sau depozite în baza de date.")
        return

    depozite_produse: dict[int,set[int]] = {}

    # 1. Garantam ca fiecare depozit are cel putin un produs
    for depozit in depozite:
        produs = random.choice(produse)
        depozite_produse[depozit.pk] = set([produs.pk])

    # 2. Garantam ca fiecare produs exista in cel putin un depozit,
    #    iar o parte dintre produse exista în mai multe depozite
    numar_depozite = len(depozite)
    for produs in produse:
        numar_depozite_produs = random.randint(1, numar_depozite);

        for _ in range(numar_depozite_produs):
            depozit = random.choice(depozite)
            depozite_produse[depozit.pk].add(produs.pk)

    # 3. Fiecare inregistrare de stoc primeste o cantitate aleatoare
    stocuri = [
        Stoc(
            produs_id=produs_id,
            depozit_id=depozit_id,
            cantitate=random.randint(1, 6)
        )
        for depozit_id, produse in depozite_produse.items()
        for produs_id in produse
    ]

    # 4. Inseram inregistrarile de stoc in baza de date, actualizand cantitatea daca exista deja o inregistrare pentru acel produs si depozit
    Stoc.objects.bulk_create(
        stocuri,
        update_conflicts=True,
        unique_fields=['produs', 'depozit'],
        update_fields=['cantitate'],
    )

    print(
        f"Au fost initializate {len(stocuri)} inregistrari de stoc pentru {len(produse)} produse in {len(depozite)} depozite."
    )
