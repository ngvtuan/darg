from django.conf.urls import include, url
from django.contrib import admin
from django.views.i18n import javascript_catalog

from rest_framework import routers

from services.rest.views import ShareholderViewSet, CompanyViewSet, UserViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'shareholders', ShareholderViewSet, base_name="shareholders")
router.register(r'company', CompanyViewSet)
router.register(r'user', UserViewSet, base_name="user")

js_info_dict = {
    'packages': ('project', 'shareholder', 'utils', 'services',),
}

urlpatterns = [
    # Examples:
    url(r'^$', 'project.views.index', name='index'),
    url(r'^start/$', 'project.views.start', name='start'),
    url(r'^positions/$', 'shareholder.views.positions', name='positions'),
    url(r'^log/$', 'shareholder.views.log', name='log'),
    url(r'^shareholder/(?P<shareholder_id>[0-9]+)/$', 'shareholder.views.shareholder', name='shareholder'),

    # auth
    url(r'^accounts/', include('registration.backends.simple.urls')),

    # rest api
    url(r'^services/rest/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # i18n
    url(r'^jsi18n/$', javascript_catalog, js_info_dict),

    # django admin
    url(r'^admin/', include(admin.site.urls)),
]
