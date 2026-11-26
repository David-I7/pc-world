from django.shortcuts import render
from ..lib.accesare import HttpRequestCuAccesare, Accesare, isValidId

def handler(request: HttpRequestCuAccesare, id:str):
    if not isValidId(id):
        return render(request, 'accesare.html', {"eroare": "ID invalid"})
    return render(request, 'accesare.html', {"id": id, "accesare": Accesare.get_accesare(int(id))})