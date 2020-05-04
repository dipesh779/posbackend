from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from datetime import date
from django.db.models import Sum


# from .serializers import SaleListByDateSerailizer, SaleListByMenuItemSerializer, SaleListByPaymentModeSerializer
from .serializers import SaleReportByItemSerialzier, SaleReportByPaymentModeSerializer
from sale.models import Invoice, MenuItem, Order, Itemline, Seating
from database.models import Credit
from employee.utils.token_helper import token_helper
from api_v1.analytics_api.SalesReportServices import SaleReportByPaymentModeService


class SaleReportByMenuItem(ListAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        company, branch = token_helper(request)

        item_id = request.GET.get('id')
        start_date = request.GET.get('start')
        end_date = request.GET.get('end')

        if item_id and start_date and end_date:
            menu_item = MenuItem.objects.get(pk=item_id)
            itemlines = Itemline.objects.filter(
                order__branch=branch, order__created_at__gte=start_date, order__created_at__lte=end_date, item=menu_item)
        elif item_id:
            menu_item = MenuItem.objects.get(pk=item_id)
            itemlines = Itemline.objects.filter(
                order__branch=branch, item=menu_item)
        else:
            return Response({'message': 'Validation Error.', 'status': status.HTTP_400_BAD_REQUEST, 'response': ''})

        final_data = itemlines.order_by('order__created_at').values(
            'order__created_at').annotate(sum=Sum('price'))

        return Response({
            'message': 'sale report by menuitem',
            'status': status.HTTP_200_OK,
            'response': final_data
        })

class SaleReportByPaymentMode(ListAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        final_data = SaleReportByPaymentModeService(request)
        return Response({
            'message': 'sale report',
            'status': status.HTTP_200_OK,
            'response': final_data
        })

class DashboardData(ListAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        company, branch = token_helper(request)

        invoice_data = SaleReportByPaymentModeService(request)
        orders = Order.objects.filter(branch=branch)
        serving_tables = Seating.objects.filter(
            branch=branch, seating_status='occupied').count()
        current_orders = orders.filter(created_at=date.today()).exclude(
            order_status='served').count()

        total_orders = orders.filter(order_status='served',created_at=date.today()).count()
        final_data = {
            'table_count': serving_tables,
            'current_orders': current_orders,
            'todays_orders': total_orders,
            'sales_data': invoice_data
        }
        return Response({
            'message': 'sale report',
            'status': status.HTTP_200_OK,
            'response': final_data
        })

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
