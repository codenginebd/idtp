import os
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from lib.api.query.get_rtp_received_list import GetRTPReceivedList


@method_decorator(csrf_exempt, name='dispatch')
class GetRTPListReceivedView(TemplateView):
    template_name = 'rtp_list_received.html'

    def get_context_data(self, **kwargs):
        request = self.request
        print(request.GET.get("receiver_vid"))
        ctx = super(GetRTPListReceivedView, self).get_context_data(**kwargs)
        rtp_sent_list = []
        _instance = GetRTPReceivedList(receiver_vid=request.GET.get("receiver_vid"))
        success, raw_response, response_as_json = _instance.send_request()
        if success and (response_as_json['GetRTPListReceivedResponse'].get("Code") == '200' or response_as_json['GetRTPListReceivedResponse'].get("Code") == 200):
            rtp_sent_list = response_as_json['GetRTPListReceivedResponse'].get('RTP', [])
            if type(rtp_sent_list) is dict:
                rtp_sent_list = [rtp_sent_list]

        ctx["rtp_received_list"] = rtp_sent_list
        ctx["qparams"] = { k:v for k, v in request.GET.items() }
        return ctx

