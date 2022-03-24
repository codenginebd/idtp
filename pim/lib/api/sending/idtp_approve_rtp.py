from lib.api.requester import APIRequester


class IDTPApproveRTP(APIRequester):
    def api_endpoint(self):
        return "/TransferFunds"

    def get_request_body_xml_file_name(self):
        return "rtp_transfer_fund.xml"

    def payload_extra_data(self):
        return {}



