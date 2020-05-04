from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework.generics import RetrieveUpdateDestroyAPIView
import numpy as np
from sale.models import  notification_table_auto_create_from_seating, notification_table_auto_create_from_order
import jwt
from pprint import pprint

from .serializers import (
    CategoryListSerialzier,
    DepartmentSerializer, CategorySerialzier, UnitOfMaterialSerailzier, MenuItemSerializer, MenuItemListserializer,
    ReservationSerilizer, SeatingSerializer, ItemlineSerializer, ItemlineListSerializer, SeatingListSerializer,
    DeliverySerializer,  OrderSerializer, OrderListSerializer, CategoryCreateUpdateSerializer, NotificationSerializer,
)
from sale.models import (
    Department, Category, UnitOfMaterial, MenuItem,  Reservation,
    Seating, Delivery, Order, Itemline, Invoice, NotificationTable
)
from employee.models import Employee
from employee.utils.token_helper import token_helper
from database.models import CompanyDetail, Branch

""" Department """


class DepartmentListView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        try:
            company, branch = token_helper(request)
            if branch is not None:
                department = Department.objects.filter(branch=branch)
            else:
                department = Department.objects.filter(branch__company=company)
            serializer = DepartmentSerializer(department, many=True)
            return Response({'message': 'Department list',
                             'status': status.HTTP_200_OK,
                             'response': serializer.data})
        except:
            return Response({'message': 'Branch doesnot exist', 'status': status.HTTP_400_BAD_REQUEST})


class DepartmentDetailView(APIView):
    """ Unused """
    permission_classes = [IsAuthenticated, ]

    def get(self, request, pk):
        try:
            department = Department.objects.get(pk=pk)
            serializer = Department(department)
            return Response({'message': 'Department {} detail'.format(department.department_name),
                             'status': status.HTTP_200_OK,
                             'response': serializer.data})

        except Exception as e:
            return Response({'message': "Department doesn't exist", 'status': status.HTTP_400_BAD_REQUEST})


class DepartmentCreateView(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        company, branch = token_helper(request)
        request.data['branch'] = branch.id
        serializer = DepartmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': '',
                             'status': status.HTTP_200_OK,
                             'response': serializer.data})
        return Response({'message': serializer.errors, 'status':status.HTTP_400_BAD_REQUEST })


class DepartmentUpdateView(APIView):
    permission_classes = [IsAuthenticated, ]

    def patch(self, request, pk, *args, **kwargs):
        company, branch = token_helper(request)
        department = Department.objects.get(pk=pk)
        if department.branch.company == company:
            serializer = DepartmentSerializer(department, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Department {} updated succesfully'.format(department.department_name),
                                 'status': status.HTTP_200_OK,
                                'response': serializer.data})
            return Response({'message': serializer.errors, 'status': status.HTTP_400_BAD_REQUEST})
        else:
            return Response({
                'message': 'Unauthorized',
                'status': status.HTTP_401_UNAUTHORIZED
            })


class DepartmentDeleteView(APIView):
    permission_classes = [IsAuthenticated, ]

    def delete(self, request, pk):
        try:
            company, branch = token_helper(request)
            department = Department.objects.get(pk=pk)
            if department.branch.company == company:
                department.delete()
                return Response({'mesaage': 'Department {} deleted successfully'.format(department.department_name),
                                 'status': status.HTTP_200_OK})
            else:
                return Response({
                    'message': 'Unauthorized',
                    'status': status.HTTP_401_UNAUTHORIZED
                })
        except Exception as e:
            return Response({'message': "Department doesn't exist", 'status': status.HTTP_400_BAD_REQUEST})


""" Category """


class CategoryListView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        '''
        pass extra parameter to get, otherwise you will get error
        :param request:
        :return:
        '''
        company, branch = token_helper(request)
        if branch is not None:
            category = Category.objects.filter(department__branch=branch)
        else:
            category = Category.objects.filter(department__branch__company=company)
        serializer = CategoryListSerialzier(category, many=True)
        return Response({'message': 'Category list', 'status': status.HTTP_200_OK, 'response': serializer.data})


class CategoryDetailView(APIView):
    """ Unused """
    permission_classes = [IsAuthenticated, ]

    def get(self, request, pk):
        try:
            category = Category.objects.get(pk=pk)
            serializer = CategorySerialzier(category)
            return Response({'message': 'Category {} detail'.format(category.category_name),
                             'status': status.HTTP_200_OK,
                             'response': serializer.data})

        except Exception as e:
            return Response({'message': "Category doesn't exist", 'status': status.HTTP_400_BAD_REQUEST})


class CategoryCreateView(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        serializer = CategoryCreateUpdateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Category created successfully',
                             'status': status.HTTP_200_OK,
                             'response': serializer.data})
        return Response({'message': serializer.errors, 'status':status.HTTP_400_BAD_REQUEST })


class CategoryUpdateView(APIView):
    permission_classes = [IsAuthenticated, ]

    def patch(self, request, pk, *args, **kwargs):
        company, branch = token_helper(request)
        category = Category.objects.get(pk=pk)
        if category.department.branch.company == company:
            serializer = CategoryCreateUpdateSerializer(category, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Category {} updated succesfully'.format(category.category_name),
                                 'status': status.HTTP_200_OK,
                                'response': serializer.data})
            return Response({'message': serializer.errors, 'status': status.HTTP_400_BAD_REQUEST})
        else:
            return Response({
                'message': 'Unauthorized',
                'status': status.HTTP_401_UNAUTHORIZED
            })


class CategoryDeleteView(APIView):
    permission_classes = [IsAuthenticated, ]

    def delete(self, request, pk):
        try:
            company, branch = token_helper(request)
            category = Category.objects.get(pk=pk)
            if category.department.company == company:
                category.delete()
                return Response({'mesaage': 'Category deleted successfully', 'status': status.HTTP_200_OK})
            else:
                return Response({
                    'message': 'Unauthorized',
                    'status': status.HTTP_401_UNAUTHORIZED
                })
        except Exception as e:
                return Response({'message': "Category doesn't exist", 'status': status.HTTP_400_BAD_REQUEST})


""" UnitOfMaterial"""


class UnitOfMaterialListView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        company, branch = token_helper(request)
        uom = company.uom.all()
        serializer = UnitOfMaterialSerailzier(uom, many=True)
        return Response({'message': 'Unit of Material list', 'status': status.HTTP_200_OK, 'response': serializer.data})


class UnitOfMaterialDetailView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request, pk):
        try:
            uom = UnitOfMaterial.objects.get(pk=pk)
            serializer = UnitOfMaterialSerailzier(uom)
            return Response({'message': '{}'.format(uom.uom),
                             'status': status.HTTP_200_OK,
                             'response': serializer.data})

        except Exception as e:
            return Response({'message': "Unit of Material doesn't exist", 'status': status.HTTP_400_BAD_REQUEST})


class UnitOfMaterialCreateView(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        company, branch = token_helper(request)
        request.data['company'] = company.id
        serializer = UnitOfMaterialSerailzier(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Unit of Material created successfully',
                             'status': status.HTTP_200_OK,
                             'response': serializer.data})
        return Response({'message': serializer.errors, 'status':status.HTTP_400_BAD_REQUEST })


class UnitOfMaterialUpdateView(APIView):
    permission_classes = [IsAuthenticated, ]

    def patch(self, request, pk, *args, **kwargs):
        company, branch = token_helper(request)
        uom = UnitOfMaterial.objects.get(pk=pk)
        if uom.company == company:
            serializer = UnitOfMaterialSerailzier(uom, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': '{} updated succesfully'.format(uom.uom),
                                 'status': status.HTTP_200_OK,
                                'response': serializer.data})
            return Response({'message': serializer.errors, 'status': status.HTTP_400_BAD_REQUEST})
        else:
            return Response({
                'message': 'Unauthorized',
                'status': status.HTTP_401_UNAUTHORIZED
            })


class UnitOfMaterialDeleteView(APIView):
    permission_classes = [IsAuthenticated, ]

    def delete(self, request, pk):
        try:
            company, branch = token_helper(request)
            uom = UnitOfMaterial.objects.get(pk=pk)
            if uom.company == company:
                uom.delete()
                return Response({'mesaage': '{} deleted successfully'.format(uom.uom),
                                 'status': status.HTTP_200_OK})
            else:
                return Response({
                    'message': 'Unauthorized',
                    'status': status.HTTP_401_UNAUTHORIZED
                })
        except Exception as e:
            return Response({'message': "Unit of Material doesn't exist", 'status': status.HTTP_400_BAD_REQUEST})


""" MenuItem """


class MenuItemListView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        '''
        pass extra parameter to get, otherwise you will get error
        :param request:
        :return:
        '''
        company, branch = token_helper(request)
        if branch is not None:
            item = MenuItem.objects.filter(category__department__branch=branch)
        else:
            item = MenuItem.objects.filter(category__department__branch__company=company)
        serializer = MenuItemListserializer(item, many=True)
        return Response({'message': 'Item list', 'status': status.HTTP_200_OK, 'response': serializer.data})


class MenuItemDetailView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request, pk):
        try:
            item = MenuItem.objects.get(pk=pk)
            serializer = MenuItemListserializer(item)
            return Response({'message': 'Item {} detail'.format(item.item_name),
                             'status': status.HTTP_200_OK,
                             'response': serializer.data})

        except Exception as e:
            return Response({'message': "Item doesn't exist", 'status': status.HTTP_400_BAD_REQUEST})


class MenuItemCreateView(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        serializer = MenuItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Item created successfully', 'status': status.HTTP_200_OK,
                             'response': serializer.data})
        return Response({'message': serializer.errors, 'status':status.HTTP_400_BAD_REQUEST })


class MenuItemUpdateView(APIView):
    permission_classes = [IsAuthenticated, ]

    def patch(self, request, pk, *args, **kwargs):
        company, branch = token_helper(request)
        item = MenuItem.objects.get(pk=pk)
        if item.category.department.branch == branch:
            serializer = MenuItemSerializer(item, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Item {} updated succesfully'.format(item.item_name),
                                 'status': status.HTTP_200_OK,
                                'response': serializer.data})
            return Response({'message': serializer.errors, 'status': status.HTTP_400_BAD_REQUEST})
        else:
            return Response({
                'message': 'Unauthenticated',
                'status': status.HTTP_401_UNAUTHORIZED
            })


class MenuItemDeleteView(APIView):
    permission_classes = [IsAuthenticated, ]

    def delete(self, request, pk):
        try:
            company, branch = token_helper(request)
            item = MenuItem.objects.get(pk=pk)
            if item.category.department.company == company:
                item.delete()
                return Response({'mesaage': 'Item {} deleted successfully'.format(item.item_name),
                                 'status': status.HTTP_200_OK})
            else:
                return Response({
                    'message': 'Unauthorized',
                    'status': status.HTTP_401_UNAUTHORIZED
                })
        except Exception as e:
            return Response({'message': "Item doesn't exist", 'status': status.HTTP_400_BAD_REQUEST})


""" Itemline"""


class ItemlineByorderView(APIView):
    permission_classes = [AllowAny, ]

    def get(self, request, pk):
        '''
        pass extra parameter to get, otherwise you will get error
        :param request:
        :return:
        '''
        try:
            order = Order.objects.get(pk=pk)
            item = Itemline.objects.filter(order=order)
            serializer = ItemlineListSerializer(item, many=True)
            return Response({'message': 'Itemline list by order',
                             'status': status.HTTP_200_OK,
                             'response': serializer.data})
        except:
            return Response({'message': 'Order does not exist', 'status': status.HTTP_400_BAD_REQUEST})


class ItemlineCreateView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ItemlineSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Itemline created successfully', 'status': status.HTTP_200_OK,
                             'response': serializer.data})
        return Response({'message': serializer.errors, 'status': status.HTTP_400_BAD_REQUEST })


class ItemlineUpdateView(APIView):
    permission_classes = [AllowAny]

    def patch(self, request, pk, *args, **kwargs):
        item = Itemline.objects.get(pk=pk)
        serializer = ItemlineSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Itemline updated succesfully',
                             'status': status.HTTP_200_OK,
                            'response': serializer.data})
        return Response({'message': serializer.errors, 'status': status.HTTP_400_BAD_REQUEST})


class ItemlineDeleteView(APIView):
    permission_classes = [AllowAny, ]

    def delete(self, request, pk):
        try:
            item = Itemline.objects.get(pk=pk)
            item.delete()
            return Response({'mesaage': 'Itemline deleted successfully',
                             'status': status.HTTP_200_OK})
        except Exception as e:
            return Response({'message': "Itemline doesn't exist", 'status': status.HTTP_400_BAD_REQUEST})


""" Reservation """


class ReservationListView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        company, branch = token_helper(request)
        if branch is not None:
            seatings = Seating.objects.filter(branch=branch)
            reservations = []
            for seating in seatings:
                reservations.append(seating.reservation)
        else:
            seatings = Seating.objects.filter(branch__company=company)
            reservations = []
            for seating in seatings:
                reservations.append(seating.reservation)
        serializer = ReservationSerilizer(reservations, many=True)
        return Response({'message': 'Reservation list', 'status': status.HTTP_200_OK, 'response': serializer.data})


class ReservationCreateView(APIView):
    permission_classes = [IsAuthenticated,]

    def post(self, request):
        serializer = ReservationSerilizer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'reservation added successfully',
                             'status': status.HTTP_200_OK,
                             'response': serializer.data})
        return Response({'message': serializer.errors, 'status':status.HTTP_400_BAD_REQUEST })


class ReservationUpdateView(APIView):
    permission_classes = [IsAuthenticated, ]

    def patch(self, request, pk, *args, **kwargs):
        company, branch = token_helper(request)
        reservation = Reservation.objects.get(pk=pk)
        if Seating.objects.filter(reservation=reservation).first().branch.company == company:
            serializer = ReservationSerilizer(reservation, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Reservation updated succesfully',
                             'status': status.HTTP_200_OK,
                            'response': serializer.data})
            return Response({'message': serializer.errors, 'status': status.HTTP_400_BAD_REQUEST})
        else:
            return Response({
                'message': 'Unauthorized',
                'status': status.HTTP_401_UNAUTHORIZED
            })


class ReservationDeleteView(APIView):
    permission_classes = [IsAuthenticated, ]

    def delete(self, request, pk):
        try:
            company, branch = token_helper(request)
            reservation = Reservation.objects.get(pk=pk)
            if Seating.objects.filter(reservation=reservation).first().branch.company == company:
                reservation.delete()
                return Response({'mesaage': 'Reservation deleted successfully',
                             'status': status.HTTP_200_OK})
            else:
                return Response({
                    'message': 'Unauthorized',
                    'status': status.HTTP_401_UNAUTHORIZED
                })
        except Exception as e:
            return Response({'message': "Reservation doesn't exist", 'status': status.HTTP_400_BAD_REQUEST})


""" Seating """


class SeatingListView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        company, branch = token_helper(request)
        if branch is not None:
            seating = branch.seating.all()
        else:
            seating = Seating.objects.filter(branch__company=company)
        serializer = SeatingListSerializer(seating, many=True)
        return Response({'message': 'seating list', 'status': status.HTTP_200_OK, 'response': serializer.data})


class SeatingDetailView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request, pk):
        try:
            seating = Seating.objects.get(pk=pk)
            serializer = SeatingListSerializer(seating)
            return Response({'message': 'Seating {} detail'.format(seating.pk),
                             'status': status.HTTP_200_OK,
                             'response': serializer.data})

        except Exception as e:
            return Response({'message': "Seating doesn't exist", 'status': status.HTTP_400_BAD_REQUEST})


class SeatingCreateView(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        company, branch = token_helper(request)
        if branch is not None:
            request.data['branch'] = branch.id
            serializer = SeatingSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                seating = Seating.objects.last()
                return Response({'message': 'Seating created successfully',
                               'status': status.HTTP_200_OK,
                             'response': serializer.data})
            return Response({'message': serializer.errors, 'status': status.HTTP_400_BAD_REQUEST})
        else:
            return Response({
                'message': 'Unauthorized',
                'status': status.HTTP_401_UNAUTHORIZED
            })


class SeatingUpdateView(APIView):
    permission_classes = [IsAuthenticated, ]

    def patch(self, request, pk, *args, **kwargs):
        company, branch = token_helper(request)
        seating = Seating.objects.get(pk=pk)
        print(seating.branch.company.id)
        print(company.id)

        if seating.branch.company == company:

            serializer = SeatingSerializer(seating, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Seating {} updated succesfully'.format(seating.pk),
                                 'status': status.HTTP_200_OK,
                                'response': serializer.data})
            return Response({'message': serializer.errors, 'status': status.HTTP_400_BAD_REQUEST})
        else:
            return Response({
                'message': 'Unauthorized',
                'status': status.HTTP_401_UNAUTHORIZED
            })


class SeatingDeleteView(APIView):
    permission_classes = [IsAuthenticated, ]

    def delete(self, request, pk):
        try:
            company, branch = token_helper(request)
            seating = Seating.objects.get(pk=pk)
            if seating.branch.company == company:
                seating.delete()
                return Response({'mesaage': 'Seating deleted successfully',
                                 'status': status.HTTP_200_OK})
            else:
                return Response({
                    'message': 'Unathorized',
                    'status': status.HTTP_401_UNAUTHORIZED
                })
        except Exception as e:
            return Response({'message': "Seating doesn't exist", 'status': status.HTTP_400_BAD_REQUEST})


class SeatingListByMergeReference(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request, id):
        try:
            obj = Seating.objects.filter(merge_reference=id)
            serializer = SeatingListSerializer(obj, many=True)
            return Response({'message': 'seating list by merge reference', 'status': status.HTTP_200_OK,
                             'response': serializer.data})
        except:
            return Response({'message': 'seating list with provided merge reference does not exist',
                             'status': status.HTTP_400_BAD_REQUEST})


class MergeSeatingView(APIView):
    permission_classes = [IsAuthenticated, ]

    def patch(self, request):
        seatings = request.data.get('tables')
        seatings_np = np.array(seatings)
        try:
            for seating in seatings:
                s = Seating.objects.get(id=seating)
                merge_reference = s.merge_reference
                if merge_reference is not None:
                    break
                else:
                    pass
        except:
            merge_reference = min(seatings)
        waiter = Employee.objects.get(id=request.data.get('waiter'))

        for i in seatings:
            seating = Seating.objects.get(id=i)
            if seating.seating_status == 'available':
                seating.waiter = waiter
                seating.seating_status = 'occupied'

            if seating.seating_status == 'occupied':
                seating.waiter = waiter

            if seating.seating_status == 'reserved':
                if seating.reservation.waiter is not None:
                    seating.waiter = seating.reservation.waiter
                    seating.seating_status = 'occupied'
                else:
                    seating.waiter = waiter

            seating.merge_reference = merge_reference
            seating.save()
        min_id = seatings_np.argmin()
        seating1 = Seating.objects.get(id=seatings.pop(min_id))
        seat = []
        for i in seatings:
            seating = Seating.objects.get(id=i)
            order = seating.order.all()
            for o in order:
                seating1.order.add(o)
            seating.order.clear()
            seat.append(seating)
        seating1.save()
        seat.append(seating1)
        serializer = SeatingListSerializer(seat, many=True)
        return Response({'message': 'Seatings successfully merged',
                         'status':status.HTTP_200_OK,
                         'response': serializer.data})


class ClearMergedSeatingView(APIView):
    permission_classes = [IsAuthenticated, ]

    def patch(self, request):
        try:
            merge_reference = request.data.get('merge_reference')
            seatings = Seating.objects.filter(merge_reference=merge_reference)
            seat = []
            for seating in seatings:
                seating.waiter = None
                seating.merge_reference = None
                seating.seating_status = 'available'
                seating.order.clear()
                seating.save()
                seat.append(seating)
            serializer = SeatingSerializer(seat, many=True)
            return Response({'message': 'seating previously merged are now available',
                             'status': status.HTTP_200_OK,
                             'response': serializer.data})
        except:
            return Response({'message': 'seating with provided merge reference does not exist',
                             'status': status.HTTP_400_BAD_REQUEST})


class ClearSeatingByInvoiceIdView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request, pk):
        try:
            invoice = Invoice.objects.get(pk=pk)
            try:
                seating = invoice.seating
                seating.order.clear()
                seating.waiter = None
                seating.merge_reference = None
                seating.customer = None
                seating.save()
                return Response({'message': 'seating successfully cleared', 'status': status.HTTP_200_OK})
            except:
                return Response({'message': 'Invoice you provided doesnot have any seatings',
                                 'status': status.HTTP_400_BAD_REQUEST})
        except:
            return Response({'message': 'Invoice doesnot exist', 'status': status.HTTP_400_BAD_REQUEST})


class ChangeSeatingView(APIView):
    permission_classes = [IsAuthenticated, ]

    def patch(self, request):
        seatings = request.data.get("seatings")

        previous_table = Seating.objects.get(id=seatings[0])
        new_table = Seating.objects.get(id=seatings[1])

        previous_table_order = previous_table.order.all()
        previous_table_waiter = previous_table.waiter

        new_table_order = new_table.order.all()
        new_table_waiter = new_table.waiter

        previous_table.waiter = new_table_waiter
        new_table.waiter = previous_table_waiter
        previous_table_order_ids = []
        new_table_order_ids = []
        for order in previous_table_order:
            new_table_order_ids.append(order.id)

        for order in new_table_order:
            previous_table_order_ids.append(order.id)
        previous_table.order.clear()
        new_table.order.clear()
        for i in previous_table_order_ids:
            previous_table.order.add(Order.objects.get(id=i))
        for i in new_table_order_ids:
            new_table.order.add(Order.objects.get(id=i))

        new_table.save()
        previous_table.save()

        seatings = [new_table, previous_table]
        serializer = SeatingSerializer(seatings, many=True)
        return Response({'message': 'Seating successfully changed',
                         'status': status.HTTP_200_OK,
                         'response': serializer.data})


""" Delivery """

""" v1.1 """


class DeliveryListView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        delivery = Delivery.objects.all()
        serializer = DeliverySerializer(delivery, many=True)
        return Response({'message': 'delivery list',
                         'status': status.HTTP_200_OK,
                         'response': serializer.data})


class DeliveryDetailView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request, pk):
        try:
            delivery = Delivery.objects.get(pk=pk)
            serializer = DeliverySerializer(delivery)
            return Response({'message': 'Delivery {} detail'.format(delivery.pk),
                             'status': status.HTTP_200_OK,
                             'response': serializer.data})

        except Exception as e:
            return Response({'message': "Delivery doesn't exist", 'status': status.HTTP_400_BAD_REQUEST})


class DeliveryCreateView(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        serializer = DeliverySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Delivery created successfully',
                             'status': status.HTTP_200_OK,
                             'response': serializer.data})
        return Response({'message': serializer.errors, 'status': status.HTTP_400_BAD_REQUEST})


class DeliveryUpdateView(APIView):
    permission_classes = [IsAuthenticated, ]

    def patch(self, request, pk, *args, **kwargs):
        delivery = Delivery.objects.get(pk=pk)
        serializer = DeliverySerializer(delivery, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Delivery {} updated succesfully'.format(delivery.pk),
                             'status': status.HTTP_200_OK,
                             'response': serializer.data})
        return Response({'message': serializer.errors, 'status': status.HTTP_400_BAD_REQUEST})


class DeliveryDeleteView(APIView):
    permission_classes = [IsAuthenticated, ]

    def delete(self, request, pk):
        try:
            delivery = Delivery.objects.get(pk=pk)
            delivery.delete()
            return Response({'mesaage': 'Delivery deleted successfully',
                             'status': status.HTTP_200_OK})
        except Exception as e:
            return Response({'message': "Delivery doesn't exist", 'status': status.HTTP_400_BAD_REQUEST})


""" Order """


class OrderListView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        company, branch = token_helper(request)
        if branch is not None:
            order = branch.order.all()
        else:
            order = Order.objects.filter(branch__company=company)
        serializer = OrderListSerializer(order, many=True)
        return Response({'message': 'Orders list', 'status': status.HTTP_200_OK, 'response': serializer.data})


class OrderDetailUpdateDelete(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request, pk):
        try:
            order = Order.objects.get(pk=pk)
            serializer = OrderListSerializer(order)
            return Response({'message': 'Order {} detail'.format(order.pk), 'status': status.HTTP_200_OK,
                             'response': serializer.data})

        except Exception as e:
            return Response({'message': "Order doesn't exist", 'status': status.HTTP_400_BAD_REQUEST})

    def patch(self, request, pk, *args, **kwargs):
        company, branch = token_helper(request)
        order = Order.objects.get(pk=pk)
        if order.branch.company == company:
            order.order_status = request.data.get('order_status', 'revised')
            serializer = OrderSerializer(order, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Order {} updated succesfully'.format(order.pk),
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
            order = Order.objects.get(pk=pk)
            if order.branch.company == company:
                order.delete()
                return Response({'mesaage': 'Order deleted successfully',
                                 'status': status.HTTP_200_OK})
            else:
                return Response({
                    'message': 'Unauthorized',
                    'status': status.HTTP_401_UNAUTHORIZED
                })
        except Exception as e:
            return Response({'message': "Order doesn't exist", 'status': status.HTTP_400_BAD_REQUEST})


class OrderCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        company, branch = token_helper(request)
        if branch is not None:
            print(branch)
            print(branch.id)
            request.data['branch'] = branch.id
            serializer = OrderSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Order created successfully',
                         'status': status.HTTP_200_OK,
                         'response': serializer.data})
            return Response({'message': serializer.errors, 'status': status.HTTP_400_BAD_REQUEST})

        else:
            return Response({
                'message': 'Unathorized',
                'status': status.HTTP_401_UNAUTHORIZED
            })


class OrderListBySeatingIdView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            seating = Seating.objects.get(pk=pk)
            try:
                order = seating.order.all()
                serializer = OrderListSerializer(order, many=True)
                return Response({'message': 'order list by seating id', 
                                'status': status.HTTP_200_OK,
                                'response': serializer.data})
            except:
                return Response({'message': 'seating doesnot have any orders', 
                                'status': status.HTTP_400_BAD_REQUEST})
        except:
            return Response({'message': 'seating doesnot exist', 
                            'status': status.HTTP_400_BAD_REQUEST})


class OrderListByMergeReferenceIdView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request, id):
        try:
            seating = Seating.objects.filter(merge_reference=id).first()
            order = seating.order.all()
            serializer = OrderListSerializer(order, many=True)
            return Response({'message': 'order list by merge reference id', 
                            'status': status.HTTP_200_OK,
                            'response': serializer.data})
        except:
            return Response({'message': 'order with given merge_reference doesnot exist',
                            'status': status.HTTP_400_BAD_REQUEST})


""" NotificationTable """


class NotificationListView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        company, branch = token_helper(request)
        if branch is not None:
            notific = branch.notification.all()
            notifications = []
            message_arr = notific.values_list('message').distinct()
            for message in message_arr:
                notification = NotificationTable.objects.filter(message=message[0]).first()
                notifications.append(notification)
        else:
            notific = NotificationTable.objects.filter(branch__company=company)
            notifications = []
            message_arr = notific.values_list('message').distinct()
            for message in message_arr:
                notification = NotificationTable.objects.filter(message=message[0]).first()
                notifications.append(notification)

        serializer = NotificationSerializer(notifications, many=True)
        return Response({
            'message': 'notification list',
            'status': status.HTTP_200_OK,
            'response': serializer.data
        })
