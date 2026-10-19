from django.http import HttpRequest
from django.shortcuts import render
from datetime import datetime
from urllib.parse import urlparse

# Create your views here.

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
    
    def __init__(self, ip_client: str | None, url: str, parametri: dict[str, str] = {}) -> None:
        self.id: int = Accesare.contor 
        Accesare.contor +=1
        
        self.ip_client: str = ip_client or "undefined"
        self.url: str = url
        self.parametri: dict[str, str] = parametri
        self.data: datetime = datetime.now()
        
        path = urlparse(self.url).path
        self._pagina = "/" if len(path) == 0 else path 
        
    def lista_parametri(self):
        return [
            (nume, valoare)
            for nume, valoare in self.parametri.items()
        ]
    
    def string_url(self):
        return self.url
    
    def pagina(self):
        return self._pagina
    
    def calculeaza_data(self, data = ""):
        format = ""

        if data == "zi":
            format = "%d %B %Y"
        elif data == "timp":
            format = "%H:%M:%S"
        else: format = "%A, %d %B %Y"
        
        if format.find("%A") != -1:
            format = format.replace("%A", ZILE_SAPTAMANA[self.data.weekday()])
        if format.find("%B") != -1:
            format = format.replace("%B", LUNI[self.data.month - 1])
        if format.find("%a") != -1:
            format = format.replace("%a", ZILE_ABRV[self.data.weekday()])
        if format.find("%b") != -1:
            format = format.replace("%b", LUNI_ABRV[self.data.month - 1])
            
        return self.data.strftime(format)
    
    def __str__(self) -> str:
        return "\n".join([
            f"id: {self.id}",
            f"ip_client: {self.ip_client}",
            f"string_url: {self.string_url()}",
            f"pagina: {self.pagina()}",
            f"calculeaza_data: {self.calculeaza_data()}",
            f"lista_parametri: {self.lista_parametri()}",
        ])

def creaza_accesare(request:HttpRequest):
    return Accesare(request.META.get("REMOTE_ADDR"),request.build_absolute_uri(),request.GET)

def index(request:HttpRequest):
    return render(request, 'index.html')

def info(request):
    accesare = request.accesare
    paramteru_data = accesare.parametri.get("data") or ""
    
    data_formatata = accesare.calculeaza_data(paramteru_data)
    dt = accesare.data.isoformat()
    return render(request, 'info.html', {"data_formatata":data_formatata, "datetime" : dt})

