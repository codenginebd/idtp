import os
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import HttpResponse
from lib.ws_xml_parser import WSXMLParser
from pim.models import AuditLog


@method_decorator(csrf_exempt, name='dispatch')
class InitiateFundTransferView(View):
    def post(self, request):
        _audit_log_instance = None

        try:
            import json
            _p = request.body.decode() # The request.data body is a ISO 20022/PAIN.001.001.04 message

            _log_data = {
                "context": "INITIATE_FUND_TRANSFER",
                "request_endpoint": request.path,
                "request_data": _p,
                "request_params": { k:v for k, v in request.GET.items() },
                "response": None,
                "status": None,
                "stacktrace": None
            }
            _audit_log_instance = AuditLog.log(**_log_data)

            request_data_dict = WSXMLParser.parse_response(json.loads(_p))
            print(request_data_dict)
            project_directory = os.path.abspath(".")
            data_directory = os.path.join(project_directory, "pim", "data", "response")
            with open(os.path.join(data_directory, "pacs.002.001.05.xml")) as f:
                _response = f.read()

                _audit_log_instance.response = _response
                _audit_log_instance.status = "SUCCESS"
                _audit_log_instance.save()

                return HttpResponse(_response) # ISO 20022/ CAMT.054.001.04
        except Exception as exp:
            print("Exception")
            print("Exception Message: ")
            print(exp)
            if _audit_log_instance:
                _audit_log_instance.status = "Failed"
                _audit_log_instance.stacktrace = exp

                if not _audit_log_instance.request_data:
                    _audit_log_instance.request_data = str(request.body)

                _audit_log_instance.save()

            _failed_response = ""
            return HttpResponse(_failed_response)


