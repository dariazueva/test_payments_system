from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import BalanceLog, Organization, Payment
from .serializers import WebhookSerializer


class BankWebhookView(APIView):
    def post(self, request):
        serializer = WebhookSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            if Payment.objects.filter(operation_id=data["operation_id"]).exists():
                return Response(
                    {"detail": "Duplicate operation. Ignored."},
                    status=status.HTTP_200_OK,
                )
            with transaction.atomic():
                Payment.objects.create(**data)
                organization, _ = Organization.objects.get_or_create(
                    inn=data["payer_inn"]
                )
                organization.balance += data["amount"]
                organization.save()
                BalanceLog.objects.create(
                    organization=organization, delta=data["amount"]
                )
                print(f"[LOG] Balance updated: {organization.inn} +{data['amount']}")
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrganizationBalanceView(APIView):
    def get(self, request, inn):
        organization = get_object_or_404(Organization, inn=inn)
        return Response({"inn": inn, "balance": organization.balance})
