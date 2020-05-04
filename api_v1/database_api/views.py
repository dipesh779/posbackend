from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser

from .serializers import (
    CompanyDetailSerializer, CompanySerializer, CustomerSerializer,
    CreditSerializer, CreditHistorySerializer, FloorSerializer,
    SeatingTypeSerializer,
    RewardSerializer, BranchSerializer
)
from database.models import (
    CompanyDetail, Customer,
    Credit,
    CreditHistory, Floor,
    SeatingType, Reward, Branch
)
from employee.models import Employee
from employee.utils.token_helper import token_helper


"""Company Detail"""


class ComanyListView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        obj = CompanyDetail.objects.all()
        serializer = CompanyDetailSerializer(obj, many=True)
        return Response({'message': 'Companies list', 'status': status.HTTP_200_OK, 'response': serializer.data})


class CompanyDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            company, branch = token_helper(request)
            obj = CompanyDetail.objects.get(pk=pk)
            if obj == company:
                serializer = CompanyDetailSerializer(obj)
                return Response({'message': 'Company detail',
                                 'status': status.HTTP_200_OK,
                                 'response': serializer.data})
            else:
                return Response({
                    'message': 'Unauthorized',
                    'status': status.HTTP_401_UNAUTHORIZED
                })

        except Exception as e:
            return Response({'message': "Company detail doesn't exist", 'status': status.HTTP_400_BAD_REQUEST})


class CompanyCreateView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        serializer = CompanySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Company Details successfully added',
                             'status': status.HTTP_200_OK,
                             'response': serializer.data})

        return Response({'message': serializer.errors, 'status': status.HTTP_400_BAD_REQUEST})


class CompanyUpdateView(APIView):
    permission_classes = [IsAdminUser]

    def patch(self, request, pk, *args, **kwargs):
        obj = CompanyDetail.objects.get(pk=pk)
        serializer = CompanySerializer(obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Company detail updated successfully',
                             'status': status.HTTP_200_OK,
                            'response': serializer.data})
        return Response({'message': serializer.errors, 'status': status.HTTP_400_BAD_REQUEST})


class CompanyDeleteView(APIView):
    permission_classes = [IsAdminUser]

    """
    This view maynot be necessary
    """
    def delete(self, pk, request):
        try:
            obj = CompanyDetail.objects.get(pk=pk)
            obj.delete()
            return Response({'message': 'Company detail successfully deleted',
                             'status': status.HTTP_200_OK})
        except Exception as e:
            return Response({'message': "Company detail doesn't exist", 'status': status.HTTP_400_BAD_REQUEST})


""" Customer """


class CustomerListView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        company, branch = token_helper(request)
        obj = company.customer_set.all()
        serializer = CustomerSerializer(obj, many=True)
        return Response({'message': 'Customers list', 'status': status.HTTP_200_OK, 'response': serializer.data})


class CustomerDetailView(APIView):

    """ this view maynot be used """

    permission_classes = [IsAuthenticated, ]

    def get(self, request, pk):
        try:
            obj = Customer.objects.get(pk=pk)
            serializer = CustomerSerializer(obj)
            return Response({'message': 'Customer detail',
                             'status': status.HTTP_200_OK,
                             'response': serializer.data})

        except Exception as e:
            return Response({'message': "Customer doesn't exist", 'status': status.HTTP_400_BAD_REQUEST})


class CustomerCreateView(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        company, branch = token_helper(request)
        request.data['company'] = company.id
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Customer added Successfully',
                             'status': status.HTTP_200_OK,
                             'response': serializer.data})
        return Response({'message': serializer.errors, 'status': status.HTTP_400_BAD_REQUEST})


class CustomerUpdateView(APIView):
    permission_classes = [IsAuthenticated, ]

    def patch(self, request, pk, *args, **kwargs):
        company, branch = token_helper(request)
        obj = Customer.objects.get(pk=pk)
        if obj.company == company:
            serializer = CustomerSerializer(obj, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Customer updated successfully',
                             'status': status.HTTP_200_OK,
                            'response': serializer.data})

            return Response({'message': serializer.errors, 'status': status.HTTP_400_BAD_REQUEST})
        else:
            return Response({
                'message': 'Unathorized',
                'status': status.HTTP_401_UNAUTHORIZED
            })


class CustomerDeleteView(APIView):
    permission_classes = [IsAuthenticated, ]

    def delete(self, request, pk):
        try:
            company, branch = token_helper(request)
            obj = Customer.objects.get(pk=pk, company=company)
            obj.delete()
            return Response({'message': 'Customer successfully deleted',
                             'status': status.HTTP_200_OK})
        except Exception as e:
            return Response({'message': "Customer doesn't exist", 'status': status.HTTP_400_BAD_REQUEST})


"""
Credit / credit history(front end)
"""


class CreditListByCustomerIdView(APIView):
    permission_classes = [IsAuthenticated,]

    def get(self, request, pk):
        company, branch = token_helper(request)
        customer = Customer.objects.get(pk=pk, company=company)
        obj = customer.credit.all()
        serializer = CreditSerializer(obj, many=True)
        return Response({'message': 'Credit History list', 'status': status.HTTP_200_OK, 'response': serializer.data})


class CreditCreateView(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        serializer = CreditSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'credit history added',
                             'status': status.HTTP_200_OK,
                             'response': serializer.data})
        return Response({'message': serializer.errors, 'status': status.HTTP_400_BAD_REQUEST})


class CreditDeleteView(APIView):
    permission_classes = [IsAuthenticated, ]

    def delete(self, request, pk):
        try:
            company, branch = token_helper(request)
            obj = Credit.objects.get(pk=pk)
            if obj.customer.company == company:
                obj.delete()
                return Response({'message': 'Credit detail successfully deleted',
                                'status': status.HTTP_200_OK})
            else:
                return Response({
                    'message': 'Unathorized',
                    'status': status.HTTP_401_UNAUTHORIZED
                })
        except Exception as e:
            return Response({'message': "Credit detail doesn't exist", 'status': status.HTTP_400_BAD_REQUEST})


""" Credit History"""


class CreditHistoryListView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        company, branch = token_helper(request)
        obj = CreditHistory.objects.filter(customer__company=company)
        serializer = CreditHistorySerializer(obj, many=True)
        return Response({'message': 'Credit List', 'status': status.HTTP_200_OK, 'response': serializer.data})
#
#
# class CreditHistoryDetailView(APIView):
#
#     def get(self, request, pk):
#         try:
#             obj = CreditHistory.objects.get(pk=pk)
#             serializer = CreditHistorySerializer(obj)
#             return Response({'message': 'Credit detail',
#                              'status': status.HTTP_200_OK,
#                              'response': serializer.data})
#
#         except Exception as e:
#             return Response({'message': "Credit detail doesn't exist", 'status': status.HTTP_400_BAD_REQUEST})
#
#
# class CreditHistoryCreateView(APIView):
#
#     def post(self, request):
#         serializer = CreditHistorySerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'message': 'credit history added',
#                              'status': status.HTTP_200_OK,
#                              'response': serializer.data})
#         return Response({'message': serializer.errors, 'status': status.HTTP_400_BAD_REQUEST})
#
#
# class CreditHistoryUpdateView(APIView):
#
#     def patch(self, request, pk, *args, **kwargs):
#         obj = CreditHistory.objects.get(pk=pk)
#         serializer = CreditHistorySerializer(obj, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'message': 'Credit detail updated successfully',
#                              'status': status.HTTP_200_OK,
#                             'response': serializer.data})
#         return Response({'message': serializer.errors, 'status': status.HTTP_400_BAD_REQUEST})


class CreditHistoryDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            company, branch = token_helper(request)
            obj = CreditHistory.objects.get(pk=pk)
            if obj.customer.company == company:
                obj.delete()
                return Response({'message': 'Credit detail successfully deleted',
                                'status': status.HTTP_200_OK})
            else:
                return Response({
                    'message': 'Unathorized',
                    'status': status.HTTP_401_UNAUTHORIZED
                })

        except Exception as e:
            return Response({'message': "Credit detail doesn't exist", 'status': status.HTTP_400_BAD_REQUEST})


"""" Floor Detail """


class FloorListView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        company, branch = token_helper(request)
        if branch is not None:
            obj = Floor.objects.filter(branch=branch)
        else:
            obj = Floor.objects.filter(branch__company=company)
        serializer = FloorSerializer(obj, many=True)
        return Response({'message': 'Floor list', 'status': status.HTTP_200_OK, 'response': serializer.data})


class FloorCreateView(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        company, branch = token_helper(request)
        request.data['branch'] = branch.id
        serializer = FloorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Floor added',
                     'status': status.HTTP_200_OK,
                     'response': serializer.data})
        return Response({'message': serializer.errors, 'status': status.HTTP_400_BAD_REQUEST})


class FloorUpdateView(APIView):
    permission_classes = [IsAuthenticated, ]

    def patch(self, request, pk, *args, **kwargs):
        company, branch = token_helper(request)
        obj = Floor.objects.get(pk=pk)
        if obj.branch.company == company:
            serializer = FloorSerializer(obj, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Floor updated successfully',
                                'status': status.HTTP_200_OK,
                                'response': serializer.data})

            return Response({'message': serializer.errors, 'status': status.HTTP_400_BAD_REQUEST})
        else:
            return Response({
                'message': 'Unauthorized',
                'status': status.HTTP_401_UNAUTHORIZED
            })


class FloorDeleteView(APIView):
    permission_classes = [IsAuthenticated, ]

    def delete(self, request, pk):
        try:
            company, branch = token_helper(request)
            obj = Floor.objects.get(pk=pk)
            if obj.branch.company == company:
                obj.delete()
                return Response({'message': 'Floor successfully deleted',
                                'status': status.HTTP_200_OK})
            else:
                return Response({
                    'message': 'Unauthorized',
                    'status': status.HTTP_401_UNAUTHORIZED
                })
        except Exception as e:
            return Response({'message': "Floor doesn't exist", 'status': status.HTTP_400_BAD_REQUEST})


""" Seating Type """


class SeatingTypeListView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        company, branch = token_helper(request)
        if branch is not None:
            obj = SeatingType.objects.filter(branch=branch)
        else:
            obj = SeatingType.objects.filter(branch__company=company)
        serializer = SeatingTypeSerializer(obj, many=True)
        return Response({'message': 'Seating Types', 'status': status.HTTP_200_OK, 'response': serializer.data})


class SeatingTypeCreateView(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        company, branch = token_helper(request)
        request.data['branch'] = branch.id
        serializer = SeatingTypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Seating type added',
                             'status': status.HTTP_200_OK,
                             'response': serializer.data})
        return Response({'message': serializer.errors, 'status': status.HTTP_400_BAD_REQUEST})


class SeatingTypeUpdateView(APIView):
    permission_classes = [IsAuthenticated, ]

    def patch(self, request, pk, *args, **kwargs):
        company, branch = token_helper(request)
        obj = SeatingType.objects.get(pk=pk)
        if obj.branch.company == company:
            serializer = SeatingTypeSerializer(obj, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Seating type updated successfully',
                               'status': status.HTTP_200_OK,
                                'response': serializer.data})
            return Response({'message': serializer.errors, 'status': status.HTTP_400_BAD_REQUEST})
        else:
            return Response({
                'message': 'Unauthorized',
                'status': status.HTTP_401_UNAUTHORIZED
            })


class SeatingTypeDeleteView(APIView):
    permission_classes = [IsAuthenticated, ]

    def delete(self, request, pk):
        try:
            company, branch = token_helper(request)
            obj = SeatingType.objects.get(pk=pk)
            if obj.branch.company == company:
                obj.delete()
                return Response({'message': 'Seating type successfully deleted',
                                 'status': status.HTTP_200_OK})
            else:
                return Response({
                    'message': 'Seating type successfully deleted',
                    'status': status.HTTP_401_UNAUTHORIZED
                })
        except Exception as e:
            return Response({'message': "Seating type doesn't exist", 'status': status.HTTP_400_BAD_REQUEST})


""" Reward """

""" v2 """


class RewardListView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        company, branch = token_helper(request)
        try:
            obj = company.reward
            serializer = RewardSerializer(obj)
            return Response({'message': 'Reward', 'status': status.HTTP_200_OK, 'response': serializer.data})
        except:
            return Response({
                'message': 'No reward defined yet',
                'status': status.HTTP_400_BAD_REQUEST
            })


class RewardDetailView(APIView):

    def get(self, request, pk):
        try:
            obj = Reward.objects.get(pk=pk)
            serializer = RewardSerializer(obj)
            return Response({'message': 'Reward detail',
                             'status': status.HTTP_200_OK,
                             'response': serializer.data})

        except Exception as e:
            return Response({'message': "Reward doesn't exist", 'status': status.HTTP_400_BAD_REQUEST})


class RewardCreateView(APIView):

    def post(self, request):
        serializer = RewardSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Reward successfully created',
                             'status': status.HTTP_200_OK,
                             'response': serializer.data})
        return Response({'message': serializer.errors, 'status': status.HTTP_400_BAD_REQUEST})


class RewardUpdateView(APIView):

    def patch(self, request, pk, *args, **kwargs):
        obj = Reward.objects.get(pk=pk)
        serializer = RewardSerializer(obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Reward updated successfully',
                             'status': status.HTTP_200_OK,
                            'response': serializer.data})
        return Response({'message': serializer.errors, 'status': status.HTTP_400_BAD_REQUEST})


class RewardDeleteView(APIView):

    def delete(self, request, pk):
        try:
            obj = Reward.objects.get(pk=pk)
            obj.delete()
            return Response({'message': 'Reward successfully deleted',
                             'status': status.HTTP_200_OK})
        except Exception as e:
            return Response({'message': "Reward doesn't exist", 'status': status.HTTP_400_BAD_REQUEST})


""" Branch """


class BranchListView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        try:
            company, branch = token_helper(request)
            obj = company.branch.all()
            serializer = BranchSerializer(obj, many=True)
            return Response({'message': 'Branch list',
                             'status': status.HTTP_200_OK,
                             'response': serializer.data})
        except:
            return Response({'mesasge': 'company doesnot exist', 'status': status.HTTP_400_BAD_REQUEST})


class BranchDetailView(APIView):
    """ Unused """
    permission_classes = [IsAuthenticated, ]

    def get(self, request, pk):
        try:
            obj = Branch.objects.get(pk=pk)
            serializer = BranchDetailView(obj)
            return Response({'message': 'Branch detail',
                             'status': status.HTTP_200_OK,
                             'response': serializer.data})

        except Exception as e:
            return Response({'message': "Branch doesn't exist", 'status': status.HTTP_400_BAD_REQUEST})


class BranchCreateView(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        company, branch = token_helper(request)
        request.data['company'] = company.id
        serializer = BranchSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Branch added successfully',
                             'status': status.HTTP_200_OK,
                             'response': serializer.data})
        return Response({'message': serializer.errors, 'status': status.HTTP_400_BAD_REQUEST})


class BranchUpdateView(APIView):
    permission_classes = [IsAuthenticated, ]

    def patch(self, request, pk, *args, **kwargs):
        company, branch = token_helper(request)
        obj = Branch.objects.get(pk=pk)
        if obj.company == company:
            serializer = BranchSerializer(obj, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Branch updated successfully',
                                 'status': status.HTTP_200_OK,
                                'response': serializer.data})
            return Response({'message': serializer.errors, 'status': status.HTTP_400_BAD_REQUEST})
        else:
            return Response({
                'message': 'Unauthorized',
                'status': status.HTTP_401_UNAUTHORIZED
            })


class BranchDeleteView(APIView):
    permission_classes = [IsAuthenticated, ]

    def delete(self, request, pk):
        try:
            company, branch = token_helper(request)
            obj = Branch.objects.get(pk=pk)
            if obj.company == company:
                obj.delete()
                return Response({'message': 'Branch successfully deleted',
                                 'status': status.HTTP_200_OK})
            else:
                return Response({
                    'message': 'Unauthorized',
                    'status': status.HTTP_401_UNAUTHORIZED
                })
        except Exception as e:
            return Response({'message': "Branch doesn't exist", 'status': status.HTTP_400_BAD_REQUEST})
