from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from rest_framework.views import APIView


class ProcessFundTransferRequestView(APIView):
    http_method_names = ['post']
    permission_classes = (AllowAny, )

    def post(self, request, *args, **kwargs):
        print(request.data)
        return Response({}, status=status.HTTP_200_OK)