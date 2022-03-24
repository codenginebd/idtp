from django.views.generic import TemplateView
from lib.api.query.get_fi_user_list import GetRegisteredFIUserList
from pim.models import Account


class SCBAccountsView(TemplateView):
    template_name = 'accounts.html'

    def get(self, request, *args, **kwargs):
        return super(SCBAccountsView, self).get(request)
    
    def get_context_data(self):
        ctx = super().get_context_data()
        ctx["accounts"] = Account.objects.all().order_by("-date_created")
        return ctx