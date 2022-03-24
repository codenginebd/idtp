from django.db import models
from pim.models.base_entity import BaseEntity


class AuditLog(BaseEntity):
    context = models.CharField(max_length=200)
    request_endpoint = models.CharField(max_length=1000, null=True, blank=True)
    request_data = models.CharField(max_length=1000, null=True, blank=True)
    request_params = models.CharField(max_length=1000, null=True, blank=True)
    response = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=50, null=True, blank=True, default="SUCCESS")
    stacktrace = models.TextField(null=True, blank=True)

    @classmethod
    def log(cls, context, request_endpoint, request_data, request_params,
            response = None, status=None, stacktrace=None):
        try:
            instance = cls()
            instance.context = context
            instance.request_endpoint = request_endpoint
            instance.request_data = request_data
            instance.request_params = request_params
            instance.response = response
            instance.status = status
            instance.stacktrace = stacktrace
            instance.save()
            return instance
        except Exception as exp:
            print("Logging Failed")
            print(exp)


