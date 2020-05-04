from django.contrib.auth import authenticate
from django.contrib.auth.models import Group, Permission
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from utils.create_response import create_response
from .serializers import (
    EmployeeSerializer, EmployeeListSerializer, LoginSerializer,
    GroupListSerializer, GroupSerializer, PermissionSerializer
)
from database.models import CompanyDetail, Branch
from employee.models import Employee
from employee.utils.token_helper import token_helper, token_helper_employee


class Login(APIView):
    permission_classes = [AllowAny, ]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            employee = authenticate(**serializer.validated_data)
            if employee is not None:
                refresh = RefreshToken.for_user(employee)
                context = dict()
                user_permissions = employee.user_permissions.all()
                permissions = []
                groups = employee.groups.all()
                for permission in user_permissions:
                    permissions.append(permission.codename)

                context['employee'] = {
                    "id": employee.id,
                    "email": employee.email,
                    "employee_name": employee.employee_name,
                    "employee_type": employee.employee_type,
                    "employee_position": employee.employee_position,
                    "user_permissions": permissions
                }
                if employee.company is not None:
                    context['employee']['company'] = employee.company.company_name
                context['access_token'] = str(refresh.access_token)
                context['is_superuser'] = employee.is_superuser
                return Response(create_response(True, data=context), status=status.HTTP_200_OK)
            else:
                return Response(create_response(False, err_name="Incorrect credentials",
                                                err_message=f'Authenticate returned' f'None'),
                                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(create_response(False, err_name="Provided data didn't validate ",
                                            err_message=f'{serializer.errors}'),
                                            status=status.HTTP_400_BAD_REQUEST)


""" Employee """


class EmployeeListView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        try:
            # company, branch = token_helper(request)
            # if branch is not None:
            #     obj = branch.employee.all()
            # else:
            #     obj = company.employee.all()
            obj=Employee.objects.all()
            serializer = EmployeeListSerializer(obj, many=True)
            return Response({'message': 'Employee List by company', 'status': status.HTTP_200_OK,
                                 'response': serializer.data})

        except CompanyDetail.DoesNotExist:
            return Response({
                'message': 'company doesnot exist',
                'status': status.HTTP_400_BAD_REQUEST
            })


class EmployeeListByBranchIdView(APIView):
    """ unused """
    permission_classes = [IsAuthenticated, ]

    def get(self, request, pk):
        try:
            company, branch = token_helper(request)
            branch = Branch.objects.get(pk=pk)
            if branch.company == company:
                obj = branch.employee.all()
                serializer = EmployeeSerializer(obj, many=True)
                return Response({'message': 'Employee List by branch', 'status': status.HTTP_200_OK,
                                 'response': serializer.data})
            else:
                return Response({
                    'message': 'Unauthorized',
                    'status': status.HTTP_401_UNAUTHORIZED
                })

        except CompanyDetail.DoesNotExist:
            return Response({
                'message': 'branch doesnot exist',
                'status': status.HTTP_400_BAD_REQUEST
            })


class EmployeeDetailView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request, pk):
        try:
            company, branch = token_helper(request)
            obj = Employee.objects.get(pk=pk)
            if obj.company == company:
                serializer = EmployeeSerializer(obj)
                return Response({'message': 'Department {} detail'.format(obj.employee_name),
                                 'status': status.HTTP_200_OK,
                                 'response': serializer.data})
            else:
                return Response({
                    'message': 'Unauthorized',
                    'status': status.HTTP_401_UNAUTHORIZED
                })

        except Exception as e:
            return Response({'message': "Employee doesn't exist", 'status': status.HTTP_400_BAD_REQUEST})


class EmployeeCreateView(APIView):

    permission_classes = [IsAdminUser, ]

    def post(self, request):
            serializer = EmployeeSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Employee  added successfully',
                                 'status': status.HTTP_200_OK,
                                 'response': serializer.data})
            return Response({'message': serializer.errors, 'status': status.HTTP_400_BAD_REQUEST })



class EmployeeUpdateView(APIView):

    permission_classes = [IsAdminUser, ]

    def patch(self, request, pk, *args, **kwargs):
        obj = Employee.objects.get(pk=pk)
        serializer = EmployeeSerializer(obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Employee {} updated succesfully'.format(obj.employee_name),
                             'status': status.HTTP_200_OK,
                            'response': serializer.data})
        return Response({'message': serializer.errors, 'status': status.HTTP_400_BAD_REQUEST})


class EmployeeDeleteView(APIView):

    permission_classes = [IsAdminUser, ]

    def delete(self, request, pk):
        try:
            obj = Employee.objects.get(pk=pk)
            obj.delete()
            return Response({'mesaage': 'Employee removed successfully',
                             'status': status.HTTP_200_OK})
        except Exception as e:
            return Response({'message': "Employee doesn't exist", 'status': status.HTTP_400_BAD_REQUEST})


""" Groups """


# class GroupListView(APIView):
#     permission_classes = [IsAuthenticated, ]

#     def get(self, request):
#         try:
#             company, branch = token_helper(request)
#             obj = company.group_set.all()
#             serializer = GroupListSerializer(obj, many=True)
#             return Response({'message': 'Group list', 'status': status.HTTP_200_OK,
#                              'response': serializer.data})

#         except CompanyDetail.DoesNotExist:
#             return Response({
#                 'message': 'company doesnot exist',
#                 'status': status.HTTP_400_BAD_REQUEST
#             })


# class GroupCreateView(APIView):

#     permission_classes = [IsAuthenticated, ]

#     def post(self, request):
#         company, branch = token_helper(request)
#         request.data['company'] = company.id
#         serializer = GroupSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'message': 'Group  added successfully',
#                              'status': status.HTTP_200_OK,
#                              'response': serializer.data})
#         return Response({'message': serializer.errors, 'status': status.HTTP_400_BAD_REQUEST })


# class GroupUpdateView(APIView):

#     permission_classes = [IsAuthenticated, ]

#     def patch(self, request, pk, *args, **kwargs):
#         company, branch = token_helper(request)
#         obj = Group.objects.get(pk=pk)
#         if obj.company == company:
#             serializer = GroupSerializer(obj, data=request.data, partial=True)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response({'message': 'Group updated succesfully',
#                                  'status': status.HTTP_200_OK,
#                                 'response': serializer.data})
#             return Response({'message': serializer.errors, 'status': status.HTTP_400_BAD_REQUEST})
#         return Response({
#             'message': 'Unauthorized',
#             'status': status.HTTP_401_UNAUTHORIZED
#         })


# class GroupDeleteView(APIView):

#     permission_classes = [IsAuthenticated, ]

#     def delete(self, request, pk):
#         try:
#             company, branch = token_helper(request)
#             obj = Group.objects.get(pk=pk)
#             if obj.company == company:
#                 obj.delete()
#                 return Response({'mesaage': 'Group removed successfully',
#                                  'status': status.HTTP_200_OK})
#             else:
#                 return Response({
#                     'message': 'Unauthorized',
#                     'status': status.HTTP_401_UNAUTHORIZED
#                 })
#         except Exception as e:
#             return Response({'message': "Employee doesn't exist", 'status': status.HTTP_400_BAD_REQUEST})


""" Permissions """


class PermissionListView(APIView):
    permission_classes = [AllowAny, ]

    def get(self, request):
        obj = Permission.objects.all().exclude(content_type__in=[1, 2, 3, 4, 5])
        serializer = PermissionSerializer(obj, many=True)
        return Response({'message': 'Permission List', 'status': status.HTTP_200_OK,
                         'response': serializer.data})



