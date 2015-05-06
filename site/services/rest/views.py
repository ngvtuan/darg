from django.contrib.auth import get_user_model

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from services.rest.serializers import ShareholderSerializer, CompanySerializer, UserSerializer, PositionSerializer
from services.rest.permissions import UserCanAddCompanyPermission, \
    SafeMethodsOnlyPermission, UserCanAddShareholderPermission, UserCanAddPositionPermission,\
    UserCanAddInviteePermission
from shareholder.models import Shareholder, Company, Operator, Position

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

    def get_queryset(self):
        user = self.request.user
        return Company.objects.filter(operator__user=user)

        return super(CompanyViewSet, self).create(obj)

class UserViewSet(viewsets.ModelViewSet):
    """ API endpoint to get user base info """
    serializer_class = UserSerializer
    permission_classes = [
        SafeMethodsOnlyPermission,
    ]

    def get_queryset(self):
        user = self.request.user
        return User.objects.filter(id = user.id)

class InviteeUpdateView(APIView):
    """ API endpoint to get user base info """
    #permission_classes = [
    #    UserCanAddInviteePermission,
    #]

    def post(self, request, format=None):
        
        serializer = UserSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save(username=serializer.validated_data['email'])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PositionViewSet(viewsets.ModelViewSet):
    """ API endpoint to get user base info """
    serializer_class = PositionSerializer
    permission_classes = [
        UserCanAddPositionPermission,
    ]

    def get_queryset(self):
        user = self.request.user
        return Position.objects.filter(buyer__company__operator__user=user).order_by('bought_at')
