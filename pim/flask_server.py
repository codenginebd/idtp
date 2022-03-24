import os
import uuid
import json
from xml.etree import ElementTree
from datetime import datetime
from flask import request
from flask import Response
from django.apps import apps
from django.conf import settings

settings.configure()

settings.DEBUG = True

project_directory = os.path.abspath(".")
_db_path = os.path.join(project_directory, "db.sqlite3")

settings.DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': _db_path,
    }
}

settings.INSTALLED_APPS = ("lib", "pim")

apps.populate(settings.INSTALLED_APPS)

# import models
from pim.models.account import Account

from flask import Flask
from flask import render_template
app = Flask(__name__)

@app.route('/ProcessRTPRequest', methods=['POST'])
def ProcessRTPRequest():
    pass


@app.route('/ProcessRTPDeclinedResponse', methods=['POST'])
def ProcessRTPDeclinedResponse():
    pass


@app.route('/ValidateFIUser', methods=['POST'])
def ValidateFIUser():
    pass


@app.route('/ProcessFundTransferRequest', methods=['POST'])
def ProcessFundTransferRequest():
    from lib.iso_20022_extractor import ISO20022Extractor

    _xml_payload = request.data.decode('utf-8')
    _xml_payload = json.loads(_xml_payload)
    _xml_payload = _xml_payload[_xml_payload.rindex("<?xml"):]

    _extractor = ISO20022Extractor(request_body=_xml_payload, context="process_ft")
    _params = _extractor.extract()

    _unique_id = str(uuid.uuid4())
    _timestamp = datetime.now().strftime("%m/%d/%Y %I:%M:%S")

    _ft_status = "ACSP"
    _ft_reason = ""

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
        print(_xmlStr)
        r = Response(_xmlStr, mimetype='application/json')

        return r


@app.route('/', methods=['GET'])
def Index():
    a = Account.objects.all()
    print(a)
    r = Response("Hello", mimetype='application/json')
    return r


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="8021")