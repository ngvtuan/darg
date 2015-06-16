from django.contrib import admin

from shareholder.models import *

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

admin.site.register(Shareholder, ShareholderAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(Operator, OperatorAdmin)
admin.site.register(Position, PositionAdmin)
