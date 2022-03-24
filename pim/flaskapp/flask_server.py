import os
import uuid
import json
import logging
from decimal import Decimal
from xml.etree import ElementTree
from datetime import datetime
from flask import request
from flask import Response
from django.apps import apps
from django.conf import settings

from lib.iso_20022_extractor import ISO20022Extractor


logging.basicConfig(level=logging.DEBUG,
                   format='[%(asctime)s]: {} %(levelname)s %(message)s'.format(os.getpid()),
                   datefmt='%Y-%m-%d %H:%M:%S',
                   handlers=[logging.StreamHandler()])

logger = logging.getLogger()


apps.populate(settings.INSTALLED_APPS)

# import models
from pim.models.account import Account
from pim.models.audit_log import AuditLog

from flask import Flask
from flask import render_template


def create_app():
    app = Flask(__name__)

    @app.route('/ProcessRTPRequest', methods=['POST'])
    def ProcessRTPRequest():
        _xml_payload = request.data.decode('utf-8')
        print(_xml_payload)
        "<?xml version=\"1.0\" encoding=\"UTF-8\"?><Body><AppHdr xmlns=\"urn:iso:std:iso:20022:tech:xsd:head.001.001.01\"><Fr><FIId><FinInstnId><BICFI>IDTP</BICFI></FinInstnId></FIId></Fr><To><FIId><FinInstnId><BICFI>SCBLBDDX</BICFI></FinInstnId></FIId></To><BizMsgIdr>9d186739-2645-4848-9aec-926b22e9374d</BizMsgIdr><MsgDefIdr>pain.013.001.06</MsgDefIdr><BizSvc>IDTP</BizSvc><CreDt>2021-02-07T06:54:05Z</CreDt><ds:Signature xmlns:ds=\"http://www.w3.org/2000/09/xmldsig#\"><ds:SignedInfo><ds:CanonicalizationMethod Algorithm=\"http://www.w3.org/2001/10/xml-exc-c14n#\" /><ds:SignatureMethod Algorithm=\"http://www.w3.org/2001/04/xmldsig-more#rsa-sha256\" /><ds:Reference><ds:DigestMethod Algorithm=\"http://www.w3.org/2001/04/xmldsig-more#rsa-sha256\" /><ds:DigestValue>D/XkfYkqnDE1W1OQwWvP8i6yTMxMGzj60Z4sDumU5qE=</ds:DigestValue></ds:Reference></ds:SignedInfo><ds:SignatureValue>Jv5B4VaoXmpiqHvcv+nwNP0BE7R/7TVxuJs1XDCFjLULdTmkOi+DCzYLVkZMIe0NMui6C6KOc59BmnaOpfq4snAm+gqMvjxcTYVNFpIWKBLTpUvm5R6jkiyAARIJPVy7qjNrXtIXM1SzBNcS9OAo3Sg74tzd5HulNvGstmrg0ZJGK7JvkYusaaiaMatb/ai5UEzEMG920M9MzKQF1dDyzadUelAmsTg2bhTp7NZ31bymgtOBHUbVn/yvD0rnVPVCRHfGM9GI+g2rwtdRKS63nS3HcQPTJBtlMG6+gQxUUEU01FwMKGHE0RkXBLecV1rZK+DcxOvYVX1XCNr7Bjr/XA==</ds:SignatureValue></ds:Signature></AppHdr><Document xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xmlns=\"urn:iso:std:iso:20022:tech:xsd:pain.013.001.06\"><CdtrPmtActvtnReq><GrpHdr><MsgId>9d186739-2645-4848-9aec-926b22e9374d</MsgId><CreDtTm>2021-02-07T06:54:05</CreDtTm><NbOfTxs>1</NbOfTxs><InitgPty><Id><OrgId><Othr><Id>sohelscbl@user.idtp</Id></Othr></OrgId></Id></InitgPty></GrpHdr><PmtInf><PmtInfId>9d186739-2645-4848-9aec-926b22e9374d</PmtInfId><PmtMtd>TRF</PmtMtd><ReqdExctnDt>2021-02-07</ReqdExctnDt><Dbtr><Nm>kahsanscbl@user.idtp</Nm><Id><OrgId><Othr><Id>kahsanscbl@user.idtp</Id><SchmeNm><Cd>CUST</Cd></SchmeNm></Othr></OrgId></Id><CtryOfRes>BD</CtryOfRes></Dbtr><DbtrAcct><Id><Othr><Id></Id></Othr></Id></DbtrAcct><DbtrAgt><FinInstnId><ClrSysMmbId><MmbId></MmbId></ClrSysMmbId></FinInstnId></DbtrAgt><CdtTrfTx><PmtId><EndToEndId>9d186739-2645-4848-9aec-926b22e9374d</EndToEndId></PmtId><PmtTpInf><SvcLvl><Cd>SDVA</Cd></SvcLvl><LclInstrm><Prtry>BUSINESS</Prtry></LclInstrm></PmtTpInf><Amt><InstdAmt Ccy=\"BDT\">13000</InstdAmt></Amt><ChrgBr>SLEV</ChrgBr><CdtrAgt><FinInstnId><ClrSysMmbId><MmbId></MmbId></ClrSysMmbId></FinInstnId></CdtrAgt><Cdtr><Nm>sohelscbl@user.idtp</Nm><Id><OrgId><Othr><Id>sohelscbl@user.idtp</Id><SchmeNm><Cd>CUST</Cd></SchmeNm></Othr></OrgId></Id></Cdtr><CdtrAcct><Id><Othr><Id></Id></Othr></Id></CdtrAcct><RmtInf><Ustrd>Test</Ustrd></RmtInf><SplmtryData><Envlp><ChannelInfo><ChannelID>Online</ChannelID></ChannelInfo><Creds><Cred type=\"IDTP_PIN\" subtype=\"\"><Data>1234</Data></Cred></Creds><Device_Info><Device_ID></Device_ID><Mobile_No></Mobile_No><Location></Location><IP></IP></Device_Info><Call_From>FIApp</Call_From></Envlp></SplmtryData></CdtTrfTx></PmtInf></CdtrPmtActvtnReq></Document></Body>"
        return Response("ok", mimetype="application/json")

    @app.route('/ProcessRTPDeclinedResponse', methods=['POST'])
    def ProcessRTPDeclinedResponse():
        _xml_payload = request.data.decode('utf-8')
        print(_xml_payload)
        return Response("ok", mimetype="application/json")

    @app.route('/GetAccountBalance', methods=['POST'])
    def GetAccountBalance():
        _xml_payload = request.data.decode('utf-8')
        _xml_payload = json.loads(_xml_payload)
        print(_xml_payload)
        _instance = ISO20022Extractor(request_body=_xml_payload, context="balance")
        _eparams = _instance.extract()

        _unique_id = str(uuid.uuid4())
        _timestamp = datetime.now().strftime("%m/%d/%Y %I:%M:%S")

        _eparams["unique_id"] = _unique_id
        _eparams["timestamp"] = _timestamp

        _account_no = _eparams.get("account_number")
        if _account_no:
            _account_instances = Account.objects.filter(account_number=_account_no, account_status="ACTIVE")
            if _account_instances.exists():
                _account_instance = _account_instances.first()
                _balance = _account_instance.balance
                _eparams["balance"] = _balance

                project_directory = os.path.abspath(".")
                data_directory = os.path.join(project_directory, "pim", "data", "response")
                with open(os.path.join(data_directory, "CAMT.004.001.05.xml")) as f:
                    _data = f.read()
                    _formatted_data = _data.format(**_eparams)
                    _xml = ElementTree.fromstring(_formatted_data)
                    # _xmlStr = ElementTree.tostring(_xml, encoding='utf8', method='xml')
                    _xmlStr = _formatted_data.replace(r"\n", "")
                    print(_xmlStr)
                    r = Response(_xmlStr, mimetype='application/json')

                    return r

        return Response("ok", mimetype="application/json")

    @app.route('/ValidateFIUser', methods=['POST'])
    def ValidateFIUser():
        _http_success_response = """<ValidateFIUserResponse>
                    <Code>200</Code>
                    <Message>Success</Message>
                    </ValidateFIUserResponse>
                """

        _http_failed_response = """<ValidateFIUserResponse>
                        <Code>400</Code>
                        <Message>The provided account is either invalid or inactive</Message>
                        </ValidateFIUserResponse>
                        """
        # import json
        # return HttpResponse(json.dumps(_http_success_response), content_type="application/json")

        _audit_log_instance = None

        try:
            import json
            _p = request.data.decode()

            _log_data = {
                "context": "VALIDATE_FI_USER",
                "request_endpoint": request.path,
                "request_data": _p,
                "request_params": {},#{k: v for k, v in request.GET.items()},
                "response": None,
                "status": None,
                "stacktrace": None
            }
            _audit_log_instance = AuditLog.log(**_log_data)

            try:
                _p = json.loads(_p)
            except Exception as e:
                pass

            _instance = ISO20022Extractor(request_body=_p, context="validate_fi_user")
            _eparams = _instance.extract()

            print("params received: %s" % _eparams)

            _nid = _eparams.get("nid")
            if _nid:
                is_valid = Account.check_if_valid(nid=_nid)
                if is_valid:
                    _audit_log_instance.response = json.dumps(_http_success_response).strip()
                    _audit_log_instance.status = "SUCCESS"
                    _audit_log_instance.save()

                    _r = _http_success_response

                    return Response(_http_success_response, content_type="application/json")
            _r = _http_failed_response
            return Response(_http_failed_response, content_type="application/json")

        except Exception as exp:
            print("Exception")
            print("Exception Message: ")
            print(exp)
            if _audit_log_instance:
                _audit_log_instance.response = _http_failed_response
                _audit_log_instance.status = "FAILED"
                _audit_log_instance.stacktrace = exp

                if not _audit_log_instance.request_data:
                    _audit_log_instance.request_data = str(request.body)

                _audit_log_instance.save()
            _r = _http_success_response
            return Response(_http_failed_response, content_type="application/json")

    @app.route('/ProcessFundTransferRequest', methods=['POST'])
    def ProcessFundTransferRequest():
        from lib.iso_20022_extractor import ISO20022Extractor

        _xml_payload = request.data.decode('utf-8')
        #_xml_payload = json.loads(_xml_payload)
        _xml_payload = _xml_payload[_xml_payload.rindex("<?xml"):]

        _extractor = ISO20022Extractor(request_body=_xml_payload, context="process_ft")
        _params = _extractor.extract()

        _unique_id = str(uuid.uuid4())
        _timestamp = datetime.now().strftime("%m/%d/%Y %I:%M:%S")

        _ft_status = "ACSP"
        _ft_reason = ""
        _ft_status_reason = ""

        _cr_account = _params.get("cr_account")
        _cr_amount = _params.get("amount")
        if _cr_account and _cr_amount:
            _acc_instances = Account.objects.filter(account_number=_cr_account, account_status="ACTIVE")
            if _acc_instances.exists():
                _acc_instance = _acc_instances.first()
                _acc_instance.balance += Decimal(_cr_amount)
                _acc_instance.save()
                _ft_status = "ACSP"
            else:
                _ft_status = "RJCT"
                _ft_reason = "Either the account does not exist or account is inactive"
                _ft_status_reason = "INACTIVE"
        else:
            _ft_status = "RJCT"
            _ft_reason = "The request payload was invalid"
            _ft_status_reason = "INVALID_REQUEST"

        _payload_context = {
            "unique_id": _unique_id,
            "timestamp": _timestamp,
            "settlement_date": datetime.now().strftime("%Y-%m-%d"),
            "receiving_bank_ref": _unique_id,
            "ft_status": _ft_status,
            "ft_reason": _ft_reason
        }

        _payload_context.update(**_params)

        project_directory = os.path.abspath(".")
        data_directory = os.path.join(project_directory, "pim", "data", "response")
        with open(os.path.join(data_directory, "pacs.002.001.05.xml")) as f:
            _data = f.read()
            _formatted_data = _data.format(**_payload_context)
            _xml = ElementTree.fromstring(_formatted_data)
            # _xmlStr = ElementTree.tostring(_xml, encoding='utf8', method='xml')
            _xmlStr = _formatted_data.replace(r"\n", "")  #""""<?xml version=\"1.0\" encoding=\"UTF-8\"?><DataPDU xmlns=\"urn:swift:saa:xsd:saa.2.0\">   <Revision>2.0.5</Revision>   <Body>      <AppHdr xmlns=\"urn:iso:std:iso:20022:tech:xsd:head.001.001.01\">         <Fr>            <FIId>               <FinInstnId>                  <BICFI>SCBLBDDX</BICFI>               </FinInstnId>            </FIId>         </Fr>         <To>            <FIId>               <FinInstnId>                  <BICFI>IDTP</BICFI>               </FinInstnId>            </FIId>         </To>         <BizMsgIdr>IDTP20210204173507310</BizMsgIdr>         <MsgDefIdr>pacs.002.001.05</MsgDefIdr>         <BizSvc>IDTP</BizSvc>         <CreDt>02/04/2021 11:36:22</CreDt>      </AppHdr>      <Document xmlns=\"urn:iso:std:iso:20022:tech:xsd:pacs.002.001.05\">         <FIToFIPmtStsRpt>            <GrpHdr>               <MsgId>96ce5f87-3262-463e-93e1-146301428707</MsgId>               <CreDtTm>02/04/2021 11:36:22</CreDtTm>            </GrpHdr>            <OrgnlGrpInfAndSts>               <OrgnlMsgId>IDTP20210204173507310</OrgnlMsgId>               <OrgnlMsgNmId>pacs.008.001.06</OrgnlMsgNmId>               <OrgnlCreDtTm>2021-02-04T17:35:07</OrgnlCreDtTm>               <GrpSts>ACSP</GrpSts>               <StsRsnInf>                  <Rsn>                     <Prtry />                  </Rsn>                  <AddtlInf />               </StsRsnInf>            </OrgnlGrpInfAndSts>            <TxInfAndSts>               <OrgnlInstrId>IDTP20210204173507310</OrgnlInstrId>               <OrgnlEndToEndId>96ce5f87-3262-463e-93e1-146301428707</OrgnlEndToEndId>               <OrgnlTxId>IDTP20210204173507310</OrgnlTxId>               <TxSts>ACSP</TxSts>               <StsRsnInf>                  <Rsn>                     <Prtry />                  </Rsn>               </StsRsnInf>               <InstgAgt>                  <FinInstnId>                     <BICFI>SCBLBDDX</BICFI>                  </FinInstnId>               </InstgAgt>               <OrgnlTxRef>                  <IntrBkSttlmDt>2021-02-04</IntrBkSttlmDt>                  <IntrBkSttlmAmt Ccy=\"BDT\">100.00</IntrBkSttlmAmt>               </OrgnlTxRef>            </TxInfAndSts>            <SplmtryData>               <PlcAndNm />               <Envlp>                  <ChannelInfo>                     <ChannelID>Online</ChannelID>                  </ChannelInfo>                  <Tx_Tracking_Info>                     <RefNo_SendingPSP />                     <RefNo_SendingBank>96ce5f87-3262-463e-93e1-146301428707</RefNo_SendingBank>                     <RefNo_ReceivingBank>96ce5f87-3262-463e-93e1-146301408707</RefNo_ReceivingBank>                     <RefNo_ReceivingPSP />                     <RefNo_IDTP>IDTP20210204173507310</RefNo_IDTP>                  </Tx_Tracking_Info>               </Envlp>            </SplmtryData>         </FIToFIPmtStsRpt>      </Document>   </Body></DataPDU>""""
            # print(_xmlStr)
            r = Response(_xmlStr, mimetype='application/json')

            try:
                # Log the request
                _log_data = {
                    "context": "PROCESS_FT",
                    "request_endpoint": None,
                    "request_data": _xml_payload,
                    "request_params": _params,
                    "response": _xmlStr,
                    "status": _ft_status,
                    "stacktrace": _ft_reason
                }

                AuditLog.log(**_log_data)
            except Exception as eexp:
                pass

            return r

    @app.route('/', methods=['GET'])
    def Index():
        print(AuditLog.objects.all())
        r = Response("Hello", mimetype='application/json')
        return r

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host="0.0.0.0", port="8021")