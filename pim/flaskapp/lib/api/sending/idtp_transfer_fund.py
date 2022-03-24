from lib.api.requester import APIRequester


class IDTPTransferFund(APIRequester):
    def api_endpoint(self):
        return "/TransferFunds"

    def get_request_body_xml_file_name(self):
        return "transfer_fund.xml"

    def payload_extra_data(self):
        return {
            "ref_no": self._req_id
        }



