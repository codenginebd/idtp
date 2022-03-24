import os
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import HttpResponse
from lib.ws_xml_parser import WSXMLParser


@method_decorator(csrf_exempt, name='dispatch')
class ProcessRTPDeclineResponseView(View):
    def post(self, request):
        print("Inside Process RTP Decline Response!")
        print(request.body)
        import json
        _p = request.body.decode() # The request.data body is a ISO PAIN.013.001.06 message
        response_dict = WSXMLParser.parse_response(json.loads(_p))
        # print(response_dict)
        project_directory = os.path.abspath(".")
        data_directory = os.path.join(project_directory, "pim", "data", "response")
        with open(os.path.join(data_directory, "PAIN.013.001.06.xml")) as f:
            _response = f.read()
            return HttpResponse(_response) # PAIN.013.001.06.xml

