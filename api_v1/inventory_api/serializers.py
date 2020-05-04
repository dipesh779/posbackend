from django.db.models.signals import post_save
from rest_framework import serializers
from inventory.models import PurchaseOrder, PurchaseItem, BillOfStock, BillOfStockItem, StockComputation, \
     MenuItemCosting, ItemsForMenuItem, Stock, Item
from datetime import datetime
from inventory.models import Vendor, ContactPerson
from sale.models import MenuItem
from rest_framework.response import Response
from rest_framework import status



"""vendor serializer for listing with id and vendor name"""
class VendorSerializers(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ["id","vendor_name"]



"""purchase item serializer to be added in Purchase Order"""
class PurchaseItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseItem
        fields = ['id', 'item', 'uom', 'unit_price', 'quantity', 'discount', 'amount']




"""serializer for purchase order list only"""
class PurchaseOrderSerializer(serializers.ModelSerializer):
    item = PurchaseItemSerializer(many=True)
    vendor = VendorSerializers()

    class Meta:
        model = PurchaseOrder
        fields = ['id','branch', 'vendor', 'shipping_date', 'payment_method',
                  'shipping_charge', 'additional_discount_percentage',
                  'vat', 'tax', 'final_amount','created_at', 'item']




"""serializer for create and update purchase order"""
class PurchaseOrderCreateSerializer(serializers.ModelSerializer):
    item = PurchaseItemSerializer(many=True)

    class Meta:
        model = PurchaseOrder
        fields = ['id','branch', 'vendor', 'shipping_date', 'payment_method',
                  'shipping_charge', 'additional_discount_percentage',
                  'vat', 'tax', 'final_amount','created_at', 'item']

    def create(self, validated_data):
        item_data = validated_data.pop('item')
        order = PurchaseOrder.objects.create(**validated_data)
        for item in item_data:
            PurchaseItem.objects.create(purchase_order=order, **item)
        return order
    
    def update(self, instance, validated_data):
        item_data = validated_data.pop('item')
        items = (instance.item).all()
        items = list(items)
        instance.branch = validated_data.pop('branch', instance.branch)
        instance.vendor = validated_data.get('vendor', instance.vendor)
        instance.shipping_date = validated_data.get('shipping_date', instance.shipping_date)
        instance.payment_method = validated_data.get('payment_method', instance.payment_method)
        instance.shipping_charge = validated_data.get('shipping_charge', instance.shipping_charge)
        instance.additional_discount_percentage = validated_data.get('additional_discount_percentage',
                                                                        instance.additional_discount_percentage)
        instance.vat = validated_data.get('vat', instance.vat)
        instance.tax = validated_data.get('tax', instance.tax)
        instance.final_amount = validated_data.get('final_amount', instance.final_amount)
        instance.save()

        for item in item_data:
            p_item = items.pop(0)
            p_item.item = item.get('item', p_item.item)
            p_item.uom = item.get('uom', p_item.uom)
            p_item.unit_price = item.get('unit_price', p_item.unit_price)
            p_item.quantity = item.get('quantity', p_item.quantity)
            p_item.discount = item.get('discount', p_item.discount)
            p_item.amount = item.get('amount', p_item.amount)
            p_item.save()
        return instance



""""bill of stock item serializer to be added in bill of stock serializer"""
class BillOfStockItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillOfStockItem
        fields = "__all__"



"""serializer for listing bill of stock lists"""
class BillOfStockSerializer(serializers.ModelSerializer):
    items= BillOfStockItemSerializer(many=True)
    vendor = VendorSerializers()
    class Meta:
        model = BillOfStock
        fields = ['id','branch','created_at', 'invoice_number', 'purchase_order', 'vendor',
                  'shipping_charge', 'additional_discount', 'payment_status',
                  'vat', 'tax', 'final_amount', 'payment_mode','credit_date', 'payment_terms', 'items']


class BillOfStockUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillOfStock
        fields = "__all__"



"""serializer to create and update bill of stock"""
class BillOfStockCreateSerializer(serializers.ModelSerializer):
    items = BillOfStockItemSerializer(many=True)

    class Meta:
        model = BillOfStock
        fields = ['id','branch', 'invoice_number', 'purchase_order', 'vendor',
                  'shipping_charge', 'additional_discount',"payment_status",
                  'vat', 'tax', 'final_amount', 'payment_mode','credit_date', 'payment_terms', 'items']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = BillOfStock.objects.create(**validated_data)
        for item in items_data:
            BillOfStockItem.objects.create(bill_of_stock=order, **item)
        return order

    # def update(self, instance, validated_data):
    #     item_data = validated_data.pop('items', instance.items)
    #     items = (instance.items).all()
    #     items = list(items)
    #     instance.invoice_number = validated_data.get('invoice_number', instance.invoice_number)
    #     instance.purchase_order = validated_data.get('purchase_order', instance.purchase_order)
    #     instance.vendor = validated_data.get('vendor', instance.vendor)
    #     instance.shipping_charge = validated_data.get('shipping_charge', instance.shipping_charge)
    #     instance.additional_discount = validated_data.get('additional_discount', instance.additional_discount)
    #     instance.vat = validated_data.get('vat', instance.vat)
    #     instance.tax = validated_data.get('tax', instance.tax)
    #     instance.final_amount = validated_data.get('final_amount', instance.final_amount)
    #     instance.payment_mode = validated_data.get('payment_mode', instance.payment_mode)
    #     instance.payment_terms = validated_data.get('payment_terms', instance.payment_terms)

    #     if item_data != instance.items:
    #         for item in item_data:
    #             b_item = items.pop(0)
    #             b_item.item = item.get('item', b_item.item)
    #             b_item.uom = item.get('uom', b_item.uom)
    #             b_item.unit_price = item.get('unit_price', b_item.unit_price)
    #             b_item.ordered_quantity = item.get('ordered_quantity', b_item.ordered_quantity)
    #             b_item.received_quantity = item.get('received_quantity', b_item.received_quantity)
    #             b_item.quantity_not_received = item.get('quantity_not_received', b_item.quantity_not_received)
    #             b_item.discount = item.get('discount', b_item.discount)
    #             b_item.amount = item.get('amount', b_item.amount)
    #             b_item.save()
    #     instance.save()
    #     return instance


"""serializer for stock computation all"""
class StockComputationSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockComputation
        fields = "__all__"

    def create(self, validated_data):
        item = validated_data.get('item').lower()
        branch = validated_data.get('branch')
        if StockComputation.objects.filter(item=item,created_at=datetime.today(),branch=branch).count() ==0 :
            lastItem=StockComputation.objects.filter(branch=branch,item=item).last()
            if lastItem:
                opening_stock = lastItem.final_closing_stock
                uom = lastItem.uom
                unit_price = lastItem.unit_price
                weigh_price = unit_price
                threshold_quantity = lastItem.threshold_quantity
            else:
                opening_stock = validated_data.pop('opening_stock')
                uom = validated_data.pop('uom').lower()
                unit_price = validated_data.pop('unit_price')
                weigh_price = unit_price
                threshold_quantity = validated_data.pop('threshold_quantity')
            
            stock = StockComputation.objects.create(
                branch = branch,
                item=item,
                uom=uom,
                unit_price=unit_price,
                opening_stock=opening_stock,
                weigh_price = weigh_price,
                threshold_quantity = threshold_quantity,
            )
            stock.save()
            return stock
        else:
            raise ValueError("item already exists")


class StockComputationSerializerToPopulate(serializers.ModelSerializer):
    class Meta:
        model = StockComputation
        fields = "__all__"

class ItemsListToPopulateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ["item"]


"""serializer for Stock details in company or branch"""
class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = "__all__"


class StockSerializerForMenuItemList(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ['id','item', 'weigh_price']

"""serializer for Items detail in company or branch"""
class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = "__all__"



"""this serializer is to be added with Item for menu item costing serializer"""
class ItemsForMenuItemSerializerList(serializers.ModelSerializer):
    item = StockSerializerForMenuItemList()
    class Meta:
        model = ItemsForMenuItem
        fields = ["id", "item", "quantity_used", "partial_cost"]



"""serializer to add items in menu item costing"""
class ItemsForMenuItemSerializerCreate(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    class Meta:
        model = ItemsForMenuItem
        fields = ["id", "item", "quantity_used", "partial_cost"] 




class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ["item_name"]



class MenuItemCostingListSerializer(serializers.ModelSerializer):
    items = ItemsForMenuItemSerializerList(many=True)
    menu_category_name = MenuSerializer()
    
    class Meta:
        model = MenuItemCosting
        fields = ["id","branch", "menu_category_name", "selling_price", "items"]



class MenuItemCostingSerializersList(serializers.ModelSerializer):
    items = ItemsForMenuItemSerializerList()
    class Meta:
        model = MenuItemCosting
        fields = ["id","branch", "menu_category_name", "selling_price", "items"]


"""add and update menu item costing serializer"""
class MenuItemCostingSerializer(serializers.ModelSerializer):
    items = ItemsForMenuItemSerializerCreate(many=True)

    class Meta:
        model = MenuItemCosting
        fields = ["id","branch", "menu_category_name", "selling_price", "items"]

    def create(self, validated_data):
        item_data = validated_data.pop("items")
        menu = MenuItemCosting.objects.create(**validated_data)
        for item in item_data:
            ItemsForMenuItem.objects.create(menu=menu, **item)
        return menu


    def update(self, instance, validated_data):
        existing_ids = [i.id for i in instance.items.all()]
        items = validated_data.pop('items')
        keep_choices = []
        super(MenuItemCostingSerializer, self).update(instance, validated_data)

        for item in items:
            if item.get('id'):
                instance.items.filter(pk=item.get('id')).update(**item)
                keep_choices.append(item.get('id'))
            else:
                c = instance.items.create(**item)
                keep_choices.append(c.id)

        for req_items in instance.items.all():
            if req_items.id not in keep_choices:
                req_items.delete()

        return instance



class ContactPersonSerializer(serializers.ModelSerializer):
    """conatct person serializer to add in Vendor serializer"""

    class Meta:
        model = ContactPerson
        fields = ['id', 'name', 'designation',
                  'phone_number', 'email', 'vat_or_pan_number']


class VendorSerializer(serializers.ModelSerializer):
    """vendor serializer to create, update, list"""

    contact_persons = ContactPersonSerializer(many=True)

    class Meta:
        model = Vendor
        fields = ['id','branch', 'vendor_name','email', 'address', 'phone_number', 'total_paid_amount',
                  'total_credit_amount', 'total_purchase_amount', 'credit_limit', 'notify_credit_limit',
                  'contact_persons']

    def create(self, validated_data):
        contact_persons_data = validated_data.pop('contact_persons')
        vendor = Vendor.objects.create(**validated_data)
        for contact_person in contact_persons_data:
            ContactPerson.objects.create(vendor=vendor, **contact_person)
        return vendor

    def update(self, instance, validated_data):
        contact_person_data = validated_data.pop('contact_persons')
        contact_person = (instance.contact_persons).all()
        contact_person = list(contact_person)
        instance.branch = validated_data.get(
            'branch', instance.branch)
        instance.vendor_name = validated_data.get(
            'vendor_name', instance.vendor_name)
        instance.address = validated_data.get('address', instance.address)
        instance.phone_number = validated_data.get(
            'phone_number', instance.phone_number)
        instance.email = validated_data.get(
            'email', instance.email)
        instance.total_paid_amount = validated_data.get(
            'total_paid_amount', instance.total_paid_amount)
        instance.total_credit_amount = validated_data.get(
            'total_credit_amount', instance.total_credit_amount)
        instance.total_purchase_amount = validated_data.get(
            'total_purchase_amount', instance.total_purchase_amount)
        instance.credit_limit = validated_data.get(
            'credit_limit', instance.credit_limit)
        instance.notify_credit_limit = validated_data.get(
            'notify_credit_limit', instance.notify_credit_limit)
        instance.save()

        for persons in contact_person_data:
            person = contact_person.pop(0)
            person.name = persons.get('name', person.name)
            person.designation = persons.get('designation', person.designation)
            person.phone_number = persons.get(
                'phone_number', person.phone_number)
            person.email = persons.get('email', person.email)
            person.vat_or_pan_number = persons.get(
                'vat_or_pan_number', person.vat_or_pan_number)
            person.save()
        return instance