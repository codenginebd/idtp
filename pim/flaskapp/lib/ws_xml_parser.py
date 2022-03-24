import xmltodict
import json

class WSXMLParser(object):

    @classmethod
    def parse_content_to_json(cls, xml_content_string):
        data_dict = xmltodict.parse(xml_content_string)
        json_data = json.dumps(data_dict)
        json_data = json.loads(json_data)
        return json_data

    @classmethod
    def parse_response(cls, content_string):
        try:
            return cls.parse_content_to_json(xml_content_string=content_string)
        except Exception as exp:
            print("Response parsing failed")
            print(exp)
            return {}