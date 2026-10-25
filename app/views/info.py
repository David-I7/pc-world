from django.shortcuts import render

def handler(request):
    accesare = request.accesare
    data = accesare.parametri.get("data") or ""
    
    data_formatata = accesare.calculeaza_data(data)
    dt = accesare.data.isoformat()
    return render(request, 'info.html', {"data_formatata":data_formatata, "datetime" : dt})
