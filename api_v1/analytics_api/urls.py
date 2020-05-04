from django.urls import path

# from .views import SaleReportByDateList, SaleReportByItemList, SaleReportByPaymentModeList
from .views import SaleReportByMenuItem, SaleReportByPaymentMode, DashboardData

urlpatterns = [
    path('sale/report/payment_mode', SaleReportByPaymentMode.as_view()),
    path('sale/report/menu_item', SaleReportByMenuItem.as_view()),
    path('dashboard/stats', DashboardData.as_view()),
]