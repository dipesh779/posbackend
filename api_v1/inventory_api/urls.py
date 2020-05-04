from django.urls import path
from .views import *

app_name = 'inventory_api'

urlpatterns = [
    path('inventory/purchase-order', PurchaseOrderListCreateView.as_view()),
    path('inventory/purchase-order/<int:pk>', PurchaseOrderDetailView.as_view()),

    path('inventory/bill-of-stock', BillOfStockListCreateView.as_view()),
    path('inventory/bill-of-stock/<int:pk>', BillOfStockDetailView.as_view()),

    path('inventory/stock-computation', StockComputationCreateView.as_view()),
    path('inventory/stock-computation-populate', StockComputationPopulateView.as_view()),
    path('inventory/stock-computation/<int:pk>', StockComputationDetailView.as_view()),
    path('inventory/stock-computation-items-list', StockComputationItemslist.as_view()),

    path('inventory/stock', StockCreateListView.as_view(), ),

    path('inventory/item', ItemListCreateView.as_view(),),
    path('inventory/item/<int:pk>', ItemUpdateDeleteView.as_view(),),

    path('inventory/menu-item-costing', MenuItemCostingView.as_view(),),
    path('inventory/menu-item-costing/<int:pk>', MenuItemCostingUpdateDeleteView.as_view(),),

    path('inventory/vendor', VendorListCreateView.as_view(),),
    path('inventory/vendor/<int:pk>', VendorDetailView.as_view(),),


    #PDF
    path("purchase-order-pdf/", PurchaseOrderPdf.as_view(),),
    path("bill-of-stock-pdf/", BillOfStockPdf.as_view(),),
    path("stock-computation-pdf/", StockComputationPdf.as_view(),),

    path("purchase-order", PurchaseOrderAnalyticsView.as_view(), ),
    path("bill-of-stock", BillOfStockAnalyticsView.as_view(), ),
    path("stock-computation", StockComputationAnalyticsView.as_view(), )
]