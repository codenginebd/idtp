import os
import json
import uuid
from datetime import datetime
from decimal import Decimal

from django.http import HttpResponse
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.generic.base import View
from lib.api.sending.idtp_transfer_fund import IDTPTransferFund
from pim.models import AuditLog, Account


@method_decorator(csrf_exempt, name='dispatch')
class SubmitFundTransferView(View):
    def post(self, request, *args, **kwargs):
        _response = {
            "status": "FAILED",
            "message": None
        }
        _data = { k:v for k, v in request.POST.items() }

        # Check for Fund Transfer Eligibility
        sender_vid = _data.get("sender_vid")
        _acc_instances = Account.objects.filter(idtp_vid=sender_vid, account_status="ACTIVE")
        if not _acc_instances.exists():
            _response["message"] = "Either the account is invalid or does not exists"
            return HttpResponse(json.dumps(_response), content_type="application/json");

        _acc_instance = _acc_instances.first()
        _fund_amount = _data.get("amount")
        _fund_amount = Decimal(_fund_amount)
        if _acc_instance.balance - _fund_amount < 0:
            _response["message"] = "Insufficient fund"
            return HttpResponse(json.dumps(_response), content_type="application/json")

        _instance = IDTPTransferFund(**_data)
        success, raw_response, response_as_json = _instance.send_request()

        # Log the request
        _log_data = {
            "context": "SUBMIT_FUND_TRANSFER",
            "request_endpoint": _instance.get_api_endpoint(),
            "request_data": _instance.get_payload(),
            "request_params": None,
            "response": raw_response,
            "status": _instance.get_http_status(),
            "stacktrace": _instance.get_stacktrace()
        }
        AuditLog.log(**_log_data)

        print(raw_response)
        if success:
            if (response_as_json["TransactionResponse"].get("Code") == '200' or
                    response_as_json["TransactionResponse"].get("Code") == 200):
                print("Successful")
                _acc_instance.balance -= _fund_amount
                _acc_instance.save()
                _response["status"] = "SUCCESS"
                _response["message"] = "Fund Transfer Successful"
            else:
                print("Failed")
                print(raw_response)
                _response["status"] = "FAILED"
                _response["message"] = response_as_json["TransactionResponse"].get("Message", "")
        else:
            print("Failed")
            print(raw_response)
            _response["status"] = "FAILED"
            _response["message"] = "Something did not happen right"
        return HttpResponse(json.dumps(_response), content_type="application/json");

