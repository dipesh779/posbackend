from django.db import transaction
from rest_framework import serializers
from sale.models import (
    Department, Category, UnitOfMaterial, MenuItem, Itemline,
    Reservation, Seating, Delivery, Order, ModifierItem, NotificationTable
)
from database.models import Branch

#
# class BranchSerializerForDepartment(serializers.ModelSerializer):
#     class Meta:
#         model = Branch
#         fields = ['id', 'location']
#
#
# class DepartmentListSerializer(serializers.ModelSerializer):
#     branch = BranchSerializerForDepartment()
#
#     class Meta:
#         model = Department
#         fields = ['id', 'department_name', 'branch']


class DepartmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Department
        fields = ['id', 'department_name', 'branch']


class CategoryListSerialzier(serializers.ModelSerializer):
    department = DepartmentSerializer()

    class Meta:
        model = Category
        fields = ['id', 'category_name', 'department']


class CategorySerialzier(serializers.ModelSerializer):
    department = serializers.StringRelatedField()

    class Meta:
        model = Category
        fields = ['id', 'category_name', 'department']


class CategoryCreateUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'category_name', 'department']


class UnitOfMaterialSerailzier(serializers.ModelSerializer):
    class Meta:
        model = UnitOfMaterial
        fields = '__all__'


class MenuItemListserializer(serializers.ModelSerializer):
    category = CategorySerialzier()
    uom = serializers.StringRelatedField()

    class Meta:
        model = MenuItem
        fields = [
            'id', 'item_name', 'price', 'item_type', 'item_image', 'item_description', 'size', 'uom',
            'modifier_item', 'packing_charge', 'category', 'can_be_free', 'reward_point'
            ]


class MenuItemList2serializer(serializers.ModelSerializer):
    uom = serializers.StringRelatedField()

    class Meta:
        model = MenuItem
        fields = [
            'id', 'item_name', 'price', 'item_type', 'item_image', 'item_description', 'size', 'uom',
            'modifier_item', 'packing_charge', 'category', 'can_be_free', 'reward_point'
            ]


class MenuItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = MenuItem
        fields = [
            'id', 'item_name', 'price', 'item_type', 'item_image', 'item_description', 'size', 'uom',
            'modifier_item', 'packing_charge', 'category', 'can_be_free', 'reward_point'
            ]


class ReservationSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ['id', 'customer', 'phone_number', 'sd', 'ed', 'special_mention']


class ItemlineSerializer(serializers.ModelSerializer):

    class Meta:
        model = Itemline
        fields = ['id', 'item', 'quantity', 'price', 'free', 'order']


class ItemlineListSerializer(serializers.ModelSerializer):
    item = MenuItemList2serializer()

    class Meta:
        model = Itemline
        fields = ['id', 'item', 'quantity', 'price', 'free', 'order']


class ItemlineForOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Itemline
        fields = ['id', 'item', 'quantity', 'price', 'free', 'order']


class ModifierSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModifierItem
        fields = ['id', 'modifier_name', 'price', 'item_type', 'item_image', 'item_description', 'uom']


class SeatingSerializer(serializers.ModelSerializer):
    order = serializers.PrimaryKeyRelatedField(many=True, required=False, read_only=True)

    class Meta:
        model = Seating
        fields = ['id', 'floor', 'seating_type', 'seating_number', 'seating_name', 'capacity', 'seating_status',
                 'branch', 'waiter', 'order', 'reservation', 'merge_reference', 'customer']



class OrderSerializer(serializers.ModelSerializer):
    itemline = ItemlineForOrderSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'itemline', 'date_of_order', 'take_away_charge', 'order_type', 'order_status', 'delivery',
                  'seating', 'customer', 'branch', 'instruction', 'waiter']

    def create(self, validated_data):
        order = Order.objects.create(
            order_type=validated_data.get('order_type'),
            order_status=validated_data.get('order_status', 'ordered'),
            delivery=validated_data.get('delivery'),
            seating=validated_data.get('seating'),
            branch=validated_data.get('branch'),
            instruction=validated_data.get('instruction'),
            waiter=validated_data.get('waiter')
        )
        itemlines = validated_data.get('itemline')
        for itemline in itemlines:
            item = itemline.get('item')
            quantity = itemline.get('quantity')
            free = itemline.get('free')
            item_line = Itemline.objects.create(
                item=item,
                quantity=quantity,
                free=free,
                order=order,
            )
            # item_line.save()
            order.itemline.add(item_line)
        # order.save()
        return order


class SeatingForOrderSerializer(serializers.ModelSerializer):
    customer = serializers.StringRelatedField()
    floor = serializers.StringRelatedField()

    class Meta:
        model = Seating
        fields = ['id', 'floor', 'seating_type', 'seating_number', 'seating_name', 'capacity', 'seating_status',
                  'waiter', 'order', 'reservation', 'merge_reference', 'customer']


class OrderListSerializer(serializers.ModelSerializer):
    seating = SeatingForOrderSerializer()
    itemline = ItemlineListSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'itemline', 'date_of_order', 'take_away_charge', 'order_type', 'order_status', 'delivery',
                  'seating', 'customer', 'branch', 'instruction', 'waiter']


class SeatingListSerializer(serializers.ModelSerializer):
    order = OrderListSerializer(many=True)

    class Meta:
        model = Seating
        fields = ['id', 'floor', 'seating_type', 'seating_number', 'seating_name', 'capacity', 'seating_status',
                  'waiter', 'order', 'reservation', 'merge_reference', 'customer', 'branch']


class DeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = ['id', 'delivery_person', 'delivery_charge', 'customer', 'delivery_status', 'order']


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationTable
        fields = '__all__'
















