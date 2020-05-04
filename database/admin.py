from django.contrib import admin
from database.models import (
    Customer, CreditHistory, Credit, Floor,
    SeatingType,
    CompanyDetail, Branch, Reward,
)


class CreditHistoryHelperInline(admin.TabularInline):
    model = Credit


class CreditHistoryAdmin(admin.ModelAdmin):
    inlines = [
        CreditHistoryHelperInline
    ]


admin.site.register(CreditHistory, CreditHistoryAdmin)


class CreditHistoryInline(admin.TabularInline):
    model = CreditHistory


class CustomerAdmin(admin.ModelAdmin):
    inlines = [
        CreditHistoryInline,
    ]


admin.site.register(Customer, CustomerAdmin)
admin.site.register([Floor, SeatingType, CompanyDetail, Branch, Reward, Credit])
