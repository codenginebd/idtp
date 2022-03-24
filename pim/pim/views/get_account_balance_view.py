import os
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import HttpResponse
from lib.ws_xml_parser import WSXMLParser


@method_decorator(csrf_exempt, name='dispatch')
class GetAccountBalanceView(View):
    def post(self, request):
        import json
        _p = request.body.decode() # The request.data body is a CAMT.003.001.05 message
        response_dict = WSXMLParser.parse_response(json.loads(_p))
        # print(response_dict)
        project_directory = os.path.abspath(".")
        data_directory = os.path.join(project_directory, "pim", "data", "response")
        with open(os.path.join(data_directory, "CAMT.004.001.05.xml")) as f:
            _response = f.read()
            return HttpResponse(_response) # CAMT.004.001.05.xml

