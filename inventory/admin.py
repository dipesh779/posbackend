from django.contrib import admin
from .models import PurchaseOrder, PurchaseItem, BillOfStock, BillOfStockItem, StockComputation, \
    MenuItemCosting, ItemsForMenuItem, Stock, Item, Vendor, ContactPerson

admin.site.register([BillOfStockItem])


class ItemAdmin(admin.ModelAdmin):
    list_display = ('branch','item', 'uom', 'unit_price')

admin.site.register(Item, ItemAdmin)

class StockAdmin(admin.ModelAdmin):
    list_display = ('created_at','branch','item', 'uom', 'unit_price', 'stock_quantity', 'weigh_price', 'threshold_quantity')

admin.site.register(Stock, StockAdmin)

class PurchaseItemAdmin(admin.ModelAdmin):
    model = PurchaseItem
    list_display = ('id', 'purchase_order', 'item', 'unit_price', 'amount')

admin.site.register(PurchaseItem, PurchaseItemAdmin)

class PurchaseItemInline(admin.TabularInline):
    model = PurchaseItem
    extra = 1


class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'vendor')
    inlines = [PurchaseItemInline]


admin.site.register(PurchaseOrder, PurchaseOrderAdmin)


class ItemsDescriptionInline(admin.TabularInline):
    model = BillOfStockItem
    extra = 1


class BillOfStockAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'purchase_order', 'created_at')
    inlines = [ItemsDescriptionInline]


admin.site.register(BillOfStock, BillOfStockAdmin)


class StockInline(admin.ModelAdmin):
    list_display = ('created_at','branch','item','unit_price','opening_stock','received_stock','sale', 'complimentory_sale','expired_quantity','theoritical_QOH',
    'inspected_stock', 'discrepancy_stock','final_closing_stock','weigh_price', 'threshold_quantity')


admin.site.register(StockComputation, StockInline)


class ItemsForMenuItemInline(admin.TabularInline):
    model = ItemsForMenuItem
    extra = 1


class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('branch','menu_category_name', 'selling_price')
    inlines = [ItemsForMenuItemInline]


admin.site.register(MenuItemCosting, MenuItemAdmin)


class ContactPersonInline(admin.TabularInline):
    model = ContactPerson
    extra = 1

class VendorAdmin(admin.ModelAdmin):
    list_display = ['branch', 'vendor_name']
    inlines = [ContactPersonInline]


admin.site.register(Vendor, VendorAdmin)

