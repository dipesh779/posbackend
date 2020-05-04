from django.contrib import admin
from .models import *


class ItemlineInline(admin.TabularInline):
    model = Itemline


class OrderAdmin(admin.ModelAdmin):
    inlines = [
        ItemlineInline
    ]


admin.site.register(Order, OrderAdmin)


admin.site.register([
    Department, Category, MenuItem, Itemline, Reservation, Invoice, Seating, Delivery,
    ModifierItem, UnitOfMaterial, NotificationTable
])


