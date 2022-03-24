import os
import json
from lib.api.requester import APIRequester
from django.conf import settings


class GetDailyTnxList(APIRequester):

    def __init__(self, **kwargs):
        self._kwargs = kwargs

    def api_endpoint(self):
        return "/GetTransactionsbyFI/"

    def prepare_payload_data(self):
        import uuid
        from datetime import datetime
        _payload_context = {
            "timestamp": datetime.now().strftime("%m/%d/%Y %I:%M:%S"),
            "request_id": str(uuid.uuid4())
        }

        if self._kwargs:
            _payload_context.update(self._kwargs)

        return _payload_context

    def prepare_payload(self):
        try:
            _payload_context = self.prepare_payload_data()

            project_directory = os.path.abspath(".")
            data_directory = os.path.join(project_directory, "pim", "data")
            with open(os.path.join(data_directory, "get_daily_transactions.xml")) as f:
                _data = f.read()
                _formatted_data = _data.format(**_payload_context)
                return json.dumps(_formatted_data)
        except Exception as exp:
            print(exp)




