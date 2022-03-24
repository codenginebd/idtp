from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from lib.api.query.get_daily_tnx_list import GetDailyTnxList
from lib.api.query.get_user_daily_tnx_list import GetUserDailyTnxList


@method_decorator(csrf_exempt, name='dispatch')
class GetDailyTransactionsView(TemplateView):
    template_name = 'daily_tnx_list.html'

    def get_context_data(self, **kwargs):
        request = self.request
        print(request.GET.get("vid"))
        ctx = super(GetDailyTransactionsView, self).get_context_data(**kwargs)
        daily_tnx_list = []
        _vid = request.GET.get("vid")
        _idtp_pin = request.GET.get("idtp_pin")
        if _vid:
            _instance = GetUserDailyTnxList(vid=_vid, idtp_pin=_idtp_pin)
        else:
            _vid = "SCBL@fin.idtp"
            _instance = GetDailyTnxList(vid=_vid, idtp_pin=_idtp_pin)
        success, raw_response, response_as_json = _instance.send_request()
        print(response_as_json)
        if success:
            if _vid == "SCBL@fin.idtp":
                if (response_as_json['GetTransactionsbyFIResponse'].get("Code") == '200' or
                            response_as_json['GetTransactionsbyFIResponse'].get("Code") == 200):
                    daily_tnx_list = response_as_json['GetTransactionsbyFIResponse'].get('Transaction', [])
                    if type(daily_tnx_list) is dict:
                        daily_tnx_list = [daily_tnx_list]
            else:
                self.template_name = "daily_user_tnx_list.html"
                if (response_as_json['GetTransactionsbyUserResponse'].get("Code") == '200' or
                            response_as_json['GetTransactionsbyUserResponse'].get("Code") == 200):
                    daily_tnx_list = response_as_json['GetTransactionsbyUserResponse'].get('Transaction', [])
                    if type(daily_tnx_list) is dict:
                        daily_tnx_list = [daily_tnx_list]
        ctx["daily_tnx_list"] = daily_tnx_list
        return ctx

