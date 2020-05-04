from django.db import models
from django.utils import timezone
from django.conf import settings
from django.db.models.signals import post_save
from django.core.validators import MinValueValidator, MaxValueValidator


from libs.validators import PHONE_REGEX
from libs.constants import CREDIT_STATUS_CHOICES
from employee.models import Employee

User = settings.AUTH_USER_MODEL


class CompanyDetail(models.Model):
    class Meta:
        verbose_name = 'Company Detail'
        verbose_name_plural = 'Company Details'

    company_name = models.CharField(max_length=100)
    company_logo = models.ImageField(null=True)
    address = models.CharField(max_length=100)
    established = models.DateField(default=timezone.now)
    contact_number = models.CharField(max_length=17, validators=[PHONE_REGEX], null=True)
    company_vat_no = models.CharField(max_length=50, unique=True)
    vat_percentage = models.DecimalField("VAT", max_digits=10, decimal_places=2, validators=[
        (MinValueValidator(0)),
        (MaxValueValidator(100))
    ], default=0)
    vat_activated = models.BooleanField(default=False)
    service_charge = models.DecimalField("service charge(%)", max_digits=10, decimal_places=2, validators=[
        (MinValueValidator(0)),
        (MaxValueValidator(100))
    ], default=0)
    service_charge_activated = models.BooleanField(default=False)

    def __str__(self):
        return self.company_name


class Branch(models.Model):
    class Meta:
        verbose_name_plural = 'Branches'
    company = models.ForeignKey(CompanyDetail, on_delete=models.CASCADE, related_name='branch', null=True)
    location = models.CharField(max_length=100, default='head office')
    branch_contact = models.CharField(max_length=15, validators=[PHONE_REGEX], null=True)
    branch_contact_extra = models.CharField(max_length=15, validators=[PHONE_REGEX], null=True, blank=True)
    branch_manager = models.ForeignKey(Employee, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.location

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super().save()


class Reward(models.Model):
    company = models.OneToOneField(CompanyDetail, on_delete=models.CASCADE, related_name='reward', null=True)
    reward_point = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    reward_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    reward_percentage = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    # after this limit, reward will convert into discount
    reward_limit = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    active = models.BooleanField(default=True)
    created = models.DateField(auto_now_add=True)
    update = models.DateField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.reward_percentage = self.reward_amount/self.reward_point * 100
        super(Reward, self).save()

    def __str__(self):
        return str(self.id)


class Customer(models.Model):
    """
    customer of our system, only verified customer are given credit 
    """

    customer_id = models.CharField(max_length=100, unique=True)
    customer_name = models.CharField(max_length=50, null=True)
    phone_number = models.CharField(max_length=15, validators=[PHONE_REGEX], blank=True, null=True)
    home_address = models.CharField(max_length=70, null=True, blank=True)
    work_address = models.CharField(max_length=70, null=True, blank=True)
    other_address = models.CharField(max_length=70, null=True, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    created = models.DateField(auto_now_add=True)
    modified = models.DateField(auto_now=True)
    email = models.EmailField(null=True, blank=True)
    pan_number = models.CharField(max_length=50, null=True, blank=True, unique=True)
    credit_privilege = models.BooleanField(default=False)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    company = models.ForeignKey(CompanyDetail, on_delete=models.CASCADE, null=True)
    total_reward = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return str(self.customer_name)

    @property
    def available_amount(self):
        if self.credit_history is not None:
            if self.credit_history.total_debit > self.credit_history.total_credit:
                return self.credit_history.total_debit
            elif self.credit_history.total_credit > self.credit_history.total_debit:
                return -self.credit_history.total_credit
            else:
                return 0
        else:
            return 0


class CreditHistory(models.Model):
    """
    after certain credit limit, individual customers are given no more credit.
    total remaining credit to be calculated in front end summing transaction amount
    """

    class Meta:
        verbose_name_plural = 'Credit Histories'

    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, related_name='credit_history', null=True)
    total_credit = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_debit = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return str(self.customer)


class Credit(models.Model):
    """
    provide credit of individual customer.
    """

    class Meta:
        verbose_name = 'Credit',
        verbose_name_plural = 'Credits'
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, related_name='credit')
    transaction_date = models.DateTimeField(auto_now_add=True)
    credit_status = models.CharField(max_length=50, choices=CREDIT_STATUS_CHOICES, default='credited')
    remarks = models.CharField(max_length=100, null=True, blank=True)
    transaction_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    invoice = models.OneToOneField('sale.Invoice', on_delete=models.CASCADE, null=True, blank=True, related_name='credit')
    credit_history = models.ForeignKey(
        CreditHistory, on_delete=models.CASCADE, related_name='credit', null=True, blank=True)

    def __str__(self):
        return ('{}, {}' .format(self.customer,self.credit_status))


class Floor(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, related_name='floor')
    floor_name = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.floor_name)


class SeatingType(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='seating_type', null=True)
    seating_tool = models.CharField(max_length=30)

    def __str__(self):
        return self.seating_tool




"""
signal
"""


def create_credit_history(instance, **kwargs):
    """
    automatically creates/updates CreditHistory model when creating creating Credit model
    :param instance:
    :param kwargs:
    :return:
    """
    try:
        customer = instance.customer
        ch = CreditHistory.objects.get(customer=customer)
        ch.credit.add(instance)
        credit = ch.credit.all()
        total_credit = 0
        total_debit = 0
        for c in credit:
            if c.credit_status == 'credited':
                total_credit += c.transaction_amount
            else:
                total_debit += c.transaction_amount
            if total_credit >= total_debit:
                total_credit = total_credit-total_debit
                total_debit = 0
            else:
                total_debit = total_debit - total_credit
                total_credit = 0
        ch.total_credit = total_credit
        ch.total_debit = total_debit
        ch.save()

    except:
        customer = instance.customer
        if instance.credit_status == 'credited':
            total_credit = instance.transaction_amount
            total_debit = 0
        else:
            total_debit = instance.transaction_amount
            total_credit = 0

        ch = CreditHistory.objects.create(
            customer=customer,
            total_credit=total_credit,
            total_debit=total_debit,

        )
        ch.credit.add(instance)
        ch.save()


post_save.connect(create_credit_history, sender=Credit)