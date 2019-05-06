from django.utils.deprecation import MiddlewareMixin



class CORSMiddleware(MiddlewareMixin):

    '''
    Solving homologous cross
    '''

    def process_request(self, request):
        setattr(request, '_dont_enforce_csrf_checks', True)

    def process_response(self, request, response):
        response['Access-Control-Allow-Origin'] = "*"
        response['Access-Control-Allow-Headers'] = "Content-Type"
        response['Access-Control-Allow-Methods'] = "GET,DELETE,PUT,POST"
        return response


