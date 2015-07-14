from django.contrib import admin

from shareholder.models import Shareholder, Company, Operator, Position, UserProfile, Country


class ShareholderAdmin(admin.ModelAdmin):
    pass


class CompanyAdmin(admin.ModelAdmin):
    pass


class OperatorAdmin(admin.ModelAdmin):
    list_display = ('user', 'company')
    pass


class PositionAdmin(admin.ModelAdmin):
    list_display = ('bought_at', 'buyer', 'seller', 'count', 'value')
    pass


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)
    pass


class CountryAdmin(admin.ModelAdmin):
    list_display = ('iso_code',)
    pass

admin.site.register(Shareholder, ShareholderAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(Operator, OperatorAdmin)
admin.site.register(Position, PositionAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Country, CountryAdmin)
