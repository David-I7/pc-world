from django.shortcuts import render
from ..lib.accesare import Accesare, HttpRequestCuAccesare, isValidId


def handler(request:HttpRequestCuAccesare):
    accesare: Accesare = request.accesare  
    ultimele = accesare.parametri.get("ultimele")
    accesari = accesare.parametri.get("accesari")
    iduri = accesare.parametri.getlist("iduri")
    dubluri = accesare.parametri.get("dubluri",False)
    tabel = accesare.parametri.get("tabel","")
        
    context: dict[str, object] = {
        "eroare_accesari": None,
        "accesari": None,
        "nr_accesari": str(len(Accesare.accesari)) if accesari == "nr" else None,
        "afisare": "tabel" if tabel != "" else "lista",
        "atribute": None
    }
    
    coloane = ["id", "ip_client", "url", "pagina", "parametri", "data"]
    colane_tabel = coloane if tabel == "tot" else tabel.split(",")
    
    if tabel != "":
        for col in colane_tabel:
            if col not in coloane:
                context['eroare_accesari'] = f"Coloana '{col}' nu este validă. Coloanele valide sunt: {', '.join(coloane)}"
                return render(request, 'log.html', context, status=400)
        
        context["atribute"] = colane_tabel
    else:
        if accesari != "detalii":
            coloane.remove("data")
        context["atribute"] = coloane
    
    if iduri is not None and len(iduri) > 0:
        res = []
        for id in iduri:
            try:
                indecsi = []
                for x in id.split(","):
                    if not isValidId(x):
                        raise ValueError("Parametrul 'iduri' trebuie sa contina numai numere întregi si sa fie in intervalul [0, " + str(len(Accesare.accesari) - 1) + ").")
                    indecsi.append(int(x))
                
                for index in indecsi:
                    if not dubluri: 
                        if Accesare.accesari[len(Accesare.accesari) - index - 1] not in res:
                            res.append(Accesare.accesari[len(Accesare.accesari) - index - 1])
                    else: res.append(Accesare.accesari[len(Accesare.accesari) - index - 1])
                
            except ValueError as e:
                context["eroare_accesari"] = str(e)
                return render(request, 'log.html', context, status=400)
            
        context["accesari"] = res
    
    elif ultimele is None:
        context["eroare_accesari"] = "Parametrul 'ultimele' sau 'iduri' nu a fost specificat."
        return render(request, 'log.html', context, status=400)
    else:
        
        if not isValidId(ultimele):
            context["eroare_accesari"] = "Parametrul 'ultimele' trebuie să fie un număr întreg."
            return render(request, 'log.html', context, status=400)
        
        ultimele = int(ultimele)
        
        if ultimele > len(Accesare.accesari):
            context["eroare_accesari"] = f"Exista doar ({len(Accesare.accesari)}) accesări înregistrate față de ({ultimele}) cerute."
            context["accesari"] = Accesare.accesari
            return render(request, 'log.html', context, status=400)
        else: 
            context["accesari"] = Accesare.accesari[:ultimele] 
    
    return render(request, 'log.html', context) 
