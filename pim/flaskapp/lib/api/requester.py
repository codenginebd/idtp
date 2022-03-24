import requests
import os, json
import uuid
from datetime import datetime
from django.conf import settings
from lib.ws_xml_parser import WSXMLParser


class APIRequester(object):

    def __init__(self, **kwargs):
        self._kwargs = kwargs
        _unique_id = str(uuid.uuid4())
        self._req_id = str(_unique_id)
        self._timestamp = datetime.now().strftime("%m/%d/%Y %I:%M:%S")
        self._payload = {}
        self._endpoint = None
        self._http_status = None
        self._stacktrace = None
        self._response_dict = {}

    def get_stacktrace(self):
        return self._stacktrace

    def get_http_status(self):
        return self._http_status

    def get_payload(self):
        return self._payload

    def get_api_endpoint(self):
        return self._endpoint

    def api_endpoint(self):
        pass

    def prepare_payload_data(self):
        _payload_context = {
            "timestamp": self._timestamp,
            "request_id": self._req_id
        }
        if hasattr(self, "_kwargs") and self._kwargs:
            _payload_context.update(self._kwargs)

        _extra_data = self.payload_extra_data()
        if _extra_data:
            _payload_context.update(_extra_data)

        return _payload_context

    def payload_extra_data(self):
        return {}

    def get_request_body_xml_file_name(self):
        return ""

    def prepare_payload(self):
        try:
            _payload_context = self.prepare_payload_data()
            _body_xml_file = self.get_request_body_xml_file_name()
            project_directory = os.path.abspath(".")
            data_directory = os.path.join(project_directory, "pim", "data")
            with open(os.path.join(data_directory, _body_xml_file)) as f:
                _data = f.read()
                _formatted_data = _data.format(**_payload_context)
                print(_formatted_data)
                return json.dumps(_formatted_data)
        except Exception as exp:
            print(exp)

    def compile(self):
        endpoint = settings.ICP_BASE + self.api_endpoint()
        self._endpoint = endpoint
        payload = self.prepare_payload()
        self._payload = payload

    def is_request_success(self):
        return False

    def get_failed_reason(self):
        return None

    def send_request(self):
        try:
            self.compile()
            print("=================BEGIN===========================")
            print("Requesting API for endpoint: %s with payload: %s" % (self._endpoint, self._payload))
            r = requests.post(self._endpoint,
                              data=self._payload,
                              headers={
                                  'Content-Type': 'application/json'
                              })
            self._http_status = r.status_code
            print("Response Status: %s" % r.status_code)
            print("Response Received: ")
            _decoded_body_string = r.content.decode()
            print(_decoded_body_string)
            response_dict = WSXMLParser.parse_response(_decoded_body_string)
            print("=================END===========================")
            self._response_dict = response_dict
            return r.status_code==200, r.content.decode(), response_dict
        except Exception as exp:
            self._stacktrace = exp
            print("=================BEGIN===========================")
            print("Exception while requesting for endpoint %s with payload %s" % (self._endpoint, self._payload))
            print("Exception Message: ")
            print(exp)
            print("=================END===========================")
            return None, None, None

