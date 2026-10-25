from .lib.accesare import creaza_accesare, HttpRequestCuAccesare

class MiddlewareAccesare:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.accesare = creaza_accesare(request) 
        print(request.accesare)
        return self.get_response(request)

class MiddlewareFooterClientIp:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request:HttpRequestCuAccesare):
        response = self.get_response(request)
        ip = request.accesare.ip_client
        
        if response.has_header('Content-Type') and 'text/html' in response['Content-Type']:
            content = response.content.decode('utf-8')
            print(content)
            new_content = content.replace(
                '<p class="footer__client-ip"></p>',
                f'<p class="footer__client-ip">adresa ip: {ip}</p>'
            ).replace(
                '<p class="footer-client-ip"></p>',
                f'<p class="footer-client-ip">adresa ip: {ip}</p>'
            )
           
            response.content = new_content.encode('utf-8')           
            response['Content-Length'] = len(response.content)
       
        return response
