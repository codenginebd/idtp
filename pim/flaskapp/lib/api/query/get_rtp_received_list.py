import os
import json
from lib.api.requester import APIRequester
from django.conf import settings


class GetRTPReceivedList(APIRequester):

    def api_endpoint(self):
        return "/GetRTPListReceived/"

    def get_request_body_xml_file_name(self):
        return "get_rtp_request_received.xml"

    def payload_extra_data(self):
        return {}





