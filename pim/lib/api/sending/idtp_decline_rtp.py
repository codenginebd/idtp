import os
import json
from lib.api.requester import APIRequester


class IDTPDeclineRTP(APIRequester):
    def api_endpoint(self):
        return "/SendRTPDeclinedResponse/"

    def get_request_body_xml_file_name(self):
        return "decline_rtp.xml"

    def payload_extra_data(self):
        return {}


