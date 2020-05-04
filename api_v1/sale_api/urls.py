from django.urls import path

from .views import (
    DepartmentListView, DepartmentDetailView, DepartmentCreateView, DepartmentUpdateView, DepartmentDeleteView,
    CategoryListView, CategoryDetailView, CategoryCreateView, CategoryUpdateView, CategoryDeleteView,
    UnitOfMaterialListView, UnitOfMaterialDetailView, UnitOfMaterialCreateView, UnitOfMaterialUpdateView,
    UnitOfMaterialDeleteView,
    MenuItemListView, MenuItemDetailView, MenuItemCreateView, MenuItemUpdateView, MenuItemDeleteView,
    ItemlineByorderView, ItemlineCreateView, ItemlineUpdateView, ItemlineDeleteView,
    ReservationListView, ReservationCreateView, ReservationUpdateView, ReservationDeleteView,
    SeatingListView, SeatingDetailView, SeatingCreateView, SeatingUpdateView, SeatingDeleteView,
    SeatingListByMergeReference, MergeSeatingView, ChangeSeatingView, ClearMergedSeatingView, ClearSeatingByInvoiceIdView,
    DeliveryListView, DeliveryDetailView, DeliveryCreateView, DeliveryUpdateView, DeliveryDeleteView,
    OrderListView, OrderDetailUpdateDelete, OrderListBySeatingIdView,OrderListByMergeReferenceIdView, OrderCreateView,
    NotificationListView

)
urlpatterns = [

    path('department/list', DepartmentListView.as_view()),
    path('department/<int:pk>/details', DepartmentDetailView.as_view()),
    path('department/create', DepartmentCreateView.as_view()),
    path('department/<int:pk>/update', DepartmentUpdateView.as_view()),
    path('department/<int:pk>/delete', DepartmentDeleteView.as_view()),

    path('category/list', CategoryListView.as_view()),
    path('category/<int:pk>/details', CategoryDetailView.as_view()),
    path('category/create', CategoryCreateView.as_view()),
    path('category/<int:pk>/update', CategoryUpdateView.as_view()),
    path('category/<int:pk>/delete', CategoryDeleteView.as_view()),

    path('uom/list', UnitOfMaterialListView.as_view()),
    path('uom/<int:pk>/details', UnitOfMaterialDetailView.as_view()),
    path('uom/create', UnitOfMaterialCreateView.as_view()),
    path('uom/<int:pk>/update', UnitOfMaterialUpdateView.as_view()),
    path('uom/<int:pk>/delete', UnitOfMaterialDeleteView.as_view()),

    path('item/list', MenuItemListView.as_view()),
    path('item/<int:pk>/details', MenuItemDetailView.as_view()),
    path('item/create', MenuItemCreateView.as_view()),
    path('item/<int:pk>/update', MenuItemUpdateView.as_view()),
    path('item/<int:pk>/delete', MenuItemDeleteView.as_view()),

    path('order/<int:pk>/itemline', ItemlineByorderView.as_view()),
    path('itemline/create', ItemlineCreateView.as_view()),
    path('itemline/<int:pk>/update', ItemlineUpdateView.as_view()),
    path('itemline/<int:pk>/delete', ItemlineDeleteView.as_view()),

    path('reservation/list', ReservationListView.as_view()),
    path('reservation/create', ReservationCreateView.as_view()),
    path('reservation/<int:pk>/update', ReservationUpdateView.as_view()),
    path('reservation/<int:pk>/delete', ReservationDeleteView.as_view()),

    path('seating/list', SeatingListView.as_view()),
    path('seating/<int:pk>/details', SeatingDetailView.as_view()),
    path('seating/create', SeatingCreateView.as_view()),
    path('seating/<int:pk>/update', SeatingUpdateView.as_view()),
    path('seating/<int:pk>/delete', SeatingDeleteView.as_view()),
    path('merge_reference/<int:id>/seating/list', SeatingListByMergeReference.as_view()),
    path('seating/merge', MergeSeatingView.as_view()),
    path('merge_reference/seating/remove', ClearMergedSeatingView.as_view()),
    path('seating/change', ChangeSeatingView.as_view()),
    path('invoice/<int:pk>/seating/clear', ClearSeatingByInvoiceIdView.as_view()),

    path('delivery/list', DeliveryListView.as_view()),
    path('delivery/<int:pk>/details', DeliveryDetailView.as_view()),
    path('delivery/create', DeliveryCreateView.as_view()),
    path('delivery/<int:pk>/update', DeliveryUpdateView.as_view()),
    path('delivery/<int:pk>/delete', DeliveryDeleteView.as_view()),

    path('order', OrderListView.as_view()),
    path('order/<int:pk>', OrderDetailUpdateDelete.as_view()),
    path('order/create', OrderCreateView.as_view()),
    path('seating/<int:pk>/order/list', OrderListBySeatingIdView.as_view()),
    path('merge_reference/<int:pk>/order/list', OrderListByMergeReferenceIdView.as_view()),
    path('notification/list', NotificationListView.as_view()),

]