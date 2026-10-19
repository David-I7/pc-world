from .views import creaza_accesare

class MiddlewareAccesare:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.accesare = creaza_accesare(request) 
        print(request.accesare)
        return self.get_response(request)
