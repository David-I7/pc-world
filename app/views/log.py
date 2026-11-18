from django.shortcuts import render
from django.contrib import messages
from ..lib.accesare import Accesare, HttpRequestCuAccesare, isValidId


def handler(request:HttpRequestCuAccesare):
    accesare: Accesare = request.accesare  
    ultimele = accesare.parametri.get("ultimele")
    accesari = accesare.parametri.get("accesari")
    iduri = accesare.parametri.getlist("iduri")
    dubluri = accesare.parametri.get("dubluri",False)
    tabel = accesare.parametri.get("tabel","")
    cea_mai_putin_accesata_pagina = Accesare.get_pagina_cea_mai_putin_accesata()
    cea_mai_accesata_pagina = Accesare.get_pagina_cea_mai_accesata()
    
    context: dict[str, object] = {
            "accesari_iduri": None,
            "accesari_ultimele": None,
            "nr_accesari": str(len(Accesare.accesari)) if accesari == "nr" else None,
            "afisare": "tabel" if tabel != "" else "lista",
            "atribute": None,
            "cea_mai_putin_accesata_pagina": cea_mai_putin_accesata_pagina[0],
            "nr_accesari_cea_mai_putin_accesata_pagina": cea_mai_putin_accesata_pagina[1],
            "cea_mai_accesata_pagina": cea_mai_accesata_pagina[0],
            "nr_accesari_cea_mai_accesata_pagina": cea_mai_accesata_pagina[1]
        }
    
    if ultimele is None and iduri is None:
        messages.error(request, "Parametrul 'ultimele' sau 'iduri' nu a fost specificat.")
        return render(request, 'log.html', context, status=400)
        
    coloane = ["id", "ip_client", "url", "pagina", "parametri", "data"]
    colane_tabel = coloane if tabel == "tot" else tabel.split(",")
    
    if tabel != "":
        for col in colane_tabel:
            if col not in coloane:
                messages.error(request, f"Coloana '{col}' nu este validă. Coloanele valide sunt: {', '.join(coloane)}")
                return render(request, 'log.html', context, status=400)
        
        context["atribute"] = colane_tabel
    else:
        if accesari != "detalii":
            coloane.remove("data")
        context["atribute"] = coloane
    
    if iduri is not None and len(iduri) > 0:
        res:list[Accesare] = []
        iduri_unice = set()
        try:
          for id in iduri:
            iduri_parsate = []
            for x in id.split(","):
                if not isValidId(x):
                    raise ValueError(f"Parametrul 'iduri' trebuie sa contina numai numere întregi si sa fie in intervalul [0, {Accesare.contor -1}].")
                id_parsat = int(x)
                if dubluri: 
                  iduri_parsate.append(id_parsat)
                else: 
                  if id_parsat not in iduri_unice:
                    iduri_unice.add(id_parsat)
                    iduri_parsate.append(id_parsat) 
            
            for id in iduri_parsate:
              accessare = Accesare.get_accesare(id)
              if accessare is not None:
                res.append(accessare)
                  
        except ValueError as e:
            messages.error(request, str(e))
            res = []
            
        context["accesari_iduri"] = res if len(res) > 0 else None
    
    if ultimele is not None:
        if not ultimele.isdigit() or int(ultimele) <= 0:
            messages.error(request, "Parametrul 'ultimele' trebuie să fie un număr natural pozitiv.")
            return render(request, 'log.html', context, status=400)
        
        ultimele = int(ultimele)
        
        if ultimele > len(Accesare.accesari):
            messages.error(request, f"Exista doar ({len(Accesare.accesari)}) accesări înregistrate față de ({ultimele}) cerute.")
            context["accesari_ultimele"] = Accesare.accesari
            return render(request, 'log.html', context, status=400)
        else: 
            context["accesari_ultimele"] = Accesare.get_ultimele_accesari(ultimele)
    
    return render(request, 'log.html', context) 
