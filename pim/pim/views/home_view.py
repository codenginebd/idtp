from django.views.generic import TemplateView
from lib.api.query.get_fi_user_list import GetRegisteredFIUserList


class HomeView(TemplateView):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        return super(HomeView, self).get(request)
    
    def get_context_data(self):
        ctx = super().get_context_data()
        _instance = GetRegisteredFIUserList()
        user_list = []
        success, raw_response, response_as_json = _instance.send_request()
        print(response_as_json)
        if success and (response_as_json['GetFIUserListResponse'].get("Code") == '200' or
                        response_as_json['GetFIUserListResponse'].get("Code") == 200):
            user_list = response_as_json['GetFIUserListResponse'].get('UserInfo', [])
            if type(user_list) is dict:
                user_list = [user_list]
            print(user_list)
        else:
            print("Hmm")
        ctx["user_list"] = user_list
        return ctx
