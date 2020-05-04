from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.signals import post_save
from libs.constants import PAYMENT_CHOICE, PAYMENT_STATUS, PAYMENT_MODE_FOR_VENDOR
from inventory.models import BillOfStock, Vendor
# from sale.models import Invoice
#
#
# class Payment(models.Model):
#     branch = models.ForeignKey('database.Branch', on_delete=models.CASCADE, null=True, related_name='payment')
#     invoice = models.OneToOneField('sale.Invoice', on_delete=models.CASCADE, null=True)
#     seating = models.OneToOneField('sale.Seating', on_delete=models.CASCADE, null=True, blank=True, related_name='payment')
#     bill_date = models.DateField(null=True, blank=True)
#     customer = models.ForeignKey('database.Customer', on_delete=models.CASCADE, null=True, blank=True)
#     bill_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
#     vat = models.DecimalField('VAT(%)',  max_digits=5, decimal_places=2, default=0, validators=[
#         MinValueValidator(0), MaxValueValidator(100)
#     ])
#     vat_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
#     discount = models.DecimalField('Discount(%)', max_digits=5, decimal_places=2, default=0, validators=[
#         MinValueValidator(0), MaxValueValidator(100)
#     ])
#     discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
#     service_charge = models.DecimalField("service_charge(%)",  max_digits=5, decimal_places=2, default=0, validators=[
#         MinValueValidator(0), MaxValueValidator(100)
#     ])
#     service_charge_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
#     net_bill_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
#     payment_mode = models.CharField(max_length=50, choices=PAYMENT_CHOICE, default='cash')
#     # if payment mode is card, add card detail
#     card_number = models.PositiveIntegerField(null=True, blank=True)
#     received_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
#
#     def add_payment(self, **kwargs):
#         invoice = self.invoice
#         if invoice.seating is not None:
#             self.seating = invoice.seating
#             self.order = None
#         else:
#             self.order = invoice.order
#             self.seating = None
#         self.customer_name = invoice.customer_name
#         self.vat = invoice.vat
#         self.vat_amount = invoice.vat_amount
#         self.bill_amount = invoice.bill_amount
#         self.discount_amount = invoice.discount + invoice.discount_from_reward
#         self.net_bill_amount = invoice.final_bill_amount
#         self.payment_mode = invoice.payment_mode
#         self.card_number = invoice.card_number
#         self.received_amount = invoice.paid_amount - invoice.return_amount
#         self.branch = invoice.branch
#
#     def save(self, *args, **kwargs):
#         """
#         add *args and **kwargs otherwise, it will give error
#         :param args:
#         :param kwargs:
#         :return:
#         """
#         self.add_payment()
#         super(Payment, self).save(*args, **kwargs)
#
#     def __str__(self):
#         return str(self.id)
#

""" signals """

#
# def add_payment_on_invoice_save(instance, **kwargs):
#     """
#     add payments on invoice save
#     :param instance:
#     :param kwargs:
#     :return:
#     """
#     invoice = instance
#     try:
#         payment = Payment.objects.get(invoice=invoice)
#         if instance.seating is not None:
#             payment.seating = instance.seating
#
#         else:
#             payment.order = instance.order
#             payment.seating = None
#         payment.branch = instance.branch
#         payment.customer_name = instance.customer_name
#         payment.vat = instance.vat
#         payment.vat_amount = instance.vat_amount
#         payment.bill_amount = instance.bill_amount
#         payment.discount_amount = instance.discount + instance.discount_from_reward
#         payment.net_bill_amount = instance.final_bill_amount
#         payment.payment_mode = instance.payment_mode
#         payment.card_number = instance.card_number
#         payment.received_amount = instance.paid_amount - instance.return_amount
#         payment.save()
#
#     except:
#         if instance.seating is not None:
#             seating = instance.seating
#             order = None
#         else:
#             order = instance.order
#             seating = None
#         branch = instance.branch
#         customer_name = instance.customer_name
#         vat = instance.vat
#         vat_amount = instance.vat_amount
#         bill_amount = instance.bill_amount
#         discount_amount = instance.discount + instance.discount_from_reward
#         net_bill_amount = instance.final_bill_amount
#         payment_mode = instance.payment_mode
#         card_number = instance.card_number
#         received_amount = instance.paid_amount - instance.return_amount
#         if instance.paid_amount >= instance.final_bill_amount:
#             payment = Payment.objects.create(
#                 invoice=invoice,
#                 seating=seating,
#                 order=order,
#                 customer_name=customer_name,
#                 vat=vat,
#                 vat_amount=vat_amount,
#                 bill_amount=bill_amount,
#                 discount_amount=discount_amount,
#                 net_bill_amount=net_bill_amount,
#                 payment_mode=payment_mode,
#                 card_number=card_number,
#                 service_charge=instance.service_charge,
#                 service_charge_amount=instance.service_charge_amount,
#                 received_amount=received_amount,
#                 branch=branch
#             )
#             payment.save()
#     else:
#         pass
#
#
# post_save.connect(add_payment_on_invoice_save, sender=Invoice)


class VendorPayment(models.Model):

    class Meta:
        ordering = ['-payment_status', "-created_at"]

    branch = models.ForeignKey('database.branch', on_delete=models.CASCADE, null=True, blank=True)
    bill_of_stock = models.OneToOneField(BillOfStock, on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, on_delete = models.CASCADE)
    amount = models.DecimalField(max_digits = 10, decimal_places=2)
    payment_status = models.CharField(max_length=100, choices = PAYMENT_STATUS, default="unpaid")
    payment_mode = models.CharField(max_length = 100, choices = PAYMENT_MODE_FOR_VENDOR, blank=True, null=True)
    payment_date = models.DateField(blank=True, null=True)
    bank_name = models.CharField(max_length=100, null=True, blank=True)
    cheque_number = models.BigIntegerField(null=True, blank=True)
    cheque_date = models.DateField(blank=True, null=True)
    received_by = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateField(auto_now_add = True)



    def __str__(self):
        return str(self.vendor)


def SubsractFromVendor(instance, **kwargs):
    vendor = instance
    branch = instance.branch
    if vendor.payment_status == "paid":
        ven = Vendor.objects.get(branch=branch, id = instance.vendor_id)
        if ven.total_credit_amount >= 0:
            s2 = ven.total_credit_amount - vendor.amount
        else:
            s2 = ven.total_credit_amount + vendor.amount
        ven.total_credit_amount = s2
        ven.save()
        return ven
        

post_save.connect(SubsractFromVendor, sender = VendorPayment)



def pay(instance, **kwargs):
    bill_of_stock = instance
    if bill_of_stock:
        payments =  VendorPayment.objects.create(branch = bill_of_stock.branch, 
                                                bill_of_stock = bill_of_stock, 
                                                vendor = bill_of_stock.vendor, 
                                                amount = bill_of_stock.final_amount, 
                                                payment_status = bill_of_stock.payment_status)
        payments.save()
        return payments

post_save.connect(pay, sender = BillOfStock)

