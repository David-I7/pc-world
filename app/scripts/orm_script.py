from datetime import timedelta, date
from decimal import Decimal
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db import connection
from django.forms.models import model_to_dict
import json
from urllib.parse import urlencode, unquote
from django.utils.text import slugify
from pprint import pprint
from ..models import Categorie, Produs, Laptop, Procesor, PlacaVideo, Stoc, Depozit, Adresa, Promotie,Brand
from django.db.models import Prefetch, Sum
import requests

def run(): 
  
  # laptopuri = (Laptop.objects.select_related('brand')
  #   .prefetch_related('categorii')
  #   .annotate(stoc_total=Sum('stocuri__cantitate', default=0))
  #   .filter(slug='categorie-fara-')
  #   .first()
  # )
  
  #apple = Brand.objects.filter(nume__icontains='apple').get()
  #produse_apple = apple.produse.all()
  #for produs in produse_apple:
  # print(produs)
  
  produse = (
        Laptop.objects.select_related('brand')
        .prefetch_related('categorii')
        .annotate(stoc_total=Sum('stocuri__cantitate', default=0))
        .first()
    )
  
  pprint(connection.queries[2:])

    
    

