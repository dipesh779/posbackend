from rest_framework import serializers
from database.models import (
    CompanyDetail, Customer, Credit, CreditHistory, Floor, SeatingType, Reward, Branch
)


class FloorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Floor
        fields = '__all__'


class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = ['id', 'company', 'location', 'branch_contact', 'branch_contact_extra', 'branch_manager']


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyDetail
        fields = "__all__"

    def create(self, validated_data):
        company = CompanyDetail.objects.create(**validated_data)
        company.save()
        branch = Branch.objects.create(
            company=company,
            location="head office",
            branch_contact=company.contact_number
        )
        branch.save()
        return company


class CompanyDetailSerializer(serializers.ModelSerializer):
    branch = BranchSerializer(many=True)

    class Meta:
        model = CompanyDetail
        fields = ['id', 'company_name', 'company_logo', 'address', 'established', 'company_vat_no', 'vat_percentage',
                  'vat_activated', 'service_charge', 'service_charge_activated', 'branch']


class CompanyForBranchSerailizer(serializers.ModelSerializer):

    class Meta:
        model = CompanyDetail
        fields = "__all__"


class BranchListSerializer(serializers.ModelSerializer):
    company = CompanyForBranchSerailizer()
    branch_manager = serializers.StringRelatedField()

    class Meta:
        model = Branch
        fields = ['id', 'company', 'location', 'branch_contact', 'branch_contact_extra', 'branch_manager']


class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = [
            'id', 'customer_id', 'customer_name', 'phone_number', 'home_address', 'work_address',
            'other_address', 'date_of_birth','created', 'modified', 'email', 'pan_number', 'credit_privilege',
            'discount', 'other_address', 'total_reward', 'company'
        ]


class CreditSerializer(serializers.ModelSerializer):

    class Meta:
        model = Credit
        fields = ['id', 'transaction_date', 'customer', 'credit_status', 'remarks', 'transaction_amount', 'credit_history']

    def create(self, validated_data):
        customer = validated_data.get('customer')
        credit_status = validated_data.get('credit_status')
        remarks = validated_data.get('transaction_amount')
        transaction_amount = validated_data.get('transaction_amount')
        credit_history = validated_data.get('credit_history')
        credit = Credit.objects.create(
            customer=customer,
            credit_status=credit_status,
            remarks=remarks,
            transaction_amount=transaction_amount,
            credit_history=credit_history
        )
        credit.save()
        return credit

    def update(self, instance, validated_data):
        instance.customer = validated_data.get('customer', instance.customer)
        instance.credit_status = validated_data.get('credit_status', instance.credit_status)
        instance.remarks = validated_data.get('remarks', instance.remarks)
        instance.transaction_amount = validated_data.get('transaction_amount', instance.transaction_amount)
        instance.credit_history = validated_data.get('credit_history', instance.credit_history)
        instance.save()
        return instance


class CreditHistorySerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()

    class Meta:
        model = CreditHistory
        fields = ['id', 'customer', 'total_debit', 'total_credit', 'credit']


class SeatingTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeatingType
        fields = '__all__'


class RewardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reward
        fields = '__all__'






