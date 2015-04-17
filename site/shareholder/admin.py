from django.contrib import admin

from shareholder.models import *

class ShareholderAdmin(admin.ModelAdmin):
    pass
class CompanyAdmin(admin.ModelAdmin):
    pass
class OperatorAdmin(admin.ModelAdmin):
    list_display = ('user', 'company')
    pass

admin.site.register(Shareholder, ShareholderAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(Operator, OperatorAdmin)
