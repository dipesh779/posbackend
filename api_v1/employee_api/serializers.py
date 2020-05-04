from rest_framework import serializers
from django.contrib.auth.models import Group, Permission

from employee.models import Employee


class PermissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Permission
        fields = '__all__'


class GroupListSerializer(serializers.ModelSerializer):
    permissions = PermissionSerializer(many=True)

    class Meta:
        model = Group
        fields = '__all__'


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = "__all__"


class EmployeeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = [
            'id', 'employee_id', 'employee_name', 'employee_position', 'address', 'dob', 'phone', 'email',
            'is_staff', 'is_active', 'branchh', 'company', 'employee_type',
            'is_superuser'
        ]


class EmployeeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Employee
        fields = [
            'id', 'employee_id', 'employee_name', 'employee_position', 'address', 'dob', 'phone', 'email',
            'is_staff', 'is_active', 'password', 'branchh', 'groups', 'user_permissions', 'company', 'employee_type'
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }
        read_only_fields = ('id', )

    def create(self, validated_data):
        employee = Employee.objects.create(
            employee_id=validated_data.get('employee_id'),
            employee_name=validated_data.get('employee_name'),
            employee_position=validated_data.get('employee_position'),
            address=validated_data.get('address'),
            dob=validated_data.get('dob'),
            phone=validated_data.get('phone'),
            email=validated_data.get('email'),
            is_active=validated_data.get('is_active', True),
            is_staff=validated_data.get('is_staff', False),
            branchh=validated_data.get('branchh', None),
            company=validated_data.get('company')

        )
        groups = validated_data.get('groups')
        user_permissions = validated_data.get('user_permissions')
        try:
            for group in groups:
                employee.groups.add(group)
        except:
            pass

        try:
            for permission in user_permissions:
                employee.user_permissions.add(permission)

        except:
            pass

        employee.set_password(validated_data['password'])
        employee.save()
        return employee

    def update(self, instance, validated_data):
        instance.employee_name=validated_data.get('employee_name',instance.employee_name)
        instance.employee_position=validated_data.get('employee_position',instance.employee_position)
        instance.address=validated_data.get('address',instance.address)
        instance.dob=validated_data.get('dob',instance.dob)
        instance.phone=validated_data.get('phone',instance.phone)
        instance.email=validated_data.get('email',instance.email)
        instance.is_active=validated_data.get('is_active', True)
        instance.is_staff=validated_data.get('is_staff', False)
        instance.branchh=validated_data.get('branch', None)
        instance.company=validated_data.get('company',instance.company)        
        
        if validated_data.get('groups'):
            instance.groups = validated_data.get('groups',instance.groups)
            instance.user_permissions = validated_data.get('user_permissions',instance.user_permissions)
            try:
                for group in groups:
                    instance.groups.add(group)
            except:
                pass            
            
            try:
                for permission in user_permissions:
                    instance.user_permissions.add(permission)            
            except:
                pass

        if validated_data['password']:
            instance.set_password(validated_data['password'])        
            instance.save()
        return instance


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, attrs):
        return attrs
