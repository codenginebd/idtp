import os
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from lib.api.query.get_rtp_sent_list import GetRTPSentList


@method_decorator(csrf_exempt, name='dispatch')
class GetRTPListSentView(TemplateView):
    template_name = 'rtp_list_sent.html'

    def get_context_data(self, **kwargs):
        request = self.request
        print(request.GET.get("vid"))
        ctx = super(GetRTPListSentView, self).get_context_data(**kwargs)
        rtp_sent_list = []

        _instance = GetRTPSentList(vid=request.GET.get("vid"))
        success, raw_response, response_as_json = _instance.send_request()
        if success and (response_as_json['GetRTPListSentResponse'].get("Code") == '200' or response_as_json['GetRTPListSentResponse'].get("Code") == 200):
            rtp_sent_list = response_as_json['GetRTPListSentResponse'].get('RTP', [])
            if type(rtp_sent_list) is dict:
                rtp_sent_list = [rtp_sent_list]
        ctx["rtp_sent_list"] = rtp_sent_list
        return ctx

