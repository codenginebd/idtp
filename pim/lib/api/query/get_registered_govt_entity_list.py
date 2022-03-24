import os
import json
from lib.api.requester import APIRequester
from django.conf import settings


class GetRegisteredGovtEntityList(APIRequester):
    def api_endpoint(self):
        return "/GetRegisteredGovtEntityList/"

    def get_request_body_xml_file_name(self):
        return "get_registered_govt_entities.xml"


