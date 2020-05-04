from rest_framework import generics
from .models import PurchaseOrder, BillOfStock,Vendor, PurchaseItem, Item
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, AllowAny
from utils.create_response import create_response
from database.models import CompanyDetail, Branch
from employee.utils.token_helper import token_helper
from django.db.models import Sum
from .render import Render
from datetime import datetime
from django.shortcuts import get_object_or_404


class PurchaseOrderPdf(generics.ListAPIView):
    permission_classes = [IsAuthenticated, ]
    queryset = PurchaseOrder.objects.all()

    def get(self, request):
        vendor_id = request.GET.get("vendor")
        start = request.GET.get("start")
        end = request.GET.get("end")
        vendor=Vendor.objects.get(pk=vendor_id)
        
        if start and end is not None:
            total_amount = PurchaseOrder.objects.filter(vendor=vendor, 
                                created_at__gte=start,
                                created_at__lte=end
                                ).aggregate(Sum("final_amount")).get("final_amount__sum")
            purchase_orders = PurchaseOrder.objects.filter(vendor=vendor,
                        created_at__gte = start,
                        created_at__lte = end
                        )
            return Render.render('purchaseorderpdf.html', {'purchase_orders':purchase_orders,
                                                            'vendor':vendor,
                                                            'final_amount':total_amount,
                                                            'start_date':start,
                                                            'end_date':end})

        else:
            total_amount = PurchaseOrder.objects.filter(vendor=vendor
                            ).aggregate(Sum("final_amount")).get("final_amount__sum")
            purchase_orders = PurchaseOrder.objects.filter(vendor=vendor)
            return Render.render('purchaseorderpdf.html', {'purchase_orders':purchase_orders,
                                                            'vendor':vendor, 'final_amount':total_amount,
                                                            })



class BillOfStockPdf(generics.ListAPIView):
    # permission_classes = [IsAuthenticated, ]
    queryset = BillOfStock.objects.all()
    
    def get(self, request):
        vendor_id = request.GET.get("vendor")
        start = request.GET.get("start")
        end = request.GET.get("end")
        vendor = Vendor.objects.get(pk=vendor_id)
        if start and end is not None:
            total_amount = BillOfStock.objects.filter(vendor=vendor,created_at__gte=start, 
                            created_at__lte=end).aggregate(Sum("final_amount")).get("final_amount__sum")
            bill_of_stock = BillOfStock.objects.filter(vendor=vendor,
                            created_at__gte=start,
                            created_at__lte = end)
            return Render.render('billofstockpdf.html', {'bill_of_stock':bill_of_stock, 
                                'start_date':start, 'end_date':end,
                                 'vendor':vendor, 'final_amount':total_amount})
        
        else:
            total_amount = BillOfStock.objects.filter(vendor=vendor).aggregate(Sum("final_amount")).get("final_amount__sum")
            bill_of_stock = BillOfStock.objects.filter(vendor=vendor)
            return Render.render('billofstockpdf.html', {'bill_of_stock':bill_of_stock, 
                                 'vendor':vendor, 'final_amount':total_amount})