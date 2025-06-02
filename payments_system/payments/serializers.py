from rest_framework import serializers


class WebhookSerializer(serializers.Serializer):
    operation_id = serializers.UUIDField()
    amount = serializers.IntegerField()
    payer_inn = serializers.CharField()
    document_number = serializers.CharField()
    document_date = serializers.DateTimeField()
