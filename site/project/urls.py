from django.conf.urls import include, url, patterns
from django.contrib import admin
from django.views.i18n import javascript_catalog
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

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
]

# admin
admin_url = settings.DEBUG and r'^admin/' or r'^__adm/'
urlpatterns += patterns('',
    url(admin_url, include(admin.site.urls)),
)

# rosetta
if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += patterns('',
        url(r'^rosetta/', include('rosetta.urls')),
    )

# serving files
#urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
#urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^_403/$', TemplateView.as_view(template_name="403.html")),
        (r'^_404/$', TemplateView.as_view(template_name="404.html")),
        (r'^_500/$', TemplateView.as_view(template_name="500.html")),
    )
