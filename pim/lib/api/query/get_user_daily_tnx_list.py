import os
import json
from lib.api.requester import APIRequester
from django.conf import settings


class GetUserDailyTnxList(APIRequester):

    def api_endpoint(self):
        return "/GetTransactionsbyUser/"

    def get_request_body_xml_file_name(self):
        return "get_daily_user_transactions.xml"






