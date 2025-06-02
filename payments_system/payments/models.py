from django.db import models


class Organization(models.Model):
    inn = models.CharField(max_length=12, unique=True)
    balance = models.BigIntegerField(default=0)

    def __str__(self):
        return f"Organization {self.inn}"


class Payment(models.Model):
    operation_id = models.UUIDField(primary_key=True)
    amount = models.BigIntegerField()
    payer_inn = models.CharField(max_length=12)
    document_number = models.CharField(max_length=50)
    document_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)


class BalanceLog(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    delta = models.BigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
