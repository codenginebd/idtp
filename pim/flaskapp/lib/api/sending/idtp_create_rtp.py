import os
import json
from lib.api.requester import APIRequester


class IDTPCreateRTP(APIRequester):
    def api_endpoint(self):
        return "/CreateRTP/"

    def get_request_body_xml_file_name(self):
        return "create_rtp.xml"

    def payload_extra_data(self):
        return {}


