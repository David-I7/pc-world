UNITATI = {
  "stocare" : ["KB", "MB", "GB", "TB", "PB"],
  "putere" : ["W", "KW", "MW", "GW", "TW"],
  "frecventa" : ["Hz", "KHz", "MHz", "GHz", "THz"]
}
UNITATI_PRODUSE = {
    "laptop":{
      "capacitate_ram": "GB",
      "capacitate_stocare": "GB",
      "rata_refresh": "Hz"
    },
    "placa_video":{
      "memorie": "GB",
      "frecventa": "MHz"
    },
    "procesor":{
      "putere_totala_disipata": "W",
      "frecventa": "MHz",
      "memorie_cache_l1": "KB",
      "memorie_cache_l2": "KB",
      "memorie_cache_l3": "KB"
    }
}

def normalizeaza_unitate(valoare: int | float, unitate: str,unitati:list[str], preserve_float: bool = False) -> tuple[int|float, str]:
    while valoare >= 1000 and unitate in unitati:
        if preserve_float:
            valoare = round(valoare / 1000, 2)
        else:
            valoare //= 1000
        unitate = unitati[unitati.index(unitate) + 1]

    valoare_fianla = round(valoare, 2) if preserve_float and int(valoare) != valoare else int(valoare)
    return valoare_fianla, unitate
