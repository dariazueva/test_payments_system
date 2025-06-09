from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Organization
from .serializers import WebhookSerializer
from .services import PaymentService


class BankWebhookView(APIView):
    def post(self, request):
        serializer = WebhookSerializer(data=request.data)
        if serializer.is_valid():
            PaymentService.process_webhook(serializer.validated_data)
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrganizationBalanceView(APIView):
    def get(self, request, inn):
        organization = get_object_or_404(Organization, inn=inn)
        return Response({"inn": inn, "balance": organization.balance})
