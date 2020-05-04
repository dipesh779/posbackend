import decimal
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.db.models.signals import pre_save, post_save, m2m_changed

from libs.constants import (
    ITEM_TYPE_CHOICES, ORDER_TYPE_CHOICES, ENABLE_DISABLE_CHOICES,
    PAYMENT_CHOICE, INVOICE_STATUS, SEATING_STATUS, ORDER_STATUS_CHOICES
)
from libs.validators import PHONE_REGEX
from libs.signals import set_price_for_modifiers, seating_modifier, invoice_modifier
from libs.constants import DELIVERY_CHOICES
from database.models import Customer, Reward, Floor, SeatingType, CompanyDetail, CreditHistory, Credit, Branch
from employee.models import Employee
from datetime import datetime


class Department(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, related_name='department')
    department_name = models.CharField(max_length=30)

    def __str__(self):
        return self.department_name

    def check_branch_and_company(self):
        if self.branch is not None:
            self.company = self.branch.company
        else:
            pass

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.check_branch_and_company()
        super().save()


class Category(models.Model):
    class Meta:
        verbose_name_plural = 'Categories'

    category_name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='category', null=True)

    def __str__(self):
        return self.category_name


class UnitOfMaterial(models.Model):
    company = models.ForeignKey(CompanyDetail, on_delete=models.CASCADE, related_name='uom', null=True)
    uom = models.CharField(max_length=50)

    def __str__(self):
        return self.uom


class ModifierItem(models.Model):
    modifier_name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    item_type = models.CharField(max_length=30, choices=ITEM_TYPE_CHOICES, default='veg')
    item_image = models.ImageField(blank=True, null=True)
    item_description = models.TextField(blank=True, null=True)
    uom = models.ForeignKey(UnitOfMaterial, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.modifier_name


class MenuItem(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    item_name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    item_type = models.CharField(max_length=30, choices=ITEM_TYPE_CHOICES, default='undefined')
    item_image = models.ImageField(null=True)
    item_description = models.TextField(blank=True, null=True)
    size = models.CharField(max_length=100, null=True, blank=True)
    uom = models.ForeignKey(UnitOfMaterial, on_delete=models.CASCADE, null=True)
    modifier_item = models.ManyToManyField(ModifierItem, blank=True)
    packing_charge = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)
    reward_point = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    can_be_free = models.BooleanField(default=False)

    def __str__(self):
        return self.item_name


class Delivery(models.Model):
    """
    delivery model to be used only when order_type is delivery in order model
    """

    class Meta:
        verbose_name_plural = 'Deliveries'
        
    delivery_person = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True)
    delivery_charge = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    delivery_status = models.CharField(max_length=20, choices=DELIVERY_CHOICES, default='in_progress')

    def __str__(self):
        return str(self.pk)


class Reservation(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    # phone number to be auto populated from customer id if not provided while doing reservation
    phone_number = models.CharField(max_length=15, validators=[PHONE_REGEX])
    waiter = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True, blank=True,
                               related_name='reservation_waiter')
    sd = models.DateTimeField('start time')
    ed = models.DateTimeField('end time')
    special_mention = models.TextField(blank=True, null=True)
    approved_by = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True,
                                    related_name='reservation_approved')

    def __str__(self):
        return "{}'s reservation".format(self.customer.customer_name)


class Seating(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, related_name='seating')
    floor = models.ForeignKey(Floor, on_delete=models.CASCADE, related_name='seating', null=True)
    seating_type = models.ForeignKey(SeatingType, on_delete=models.CASCADE, null=True)
    seating_number = models.PositiveIntegerField(blank=True, null=True)
    seating_name = models.CharField(max_length=100,null=True, unique=False)
    capacity = models.PositiveIntegerField(default=0)
    seating_status = models.CharField(max_length=30, choices=SEATING_STATUS, default='available')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    # if reservation relation has waiter assigned then use waiter from reservation
    # if seating_status is available then waiter and order should be null, otherwise it should have value
    waiter = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True, blank=True,
                               related_name='seating_waiter')
    # order
    # if seating_status is reserved then reservation should have vale otherwise null
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, null=True, blank=True)
    # if seatings are merged it should have value, else null
    merge_reference = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return str(self.pk)
    
    def set_company_and_branch_from_floor(self):
            self.branch = self.floor.branch
    
    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.set_company_and_branch_from_floor()
        super(Seating, self).save()


class Invoice(models.Model):
    bill_date = models.DateTimeField(default=timezone.now)
    invoice_number = models.PositiveIntegerField(unique=True, null=True)
    seating = models.ForeignKey(Seating, on_delete=models.CASCADE, null=True, blank=True, related_name='invoice')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    customer_name = models.CharField(max_length=100, null=True)
    available_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    bill_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    misc_charge = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    service_charge = models.DecimalField('Service charge(%)', max_digits=5, decimal_places=2, default=0, validators=[
        MinValueValidator(0), MaxValueValidator(100)
    ])
    pay_from_debit = models.BooleanField(default=False)
    service_charge_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, related_name='invoice')
    vat = models.DecimalField('VAT(%)', max_digits=5, decimal_places=2, default=0, validators=[
        MinValueValidator(0), MaxValueValidator(100)
    ])
    vat_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    # discount_from_reward = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    final_bill_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    return_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_mode = models.CharField(max_length=50, choices=PAYMENT_CHOICE, default='cash')
    card_number = models.PositiveIntegerField(null=True, blank=True)
    remark = models.TextField(blank=True, null=True)
    invoice_status = models.CharField(max_length=20, choices=INVOICE_STATUS, default='unpaid')
    approved_by = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True, blank=True)
    total_amount = 0
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.id)


class Order(models.Model):
    date_of_order = models.DateTimeField(auto_now_add=True)
    # if take away, add packing charge
    take_away_charge = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)
    order_type = models.CharField(max_length=15, choices=ORDER_TYPE_CHOICES, default='dine_in')
    order_status = models.CharField(max_length=30, choices=ORDER_STATUS_CHOICES, default='ordered', null=True)
    seating = models.ForeignKey(Seating, on_delete=models.CASCADE, null=True, blank=True, related_name='order')
    # if order_type is delivery then this field must have value
    delivery = models.OneToOneField(Delivery, on_delete=models.CASCADE, null=True, related_name='order', blank=True)
    delivery_charge = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, blank=True, null=True, related_name='order')
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, related_name='order')
    instruction = models.TextField(null=True, blank=True)
    final_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    waiter = models.ForeignKey(Employee, on_delete=models.CASCADE, blank=True, null=True)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, blank=True, null=True, related_name='order')
    updated = models.DateTimeField(auto_now=True)
    total_price = 0
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return 'order #{}'.format(self.pk)

    def calculation_based_on_order_type(self, **kwargs):
        if self.order_type == 'take_away':
            self.delivery = None
            self.seating = None
            self.waiter = None
            self.delivery_charge = 0
            itemline = self.itemline.all()
            packing_charge = 0
            for item in itemline:
                packing_charge = packing_charge + item.item.packing_charge * decimal.Decimal(item.quantity)
            self.take_away_charge = packing_charge

        elif self.order_type == 'delivery':
            self.seating = None
            self.waiter = None
            self.take_away_charge =0
        else:
            if self.waiter is None:
                raise ValueError('waiter is required, when order_status is "dine in"')
            if self.seating is not None:
                if self.seating.customer is not None:
                    self.customer = self.seating.customer
                else:
                    pass
            else:
                pass
            self.delivery = None
            self.delivery_charge = 0
            self.take_away_charge = 0

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.calculation_based_on_order_type()
        # self.order_final_price()
        super().save()

# using pre_save works when adding using django models and using post_save works when using postman(api)


class Itemline(models.Model):
    item = models.ForeignKey(MenuItem, on_delete=models.CASCADE, blank=False, null=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    free = models.BooleanField(default=False)
    order = models.ForeignKey(Order, related_name='itemline', on_delete=models.CASCADE, null=True)

    def check_if_item_can_be_free(self):
        if not self.item.can_be_free:
                self.free = False
        else:
            pass

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.check_if_item_can_be_free()
        if self.free:
            self.price = 0
        else:
            self.price = self.item.price * self.quantity
        super(Itemline, self).save()
        self.order.save()

    def __str__(self):
        return str(self.id)


pre_save.connect(invoice_modifier, sender=Invoice)


class NotificationTable(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, related_name='notification')
    seating_id = models.PositiveIntegerField(null=True)
    waiter_id = models.PositiveIntegerField(null=True)
    message = models.CharField(max_length=255, null=True)

    def __str__(self):
        return str(self.id)


"""
signals
"""


def notification_table_auto_create_from_seating(instance, **kwargs):
    if instance.seating_status == 'occupied':
        seating_id = instance.id
        if instance.waiter is not None:
            waiter_id = instance.waiter.id
        else:
            waiter_id = None
        branch = instance.branch
        message = "seating {}, {} ".format(instance.seating_name, instance.seating_status)
        notification= NotificationTable.objects.create(
            branch=branch,
            seating_id=seating_id,
            waiter_id=waiter_id,
            message=message
        )
        notification.save()
    else:
        pass


def notification_table_auto_create_from_order(instance, **kwargs):
    order = instance
    if order.seating is not None:
        if order.order_type == 'dine_in':
            if order.order_status == 'ordered':
                message = 'order {} created '.format(order.id)
            elif order.order_status == 'in_progress':
                message = 'order {} in progress'.format(order.id)
            elif order.order_status == 'ready':
                message = 'order {} is ready'.format(order.id)
            elif order.order_status == 'served':
                message = 'order {} is served'.format(order.id)
            else:
                message = 'order {}, revised'.format(order.id)
            branch = order.branch
            seating_id = order.seating.id
            if order.seating.waiter is not None:
                waiter_id = order.seating.waiter.id
            else:
                waiter_id = None
            notification= NotificationTable.objects.create(
                branch=branch,
                seating_id=seating_id,
                waiter_id=waiter_id,
                message=message
            )
            notification.save()
        else:
            pass
    else:
        pass


def customer_reward_calulation(instance, **kwargs):

    try:
        customer = instance.customer
        orders = Order.objects.filter(customer=customer)
        reward = 0
        rew = 0
        for order in orders:
            itemline = order.itemline.all()
            for j in itemline:
                item = j.item
                reward_point = item.reward_point * j.quantity
                reward += reward_point
        invoice_id = set()
        try:
            try:
                orders = customer.order.all()
                for order in orders:
                    invoice_id.add(order.invoice.id)
            except:
                pass
            try:
                seatings = customer.seating.all()
                for seating in seatings:
                    invoice_id.add(seating.invoice.id)
            except:
                pass
            for invoice in Invoice.objects.filter(id=invoice_id):
                discount_from_reward = invoice.discount_from_reward
                reward_percentage = invoice.customer.company.reward.reward_percentage
                r = 100 * discount_from_reward/reward_percentage
                rew += r
        except:
            pass
        customer.total_reward = reward - rew
        customer.save()
    except:
        pass


def seating_update_on_order_save(instance, **kwargs):
    try:
        seating = instance.seating
        seating.waiter = instance.waiter
        seating.seating_status = 'occupied'
        seating.save()

    except:
        pass


def seating_update_on_reservation(instance, **kwargs):
    try:
        seatings = instance.seating_set.all()
        for seating in seatings:
            seating.seating_status == 'reserved'
            seating.save()
    except:
        pass


def order_final_price(instance, **kwargs):
    total_price = 0
    itemlines = instance.itemline.all()
    itemline_id = []
    for itemline in itemlines:
        itemline_id.append(itemline.id)
    for i in itemline_id:
        itemline = Itemline.objects.get(id=i)
        total_price += itemline.price

    instance.final_price = total_price + instance.take_away_charge + instance.delivery_charge


post_save.connect(notification_table_auto_create_from_seating, sender=Seating)
post_save.connect(notification_table_auto_create_from_order, sender=Order)
post_save.connect(seating_update_on_order_save, sender=Order)
post_save.connect(seating_modifier, sender=Seating)
post_save.connect(customer_reward_calulation, sender=Order)
pre_save.connect(order_final_price, sender=Order)
post_save.connect(seating_update_on_reservation, sender=Reservation)



















