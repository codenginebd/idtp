import os
import json
from lib.api.requester import APIRequester
from django.conf import settings


class GetRegisteredFIUserList(APIRequester):
    def api_endpoint(self):
        return "/GetFIUserList/"

    def get_request_body_xml_file_name(self):
        return "get_registered_fi_list.xml"

    def payload_extra_data(self):
        return {
            "fi_vid": settings.SCB_FIN_VID
        }




