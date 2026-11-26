from django.shortcuts import render

from app.utils.produse.listare_produse import obtine_produse_display, obtine_produse_promotii
from ...models import Produs

def handler(request):
    context = {
      'laptopuri': obtine_produse_display(Produs.TipProdus.LAPTOP),
      'placi_video': obtine_produse_display(Produs.TipProdus.PLACA_VIDEO),
      'procesoare': obtine_produse_display(Produs.TipProdus.PROCESOR),
      'promotii': obtine_produse_promotii(),
    }
    
    return render(request, 'app/index.html', context)