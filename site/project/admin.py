#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.db import models
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage

from markdownx.widgets import AdminMarkdownxWidget
from reversion.helpers import patch_admin

# ReVersioned UserAdmin
patch_admin(User)


UserAdmin.list_display = (
    'email',
    'first_name',
    'last_name',
    'is_active',
    'last_login',
    'date_joined',
    'is_staff')
UserAdmin.list_filter = (
    'is_staff', 'date_joined', 'operator__company', 'shareholder__company',
    'last_login',
    )


class FlatPageAdminX(FlatPageAdmin):
    formfield_overrides = {
        models.TextField: {'widget': AdminMarkdownxWidget},
    }


admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageAdminX)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
