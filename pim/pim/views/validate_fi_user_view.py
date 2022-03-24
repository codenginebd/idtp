import os
import json
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import HttpResponse
from lib.iso_20022_extractor import ISO20022Extractor
from lib.ws_xml_parser import WSXMLParser
from pim.models import AuditLog, Account


@method_decorator(csrf_exempt, name='dispatch')
class ValidateFIUserView(View):
    def post(self, request):

        _http_success_response = """<ValidateFIUserResponse>
            <Code>200</Code>
            <Message>Success</Message>
            </ValidateFIUserResponse>
        """

        _http_failed_response = """<ValidateFIUserResponse>
                <Code>400</Code>
                <Message>The provided account is either invalid or inactive</Message>
                </ValidateFIUserResponse>
                """
        # import json
        # return HttpResponse(json.dumps(_http_success_response), content_type="application/json")

        _audit_log_instance = None

        try:
            import json
            _p = request.body.decode()

            print(_p)

            _log_data = {
                "context": "VALIDATE_FI_USER",
                "request_endpoint": request.path,
                "request_data": _p,
                "request_params": { k:v for k, v in request.GET.items() },
                "response": None,
                "status": None,
                "stacktrace": None
            }
            _audit_log_instance = AuditLog.log(**_log_data)

            try:
                _p = json.loads(_p)
            except Exception as e:
                pass

            _instance = ISO20022Extractor(request_body=_p, context="validate_fi_user")
            _eparams = _instance.extract()

            print("params received: %s" % _eparams)

            _nid = _eparams.get("nid")
            if _nid:
                is_valid = Account.check_if_valid(nid=_nid)
                if is_valid:
                    _audit_log_instance.response = json.dumps(_http_success_response).strip()
                    _audit_log_instance.status = "SUCCESS"
                    _audit_log_instance.save()

                    _r = _http_success_response

                    return HttpResponse(json.dumps(_http_success_response), content_type="application/json")
            _r = _http_failed_response
            return HttpResponse(json.dumps(_http_failed_response), content_type="application/json")

        except Exception as exp:
            print("Exception")
            print("Exception Message: ")
            print(exp)
            if _audit_log_instance:
                _audit_log_instance.response = _http_failed_response
                _audit_log_instance.status = "FAILED"
                _audit_log_instance.stacktrace = exp

                if not _audit_log_instance.request_data:
                    _audit_log_instance.request_data = str(request.body)

                _audit_log_instance.save()
            _r = _http_success_response
            return HttpResponse(json.dumps(_http_failed_response), content_type="application/json")


