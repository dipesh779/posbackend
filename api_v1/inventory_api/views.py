from .serializers import *
from rest_framework import generics
from django.db.models.signals import pre_save
from rest_framework import status
from inventory.models import PurchaseOrder, PurchaseItem, BillOfStock, StockComputation, \
    MenuItemCosting, ItemsForMenuItem, Vendor, ContactPerson, Vendor
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, AllowAny
from utils.create_response import create_response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
import numpy as np
from employee.models import Employee
from database.models import CompanyDetail, Branch
from employee.utils.token_helper import token_helper
from datetime import datetime,timedelta
from django.db.models import Sum
from .render import Render
from datetime import datetime, date
from django.shortcuts import get_object_or_404
from num2words import num2words
from payment.models import VendorPayment


"""Purchase Order"""
class PurchaseOrderListCreateView(generics.ListCreateAPIView):
    """
    list of all purchase order and create new purchaseorder
    """

    permission_classes = [IsAuthenticated,  ]
    def get(self, request):
        try:
            company, branch = token_helper(request)
            if branch is not None:
                purchaseorder = PurchaseOrder.objects.filter(branch=branch)
            else:
                purchaseorder = PurchaseOrder.objects.filter(branch__company=company)
            serializer = PurchaseOrderSerializer(purchaseorder, many=True)
            return Response({'message': 'purchase order list',
                             'status': status.HTTP_200_OK,
                             'response': serializer.data})
        except:
            return Response({'message': 'purchase order doesnot exist', 'status': status.HTTP_400_BAD_REQUEST})

    def post(self, request):
        company, branch = token_helper(request)
        if branch is not None:
            request.data['branch'] = branch.id
            serializer = PurchaseOrderCreateSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'purhchase order created',
                                 'status': status.HTTP_200_OK,
                                 'response': serializer.data})
            return Response({'message': serializer.errors, 'status':status.HTTP_400_BAD_REQUEST })
        else:
            return Response({
                'message': 'Unauthorized',
                'status': status.HTTP_401_UNAUTHORIZED
            })


class PurchaseOrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = PurchaseOrderSerializer
    queryset = PurchaseOrder.objects.all()

    def get(self, request, pk):
        try:
            company, branch = token_helper(request)
            purchase = PurchaseOrder.objects.get(pk=pk)
            if purchase.branch.company == company:
                serializer = PurchaseOrderCreateSerializer(purchase)
                return Response({'message': 'Purchase Order ',
                             'status': status.HTTP_200_OK,
                             'response': serializer.data})
            else:
                return Response({
                    'message': 'Unauthorized',
                    'status': status.HTTP_401_UNAUTHORIZED
                })

        except Exception as e:
            return Response({'message': "Purchase Order doesn't exist", 'status': status.HTTP_400_BAD_REQUEST})

    def update(self, request, pk):
        company, branch = token_helper(request)
        purchase = PurchaseOrder.objects.get(pk=pk)
        if purchase.branch.company == company:
            serializer = PurchaseOrderCreateSerializer(purchase, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'purchase order update ',
                                 'status': status.HTTP_200_OK,
                                'response': serializer.data})
            return Response({'message': serializer.errors, 'status': status.HTTP_400_BAD_REQUEST})
        else:
            return Response({
                'message': 'Unauthorized',
                'status': status.HTTP_401_UNAUTHORIZED
            })

    def delete(self, request, pk):
        try:
            company, branch = token_helper(request)
            purchase = PurchaseOrder.objects.get(pk=pk)
            if purchase.branch.company == company:
                purchase.delete()
                return Response({'mesaage': 'success',
                                 'status': status.HTTP_200_OK})
            else:
                return Response({
                    'message': 'Unauthorized',
                    'status': status.HTTP_401_UNAUTHORIZED
                })
        except Exception as e:
            return Response({'message': "Purchase Order doesn't exist", 'status': status.HTTP_400_BAD_REQUEST})


class BillOfStockListCreateView(generics.ListCreateAPIView):
    """
    list of bill of stock instance and create new one
    """
    permission_classes = [IsAuthenticated,  ]
    def get(self, request):
        try:
            company, branch = token_helper(request)
            if branch is not None:
                billofstock = BillOfStock.objects.filter(branch=branch)
            else:
                billofstock = BillOfStock.objects.filter(branch__company=company)
            serializer = BillOfStockSerializer(billofstock, many=True)
            return Response({'message': 'bill of stock list',
                             'status': status.HTTP_200_OK,
                             'response': serializer.data})
        except:
            return Response({'message': 'bill of stock doesnot exist', 'status': status.HTTP_400_BAD_REQUEST})

    def post(self, request):
        company, branch = token_helper(request)
        if branch is not None:
            request.data['branch'] = branch.id
            serializer = BillOfStockCreateSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'bill of stock created',
                                    'status': status.HTTP_200_OK,
                                    'response': serializer.data})
            return Response({'message': serializer.errors, 'status':status.HTTP_400_BAD_REQUEST })
        else:
            return Response({
                'message': 'Unauthorized',
                'status': status.HTTP_401_UNAUTHORIZED
            })


class BillOfStockDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    retrieve, update and delete bill of stock instance
    """
    permission_classes = [IsAuthenticated,]

    def get(self, request, pk):
        try:
            company, branch = token_helper(request)
            billofstock = BillOfStock.objects.get(pk=pk)
            if billofstock.branch.company == company:
                serializer = BillOfStockCreateSerializer(billofstock)
                return Response({'message': 'bill of stock ',
                             'status': status.HTTP_200_OK,
                             'response': serializer.data})
            else:
                return Response({
                    'message': 'Unauthorized',
                    'status': status.HTTP_401_UNAUTHORIZED
                })

        except Exception as e:
            return Response({'message': "bill of stock doesn't exist", 'status': status.HTTP_400_BAD_REQUEST})

    def update(self, request, pk):
        company, branch = token_helper(request)
        billofstock = BillOfStock.objects.get(pk=pk)
        if billofstock.branch.company == company:
            serializer = BillOfStockUpdateSerializer(billofstock, data=request.data, partial = True)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'bill of stock update ',
                                 'status': status.HTTP_200_OK,
                                'response': serializer.data})
            return Response({'message': serializer.errors, 'status': status.HTTP_400_BAD_REQUEST})
        else:
            return Response({
                'message': 'Unauthorized',
                'status': status.HTTP_401_UNAUTHORIZED
            })

    def delete(self, request, pk):
        try:
            company, branch = token_helper(request)
            billofstock = BillOfStock.objects.get(pk=pk)
            if billofstock.branch.company == company:
                billofstock.delete()
                return Response({'mesaage': 'success',
                                 'status': status.HTTP_200_OK})
            else:
                return Response({
                    'message': 'Unauthorized',
                    'status': status.HTTP_401_UNAUTHORIZED
                })
        except Exception as e:
            return Response({'message': "bill of stock doesn't exist", 'status': status.HTTP_400_BAD_REQUEST})


class StockComputationCreateView(generics.ListCreateAPIView):
    """
    list of stock instance and create new one
    """
    permission_classes = [IsAuthenticated,  ]

    def get(self, request):
        try:
            company, branch = token_helper(request)
            if branch is not None:
                stockcomputation = StockComputation.objects.filter(branch=branch)
            else:
                stockcomputation = StockComputation.objects.filter(branch__company=company)
            serializer = StockComputationSerializer(stockcomputation, many=True)
            return Response({'message': 'stock computation list',
                             'status': status.HTTP_200_OK,
                             'response': serializer.data})
        except:
            return Response({'message': 'stock computation doesnot exist', 'status': status.HTTP_400_BAD_REQUEST})

    def post(self, request):
        company, branch = token_helper(request)
        if branch is not None:
            request.data['branch'] = branch.id
            serializer = StockComputationSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'stock computation created',
                                 'status': status.HTTP_200_OK,
                                 'response': serializer.data})
            return Response({'message': "errors", 'status':status.HTTP_400_BAD_REQUEST, 
                            'response':serializer.errors })
        else:
            return Response({
                'message': 'Unauthorized',
                'status': status.HTTP_401_UNAUTHORIZED
            })


class StockComputationPopulateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated,]
    
    def get(self, request):
        try:
            company, branch = token_helper(request)
            if branch is not None:
                stockcomputation = StockComputation.objects.filter(branch=branch)
                item = stockcomputation.filter(created_at=datetime.today()-timedelta(days=1))
                
                for i in item:
                    isExists= stockcomputation.filter(created_at=datetime.today(),item=i.item).count()
                    if isExists:
                        continue
                    else:
                        s1 = StockComputation.objects.create(item=i.item,
                            branch=i.branch,
                            uom=i.uom,
                            unit_price=i.unit_price,
                            opening_stock = i.final_closing_stock,
                            received_stock=0,
                            sale =0,
                            complimentory_sale = 0,
                            expired_quantity = 0,
                            inspected_stock = 0,
                            discrepancy_stock = 0,
                            weigh_price = i.weigh_price,
                            threshold_quantity = i.threshold_quantity)       
                        s1.save()
            
            else:
                stockcomputation = StockComputation.objects.filter(branch__company=company)
                item = stockcomputation.filter(created_at=datetime.today() - timedelta(days=1))
                for i in item:
                    isExists= StockComputation.objects.filter(created_at=datetime.today(),item=i.item).count()
                    if isExists:
                        continue
                    else:
                        s1 = StockComputation.objects.create(item=i.item,
                            branch=i.branch,
                            uom=i.uom,
                            unit_price=i.unit_price,
                            opening_stock = i.final_closing_stock,
                            received_stock=0,
                            sale =0,
                            complimentory_sale = 0,
                            expired_quantity = 0,
                            inspected_stock = 0,
                            discrepancy_stock = 0,
                            weigh_price = i.weigh_price,
                            threshold_quantity = i.threshold_quantity)       
                        s1.save()


            #serializer = StockComputationSerializer(stockcomputation, many=True)
            return Response({'message': 'stock computation list',
                            'status': status.HTTP_204_NO_CONTENT})
        except Exception as e:            
            return Response({'message': 'Could not populate data.', 'error': e})


class StockComputationItemslist(generics.ListCreateAPIView):
    queryset = Stock.objects.all()
    serializer_class = ItemsListToPopulateSerializer



class StockComputationDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    retrieve, update and delete stock instance
    """
    serializer_class = StockComputationSerializer
    queryset = StockComputation.objects.all()
    permission_classes = [IsAuthenticated,]

    def get(self, request, pk):
        try:
            company, branch = token_helper(request)
            stockcomputation = StockComputation.objects.get(pk=pk)
            if stockcomputation.branch.company == company:
                serializer = StockComputationSerializer(stockcomputation)
                return Response({'message': 'stock computation ',
                             'status': status.HTTP_200_OK,
                             'response': serializer.data})
            else:
                return Response({
                    'message': 'Unauthorized',
                    'status': status.HTTP_401_UNAUTHORIZED
                })

        except Exception as e:
            return Response({'message': "stock computation doesn't exist", 'status': status.HTTP_400_BAD_REQUEST})

    def update(self, request, pk):
        company, branch = token_helper(request)
        stockcomputation = StockComputation.objects.get(pk=pk)
        if stockcomputation.branch.company == company:
            serializer = StockComputationSerializer(stockcomputation, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'stock computation update ',
                                 'status': status.HTTP_200_OK,
                                'response': serializer.data})
            return Response({'message': serializer.errors, 'status': status.HTTP_400_BAD_REQUEST})
        else:
            return Response({
                'message': 'Unauthorized',
                'status': status.HTTP_401_UNAUTHORIZED
            })

    def delete(self, request, pk):
        try:
            company, branch = token_helper(request)
            stockcomputation = StockComputation.objects.get(pk=pk)
            if stockcomputation.branch.company == company:
                stockcomputation.delete()
                return Response({'mesaage': 'success',
                                 'status': status.HTTP_200_OK})
            else:
                return Response({
                    'message': 'Unauthorized',
                    'status': status.HTTP_401_UNAUTHORIZED
                })
        except Exception as e:
            return Response({'message': "stock computation doesn't exist", 'status': status.HTTP_400_BAD_REQUEST})


class StockCreateListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated,  ]
    queryset = Stock.objects.all()
    serializer_class = StockSerializer

    def get(self, request):
        try:
            company, branch = token_helper(request)
            if branch is not None:
                stock = Stock.objects.filter(branch=branch)
            else:
                stock = Stock.objects.filter(branch__company=company)
            serializer = StockSerializer(stock, many=True)
            return Response({'message': 'stock list',
                             'status': status.HTTP_200_OK,
                             'response': serializer.data})
        except:
            return Response({'message': 'stock doesnot exist', 'status': status.HTTP_400_BAD_REQUEST})

    def post(self, request):
        company, branch = token_helper(request)
        if branch is not None:
            request.data['branch'] = branch
            serializer = StockSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'stock created',
                                 'status': status.HTTP_200_OK,
                                 'response': serializer.data})
            return Response({'message': serializer.errors, 'status':status.HTTP_400_BAD_REQUEST })

        else:
            return Response({
                'message': 'Unauthorized',
                'status': status.HTTP_401_UNAUTHORIZED
            })


class StockDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated,]
    queryset = Stock.objects.all()
    serializer_class = StockSerializer

    def delete(self, request, pk):
        try:
            company, branch = token_helper(request)
            stock = Stock.objects.get(pk=pk)
            if stock.branch.company == company:
                stock.delete()
                return Response({'mesaage': 'success',
                                 'status': status.HTTP_200_OK})
            else:
                return Response({
                    'message': 'Unauthorized',
                    'status': status.HTTP_401_UNAUTHORIZED
                })
        except Exception as e:
            return Response({'message': "stock doesn't exist", 'status': status.HTTP_400_BAD_REQUEST})


class ItemListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated,]
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    def get(self, request):
        try:
            company, branch = token_helper(request)
            if branch is not None:
                item = Item.objects.filter(branch=branch)
            else:
                item = Item.objects.filter(branch__company=company)
            serializer = ItemSerializer(item, many=True)
            return Response({'message': 'Items list',
                             'status': status.HTTP_200_OK,
                             'response': serializer.data})
        except:
            return Response({'message': 'Item doesnot exist', 'status': status.HTTP_400_BAD_REQUEST})

    def post(self, request):
        company, branch = token_helper(request)
        if branch is not None:
            request.data['branch'] = branch.id
            serializer = ItemSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'item created',
                                 'status': status.HTTP_200_OK,
                                 'response': serializer.data})
            return Response({'message': serializer.errors, 'status':status.HTTP_400_BAD_REQUEST })

        else:
            return Response({
                'message': 'Unauthorized',
                'status': status.HTTP_401_UNAUTHORIZED
            })


class ItemUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated,]
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    def get(self, request, pk):
        try:
            company, branch = token_helper(request)
            item = Item.objects.get(pk=pk)
            if item.branch.company == company:
                serializer = ItemSerializer(item)
                return Response({'message': 'item ',
                             'status': status.HTTP_200_OK,
                             'response': serializer.data})
            else:
                return Response({
                    'message': 'Unauthorized',
                    'status': status.HTTP_401_UNAUTHORIZED
                })

        except Exception as e:
            return Response({'message': "item doesn't exist", 'status': status.HTTP_400_BAD_REQUEST})

    def update(self, request, pk):
        company, branch = token_helper(request)
        item = Item.objects.get(pk=pk)
        if item.branch.company == company:
            serializer = ItemSerializer(item, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'item update ',
                                 'status': status.HTTP_200_OK,
                                'response': serializer.data})
            return Response({'message': serializer.errors, 'status': status.HTTP_400_BAD_REQUEST})
        else:
            return Response({
                'message': 'Unauthorized',
                'status': status.HTTP_401_UNAUTHORIZED
            })

    def delete(self, request, pk):
        try:
            company, branch = token_helper(request)
            item = Item.objects.get(pk=pk)
            if item.branch.company == company:
                item.delete()
                return Response({'mesaage': 'success',
                                 'status': status.HTTP_200_OK})
            else:
                return Response({
                    'message': 'Unauthorized',
                    'status': status.HTTP_401_UNAUTHORIZED
                })
        except Exception as e:
            return Response({'message': "item doesn't exist", 'status': status.HTTP_400_BAD_REQUEST})


class MenuItemCostingView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = ItemsForMenuItemSerializerList

    def get(self, request):
        try:
            company, branch = token_helper(request)
            if branch is not None:
                menu = MenuItemCosting.objects.filter(branch=branch)
            else:
                menu = MenuItemCosting.objects.filter(branch__company=company)
            serializer = MenuItemCostingListSerializer(menu, many=True)
            return Response({'message': 'menu items list',
                             'status': status.HTTP_200_OK,
                             'response': serializer.data})
        except:
            return Response({'message': 'menu item doesnot exist', 'status': status.HTTP_400_BAD_REQUEST})

    def post(self, request):
        company, branch = token_helper(request)
        if branch is not None:
            request.data['branch'] = branch.id
            serializer = MenuItemCostingSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'menu item costing created',
                                 'status': status.HTTP_200_OK,
                                 'response': serializer.data})
            return Response({'message': serializer.errors, 'status':status.HTTP_400_BAD_REQUEST })
        else:
            return Response({
                'message': 'Unauthorized',
                'status': status.HTTP_401_UNAUTHORIZED
            })


class MenuItemCostingUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated,]
    queryset = MenuItemCosting.objects.all()
    serializer_class = MenuItemCostingSerializer

    def get(self, request, pk):
        try:
            company, branch = token_helper(request)
            menu = MenuItemCosting.objects.get(pk=pk)
            if menu.branch.company == company:
                serializer = MenuItemCostingSerializer(menu)
                return Response({'message': 'menu item costing ',
                             'status': status.HTTP_200_OK,
                             'response': serializer.data})
            else:
                return Response({
                    'message': 'Unauthorized',
                    'status': status.HTTP_401_UNAUTHORIZED
                })

        except Exception as e:
            return Response({'message': "menu item costing does not exist", 'status': status.HTTP_400_BAD_REQUEST})

    def update(self, request, pk):
        company, branch = token_helper(request)
        menu = MenuItemCosting.objects.get(pk=pk)
        if menu.branch.company == company:
            serializer = MenuItemCostingSerializer(menu, data=request.data, partial = True)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'menu item costing update ',
                                 'status': status.HTTP_200_OK,
                                'response': serializer.data})
            return Response({'message': serializer.errors, 'status': status.HTTP_400_BAD_REQUEST})
        else:
            return Response({
                'message': 'Unauthorized',
                'status': status.HTTP_401_UNAUTHORIZED
            })

    def delete(self, request, pk):
        try:
            company, branch = token_helper(request)
            menu = MenuItemCosting.objects.get(pk=pk)
            if menu.branch.company == company:
                menu.delete()
                return Response({'mesaage': 'success',
                                 'status': status.HTTP_200_OK})
            else:
                return Response({
                    'message': 'Unauthorized',
                    'status': status.HTTP_401_UNAUTHORIZED
                })
        except Exception as e:
            return Response({'message': "menu item costing doesn't exist", 'status': status.HTTP_400_BAD_REQUEST})


""" Vendor """


class VendorListCreateView(generics.ListCreateAPIView):
    """
        List all Vendors or create new vendor
    """
    permission_classes = [IsAuthenticated, ]
    serializer_class = VendorSerializer

    def get(self, request):
        try:
            company, branch = token_helper(request)
            if branch is not None:
                vendor = Vendor.objects.filter(branch=branch)
            else:
                vendor = Vendor.objects.filter(branch__company=company)
            serializer = VendorSerializer(vendor, many=True)
            return Response({'message': 'vendor list',
                             'status': status.HTTP_200_OK,
                             'response': serializer.data})
        except:
            return Response({'message': 'vendor doesnot exist', 'status': status.HTTP_400_BAD_REQUEST})

    def post(self, request):
        company, branch = token_helper(request)
        if branch is not None:
            request.data['branch'] = branch.id
            serializer = VendorSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'vendor created',
                                 'status': status.HTTP_200_OK,
                                 'response': serializer.data})
            return Response({'message': serializer.errors, 'status':status.HTTP_400_BAD_REQUEST })
        else:
            return Response({
                'message': 'Unauthorized',
                'status': status.HTTP_401_UNAUTHORIZED
            })


class VendorDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
        retrieve, update or delete vendor instance
    """
    permission_classes = [IsAuthenticated, ]
    serializer_class = VendorSerializer
    queryset = Vendor.objects.all()

    def get(self, request, pk):
        try:
            company, branch = token_helper(request)
            vendor = Vendor.objects.get(pk=pk)
            if vendor.branch.company == company:
                serializer = VendorSerializer(vendor)
                return Response({'message': ' vendor',
                             'status': status.HTTP_200_OK,
                             'response': serializer.data})
            else:
                return Response({
                    'message': 'Unauthorized',
                    'status': status.HTTP_401_UNAUTHORIZED
                })

        except Exception as e:
            return Response({'message': "vednor doesnot exist", 'status': status.HTTP_400_BAD_REQUEST})

    def update(self, request, pk):
        company, branch = token_helper(request)
        vendor = Vendor.objects.get(pk=pk)
        if vendor.branch.company == company:
            serializer = VendorSerializer(vendor, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'vendor update ',
                                 'status': status.HTTP_200_OK,
                                'response': serializer.data})
            return Response({'message': serializer.errors, 'status': status.HTTP_400_BAD_REQUEST})
        else:
            return Response({
                'message': 'Unauthorized',
                'status': status.HTTP_401_UNAUTHORIZED
            })

    def delete(self, request, pk):
        try:
            company, branch = token_helper(request)
            vendor = Vendor.objects.get(pk=pk)
            if vendor.branch.company == company:
                vendor.delete()
                return Response({'mesaage': 'success',
                                 'status': status.HTTP_200_OK})
            else:
                return Response({
                    'message': 'Unauthorized',
                    'status': status.HTTP_401_UNAUTHORIZED
                })
        except Exception as e:
            return Response({'message': "vendor doesn't exist", 'status': status.HTTP_400_BAD_REQUEST})






                    # PDF Part


                    
class PurchaseOrderPdf(generics.ListAPIView):
    permission_classes = [IsAuthenticated, ]
    queryset = PurchaseOrder.objects.all()

    def get(self, request):
        company, branch = token_helper(request)
        if branch is not None:
            branch = branch
            company = branch.company                
            vendor_id = request.GET.get("vendor")
            start = request.GET.get("start")
            end = request.GET.get("end")

            if vendor_id:
                vendor=Vendor.objects.get(pk=vendor_id)
                if start and end:
                    purchase_orders = PurchaseOrder.objects.filter(vendor=vendor, branch=branch,
                            created_at__gte = start,
                            created_at__lte = end
                            ).order_by("created_at")
                    total_amount = PurchaseOrder.objects.filter(vendor=vendor, branch=branch,
                                    created_at__gte=start,
                                    created_at__lte=end
                                    ).aggregate(Sum("final_amount")).get("final_amount__sum")
                    total_amount_in_words = num2words(total_amount)
                    return Render.render('pobydaterangeandvendor.html', {'purchase_orders':purchase_orders, 
                                                                'total_amount':total_amount,
                                                                'total_amount_in_words':total_amount_in_words, 
                                                                'start_date':start, 'end_date':end, 'vendor':vendor, 
                                                                'branch':branch, 'company':company})
                else:
                    purchase_orders = PurchaseOrder.objects.filter(vendor=vendor, branch=branch).order_by("created_at")
                    total_amount = PurchaseOrder.objects.filter(vendor=vendor, branch=branch,
                                    ).aggregate(Sum("final_amount")).get("final_amount__sum")
                    total_amount_in_words = num2words(total_amount)
                    return Render.render('pobyvendor.html', {'purchase_orders':purchase_orders, 
                                                            'total_amount':total_amount,
                                                            'total_amount_in_words':total_amount_in_words, 
                                                            'vendor':vendor, 
                                                            'branch':branch, 'company':company})
            else:
                if start and end:
                    purchase_orders = PurchaseOrder.objects.filter(branch=branch,
                            created_at__gte = start,
                            created_at__lte = end).order_by("created_at")
                    vendors = Vendor.objects.all()

                    total_amounts=purchase_orders.order_by('vendor').values('vendor').annotate(sum=Sum('final_amount'))
                    amounts={}
                    final_data=[]
                    amts=[]
                    for t in total_amounts:
                        amounts[t['vendor']]=t['sum']
                        amts.append(t['vendor'])
                    

                    for v in vendors:
                        if v.id in amts:
                            data={}
                            data['vendor']=v.vendor_name
                            data['total_amount']=amounts[v.id]
                            data['total_amount_in_words']=num2words(data['total_amount'])
                            
                            lists=[]

                            for p in purchase_orders:
                                if v.id == p.vendor.id:
                                    lists.append(p)

                            data['lists']=lists
                            final_data.append(data)

                    return Render.render('pobydaterange.html', {'start_date':start, 'end_date':end,
                                                                'branch':branch, 'company':company, 
                                                                'final_data':final_data
                                                                })
                else:
                    purchase_orders = PurchaseOrder.objects.filter(branch=branch).order_by("created_at")
                    vendors = Vendor.objects.all()

                    total_amounts=purchase_orders.order_by('vendor').values('vendor').annotate(sum=Sum('final_amount'))
                    amounts={}
                    final_data=[]
                    amts=[]
                    for t in total_amounts:
                        amounts[t['vendor']]=t['sum']
                        amts.append(t['vendor'])
                    

                    for v in vendors:
                        if v.id in amts:
                            data={}
                            data['vendor']=v.vendor_name
                            data['total_amount']=amounts[v.id]
                            data['total_amount_in_words']=num2words(data['total_amount'])
                            
                            lists=[]

                            for p in purchase_orders:
                                if v.id == p.vendor.id:
                                    lists.append(p)

                            data['lists']=lists
                            final_data.append(data)

                    return Render.render('purchaseorder.html', {'branch':branch, 'company':company, 
                                                                'final_data':final_data
                                                                })



class BillOfStockPdf(generics.ListAPIView):
    permission_classes = [IsAuthenticated, ]
    queryset = BillOfStock.objects.all()
    
    def get(self, request):
        company, branch = token_helper(request)
        if branch is not None:
            branch = branch
            company = branch.company                
            vendor_id = request.GET.get("vendor")
            start = request.GET.get("start")
            end = request.GET.get("end")

            if vendor_id:
                vendor=Vendor.objects.get(pk=vendor_id)
                if start and end:
                    bill_of_stock = BillOfStock.objects.filter(vendor=vendor, branch=branch,
                            created_at__gte = start,
                            created_at__lte = end
                            )
                    total_amount = BillOfStock.objects.filter(vendor=vendor, branch=branch,
                                    created_at__gte=start,
                                    created_at__lte=end
                                    ).aggregate(Sum("final_amount")).get("final_amount__sum")
                    total_amount_in_words = num2words(total_amount)
                    return Render.render('bosbydaterangeandvendor.html', {'bill_of_stock':bill_of_stock, 
                                                                'total_amount':total_amount,
                                                                'total_amount_in_words':total_amount_in_words, 
                                                                'start_date':start, 'end_date':end, 'vendor':vendor, 
                                                                'branch':branch, 'company':company})
                else:
                    bill_of_stock = BillOfStock.objects.filter(vendor=vendor, branch=branch)
                    total_amount = BillOfStock.objects.filter(vendor=vendor, branch=branch,
                                    ).aggregate(Sum("final_amount")).get("final_amount__sum")
                    total_amount_in_words = num2words(total_amount)
                    return Render.render('bosbyvendor.html', {'bill_of_stock':bill_of_stock, 
                                                            'total_amount':total_amount,
                                                            'total_amount_in_words':total_amount_in_words, 
                                                            'vendor':vendor, 
                                                            'branch':branch, 'company':company})
            else:
                if start and end:
                    bill_of_stock = BillOfStock.objects.filter(branch=branch,
                            created_at__gte = start,
                            created_at__lte = end).order_by("created_at")
                    vendors = Vendor.objects.all()
                    # for ven in vendors:
                    #     bill = BillOfStock.objects.filter(vendor=ven.id)
                    total_amounts=bill_of_stock.order_by('vendor').values('vendor').annotate(sum=Sum('final_amount'))
                    amounts={}
                    amts=[]
                    final_data=[]
                    for t in total_amounts:
                        amounts[t['vendor']]=t['sum']
                        amts.append(t['vendor'])

                    for v in vendors:
                        if v.id in amts:
                            data={}
                            data['vendor']=v.vendor_name
                            data['total_amount']=amounts[v.id]
                            data['total_amount_in_words']=num2words(data['total_amount'])
                            
                            lists=[]

                            for p in bill_of_stock:
                                if v.id == p.vendor.id:
                                    lists.append(p)

                            data['lists']=lists
                            final_data.append(data)

                    return Render.render('bosbydaterange.html', {'start_date':start, 'end_date':end,
                                                                'branch':branch, 'company':company, 
                                                                'final_data':final_data
                                                                })

                else:
                    bill_of_stock = BillOfStock.objects.filter(branch=branch).order_by("created_at")
                    vendors = Vendor.objects.all()
                    total_amounts=bill_of_stock.order_by('vendor').values('vendor').annotate(sum=Sum('final_amount'))
                    amounts={}
                    amts=[]
                    final_data=[]
                    for t in total_amounts:
                        amounts[t['vendor']]=t['sum']
                        amts.append(t['vendor'])

                    for v in vendors:
                        if v.id in amts:
                            data={}
                            data['vendor']=v.vendor_name
                            data['total_amount']=amounts[v.id]
                            data['total_amount_in_words']=num2words(data['total_amount'])
                            
                            lists=[]

                            for p in bill_of_stock:
                                if v.id == p.vendor.id:
                                    lists.append(p)

                            data['lists']=lists
                            final_data.append(data)

                    return Render.render('billofstock.html', {'branch':branch, 'company':company, 
                                                                'final_data':final_data
                                                                })
                    

class StockComputationPdf(generics.ListAPIView):
    permission_classes = [IsAuthenticated, ]
    queryset = StockComputation.objects.all()

    def get(self, request):
        company, branch = token_helper(request)
        if branch is not None:
            stock_branch = branch
            company = branch.company
            item_id = request.GET.get("item")
            start = request.GET.get("start")
            end = request.GET.get("end")
            branch = request.GET.get("branch")
            if item_id:
                if start and end is not None:
                    item = Item.objects.get(pk=item_id)
                    stock = StockComputation.objects.filter(branch=stock_branch,item=item, created_at__gte=start,
                                                        created_at__lte=end).order_by("created_at")
                    total_sale = StockComputation.objects.filter(branch=stock_branch, 
                                                                created_at__gte=start,
                                                                created_at__lte=end,
                                                                item=item).aggregate(Sum("sale")).get("sale__sum")
                    total_amount = StockComputation.objects.filter(branch=stock_branch, 
                                                                created_at__gte=start,
                                                                created_at__lte=end,
                                                                item=item).aggregate(Sum("total_amount")).get("total_amount__sum")
                    total_discrepancy = StockComputation.objects.filter(branch=stock_branch, 
                                                                created_at__gte=start,
                                                                created_at__lte=end,
                                                                item=item).aggregate(Sum("discrepancy_stock")).get("discrepancy_stock__sum")
                    total_amount_in_words = num2words(total_amount)
                    return Render.render("stockcomputationbyitemanddatepdf.html",{"stock":stock, "item":item,"branch":branch,
                                                                    "start_date":start, "end_date":end, 
                                                                    "branch":stock_branch, "total_sale":total_sale,
                                                                    "total_discrepancy":total_discrepancy,
                                                                    "total_amount":total_amount, 'company':company,
                                                                    "total_amount_in_words":total_amount_in_words})
                    
                else:
                    item = Item.objects.get(pk=item_id)
                    stock = StockComputation.objects.filter(branch=stock_branch,item=item).order_by("created_at")
                    total_sale = StockComputation.objects.filter(branch=stock_branch, item=item
                                                                ).aggregate(Sum("sale")).get("sale__sum")
                    total_amount = StockComputation.objects.filter(branch=stock_branch, item=item
                                                                ).aggregate(Sum("total_amount")).get("total_amount__sum")
                    total_amount_in_words = num2words(total_amount)
                    total_discrepancy = StockComputation.objects.filter(branch=stock_branch,
                                                                        item=item).aggregate(Sum("discrepancy_stock")).get("discrepancy_stock__sum")
                    return Render.render("stockcomputationbyitemanddatepdf.html", {"stock":stock, "item":item, "branch":stock_branch, 
                                                                    "total_sale":total_sale, 'company':company,
                                                                    "total_discrepancy":total_discrepancy,
                                                                    "total_amount":total_amount,
                                                                    'total_amount_in_words':total_amount_in_words})
            else:
                if start and end:
                    stock = StockComputation.objects.filter(branch=stock_branch, created_at__gte=start, 
                                                            created_at__lte=end).order_by("created_at")
                    total_sale = StockComputation.objects.filter(branch=stock_branch, created_at__gte=start, 
                                                                created_at__lte=end
                                                                ).aggregate(Sum("sale")).get("sale__sum")
                    total_amount = StockComputation.objects.filter(branch=stock_branch, created_at__gte=start, 
                                                                created_at__lte=end
                                                                ).aggregate(Sum("total_amount")).get("total_amount__sum")
                    total_discrepancy = StockComputation.objects.filter(branch=stock_branch, 
                                                                created_at__gte=start,
                                                                created_at__lte=end
                                                                ).aggregate(Sum("discrepancy_stock")).get("discrepancy_stock__sum")
                    total_amount_in_words = num2words(total_amount)
                    return Render.render("stockcomputationbydatepdf.html", {"stock":stock, "branch":stock_branch, 
                                                                    "total_sale":total_sale, 'company':company,
                                                                    "total_discrepancy":total_discrepancy,
                                                                    "total_amount":total_amount,
                                                                    "start_date":start, "end_date":end,
                                                                    'total_amount_in_words':total_amount_in_words})
                else:
                    stock = StockComputation.objects.filter(branch=stock_branch).order_by("created_at")
                    total_sale = StockComputation.objects.filter(branch=stock_branch
                                                                ).aggregate(Sum("sale")).get("sale__sum")
                    total_amount = StockComputation.objects.filter(branch=stock_branch
                                                                ).aggregate(Sum("total_amount")).get("total_amount__sum")
                    total_discrepancy = StockComputation.objects.filter(branch=stock_branch
                                                                        ).aggregate(Sum("discrepancy_stock")).get("discrepancy_stock__sum")
                    total_amount_in_words = num2words(total_amount)
                    return Render.render("stockcomputationpdf.html", {"stock":stock, "branch":stock_branch, 
                                                                    "total_sale":total_sale, 'company':company,
                                                                    "total_discrepancy":total_discrepancy,
                                                                    "total_amount":total_amount,
                                                                    "start_date":start, "end_date":end,
                                                                    'total_amount_in_words':total_amount_in_words})
                    
class PurchaseOrderAnalyticsView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, ]
    queryset = PurchaseOrder.objects.all()

    def get(self, request):
        company, branch = token_helper(request)
        if branch is not None:
            branch = branch
            vendor = request.GET.get("vendor")
            start = request.GET.get("start")
            end = request.GET.get("end")
            if vendor:
                if start and end is not None:
                    purchase = PurchaseOrder.objects.filter(branch=branch, vendor=vendor, created_at__gte=start, 
                                                            created_at__lte=end).values('created_at').order_by('created_at').annotate(
                                                            total_amount=(Sum('final_amount')))
                else:
                    purchase = PurchaseOrder.objects.filter(branch=branch, vendor=vendor).values(
                                                            'created_at').order_by('created_at').annotate(
                                                            total_amount=(Sum('final_amount')))
            # else:
            #     if start and end is not None:
            #         purchase = PurchaseOrder.objects.filter(branch=branch, created_at__gte=start, 
            #                                                 created_at__lte=end).values()
        return Response({'message':'success', 'status':status.HTTP_200_OK, 'response':purchase})


class BillOfStockAnalyticsView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, ]
    queryset = BillOfStock.objects.all()

    def get(self, request):
        company, branch = token_helper(request)
        if branch is not None:
            branch = branch
            vendor = request.GET.get("vendor")
            start = request.GET.get("start")
            end = request.GET.get("end")
            if start and end is not None:
                billofstock = BillOfStock.objects.filter(branch=branch, vendor=vendor, created_at__gte=start, 
                                                        created_at__lte=end).values('created_at').order_by('created_at').annotate(
                                                        total_amount=(Sum('final_amount')))
            else:
                 billofstock = BillOfStock.objects.filter(branch=branch, vendor=vendor).values(
                                                        'created_at').order_by('created_at').annotate(
                                                        total_amount=(Sum('final_amount')))
        return Response({'message':'success', 'status':status.HTTP_200_OK, 'response':billofstock})



class StockComputationAnalyticsView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        company, branch = token_helper(request)
        if branch is not None:
            branch = branch
            item_id = request.GET.get("item")
            start = request.GET.get("start")
            end = request.GET.get("end")
            item = Item.objects.get(pk=item_id)
            if item_id and start and end:
                stock = StockComputation.objects.filter(branch=branch, created_at__gte=start,item=item, 
                                                        created_at__lte=end).values('created_at').order_by('created_at').annotate(
                                                        total_amount=(Sum('total_amount')))
            else:
                stock = StockComputation.objects.filter(branch=branch,item=item).values(
                                                        'created_at').order_by('created_at').annotate(
                                                        total_amount=(Sum('total_amount')))
        return Response({'message':'success', 'status':status.HTTP_200_OK, 'response':stock})
