from lib.ws_xml_parser import WSXMLParser


class ISO20022Extractor(object):
    def __init__(self, request_body, context):
        self._request_body = request_body
        self._context = context
        self._request_json = self.request_body_to_dict()

    def request_body_to_dict(self):
        return WSXMLParser.parse_response(self._request_body)

    def extract_field(self, hierarchy):
        try:
            return self._request_json
        except Exception as exp:
            return None

    def extract_process_ft(self):
        _extracted_params = {}
        msg_id = self._request_json["DataPDU"]["Body"]["AppHdr"]["MsgDefIdr"]
        _extracted_params["msg_id"] = msg_id
        from_inst = self._request_json["DataPDU"]["Body"]["AppHdr"]["Fr"]["FIId"]["FinInstnId"]["BICFI"]
        _extracted_params["from_inst"] = from_inst
        to_inst = self._request_json["DataPDU"]["Body"]["AppHdr"]["To"]["FIId"]["FinInstnId"]["BICFI"]
        _extracted_params["to_inst"] = to_inst
        sending_fi_msg_id = self._request_json["DataPDU"]["Body"]["Document"]["FIToFICstmrCdtTrf"]["GrpHdr"]["MsgId"]
        _extracted_params["sending_fi_msg_id"] = sending_fi_msg_id
        amount = self._request_json["DataPDU"]["Body"]["Document"]["FIToFICstmrCdtTrf"]["CdtTrfTxInf"]["IntrBkSttlmAmt"]["#text"]
        _extracted_params["amount"] = amount
        idtp_ref_no = self._request_json["DataPDU"]["Body"]["Document"]["FIToFICstmrCdtTrf"]["SplmtryData"]["Envlp"]["Tx_Tracking_Info"]["RefNo_IDTP"]
        _extracted_params["idtp_ref_no"] = idtp_ref_no
        instgagt = self._request_json["DataPDU"]["Body"]["Document"]["FIToFICstmrCdtTrf"]["CdtTrfTxInf"]["InstgAgt"]["FinInstnId"]["BICFI"]
        _extracted_params["instgagt"] = instgagt
        _cred_tm = self._request_json["DataPDU"]["Body"]["Document"]["FIToFICstmrCdtTrf"]["GrpHdr"]["CreDtTm"]
        _extracted_params["cred_tm"] = _cred_tm
        _cr_account = \
        self._request_json["DataPDU"]["Body"]["Document"]["FIToFICstmrCdtTrf"]["CdtTrfTxInf"]["CdtrAcct"]["Id"]["Othr"][
            "Id"]
        _extracted_params["cr_account"] = _cr_account
        _dr_account = \
        self._request_json["DataPDU"]["Body"]["Document"]["FIToFICstmrCdtTrf"]["CdtTrfTxInf"]["DbtrAcct"]["Id"]["Othr"][
            "Id"]
        _extracted_params["dr_account"] = _dr_account
        return _extracted_params

    def extract_process_rtp(self):
        _extracted_params = {}
        _from = self._request_json["DataPDU"]["Body"]["AppHdr"]["Fr"]["FIId"]["FinInstnId"]["BICFI"]
        _extracted_params["from"] = _from
        _to = self._request_json["DataPDU"]["Body"]["AppHdr"]["To"]["FIId"]["FinInstnId"]["BICFI"]
        _extracted_params["to"] = _to
        _msg_id = self._request_json["DataPDU"]["Body"]["AppHdr"]["MsgDefIdr"]
        _extracted_params["msg_id"] = _msg_id
        tnx_msg_id = self._request_json["DataPDU"]["Body"]["Document"]["CdtrPmtActvtnReq"]["GrpHdr"]["MsgId"]
        _extracted_params["tnx_msg_id"] = tnx_msg_id
        channel_id = self._request_json["DataPDU"]["Body"]["Document"]["CdtrPmtActvtnReq"]["SplmtryData"]["Envlp"]["ChannelInfo"]["ChannelID"]
        _extracted_params["channel_id"] = channel_id
        request_id = self._request_json["DataPDU"]["Body"]["Document"]["CdtrPmtActvtnReq"]["OrgnlPmtInfAndSts"]["OrgnlPmtInfId"]
        _extracted_params["request_id"] = request_id
        sender_vid = \
        self._request_json["DataPDU"]["Body"]["Document"]["CdtrPmtActvtnReq"]["OrgnlPmtInfAndSts"]["TxInfAndSts"][
            "OrgnlTxRef"]["Cdtr"]["Nm"]
        _extracted_params["sender_vid"] = sender_vid
        receiver_vid = \
        self._request_json["DataPDU"]["Body"]["Document"]["CdtrPmtActvtnReq"]["OrgnlPmtInfAndSts"]["TxInfAndSts"][
            "OrgnlTxRef"]["Dbtr"]["Nm"]
        _extracted_params["receiver_vid"] = receiver_vid
        return _extracted_params

    def extract_validate_fi_user(self):
        _extracted_params = {}
        """
        {
           "ValidateFIUser":{
              "@xmlns:idtp":"http://idtp.gov.bd/xxx/schema/",
              "Head":{
                 "@ver":"1.0",
                 "@ts":"{timestamp}",
                 "@orgId":"sample1",
                 "@msgId":"1"
              },
              "Req":{
                 "@id":"{request_id}",
                 "@note":"Validate IDTP User",
                 "@ts":"{timestamp}",
                 "@type":"VALIDATEUSERINFO"
              },
              "UserInfo":{
                 "UserType":"Individual",
                 "NID":"234324234234234",
                 "BIN":"None",
                 "DOB":"1997/07/22",
                 "DateOfIncorporation":"None",
                 "MobileNo":"017XXXXX244"
              },
              "OtherInfo":"None"
           }
        }
        """
        _request_id = self._request_json["ValidateFIUser"]["Req"]["@id"]
        _extracted_params["request_id"] = _request_id
        _user_type = self._request_json["ValidateFIUser"]["UserInfo"]["UserType"]
        _extracted_params["user_type"] = _user_type
        _nid = self._request_json["ValidateFIUser"]["UserInfo"]["NID"]
        _extracted_params["nid"] = _nid
        _dob = self._request_json["ValidateFIUser"]["UserInfo"]["DOB"]
        _extracted_params["dob"] = _dob
        mobile_no = self._request_json["ValidateFIUser"]["UserInfo"]["MobileNo"]
        _extracted_params["mobile_no"] = mobile_no
        return _extracted_params

    def extract_balance(self):
        _extracted_params = {}
        print(self._request_json)
        _idtp_ref_no = self._request_json["DataPDU"]["Body"]["AppHdr"]["BizMsgIdr"]
        _extracted_params["idtp_ref_no"] = _idtp_ref_no
        _account_no = self._request_json["DataPDU"]["Body"]["Document"]["GetAcct"]["AcctQryDef"]["AcctCrit"]["NewCrit"]["SchCrit"]["AcctId"]["EQ"]["Othr"]["Id"]
        _extracted_params["account_number"] = _account_no
        return _extracted_params

    def extract(self):
        # print(self._request_json)
        if not self._context:
            return {}
        if not self._request_body:
            return {}
        try:
            return getattr(self, "extract_"+self._context)()
        except Exception as exp:
            print("Exception inside extractor")
            print("Exception message:")
            print(exp)
            return {}

if __name__ == "__main__":
    import os
    project_directory = os.path.abspath(".")
    data_directory = os.path.join(project_directory, "pim", "data", "request.data")
    with open(os.path.join(data_directory, "PAIN.013.001.06.xml")) as f:
        _req_body = f.read()
        _instance = ISO20022Extractor(request_body=_req_body, context="process_ft")
        _eparams = _instance.extract()
        print(_eparams)