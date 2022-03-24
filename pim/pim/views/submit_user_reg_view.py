import os
import json
import uuid
from datetime import datetime
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.generic.base import View
from lib.api.sending.idtp_user_registration import IDTPUserRegistration
from pim.models import AuditLog, Account


@method_decorator(csrf_exempt, name='dispatch')
class SubmitUserRegView(View):
    def post(self, request, *args, **kwargs):
        _response = {
            "status": "FAILED",
            "message": None
        }
        _data = { k:v for k, v in request.POST.items() }
        _instance = IDTPUserRegistration(**_data)
        success, raw_response, response_as_json = _instance.send_request()

        # Log the request
        _log_data = {
            "context": "IDTP_USER_REG",
            "request_endpoint": _instance.get_api_endpoint(),
            "request_data": _instance.get_payload(),
            "request_params": None,
            "response": raw_response,
            "status": _instance.get_http_status(),
            "stacktrace": _instance.get_stacktrace()
        }
        AuditLog.log(**_log_data)

        print(raw_response)
        if success and _instance.is_request_success():
            print("Successful")

            # Now save the user
            request_vid = _data["request_vid"]

            _account_data = _data
            _account_data.update({"idtp_vid": request_vid})
            Account.create_or_update(**_account_data)

            _response["status"] = "SUCCESS"
            _response["message"] = "User Registration Successful"
        else:
            print("Failed")
            print(raw_response)
            _response["status"] = "FAILED"
            _response["message"] = _instance.get_failed_reason() or "Registration failed"
        return HttpResponse(json.dumps(_response), content_type="application/json");

