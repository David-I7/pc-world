from .unitati_produse import UNITATI_PRODUSE, normalizeaza_unitate, UNITATI

from ...models import Laptop
import re

def get_brand_procesor(laptop):
    match = re.search(r'^(Intel|AMD|Apple)', laptop.nume_procesor)
    if match:
        nume_procesor = match.group(1)
        if nume_procesor == "Apple":
            return "Apple Silicon"
        return nume_procesor
    return "Procesor Necunoscut"

def genereaza_taguri_laptop(laptop):
    tags = ['Laptop', laptop.brand.nume]
    tags.append(f"{get_brand_procesor(laptop)}")
    tags.append(str(Laptop.SistemOperare(laptop.sistem_de_operare).label))
    valoare_ram, unitate_ram = normalizeaza_unitate(laptop.capacitate_ram, UNITATI_PRODUSE['laptop']['capacitate_ram'],UNITATI['stocare'])
    tags.append(f"{valoare_ram} {unitate_ram} RAM")
    valoare_capacitate_stocare, unitate_stocare = normalizeaza_unitate(laptop.capacitate_stocare, UNITATI_PRODUSE['laptop']['capacitate_stocare'],UNITATI['stocare'])
    tags.append(f"{valoare_capacitate_stocare} {unitate_stocare} {laptop.tip_stocare}")
    valoare_rata_refresh, unitate_rata_refresh = normalizeaza_unitate(float(laptop.rata_refresh), UNITATI_PRODUSE['laptop']['rata_refresh'],UNITATI['frecventa'], preserve_float=True)
    tags.append(f"{valoare_rata_refresh} {unitate_rata_refresh}")
    tags.append(f"{int(laptop.dimensiune_ecran)} inch")
    
    return tags
  
def genereaza_taguri_placa_video(placa_video):
  tags = ['Placa Video', placa_video.brand.nume]
  valoare_memorie, unitate_memorie = normalizeaza_unitate(placa_video.memorie, UNITATI_PRODUSE['placa_video']['memorie'],UNITATI['stocare'])
  tags.append(f"{valoare_memorie} {unitate_memorie} VRAM")
  tags.append(placa_video.interfata)
  
  return tags

def genereaza_taguri_procesor(procesor):
  tags = ['Procesor', procesor.brand.nume, procesor.socket]
  tags.append(f"{procesor.numar_nuclee}-nuclee")
  tags.append(f"{procesor.numar_threaduri}-threaduri")
  
  return tags
 