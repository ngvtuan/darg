from django.contrib import admin

from shareholder.models import Shareholder, Company, Operator, Position, \
    UserProfile, Country, OptionPlan, OptionTransaction, Security


class ShareholderAdmin(admin.ModelAdmin):
    search_fields = ['user__email', 'user__first_name', 'user__last_name']

class CompanyAdmin(admin.ModelAdmin):
    pass


class OperatorAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'company', 'user', 'date_joined')
    list_filter = ('company',)

    def date_joined(selfi, obj):
        return obj.user.date_joined


class PositionAdmin(admin.ModelAdmin):
    list_display = (
        'bought_at', 'get_buyer', 'get_seller', 'count', 'value', 'get_company'
        )
    list_filter = ('buyer__company', 'seller__company')
    search_fields = [
        'buyer__user__email', 'seller__user__email',
        'buyer__company__name', 'seller__company__name'
    ]

    def get_seller(self, obj):
        if obj.seller:
            return obj.seller.user.email
        return None

    def get_buyer(self, obj):
        if obj.buyer:
            return obj.buyer.user.email
        return None

    def get_company(self, obj):
        if obj.buyer:
            return obj.buyer.company
        elif obj.seller:
            return obj.seller.company
        return None


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('pk',)
    pass


class CountryAdmin(admin.ModelAdmin):
    list_display = ('iso_code',)
    pass


class SecurityAdmin(admin.ModelAdmin):
    list_display = ('title',)
    pass


class OptionTransactionAdmin(admin.ModelAdmin):
    list_display = ('bought_at', 'buyer', 'seller',)
    pass


class OptionPlanAdmin(admin.ModelAdmin):
    list_display = ('title',)
    pass

admin.site.register(Shareholder, ShareholderAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(Operator, OperatorAdmin)
admin.site.register(Position, PositionAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(Security, SecurityAdmin)
admin.site.register(OptionPlan, OptionPlanAdmin)
admin.site.register(OptionTransaction, OptionTransactionAdmin)
