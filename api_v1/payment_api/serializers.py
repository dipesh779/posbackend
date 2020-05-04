from rest_framework import serializers

from sale.models import Invoice
from database.models import Customer, CreditHistory
from api_v1.database_api.serializers import BranchListSerializer
from api_v1.sale_api.serializers import SeatingListSerializer, OrderListSerializer
from payment.models import VendorPayment
from inventory.models import BillOfStock

class CustomerInvoiceHelperSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = ['id', 'customer_name', 'home_address', 'pan_number', 'credit_privilege',
                  'available_amount', 'discount']


class InvoiceListSerializer(serializers.ModelSerializer):
    branch = BranchListSerializer()
    seating = SeatingListSerializer()
    order = OrderListSerializer(many=True)
    customer = CustomerInvoiceHelperSerializer()

    class Meta:
        model = Invoice
        fields = ['id', 'invoice_number', 'seating', 'order', 'available_amount', 'customer', 'customer_name', 'bill_amount',
                  'misc_charge', 'pay_from_debit', 'bill_date',
                  'service_charge','service_charge_amount', 'branch', 'vat', 'vat_amount', 'discount',
                  'final_bill_amount', 'paid_amount', 'return_amount', 'payment_mode', 'card_number', 'invoice_status',
                  'approved_by', 'remark']


class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = '__all__'



class BillOfStockDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillOfStock
        fields = ["id", "credit_date", "final_amount"]


class VendorPaymentListSerializer(serializers.ModelSerializer):
    bill_of_stock = BillOfStockDetailSerializer()
    class Meta:
        model = VendorPayment
        fields = ["id", "bill_of_stock", "vendor", "amount", "payment_status", "payment_mode", "payment_date", "bank_name", "cheque_number", "cheque_date", "received_by"]


class VendorPaymentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorPayment
        fields = ["id","branch", "bill_of_stock", "vendor", "amount","payment_status", "payment_mode", "payment_date", "bank_name", "cheque_number", "cheque_date", "received_by"]