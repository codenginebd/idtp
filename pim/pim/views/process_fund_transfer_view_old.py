import os
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import HttpResponse

from lib.iso_20022_extractor import ISO20022Extractor
from lib.ws_xml_parser import WSXMLParser
from pim.models import AuditLog


@method_decorator(csrf_exempt, name='dispatch')
class ProcessFundTransferRequestViewOld(View):
    def post(self, request):
        _audit_log_instance = None

        try:
            import json
            _p = request.body.decode() # The request.data body is a ISO PACS.008.001.06 message
            _log_data = {
                "context": "RECEIVED_PROCESS_FUND_TRANSFER",
                "request_endpoint": request.path,
                "request_data": _p,
                "request_params": { k:v for k, v in request.GET.items() },
                "response": None,
                "status": None,
                "stacktrace": None
            }
            _audit_log_instance = AuditLog.log(**_log_data)

            request_data_dict = WSXMLParser.parse_response(json.loads(_p))
            _instance = ISO20022Extractor(request_body=json.loads(_p), context="process_ft")
            _eparams = _instance.extract()
            print(_eparams)
            """
            {
               "DataPDU":{
                  "@xmlns":"u:swift:saa:xsd:saa.2.0",
                  "Revision":"2.0.5",
                  "Body":{
                     "AppHdr":{
                        "@xmlns":"u:iso:std:iso:20022:tech:xsd:head.001.001.01",
                        "Fr":{
                           "FIId":{
                              "FinInstnId":{
                                 "BICFI":"SBL1BDDH"
                              }
                           }
                        },
                        "To":{
                           "FIId":{
                              "FinInstnId":{
                                 "BICFI":"IDTP"
                              }
                           }
                        },
                        "BizMsgIdr":"TXN414517826424",
                        "MsgDefIdr":"pacs.008.001.06",
                        "BizSvc":"IDTP",
                        "CreDt":"2020-12-02T15:47:34Z"
                     },
                     "Document":{
                        "@xmlns":"u:iso:std:iso:20022:tech:xsd:pacs.008.001.06",
                        "FIToFICstmrCdtTrf":{
                           "GrpHdr":{
                              "MsgId":"TXN414517826422",
                              "CreDtTm":"2020-12-02T15:47:34",
                              "NbOfTxs":"1",
                              "TtlIntrBkSttlmAmt":"202.62",
                              "IntrBkSttlmDt":"2020-12-02",
                              "SttlmInf":{
                                 "SttlmMtd":"IDTP"
                              }
                           },
                           "CdtTrfTxInf":{
                              "PmtId":{
                                 "InstrId":"TXN414517826424",
                                 "EndToEndId":"TXN414517826423",
                                 "TxId":"TXN414517826424"
                              },
                              "PmtTpInf":{
                                 "ClrChanl":"CBS",
                                 "SvcLvl":{
                                    "Prtry":"0075"
                                 },
                                 "LclInstrm":{
                                    "Prtry":"IDTP"
                                 },
                                 "CtgyPurp":{
                                    "Prtry":"001"
                                 }
                              },
                              "IntrBkSttlmAmt":{
                                 "@Ccy":"BDT",
                                 "#text":"202.62"
                              },
                              "ChrgBr":"SHAR",
                              "InstgAgt":{
                                 "FinInstnId":{
                                    "BICFI":"None"
                                 }
                              },
                              "InstdAgt":{
                                 "FinInstnId":{
                                    "BICFI":"None"
                                 }
                              },
                              "Dbtr":{
                                 "Nm":"None"
                              },
                              "DbtrAcct":{
                                 "Id":{
                                    "Othr":{
                                       "Id":"sampleUser1@user.idtp"
                                    }
                                 }
                              },
                              "DbtrAgt":{
                                 "FinInstnId":{
                                    "BICFI":"None"
                                 }
                              },
                              "DbtrAgtAcct":{
                                 "Id":{
                                    "Othr":{
                                       "Id":"None"
                                    }
                                 }
                              },
                              "CdtrAgt":{
                                 "FinInstnId":{
                                    "BICFI":"None"
                                 }
                              },
                              "CdtrAgtAcct":{
                                 "Id":{
                                    "Othr":{
                                       "Id":"None"
                                    }
                                 }
                              },
                              "Cdtr":{
                                 "Nm":"None"
                              },
                              "CdtrAcct":{
                                 "Id":{
                                    "Othr":{
                                       "Id":"sampleUser2@user.idtp"
                                    }
                                 }
                              },
                              "RmtInf":{
                                 "Ustrd":"testing transfer funds"
                              }
                           },
                           "SplmtryData":{
                              "PlcAndNm":"None",
                              "Envlp":{
                                 "Creds":{
                                    "Cred":{
                                       "@type":"IDTP_PIN",
                                       "@subtype":"",
                                       "Data":"XXXXXX"
                                    }
                                 },
                                 "ChannelInfo":{
                                    "ChannelID":"Online"
                                 },
                                 "Device_Info":{
                                    "Device_ID":"None",
                                    "Mobile_No":"None",
                                    "Location":"None",
                                    "IP":"None"
                                 },
                                 "Tx_Tracking_Info":{
                                    "RefNo_SendingPSP":"None",
                                    "RefNo_SendingBank":"TXN414517826421",
                                    "RefNo_ReceivingBank":"None",
                                    "RefNo_ReceivingPSP":"None",
                                    "RefNo_IDTP":"None"
                                 }
                              }
                           }
                        }
                     }
                  }
               }
            }
            """
            project_directory = os.path.abspath(".")
            data_directory = os.path.join(project_directory, "pim", "data", "response")
            with open(os.path.join(data_directory, "pacs.002.001.05.xml")) as f:
                _response = f.read()

                _audit_log_instance.response = _response
                _audit_log_instance.status = "SUCCESS"
                _audit_log_instance.save()

                return HttpResponse(_response) # pacs.002.001.05.xml
        except Exception as exp:
            print("Exception")
            print("Exception Message: ")
            print(exp)
            if _audit_log_instance:
                _audit_log_instance.status = "Failed"
                _audit_log_instance.stacktrace = exp

                if not _audit_log_instance.request_data:
                    _audit_log_instance.request_data = str(request.body)

                _audit_log_instance.save()


