from ...models import Produs, Laptop, PlacaVideo, Procesor
from .unitati_produse import normalizeaza_unitate, UNITATI_PRODUSE, UNITATI

def genereaza_specificatii_cheie(produs):
  specificatii = []
  if produs.tip_produs == Produs.TipProdus.LAPTOP:
      obj = produs if isinstance(produs, Laptop) else getattr(produs, 'laptop', None)
      if obj:
        specificatii = [('Procesor', obj.nume_procesor)]
        
        valoare_ram, unitate_ram = normalizeaza_unitate(obj.capacitate_ram, UNITATI_PRODUSE['laptop']['capacitate_ram'], UNITATI['stocare'])
        specificatii.append(('Memorie',f"{valoare_ram} {unitate_ram} RAM"))
        
        valoare_capacitate_stocare, unitate_stocare = normalizeaza_unitate(obj.capacitate_stocare, UNITATI_PRODUSE['laptop']['capacitate_stocare'], UNITATI['stocare'])
        specificatii.append(('Stocare',f"{valoare_capacitate_stocare} {unitate_stocare} {obj.tip_stocare}"))
        
        valoare_rata_refresh, unitate_rata_refresh = normalizeaza_unitate(float(obj.rata_refresh), UNITATI_PRODUSE['laptop']['rata_refresh'], UNITATI['frecventa'], preserve_float=True)
        specificatii.append(('Ecran', f"{obj.dimensiune_ecran}\" {valoare_rata_refresh} {unitate_rata_refresh}"))
        
        return specificatii
  elif produs.tip_produs == Produs.TipProdus.PLACA_VIDEO:
      obj = produs if isinstance(produs, PlacaVideo) else getattr(produs, 'placavideo', None)
      if obj:
          specificatii = []
          
          valoare_memorie, unitate_memorie = normalizeaza_unitate(obj.memorie, UNITATI_PRODUSE['placa_video']['memorie'], UNITATI['stocare'])
          specificatii.append(('Memorie', f"{valoare_memorie} {unitate_memorie} VRAM"))
          
          valoare_frecventa, unitate_frecventa = normalizeaza_unitate(float(obj.frecventa), UNITATI_PRODUSE['placa_video']['frecventa'], UNITATI['frecventa'], preserve_float=True)
          specificatii.append(('Frecvență', f"{valoare_frecventa} {unitate_frecventa}"))
          
          specificatii.append(('Interfață', obj.interfata))
          
          return specificatii
  elif produs.tip_produs == Produs.TipProdus.PROCESOR:
      obj = produs if isinstance(produs, Procesor) else getattr(produs, 'procesor', None)
      if obj:
        nr_threaduri = obj.numar_threaduri if obj.numar_threaduri is not None else obj.numar_nuclee
        specificatii = [('Nuclee / Thread-uri', f'{obj.numar_nuclee} / {nr_threaduri}')]

        valoare_frecventa, unitate_frecventa = normalizeaza_unitate(float(obj.frecventa), UNITATI_PRODUSE['procesor']['frecventa'],UNITATI['frecventa'], preserve_float=True)
        specificatii.append(('Frecvență', f"{valoare_frecventa} {unitate_frecventa}"))
        
        specificatii.append(('Socket', obj.socket))
        
        valoare_tdp, unitate_tdp = normalizeaza_unitate(float(obj.putere_totala_disipata), UNITATI_PRODUSE['procesor']['putere_totala_disipata'],UNITATI['putere'], preserve_float=True)
        specificatii.append(('TDP', f"{valoare_tdp} {unitate_tdp}"))
        
        return specificatii
  return specificatii

def genereaza_specificatii_detaliate(produs):
    specificatii = []
    if produs.tip_produs == Produs.TipProdus.LAPTOP:
        obj = produs if isinstance(produs, Laptop) else getattr(produs, 'laptop', None)
        if obj:
          specificatii = [('Procesor', obj.nume_procesor)]
          specificatii.append(('Placă video', obj.placa_video))
          
          valoare_ram, unitate_ram = normalizeaza_unitate(obj.capacitate_ram, UNITATI_PRODUSE['laptop']['capacitate_ram'],UNITATI['stocare'])
          specificatii.append(('Memorie',f"{valoare_ram} {unitate_ram} RAM"))
          
          valoare_capacitate_stocare, unitate_stocare = normalizeaza_unitate(obj.capacitate_stocare, UNITATI_PRODUSE['laptop']['capacitate_stocare'],UNITATI['stocare'])
          specificatii.append(('Stocare',f"{valoare_capacitate_stocare} {unitate_stocare} {obj.tip_stocare}"))
          
          valoare_rata_refresh, unitate_rata_refresh = normalizeaza_unitate(float(obj.rata_refresh), UNITATI_PRODUSE['laptop']['rata_refresh'],UNITATI['frecventa'], preserve_float=True)
          specificatii.append(('Ecran', f"{obj.dimensiune_ecran}\" {valoare_rata_refresh} {unitate_rata_refresh}"))
          
          specificatii.append(('Sistem de operare', str(Laptop.SistemOperare(obj.sistem_de_operare).label)))
          specificatii.append(('Greutate', f"{obj.greutate} kg"))
          
          return specificatii
    elif produs.tip_produs == Produs.TipProdus.PLACA_VIDEO:
        obj = produs if isinstance(produs, PlacaVideo) else getattr(produs, 'placavideo', None)
        if obj:
            specificatii = [('Model GPU', obj.model)]
            
            valoare_memorie, unitate_memorie = normalizeaza_unitate(obj.memorie, UNITATI_PRODUSE['placa_video']['memorie'],UNITATI['stocare'])
            specificatii.append(('Memorie', f"{valoare_memorie} {unitate_memorie} VRAM"))
            
            specificatii.append(('Tip memorie', obj.tip_memorie))
            
            valoare_frecventa, unitate_frecventa = normalizeaza_unitate(float(obj.frecventa), UNITATI_PRODUSE['placa_video']['frecventa'],UNITATI['frecventa'], preserve_float=True)
            specificatii.append(('Frecvență', f"{valoare_frecventa} {unitate_frecventa}"))
            
            specificatii.append(('Interfață', obj.interfata))
            
            return specificatii
    elif produs.tip_produs == Produs.TipProdus.PROCESOR:
        obj = produs if isinstance(produs, Procesor) else getattr(produs, 'procesor', None)
        if obj:
          nr_threaduri = obj.numar_threaduri if obj.numar_threaduri is not None else obj.numar_nuclee
          specificatii = [('Serie', obj.serie), ('Nucleu', obj.nucleu), ('Socket', obj.socket), ('Număr nuclee', obj.numar_nuclee), ('Număr threaduri', nr_threaduri)]
          
          valoare_frecventa, unitate_frecventa = normalizeaza_unitate(float(obj.frecventa), UNITATI_PRODUSE['procesor']['frecventa'],UNITATI['frecventa'], preserve_float=True)
          specificatii.append(('Frecvență', f"{valoare_frecventa} {unitate_frecventa}"))
           
          valoare_tdp, unitate_tdp = normalizeaza_unitate(float(obj.putere_totala_disipata), UNITATI_PRODUSE['procesor']['putere_totala_disipata'],UNITATI['putere'], preserve_float=True)
          specificatii.append(('TDP', f"{valoare_tdp} {unitate_tdp}"))
          
          if obj.memorie_cache_l1 is not None:
              valoare_cache_l1, unitate_cache_l1 = normalizeaza_unitate(float(obj.memorie_cache_l1), UNITATI_PRODUSE['procesor']['memorie_cache_l1'],UNITATI['stocare'], preserve_float=True)
              specificatii.append(('Memorie cache L1', f"{valoare_cache_l1} {unitate_cache_l1}"))
          else:
              specificatii.append(('Memorie cache L1', '-'))
          if obj.memorie_cache_l2 is not None:
              valoare_cache_l2, unitate_cache_l2 = normalizeaza_unitate(float(obj.memorie_cache_l2), UNITATI_PRODUSE['procesor']['memorie_cache_l2'],UNITATI['stocare'], preserve_float=True)
              specificatii.append(('Memorie cache L2', f"{valoare_cache_l2} {unitate_cache_l2}"))
          else:
              specificatii.append(('Memorie cache L2', '-'))
          if obj.memorie_cache_l3 is not None:
              valoare_cache_l3, unitate_cache_l3 = normalizeaza_unitate(float(obj.memorie_cache_l3), UNITATI_PRODUSE['procesor']['memorie_cache_l3'],UNITATI['stocare'],preserve_float=True)
              specificatii.append(('Memorie cache L3', f"{valoare_cache_l3} {unitate_cache_l3}"))
          else:
              specificatii.append(('Memorie cache L3', '-'))
          
    return specificatii