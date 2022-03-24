import os
import json
from lib.api.requester import APIRequester


class IDTPUserRegistration(APIRequester):

    def api_endpoint(self):
        return "/RegisterIDTPUser/"

    def get_request_body_xml_file_name(self):
        return "idtp_user_registrationv2.xml"

    def is_request_success(self):
        if not self._response_dict:
            return False
        try:
            return self._response_dict["RegisterUserResponse"]["UserInfo"]["Status"] == "1"
        except Exception as exp:
            return False

    def get_failed_reason(self):
        if not self._response_dict:
            return False
        try:
            return self._response_dict["RegisterUserResponse"]["UserInfo"]["Reason"]
        except Exception as exp:
            return None

    def payload_extra_data(self):
        return {}

    # def prepare_payload_data(self):
    #     import uuid
    #     from datetime import datetime
    #     _payload_context = {
    #         "timestamp": datetime.now().strftime("%m/%d/%Y %I:%M:%S"),
    #         "request_id": str(uuid.uuid4())
    #     }
    #     if hasattr(self, "_kwargs") and self._kwargs:
    #         _payload_context.update(self._kwargs)
    #
    #     # _payload_context = {
    #     #     "timestamp": datetime.now().strftime("%m/%d/%Y %I:%M:%S"),
    #     #     "request_id": str(uuid.uuid4()),
    #     #     "full_name": "Farzana Afrose",
    #     #     "address_line1": "Mirpur DOHS, Dhaka",
    #     #     "address_line2": "",
    #     #     "district": "Dhaka",
    #     #     "postal_code": "1215",
    #     #     "mobile_number": "01847200329",
    #     #     "email": "Farzana.Afrose@sc.com",
    #     #     "nid": "1911872738339",
    #     #     "tin": "055710312495",
    #     #     "dob": "08/15/1981 00:00:00",
    #     #     "password": "1234",
    #     #     "account_number": "01192399709",
    #     #     "idtp_pin": "123456",
    #     #     "app_pass": "1234",
    #     #     "request_vid": "farzana.afrose@user.idtp"
    #     # }
    #     return _payload_context
    #
    # def prepare_payload(self):
    #     try:
    #         _payload_context = self.prepare_payload_data()
    #
    #         project_directory = os.path.abspath(".")
    #         data_directory = os.path.join(project_directory, "pim", "data")
    #         with open(os.path.join(data_directory, "idtp_user_registration.xml")) as f:
    #             _data = f.read()
    #             _formatted_data = _data.format(**_payload_context)
    #             return json.dumps(_formatted_data)
    #     except Exception as exp:
    #         print(exp)
    
    """
        Success Response:
        {'RegisterUserResponse': {'Code': '200', 'Message': 'Registration Successful', 'UserInfo': {'@seqNum': '1', 'Status': '1', 'VirtualID': 'mrjamesbond2@user.idtp', '#text': 'rn    rn    rn'}, '#text': 'rn  rn  rn  rn'}}

        Failed Response:
        {'RegisterUserResponse': {'Code': '90804', 'Message': 'Registration failed', 'UserInfo': {'@seqNum': '1', 'Status': '0', 'VirtualID': 'sharifulscbl@user.idtp', 'Reason': 'This Account Number already exists', '#text': 'rn    rn    rn    rn'}, '#text': 'rn  rn  rn  rn'}}
    
        {'RegisterUserResponse': {'Code': '90804', 'Message': 'Registration failed', 'UserInfo': {'@seqNum': '1', 'Status': '0', 'VirtualID': 'mrjamesbond@user.idtp', 'Reason': 'NID already exists, New Account added successfully', '#text': 'rn    rn    rn    rn'}, '#text': 'rn  rn  rn  rn'}}
    
        {'RegisterUserResponse': {'Code': '90804', 'Message': 'Registration failed', 'UserInfo': {'@seqNum': '1', 'Status': '0', 'VirtualID': 'mrjamesbond@user.idtp', 'Reason': 'Invalid NID or this NID already exists', '#text': 'rn    rn    rn    rn'}, '#text': 'rn  rn  rn  rn'}}
    """


