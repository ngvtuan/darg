from django.contrib import admin

from shareholder.models import Shareholder, Company, Operator, Position, \
    UserProfile, Country, OptionPlan, OptionTransaction, Security


class ShareholderAdmin(admin.ModelAdmin):
    pass


class CompanyAdmin(admin.ModelAdmin):
    pass


class OperatorAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'company', 'user', 'date_joined')
    list_filter = ('company',)

    def date_joined(selfi, obj):
        return obj.user.date_joined


class PositionAdmin(admin.ModelAdmin):
    list_display = ('bought_at', 'buyer', 'seller', 'count', 'value')
    pass


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
