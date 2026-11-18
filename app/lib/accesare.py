from django.http import HttpRequest, QueryDict
from datetime import datetime
from urllib.parse import urlparse

ZILE_SAPTAMANA = [
    "Luni",
    "Marți",
    "Miercuri",
    "Joi",
    "Vineri",
    "Sâmbătă",
    "Duminică",
]

ZILE_ABRV = [
    "Lun",
    "Mar",
    "Mie",
    "Joi",
    "Vin",
    "Sâm",
    "Dum",
]

LUNI = [
    "Ianuarie",
    "Februarie",
    "Martie",
    "Aprilie",
    "Mai",
    "Iunie",
    "Iulie",
    "August",
    "Septembrie",
    "Octombrie",
    "Noiembrie",
    "Decembrie",
]

LUNI_ABRV = [
    "Ian",
    "Feb",
    "Mar",
    "Apr",
    "Mai",
    "Iun",
    "Iul",
    "Aug",
    "Sep",
    "Oct",
    "Noi",
    "Dec"
]

class Accesare:
    contor = 0
    accesari = []
    map_nr_accesari_pe_pagini: dict[str,int] = {}
    
    def __init__(self, ip_client: str | None, url: str, parametri: QueryDict = QueryDict()) -> None:
        self.id: int = Accesare.contor 
        Accesare.contor +=1
        
        self.ip_client: str = ip_client or "undefined"
        self.url: str = url
        self.parametri: QueryDict = parametri
        self.data: datetime = datetime.now()
        
        path = urlparse(self.url).path       
        self._pagina = "/" if len(path) == 0 else path 
        
        Accesare.accesari.append(self)
        Accesare.map_nr_accesari_pe_pagini[self._pagina] = Accesare.map_nr_accesari_pe_pagini.get(self._pagina, 0) + 1
        
    def lista_parametri(self):
        return [
            (nume, valoare)
            for nume, valoare in self.parametri.lists()
        ]
    
    def string_url(self):
        return self.url
    
    def pagina(self):
        return self._pagina
    
    def formateaza_data(self, format: str):
        format = format.replace("%A", ZILE_SAPTAMANA[self.data.weekday()])
        format = format.replace("%B", LUNI[self.data.month - 1])
        format = format.replace("%a", ZILE_ABRV[self.data.weekday()])
        format = format.replace("%b", LUNI_ABRV[self.data.month - 1])
            
        return self.data.strftime(format)
    
    def calculeaza_data(self, data = ""):
        format = ""

        if data == "zi":
            format = "%d %B %Y"
        elif data == "timp":
            format = "%H:%M:%S"
        else: format = "%A, %d %B %Y"
        
        return self.formateaza_data(format)
    
    def __str__(self) -> str:
        return "\n ".join([
            f"id: {self.id}",
            f"ip_client: {self.ip_client}",
            f"string_url: {self.string_url()}",
            f"pagina: {self.pagina()}",
            f"calculeaza_data: {self.calculeaza_data()}",
            f"lista_parametri: {self.lista_parametri()}",
        ])
        
    def detalii_data(self):
        return self.formateaza_data("%A, %d %B %Y, %H:%M:%S")
      
    @staticmethod  
    def get_accesare(id:int):
      return Accesare.accesari[id] if 0 <= id < len(Accesare.accesari) else None
    
    @staticmethod
    def get_accesari(startId:int, endId:int):
      return Accesare.accesari[startId:endId] if 0 <= startId < len(Accesare.accesari) and 0 <= endId < len(Accesare.accesari) else None
    
    @staticmethod
    def get_ultimele_accesari(n:int):
      return Accesare.accesari[-n:] if n > 0 and n <= len(Accesare.accesari) else None
    
    @staticmethod
    def get_pagina_cea_mai_accesata():
      return max(Accesare.map_nr_accesari_pe_pagini.items(), key=lambda x: x[1])
    
    @staticmethod
    def get_pagina_cea_mai_putin_accesata() -> tuple[str,int]:
      return min(Accesare.map_nr_accesari_pe_pagini.items(), key=lambda x: x[1])

def creaza_accesare(request:HttpRequest):
    return Accesare(request.META.get("REMOTE_ADDR"),request.build_absolute_uri(),request.GET)

class HttpRequestCuAccesare(HttpRequest):
    accesare:Accesare
    
def isValidId(id:str):
    try:
        intId = int(id)
        if intId < 0 or intId >= Accesare.contor:
            return False
        return intId == float(id)
    except ValueError:
        return False
      
  

    