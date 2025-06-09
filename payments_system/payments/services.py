from django.db import transaction
from django.db.models import F

from .models import BalanceLog, Organization, Payment


class PaymentService:
    @staticmethod
    def process_webhook(data):
        with transaction.atomic():
            if Payment.objects.filter(operation_id=data["operation_id"]).exists():
                return
            organization, _ = Organization.objects.select_for_update().get_or_create(
                inn=data["payer_inn"]
            )
            organization.balance = F("balance") + data["amount"]
            organization.save()
            Payment.objects.create(**data)
            BalanceLog.objects.create(organization=organization, delta=data["amount"])
            print(f"[LOG] Balance updated: {organization.inn} +{data['amount']}")
