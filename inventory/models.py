from django.db.models.signals import pre_save
from django.db import models
from libs.constants import PAYMENT_MODE, CREDIT_LIMIT, PAYMENT_STATUS
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MinValueValidator
from sale.models import MenuItem
from datetime import datetime, timedelta
from decimal import Decimal
from django.utils import timezone
from sale.models import Invoice
from database.models import Branch
from libs.validators import PHONE_REGEX
import decimal



class TimeStamp(models.Model):
    """create a single time model for create and update and inherit to the required model"""
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        abstract = True




class Vendor(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, related_name='vendor')
    vendor_name = models.CharField(verbose_name="vendor name", max_length=100)
    address = models.TextField(verbose_name="address")
    phone_number = models.CharField(verbose_name="phone number", validators=[
        PHONE_REGEX], max_length=17, blank=True)
    email = models.EmailField(verbose_name="email")
    total_paid_amount = models.DecimalField(max_digits=20, decimal_places=2, default = 0.00,
                                            help_text="total amount paid by company", validators=[MinValueValidator('0.00')])
    total_credit_amount = models.DecimalField(max_digits=20, decimal_places=2, default = 0.00,
                                            help_text="total credit amount of company", validators=[MinValueValidator('0.00')])
    total_purchase_amount = models.DecimalField(max_digits=20, decimal_places=2,
                                                help_text="total purchase amount till date", default=0.00, validators=[MinValueValidator('0.00')])
    credit_limit = models.DecimalField(
        max_digits=20, decimal_places=0, default=0, null=True, blank=True)
    notify_credit_limit = models.CharField(max_length=100, choices=CREDIT_LIMIT, null=True, blank=True,
                                        help_text="notification for credit limits")


    def __str__(self):
        return self.vendor_name




class ContactPerson(models.Model):
    vendor = models.ForeignKey(
        Vendor, related_name="contact_persons", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    designation = models.CharField(max_length=200)
    phone_number = models.CharField(verbose_name="phone number", validators=[
        PHONE_REGEX], max_length=17)
    email = models.EmailField()
    vat_or_pan_number = models.PositiveIntegerField(
        verbose_name="vat/pan number")

    def __str__(self):
        return "{}".format(self.name)




class PurchaseOrder(TimeStamp):
    """create a single purchase order with many
     purchase items where the purchase item
        have fk with purchase order"""
    
    class Meta:
        ordering = ['id']


    branch = models.ForeignKey('database.Branch', on_delete=models.CASCADE)
    vendor = models.ForeignKey(
        Vendor, verbose_name="vendor", on_delete=models.CASCADE)
    shipping_date = models.DateField(
        verbose_name="shipping date", null=True, blank=True)
    payment_method = models.CharField(choices=PAYMENT_MODE, max_length=100,
                                      help_text="choose your payment method")
    shipping_charge = models.DecimalField(verbose_name="shipping charge",
                                          max_digits=10, decimal_places=2, default=0.00)
    additional_discount_percentage = models.DecimalField(max_digits=4, decimal_places=2,verbose_name="additional discount(%)",
                                                                 default=0.00, null=True, blank=True)
    vat = models.BooleanField(verbose_name="vat", default=True)
    tax = models.BooleanField(verbose_name="tax", default=True)
    final_amount = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        self.purchaseorder_number = PurchaseOrder.objects.count()
        super(PurchaseOrder, self).save(*args, **kwargs)



class PurchaseItem(models.Model):

    class Meta:
        ordering = ["id"]

    """create purchase items related to purchase order"""
    purchase_order = models.ForeignKey(
        PurchaseOrder, related_name="item", on_delete=models.CASCADE)
    item = models.CharField(verbose_name="item", max_length=100)
    uom = models.CharField(verbose_name="uom", max_length=100)
    unit_price = models.DecimalField(
        verbose_name="unit price", max_digits=10, decimal_places=2, validators=[MinValueValidator(0.00)])
    quantity = models.DecimalField(decimal_places=2, max_digits=10, verbose_name="quantity",
                                   validators=[MinValueValidator(0.00)])
    discount = models.DecimalField(
        verbose_name="discount(%)", max_digits=4, decimal_places=2,default=0.00 )
    amount = models.DecimalField(
        verbose_name="amount", max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return self.item

    def get_final_amount(self):
        amount = (self.unit_price * self.quantity)
        discount_amount = (self.discount * amount) / 100
        final_amount = amount - discount_amount
        return final_amount
    
    def save(self, *args, **kwargs):
        self.amount = self.get_final_amount()
        self.item = self.item.lower()
        self.uom = self.uom.lower()
        return super(PurchaseItem, self).save(*args, **kwargs)



class BillOfStock(TimeStamp):
    """create bill of stock model and update product items
        in billofstockitems model whick has fk with BOS model
        after finalising the product the product will auto populate in
        StockComputation module also can auto populate items from purchase Order
        by giving Purchase Order id """
    branch = models.ForeignKey('database.Branch', on_delete=models.CASCADE)
    invoice_number = models.PositiveIntegerField(verbose_name="invoice number")
    purchase_order = models.OneToOneField(PurchaseOrder, verbose_name="purchase order",
                                          on_delete=models.CASCADE, null=True, blank=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, null=True, blank=True)
    shipping_charge = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    additional_discount = models.DecimalField(verbose_name="additional discount(%)", max_digits=4,
                                              decimal_places=2, default=0.00, null=True, blank=True)
    vat = models.BooleanField(default=False)
    tax = models.BooleanField(default=False)
    final_amount = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    payment_mode = models.CharField(max_length=100, choices=PAYMENT_MODE, null=True, blank=True)
    credit_date = models.DateField(null=True, blank=True)
    payment_terms = models.CharField(verbose_name="payment terms",
                                     max_length=100, null=True, blank=True)
    payment_status = models.CharField(max_length=100, choices = PAYMENT_STATUS, default="unpaid")
    

    def __str__(self):
        return str(self.invoice_number)
    



class BillOfStockItem(models.Model):

    class Meta:
        ordering = ["id"]

    """can directly update items if items arrived 
        or populate ordered items by giving purchase order id in BOS module
        which have fk relation with PO this BOSitems will auto populate 
        in StockComputation after saving"""

    bill_of_stock = models.ForeignKey(BillOfStock, related_name="items", on_delete=models.CASCADE, null=True)
    item = models.CharField(verbose_name="item", max_length=100, null=True, blank=True)
    uom = models.CharField(verbose_name="uom", max_length=100, null=True, blank=True)
    unit_price = models.DecimalField(
        verbose_name="unit price", max_digits=10, decimal_places=2, null=True, blank=True,
        validators=[MinValueValidator(0.00)])
    ordered_quantity = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.00)],
                                           default=0.00)
    received_quantity = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.00)],
                                            default=0.00)
    quantity_not_received = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.00)],
                                                default=0.00)
    discount = models.DecimalField(
        verbose_name="discount(%)", max_digits=4, decimal_places=2, default=0.00)
    amount = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    created = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.item

    def get_final_bosi_amount(self):
        amount = decimal.Decimal(self.received_quantity) * decimal.Decimal(self.unit_price)
        discount_amount = (decimal.Decimal(amount) * decimal.Decimal(self.discount)) / 100
        final_amount = amount - discount_amount
        return final_amount
    
    def get_not_received_quantity(self):
        return self.ordered_quantity - self.received_quantity

    
    def save(self, *args, **kwargs):
        self.item = self.item.lower()
        self.uom = self.uom.lower()
        self.final_price = self.get_final_bosi_amount()
        self.quantity_not_received = self.get_not_received_quantity()
        return super(BillOfStockItem, self).save(*args, **kwargs)


class StockComputation(TimeStamp):
    class Meta:
        verbose_name_plural = "stock computation"
        get_latest_by = 'created_at'
    branch = models.ForeignKey('database.Branch', on_delete=models.CASCADE)
    item = models.CharField(max_length=100)
    uom = models.CharField(verbose_name="uom", max_length=100, null=True, blank=True)
    unit_price = models.DecimalField(
        verbose_name="unit price", max_digits=10, decimal_places=2, validators=[MinValueValidator(0.00)],null=True, blank=True)
    opening_stock = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    received_stock = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True)
    sale = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True)
    complimentory_sale = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True)
    expired_quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True)
    theoritical_QOH = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True)
    inspected_stock = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True)
    discrepancy_stock = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True)
    final_closing_stock = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True)
    weigh_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True)
    threshold_quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)


    def __str__(self):
        return self.item

    def get_theoritical_QOH(self):
        abc = decimal.Decimal(self.opening_stock) + decimal.Decimal(self.received_stock) - decimal.Decimal(self.sale) - decimal.Decimal(self.complimentory_sale) - decimal.Decimal(self.expired_quantity)
        return abc

    def get_discrepancy_stock(self):
        return decimal.Decimal(self.theoritical_QOH) - decimal.Decimal(self.inspected_stock)
    
    def get_total_amount(self):
        return decimal.Decimal(self.unit_price) * (decimal.Decimal(self.opening_stock) + decimal.Decimal(self.received_stock) - decimal.Decimal(self.sale) - decimal.Decimal(self.complimentory_sale) - decimal.Decimal(self.expired_quantity))
    
    
    def get_total_inspected_amount(self):
        return self.unit_price * self.inspected_stock
    
    
    def save(self, *args, **kwargs):
        if self.inspected_stock > 0:
            self.total_amount = self.get_total_inspected_amount()
        else:
            self.total_amount = self.get_total_amount()

        self.theoritical_QOH = self.get_theoritical_QOH()
        if self.inspected_stock > 0:
            self.discrepancy_stock = self.get_discrepancy_stock()
            self.final_closing_stock = self.inspected_stock
        else:
            self.final_closing_stock = self.theoritical_QOH
        return super(StockComputation, self).save(*args, **kwargs)

""" signal to auto save bill of stock item in stock computation for history"""

def stock_auto_save(instance, **kwargs):
    item = instance.item
    uom = instance.uom
    branch = instance.bill_of_stock.branch
    try:
        last_price = StockComputation.objects.filter(branch=branch,item=item).last().unit_price
        last_quantity = StockComputation.objects.filter(branch=branch,item=item).last().final_closing_stock
        latest_price = instance.unit_price
        latest_quantity = instance.received_quantity
        check_items = StockComputation.objects.get(branch=branch,item=item, created_at=datetime.today())
        check_items.item = instance.item
        check_items.uom = instance.uom
        check_items.unit_price = instance.unit_price
        check_items.received_stock += instance.received_quantity
        check_items.received_quantity = instance.received_quantity
        check_items.theoritical_QOH = check_items.opening_stock + check_items.received_stock
        check_items.final_closing_stock = check_items.theoritical_QOH
        check_items.weigh_price = ((last_price * last_quantity) + (latest_price * latest_quantity)) / (last_quantity + latest_quantity)
        check_items.save()

    except:
        if StockComputation.objects.filter(branch=branch,item=item).last() is not None:
            atam = StockComputation.objects.filter(branch=branch,item=item).last().final_closing_stock
            btm = StockComputation.objects.filter(branch=branch,item=item).last().unit_price
            bmw = StockComputation.objects.filter(branch=branch,item=item).last().final_closing_stock
            opening_stock = atam
            last_stock = bmw
            last_unit_price = btm
            last_threshold_quantity = StockComputation.objects.filter(branch=branch,item=item).last().threshold_quantity
        else:
            opening_stock = 0
            last_stock = instance.received_quantity
            last_unit_price = instance.unit_price
            last_threshold_quantity = 0
        s2 = StockComputation.objects.create(branch=branch,item=item, uom=uom, unit_price=last_unit_price, opening_stock=opening_stock, threshold_quantity=last_threshold_quantity)
        s2.received_stock = instance.received_quantity
        s2.received_quantity = instance.received_quantity
        s2.theoritical_QOH = decimal.Decimal(s2.received_quantity) + decimal.Decimal(s2.opening_stock) - decimal.Decimal(s2.sale) - decimal.Decimal(s2.complimentory_sale)
        s2.final_closing_stock = s2.theoritical_QOH
        s2.weigh_price = decimal.Decimal((last_unit_price * last_stock) / last_stock)
        b = s2.weigh_price
        s2.save()


post_save.connect(stock_auto_save, sender=BillOfStockItem)


class Stock(TimeStamp):

    class Meta:
        verbose_name_plural = "Stock"


    branch = models.ForeignKey('database.Branch', on_delete=models.CASCADE)
    item = models.CharField(max_length=100)
    uom = models.CharField(max_length=100)
    unit_price = models.DecimalField(max_digits=100, decimal_places=2)
    stock_quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    weigh_price = models.DecimalField(max_digits=5, decimal_places=2,default=0.00)
    threshold_quantity = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

    def __str__(self):
        return "{0} from {1}".format(self.item, self.branch)
    

class MenuItemCosting(models.Model):
    branch = models.ForeignKey('database.Branch', on_delete=models.CASCADE)
    menu_category_name = models.OneToOneField(MenuItem, on_delete=models.CASCADE, related_name="menu")
    selling_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="set selling price", validators=[MinValueValidator(0.00)], null=True, blank=True)
    
    def __str__(self): 
        return str(self.menu_category_name)


class ItemsForMenuItem(models.Model):
    menu = models.ForeignKey(MenuItemCosting, related_name="items", on_delete=models.CASCADE)
    item = models.ForeignKey(Stock, on_delete=models.CASCADE)
    quantity_used = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.00)])
    partial_cost = models.DecimalField(max_digits=10, decimal_places=2,default=0.00, validators=[MinValueValidator(0.00)])

    def __str__(self):
        return str(self.id)
    
    # def get_partial_cost(self):
    #     s1 = self.item.weigh_price * self.quantity_used
    #     return s1
    
    # def save(self,*args, **kwargs):
    #     self.partial_cost = self.get_partial_cost()
    #     return super(ItemsForMenuItem, self).save(*args, **kwargs)



def menu_item_signal(instance, **kwargs):
    invoice = instance
    if invoice.invoice_status == "paid" or (invoice.invoice_status == "unpaid" and invoice.payment_mode == "credit"):
        orders = invoice.order.all()
        for order in orders:
            itemlines = order.itemline.all()
            for itemline in itemlines:
                menu_item = itemline.item
                quantity = itemline.quantity
                try:
                    menu_item_costing = menu_item.menu
                    if itemline.free:
                        for i in ItemsForMenuItem.objects.filter(menu=menu_item_costing):
                            quantity_used = i.quantity_used
                            total_quantity = quantity_used * quantity
                            stock_item = i.item
                            stock_computation = StockComputation.objects.get(item=stock_item.item, created_at=datetime.today(),branch=invoice.branch)
                            stock_computation.complimentory_sale = total_quantity
                            stock_computation.save()
                    else:
                        for item in menu_item_costing.items.all():
                            quantity_used = item.quantity_used
                            total_quantity = quantity_used * quantity
                            stock_item = item.item
                            stock_computation = StockComputation.objects.get(item=stock_item.item, created_at=datetime.today(),branch=invoice.branch)
                            stock_computation.sale += total_quantity
                            stock_computation.save()
                except:
                    pass




def auto_save_from_stock(instance, **kwargs):
    branch = instance.branch
    item=instance.item
    uom=instance.uom
    unit_price = instance.unit_price
    stock_quantity = instance.final_closing_stock
    weigh_price = instance.weigh_price
    threshold_quantity = instance.threshold_quantity
    try:
        if Stock.objects.filter(branch=branch, item=item) is not None:
            s2 = Stock.objects.get(branch=branch, item=item)
            s2.uom = uom
            s2.unit_price = instance.unit_price
            s2.stock_quantity = instance.final_closing_stock
            s2.weigh_price = weigh_price
            s2.threshold_quantity = instance.threshold_quantity
            s2.save()
            return s2
    except:
        s1 = Stock.objects.create(branch=branch, item=item, uom=uom,unit_price=unit_price, stock_quantity=stock_quantity, weigh_price=weigh_price, threshold_quantity=threshold_quantity)
        s1.save()

post_save.connect(auto_save_from_stock, sender=StockComputation)






"""calculation of partial cost but auto update not working"""
# def auto_change_menu_after_price_differ(instance, **kwargs):
#     item = instance.item
#     branch = instance.branch
#     weigh_price = instance.weigh_price
#     try:
#         print("if condition_____________")
#         if ItemsForMenuItem.objects.filter(branch=branch,item=item) is not None:
#             print("try if______________")
#             m1 = ItemsForMenuItem.objects.get(branch=branch,item=item)
#             m1.partial_cost = m1.quantity * weigh_price
#             m1.save()
#             return m1
#     except:
#         print("except condition_____________")

# post_save.connect(auto_change_menu_after_price_differ,sender= Stock)


class Item(models.Model):
    branch = models.ForeignKey('database.Branch', on_delete=models.CASCADE)
    item = models.CharField(max_length=100)
    uom = models.CharField(max_length=100)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.item
    
    # def save(self, *args, **kwargs):
    #     self.item = self.item.lower()
    #     return super(Item, self).save(*args, *kwargs)
    
def item_from_po(instance, **kwargs):
    item = instance.item
    uom = instance.uom
    unit_price = instance.unit_price
    branch = instance.purchase_order.branch
    try:
        abc = Item.objects.get(item=item, branch=branch)
        abc.uom = instance.uom
        abc.unit_price = instance.unit_price
        abc.save()
    except:
        abcd = Item.objects.create(branch=branch,item=item, uom=uom, unit_price=unit_price)
        abcd.save()
    
post_save.connect(item_from_po, sender=PurchaseItem)

def item_from_bos(instance, **kwargs):
    item = instance.item
    uom = instance.uom
    unit_price = instance.unit_price
    branchs = instance.bill_of_stock.branch
    try:
        abc = Item.objects.get(item=item, branch=branchs)
        abc.uom = instance.uom
        abc.unit_price = instance.unit_price
        abc.save()
    except:
        abcd = Item.objects.create(branch=branchs,item=item, uom=uom, unit_price=unit_price)
        abcd.save()
    
post_save.connect(item_from_bos, sender=BillOfStockItem)

def items_from_stock_computation(instance, **kwargs):
    item = instance.item
    uom = instance.uom
    unit_price = instance.unit_price
    branch = instance.branch
    try:
        a1 = Item.objects.get(item=item, branch=branch)
        a1.uom = uom
        a1.unit_price = unit_price
        a1.save()
    except:
        a2 = Item.objects.create(item = item, branch=branch, uom=uom, unit_price=unit_price)
        a2.save()

post_save.connect(items_from_stock_computation, sender=StockComputation)




"""to auto save bill of stock purchase amount to vendor total purchase amount"""

def save_purchase_amount_to_related_vendor(instance, **kwargs):
    bill_of_stock = instance
    branch = instance.branch
    vendor = instance.vendor
    if Vendor.objects.filter(branch=branch, vendor_name=vendor) is not None:
        s1 = Vendor.objects.get(branch=branch, vendor_name=vendor)
        s1.total_purchase_amount += instance.final_amount
        if bill_of_stock.payment_mode == "credit":
            s1.total_credit_amount = decimal.Decimal(instance.final_amount) + decimal.Decimal(s1.total_credit_amount)
        s1.save()
        return s1


post_save.connect(save_purchase_amount_to_related_vendor, sender=BillOfStock)





"""                        # MODELS for V2


class TransferItem(TimeStamp):
    item = models.ForeignKey("StockComputation", on_delete=models.CASCADE)
    send_to = models.ForeignKey(StoreUnits, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return str(self.send_to)








class StoreUnits(models.Model):
    ###store units are like departments like Bar, Restaurant, cafe
    store_number = models.IntegerField(null=True, blank=True)
    store_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.store_name









# class Stock(TimeStamp):

#     class Meta:
#         verbose_name_plural = "stock computation Details"


#     item = models.CharField(max_length=100)
#     uom = models.CharField(max_length=100)
#     unit_price = models.DecimalField(max_digits=100, decimal_places=2)
#     stock_quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
#     threshold_quantity = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
#     weigh_price = models.DecimalField(max_digits=5, decimal_places=2,default=0.00)
#     # history = HistoricalRecords()

#     def __str__(self):
#         if self.threshold_quantity >= self.stock_quantity:
#             raise ValueError("your stock is getting low please add item greater than", self.threshold_quantity)
#         return self.item


# signal to auto save bill of stock item in stock without dublicating item
# def auto_save_stock(instance, **kwargs):
#     item = instance.item
#     uom = instance.uom
#     unit_price = instance.unit_price
#     stock_quantity = instance.received_quantity
#     weigh_price = instance.unit_price
#     try:
#         check_item = Stock.objects.get(item=item)
#         if check_item:
#             print("try, _____________________")
#             atm = Stock.objects.filter(item=instance.item).last().unit_price
#             print(atm,"atm _______________")
#             atm1 = instance.unit_price
#             print(atm1, " atm1________________")
#             atm3 = instance.received_quantity
#             print(atm3, "atm3_________________")
#             s1 = Stock.objects.get(item=instance.item)
#             s1.stock_quantity += instance.received_quantity
#             atm4 = s1.stock_quantity
#             print(atm4, "atm4____________________")
#             s1.unit_price = instance.unit_price
#             s1.weigh_price = ((atm * atm4) + (atm1 * atm3)) / (atm3 + atm4)
#             s1.save()
#     except:
#         print("except_____________________")
#         s2 = Stock.objects.create(item=item, uom= uom, unit_price= unit_price, stock_quantity = stock_quantity, weigh_price=weigh_price)
#         s2.save()
#     finally:
#         pass
    
# pre_save.connect(auto_save_stock, sender=BillOfStockItem)
"""