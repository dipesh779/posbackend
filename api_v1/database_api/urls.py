from django.urls import path

from .views import (
    ComanyListView, CompanyDetailView, CompanyCreateView, CompanyUpdateView, CompanyDeleteView,
    CustomerListView, CustomerDetailView, CustomerCreateView, CustomerUpdateView, CustomerDeleteView,
    CreditListByCustomerIdView,  CreditCreateView,  CreditDeleteView,
    CreditHistoryListView,
    CreditHistoryDeleteView,
    FloorCreateView, FloorUpdateView, FloorDeleteView, FloorListView,
    SeatingTypeListView, SeatingTypeCreateView, SeatingTypeUpdateView, SeatingTypeDeleteView,
    RewardListView, RewardDetailView, RewardCreateView, RewardUpdateView, RewardDeleteView,
    BranchListView, BranchDetailView, BranchCreateView, BranchUpdateView, BranchDeleteView,
)
urlpatterns =[
    path('company/list', ComanyListView.as_view()),
    path('company/<int:pk>/detail', CompanyDetailView.as_view()),
    path('company/create', CompanyCreateView.as_view()),
    path('company/<int:pk>/update', CompanyUpdateView.as_view()),
    path('company/<int:pk>/delete', CompanyDeleteView.as_view()),

    path('customer/list', CustomerListView.as_view()),
    path('customer/<int:pk>/detail', CustomerDetailView.as_view()),
    path('customer/create', CustomerCreateView.as_view()),
    path('customer/<int:pk>/update', CustomerUpdateView.as_view()),
    path('customer/<int:pk>/delete', CustomerDeleteView.as_view()),

    path('customer/<int:pk>/credit_history/list', CreditListByCustomerIdView.as_view()),
    path('credit_history/create', CreditCreateView.as_view()),
    path('credit_history/<int:pk>/delete', CreditDeleteView.as_view()),

    path('credit/list', CreditHistoryListView.as_view()),
    path('credit/<int:pk>/delete', CreditHistoryDeleteView.as_view()),

    path('floor/list', FloorListView.as_view()),
    path('floor/create', FloorCreateView.as_view()),
    path('floor/<int:pk>/update', FloorUpdateView.as_view()),
    path('floor/<int:pk>/delete', FloorDeleteView.as_view()),

    path('seating_type/list', SeatingTypeListView.as_view()),
    path('seating_type/create', SeatingTypeCreateView.as_view()),
    path('seating_type/<int:pk>/update', SeatingTypeUpdateView.as_view()),
    path('seating_type/<int:pk>/delete', SeatingTypeDeleteView.as_view()),

    path('reward/list', RewardListView.as_view()),
    path('reward/<int:pk>/detail', RewardDetailView.as_view()),
    path('reward/create', RewardCreateView.as_view()),
    path('reward/<int:pk>/update', RewardUpdateView.as_view()),
    path('reward/<int:pk>/delete', RewardDeleteView.as_view()),

    path('branch/list', BranchListView.as_view()),
    path('branch/<int:pk>/detail', BranchDetailView.as_view()),
    path('branch/create', BranchCreateView.as_view()),
    path('branch/<int:pk>/update', BranchUpdateView.as_view()),
    path('branch/<int:pk>/delete', BranchDeleteView.as_view()),

    # path('vendor/<int:pk>/contact_person/list', ContactPersonByVendor.as_view()),
    # path('contact_person/<int:pk>/detail', ContactPersonDetailView.as_view()),
    # path('contact_person/create', ContactPersonCreate.as_view()),
    # path('contact_person/<int:pk>/update', ContactPersonUpdate.as_view()),
    # path('contact_person/<int:pk>/delete', ContactPersonDelete.as_view()),
]