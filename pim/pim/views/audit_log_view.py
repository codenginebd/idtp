from django.views.generic import TemplateView
from lib.api.query.get_fi_user_list import GetRegisteredFIUserList
from pim.models import AuditLog


class AuditLogView(TemplateView):
    template_name = 'audit_log.html'

    def get(self, request):
        return super(AuditLogView, self).get(request)
    
    def get_context_data(self):
        ctx = super().get_context_data()
        ctx["audit_logs"] = AuditLog.objects.all().order_by("-id")
        return ctx