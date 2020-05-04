from django.template.defaultfilters import register
from xhtml2pdf import pisa
from django.conf import settings
from django.template import Context
from django.http import HttpResponse
from django.template.loader import get_template
from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny

from sale.models import Invoice, MenuItem, Order, Itemline
from database.models import Credit
from employee.utils.token_helper import token_helper


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


class SaleReportByDatePdf(ListAPIView):
    permission_classes = [IsAuthenticated, ]
    queryset = Invoice.objects.all()

    def get(self, request):
        company, branch = token_helper(request)
        context = {}
        if request.GET.get('start_date'):
            try:
                start_date = request.GET.get('start_date')
                context['start_date'] = start_date
                end_date = request.GET.get('end_date')
                context['end_date'] = end_date
                print(end_date)
                invoices = Invoice.objects.filter(bill_date__gte=start_date, bill_date__lte=end_date, branch=branch)
            except Exception as e:
                start_date = request.GET.get('start_date')
                context['start_date'] = start_date
                invoices = Invoice.objects.filter(bill_date__gte=start_date, branch=branch)
        elif request.GET.get('date'):
            date = request.GET.get('date')
            context['date'] = date
            invoices = Invoice.objects.filter(bill_date=date, branch=branch)
        context['invoices'] = invoices
        final_amount = 0
        for invoice in invoices:
            final_amount += invoice.final_bill_amount

        template_path = 'salereportbydate.html'
        context = {
            'invoices': invoices,
            'start_date': start_date,
            'end_date': end_date,
            'final_amount': final_amount

        }
        # Create a Django response object, and specify content_type as pdf
        response = HttpResponse(content_type='application/pdf')

        """ this line downloads the pdf directly """
        # response['Content-Disposition'] = 'attachment; filename="report.pdf"'

        # find the template and render it.
        template = get_template(template_path)
        html = template.render(context)

        # create a pdf
        pisaStatus = pisa.CreatePDF(
           html, dest=response)
        # if error then show some funy view
        if pisaStatus.err:
           return HttpResponse('We had some errors <pre>' + html + '</pre>')
        return response


class SaleReportByItemPdf(ListAPIView):
    permission_classes = [IsAuthenticated, ]
    queryset = Invoice.objects.all()

    def get(self, request, *args, **kwargs):
        company, branch = token_helper(request)
        menu_item = MenuItem.objects.get(id=request.GET.get('id'))
        invoices = Invoice.objects.filter(order__itemline__item=menu_item, branch=branch)
        ordertypedict = {}
        quantitydict = {}
        amountdict = {}
        final_amount = 0
        total_quantity = 0

        for i in invoices:
            order = Order.objects.get(itemline__item=menu_item, invoice=i, branch=branch)
            ordertypedict[i.id] = order.order_type
            quantity = Itemline.objects.get(item=menu_item, order__invoice=i).quantity
            quantitydict[i.id] = quantity
            amountdict[i.id] = quantity * menu_item.price
            final_amount += quantity * menu_item.price
            total_quantity += quantity
        context = {
            'menu_item': menu_item,
            'invoices': invoices,
            'ordertypedict': ordertypedict,
            'quantitydict': quantitydict,
            'amountdict': amountdict,
            'final_amount': final_amount,
            'total_quantity': total_quantity

        }
        response = HttpResponse(content_type='application/pdf')
        template = get_template('salereportbyitem.html')
        html = template.render(context)
        pdf = pisa.CreatePDF(html, dest=response)
        if pdf.err:
            return HttpResponse('we had some errors <pre>' + html + '</pre>')
        return response


class SaleReportByPaymentModePdf(ListAPIView):

    permission_classes = [IsAuthenticated]
    queryset = Invoice.objects.all()

    def get(self, request):
        final_amount = 0
        company, branch = token_helper(request)
        context = {}
        payment_mode_dict = {}
        advanced_payment_dict = {}
        credit_payment_dict = {}
        if request.GET.get('sale_mode'):
            payment_mode = request.GET.get('sale_mode')
            invoices = Invoice.objects.filter(payment_mode=payment_mode)
            for invoice in invoices:
                try:
                    credit = Credit.objects.get(invoice=invoice)
                    if credit.credit_status == 'credited':
                        credit_payment_dict[invoice.id] = credit.transaction_amount
                        advanced_payment_dict[invoice.id] = 0
                    else:
                        advanced_payment_dict[invoice.id] = credit.transaction_amount
                        credit_payment_dict[invoice.id] = 0
                except:
                    credit_payment_dict[invoice.id] = 0
                    advanced_payment_dict[invoice.id] = 0

            context['sale_mode'] = payment_mode
        else:
            invoices = Invoice.objects.filter(branch=branch)
            for invoice in invoices:
                try:
                    credit = Credit.objects.get(invoice=invoice)
                    if credit.credit_status == 'credited':
                        credit_payment_dict[invoice.id] = credit.transaction_amount
                        advanced_payment_dict[invoice.id] = 0
                    else:
                        advanced_payment_dict[invoice.id] = credit.transaction_amount
                        credit_payment_dict[invoice.id] = 0
                except:
                    credit_payment_dict[invoice.id] = 0
                    advanced_payment_dict[invoice.id] = 0
            context['sale_mode'] = 'All'
        for invoice in invoices:
            payment_mode_dict[invoice.id] = invoice.payment_mode
            final_amount += invoice.final_bill_amount
        context['final_amount'] = final_amount
        context['invoices'] = invoices
        context['advance_payment_dict'] = advanced_payment_dict
        context['credit_payment_dict'] = credit_payment_dict
        context['payment_mode_dict'] = payment_mode_dict
        response = HttpResponse(content_type='application/pdf')
        template = get_template('salereportbysalemode.html')
        html = template.render(context)
        pdf = pisa.CreatePDF(html, dest=response)
        if pdf.err:
            return HttpResponse('we had some errors <pre>' + html + '</pre>')
        return response





























