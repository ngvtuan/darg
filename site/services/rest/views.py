from django.contrib.auth import get_user_model

from rest_framework import viewsets

from services.rest.serializers import ShareholderSerializer, CompanySerializer, UserSerializer
from services.rest.permissions import UserCanAddCompanyPermission, SafeMethodsOnlyPermission, UserCanAddShareholderPermission
from shareholder.models import Shareholder, Company, Operator

User = get_user_model()

class ShareholderViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    # FIXME filter by user perms
    serializer_class = ShareholderSerializer
    permission_classes = [
        UserCanAddShareholderPermission,
    ]

    def get_queryset(self):
        user = self.request.user
        return Shareholder.objects.filter(company__operator__user=user)


class CompanyViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    # FIXME filter by user perms
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [
        UserCanAddCompanyPermission,
    ]

    def create(self, obj):
        """Force author to the current user on save"""
        operator = Operator.objects.create(user=self.request.user, company=obj)

        return super(CompanyViewSet, self).create(obj)

class UserViewSet(viewsets.ModelViewSet):
    """ API endpoint to get user base info """
    serializer_class = UserSerializer
    permission_classes = [
        SafeMethodsOnlyPermission
    ]

    def get_queryset(self):
        user = self.request.user
        return User.objects.filter(id = user.id)
