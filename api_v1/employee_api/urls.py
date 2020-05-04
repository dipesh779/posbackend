from django.urls import path

from .views import (Login, EmployeeListView, EmployeeListByBranchIdView, EmployeeDetailView,
                    EmployeeCreateView, EmployeeUpdateView, EmployeeDeleteView,
                    # GroupListView, GroupCreateView, GroupUpdateView, GroupDeleteView,
                    PermissionListView

)

urlpatterns = [
    path('employee/list', EmployeeListView.as_view()),
    # path('branch/<int:pk>/employee/list', EmployeeListByBranchIdView.as_view()),
    path('employee/login', Login.as_view()),
    path('employee/<int:pk>/details', EmployeeDetailView.as_view()),
    path('employee/create', EmployeeCreateView.as_view()),
    path('employee/<int:pk>/update', EmployeeUpdateView.as_view()),
    path('employee/<int:pk>/delete', EmployeeDeleteView.as_view()),

    # path('group/list', GroupListView.as_view()),
    # path('group/create', GroupCreateView.as_view()),
    # path('group/<int:pk>/update', GroupUpdateView.as_view()),
    # path('group/<int:pk>/delete', GroupDeleteView.as_view()),
    # path('permission/list', PermissionListView.as_view())
]