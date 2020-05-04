from django.contrib import admin

from .models import Employee

# Register your models here.
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['employee_name', 'email']
    readonly_fields = ['password']


admin.site.register(Employee, EmployeeAdmin)