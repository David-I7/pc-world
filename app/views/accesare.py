from django.shortcuts import render
from ..lib.accesare import HttpRequestCuAccesare, Accesare, isValidId

def handler(request: HttpRequestCuAccesare, id:int):
    if not isValidId(str(id)):
        return render(request, 'accesare.html', {"eroare": "ID invalid"})
    return render(request, 'accesare.html', {"id": id, "accesare": Accesare.accesari[len(Accesare.accesari) - int(id) - 1]})