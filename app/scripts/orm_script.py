from datetime import timedelta, date
from decimal import Decimal
from django.contrib.auth.models import User
from django.db import connection
from django.forms.models import model_to_dict
import json
from urllib.parse import urlencode, unquote
from django.utils.text import slugify
from pprint import pprint
from ..models import Categorie, Produs, Laptop, Procesor, PlacaVideo, Stoc, Depozit, Adresa, Promotie
from django.db.models import Prefetch
import requests

def run(): 
  # print(Stoc.objects.all().delete())
  #print(Produs.objects.filter(taguri__len__gt=1))
  # produse = Produs.objects.all()
  # for produs in produse:
  #   produs.taguri = []
  
  # Produs.objects.bulk_update(produse, ['taguri'])
  # produs = list(Procesor.objects.all().values());
  # if produs:
  #   print(json.dumps(produs, indent=4, default=str))
  categorii = Categorie.objects.all()
  for categorie in categorii:
    if categorie.sigla:
      url_sigla = unquote(categorie.sigla.url.split('/media/')[1].replace('%3A', ':/'));
      folder = 'C:\\Users\\Dave2swag\\Downloads'
      response = requests.get(url_sigla)
      if response.status_code == 200:
        with open(f"{folder}/{categorie.nume}.svg", 'w+') as f:
          f.write(response.text)
        print(f"Sigla pentru categoria {categorie.nume} a fost salvata in {folder}/{categorie.nume}.svg")
    else:
      print(f"Categoria {categorie.nume} nu are sigla.")
    
    

