from django.contrib import admin

from . import models


@admin.register(models.Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = (
        "inn",
        "balance",
    )


@admin.register(models.Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "operation_id",
        "amount",
        "payer_inn",
        "document_number",
        "document_date",
        "created_at",
    )


@admin.register(models.BalanceLog)
class BalanceLogAdmin(admin.ModelAdmin):
    list_display = (
        "organization",
        "delta",
        "created_at",
    )
