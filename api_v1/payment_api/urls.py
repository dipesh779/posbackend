from django.urls import path
from .views import (
    InvoiceListView, InvoiceDetailView, InvoiceUpdateView,
    InvoiceDeleteView, InvoiceCreateView, CustomerInvoiceHelperView, VendorPaymentView, VendorPaymentDetailView
)

urlpatterns = [
    path('invoice/list', InvoiceListView.as_view()),
    path('invoice/<int:pk>/detail', InvoiceDetailView.as_view()),
    path('invoice/create', InvoiceCreateView.as_view()),
    path('invoice/<int:pk>/update', InvoiceUpdateView.as_view()),
    path('invoice/<int:pk>/delete', InvoiceDeleteView.as_view()),
    path('invoice/customer', CustomerInvoiceHelperView.as_view()),


    path('vendor-payment', VendorPaymentView.as_view(),),
    path('vendor-payment/<int:pk>', VendorPaymentDetailView.as_view(),),

]
