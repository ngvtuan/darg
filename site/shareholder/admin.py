from django.contrib import admin

from shareholder.models import *

class ShareholderAdmin(admin.ModelAdmin):
    pass
class CompanyAdmin(admin.ModelAdmin):
    pass

admin.site.register(Shareholder, ShareholderAdmin)
admin.site.register(Company, CompanyAdmin)
