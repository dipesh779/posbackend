from django.contrib import admin
from .models import VendorPayment


class VendorPaymentAdmin(admin.ModelAdmin):
    model = VendorPayment
    list_display = ["id", "bill_of_stock", "payment_status"]


admin.site.register(VendorPayment, VendorPaymentAdmin)

