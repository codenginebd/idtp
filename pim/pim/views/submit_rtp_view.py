import os
import json
import uuid
from datetime import datetime
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.generic.base import View

from lib.api.sending.idtp_create_rtp import IDTPCreateRTP
from lib.api.sending.idtp_transfer_fund import IDTPTransferFund
from pim.models import AuditLog


@method_decorator(csrf_exempt, name='dispatch')
class SubmitRTPView(View):
    def post(self, request, *args, **kwargs):
        _response = {
            "status": "FAILED",
            "message": None
        }
        _data = { k:v for k, v in request.POST.items() }
        _instance = IDTPCreateRTP(**_data)
        print(_instance.get_payload())
        success, raw_response, response_as_json = _instance.send_request()

        # Log the request
        _log_data = {
            "context": "SUBMIT_RTP",
            "request_endpoint": _instance.get_api_endpoint(),
            "request_data": _instance.get_payload(),
            "request_params": None,
            "response": raw_response,
            "status": _instance.get_http_status(),
            "stacktrace": _instance.get_stacktrace()
        }

        AuditLog.log(**_log_data)

        print(raw_response)
        if success and (response_as_json["CreateRTPResponse"].get("Code") == '200' or
                        response_as_json["CreateRTPResponse"].get("Code") == 200):
            print("Successful")
            _response["status"] = "SUCCESS"
            _response["message"] = "RTP Request Successful"
        else:
            print("Failed")
            print(raw_response)
            _response["status"] = "FAILED"
            _response["message"] = "RTP Request Failed"
        return HttpResponse(json.dumps(_response), content_type="application/json");

