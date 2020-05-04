from rest_framework.serializers import ModelSerializer
from rest_framework import serializers


class SaleReportByItemSerialzier(serializers.Serializer):
    bill_date = serializers.DateTimeField()
    total_amount = serializers.DecimalField(max_digits=10, decimal_places=2)


class SaleReportByPaymentModeSerializer(serializers.Serializer):
    bill_date = serializers.DateTimeField()
    cash = serializers.CharField(max_length=100)
    card = serializers.CharField(max_length=100)
    credit = serializers.CharField(max_length=100)



