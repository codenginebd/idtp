import os
import json
from lib.api.requester import APIRequester


class IDTPCreateRTP(APIRequester):

    def __init__(self, **kwargs):
        super(IDTPCreateRTP, self).__init__(**kwargs)
        self._req_id = "RTP"+str(self._req_id)

    def api_endpoint(self):
        return "/CreateRTP/"

    def get_request_body_xml_file_name(self):
        return "create_rtp.xml"

    def payload_extra_data(self):
        return {}


