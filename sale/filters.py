import django_filters

from sale.models import Invoice

class InvoiceFilter(django_filters.FilterSet):
    class Meta:
        model = Invoice
        fields = ['bill_date']


    