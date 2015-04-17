from django.conf.urls import include, url
from django.contrib import admin

from rest_framework import routers

from services.rest.views import ShareholderViewSet, CompanyViewSet, UserViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'shareholders', ShareholderViewSet, base_name="shareholders")
router.register(r'company', CompanyViewSet)
router.register(r'user', UserViewSet, base_name="user")

urlpatterns = [
    # Examples:
    url(r'^$', 'project.views.index', name='index'),
    url(r'^start/$', 'project.views.start', name='start'),

    url(r'^accounts/', include('registration.backends.simple.urls')),

    url(r'^services/rest/', include(router.urls)),

    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^admin/', include(admin.site.urls)),
]
