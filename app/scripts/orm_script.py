from datetime import timedelta, date
from decimal import Decimal
from django.contrib.auth.models import User
from django.db import connection
from django.utils.text import slugify
from pprint import pprint
from ..models import Categorie, Produs, Laptop, Procesor, PlacaVideo, Stoc, Depozit, Adresa, Promotie
from django.db.models import Prefetch

def run(): 
  print(Stoc.objects.all())

    
    

