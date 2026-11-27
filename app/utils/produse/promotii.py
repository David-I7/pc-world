from decimal import Decimal, ROUND_HALF_UP
from typing import Any, Iterable

from django.utils import timezone
from django.db.models import Prefetch

from ...models import Promotie, Produs

ZERO_DEC = Decimal('0.00')
SUTA_DEC = Decimal('100.00')
DOUA_ZECIMALE = Decimal('0.01')


def obtine_promotii_active_queryset(now=None):
    now = now or timezone.now()
    return Promotie.objects.filter(data_inceput__lte=now, data_sfarsit__gte=now)

def prefetch_promotii_active(now=None):
  return Prefetch('promotii', queryset=obtine_promotii_active_queryset(now))

def calculeaza_economie_promotie(pret: Decimal, promotie: Promotie) -> Decimal:
    pret_dec = Decimal(pret).quantize(DOUA_ZECIMALE, rounding=ROUND_HALF_UP)
    if pret_dec <= ZERO_DEC:
        return ZERO_DEC

    if promotie.tip_discount == Promotie.TIP_DISCOUNT.PROCENT:
        economie = (pret_dec * Decimal(promotie.discount) / SUTA_DEC).quantize(
            DOUA_ZECIMALE,
            rounding=ROUND_HALF_UP,
        )
    elif promotie.tip_discount == Promotie.TIP_DISCOUNT.SUMA:
        economie = Decimal(promotie.discount).quantize(
            DOUA_ZECIMALE,
            rounding=ROUND_HALF_UP,
        )
    else:
        return ZERO_DEC

    if economie <= ZERO_DEC:
        return ZERO_DEC

    return min(pret_dec, economie)


def formateaza_label_discount(promotie: Promotie, economie: Decimal) -> str:
    if promotie.tip_discount == Promotie.TIP_DISCOUNT.PROCENT:
        return f"-{promotie.discount}%"

    if economie == economie.to_integral_value():
        return f"-{int(economie)} RON"
    return f"-{economie:.2f} RON"


def selecteaza_cea_mai_buna_promotie(
    produs: Produs,
    promotii_active: Any,
) -> dict[str, Any] | None:
    pret_vechi = Decimal(produs.pret).quantize(DOUA_ZECIMALE, rounding=ROUND_HALF_UP)
    candidate: list[tuple[Decimal, Promotie]] = []

    for promotie in promotii_active.all():
        economie = calculeaza_economie_promotie(pret_vechi, promotie)
        if economie > ZERO_DEC:
            candidate.append((economie, promotie))

    if len(candidate) == 0:
        return None

    # Best Discount Wins: cea mai mare economie in RON, apoi promotia care expira mai repede, apoi id-ul cel mai mic.
    best_economie, best_promotie = min(
        candidate,
        key=lambda item: (-item[0], item[1].data_sfarsit, item[1].pk),
    )
    pret_nou = max(ZERO_DEC, (pret_vechi - best_economie).quantize(DOUA_ZECIMALE, rounding=ROUND_HALF_UP))

    return {
        'promotie': best_promotie,
        'tip_discount': best_promotie.tip_discount,
        'label_discount': formateaza_label_discount(best_promotie, best_economie),
        'pret_vechi': pret_vechi,
        'pret_nou': pret_nou,
        'economie': best_economie,
        'numar_promotii_active': len(candidate),
    }

def ataseaza_cea_mai_buna_promotie(produse: list[Produs]):
    if produse is None or len(produse) == 0:
        return []
    for produs in produse:
        if produs.promotii.count() > 0: #type: ignore
          produs.info_promotie = selecteaza_cea_mai_buna_promotie(produs, produs.promotii) #type: ignore
    return produse


def obtine_pret_efectiv(produs: Any) -> Decimal:
    info_promotie = getattr(produs, 'info_promotie', None)
    if info_promotie is not None:
        return info_promotie['pret_nou']
    return produs.pret


def sorteaza_produse_dupa_pret_efectiv(produse: Iterable[Any], descrescator: bool = False) -> list[Any]:
    produse_list = list(produse)
    if descrescator:
        produse_list.sort(key=lambda produs: (-obtine_pret_efectiv(produs), produs.id))
    else:
        produse_list.sort(key=lambda produs: (obtine_pret_efectiv(produs), produs.id))
    return produse_list
