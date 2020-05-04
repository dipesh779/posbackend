from django.urls import path

from .views import (
    SaleReportByDatePdf, SaleReportByItemPdf, SaleReportByPaymentModePdf
)
urlpatterns = [
    path('sale/report/date/pdf', SaleReportByDatePdf.as_view()),
    path('sale/report/menu_item/pdf', SaleReportByItemPdf.as_view()),
    path('sale/report/payment_mode/pdf', SaleReportByPaymentModePdf.as_view()),

]
