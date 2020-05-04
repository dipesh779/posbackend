from sale.models import Invoice, MenuItem, Order, Itemline, Seating
from employee.utils.token_helper import token_helper
from django.db.models import Sum

def SaleReportByPaymentModeService(request):
    company, branch = token_helper(request)
    start_date = request.GET.get('start')
    end_date = request.GET.get('end')

    if start_date and end_date:
        invoices = Invoice.objects.filter(
            created_at__gte=start_date, created_at__lte=end_date, branch=branch)
    else:
        invoices = Invoice.objects.filter(branch=branch)

    return invoices.values('created_at', 'payment_mode').order_by(
        'created_at').annotate(sum=Sum('final_bill_amount'))
