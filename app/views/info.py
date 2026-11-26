from django.shortcuts import render

from app.lib.accesare import HttpRequestCuAccesare

def handler(request: HttpRequestCuAccesare):
    accesare = request.accesare
    parametru_data = accesare.parametri.get("data") or ""
    
    data_formatata = accesare.calculeaza_data(parametru_data)
    dt = accesare.data.isoformat()
    return render(request, 'info.html', {"data_formatata":data_formatata, "datetime" : dt})
