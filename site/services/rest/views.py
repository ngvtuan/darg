from django.contrib.auth import get_user_model

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from services.rest.serializers import ShareholderSerializer, CompanySerializer, UserSerializer, \
    PositionSerializer, AddCompanySerializer, UserWithEmailOnlySerializer, CountrySerializer, \
    OptionPlanSerializer, OptionTransactionSerializer, SecuritySerializer
from services.rest.permissions import UserCanAddCompanyPermission, \
    SafeMethodsOnlyPermission, UserCanAddShareholderPermission, UserCanAddPositionPermission,\
    UserCanEditCompanyPermission, UserCanAddOptionPlanPermission, \
    UserCanAddOptionTransactionPermission
from shareholder.models import Shareholder, Company, Position, Country, OptionPlan, \
    OptionTransaction, Security

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
        return Shareholder.objects.filter(company__operator__user=user)\
            .distinct()


class CompanyViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    # FIXME filter by user perms
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [
        UserCanEditCompanyPermission,
    ]

    def get_queryset(self):
        user = self.request.user
        return Company.objects.filter(operator__user=user)


class AddCompanyView(APIView):
    """ view to initially setup a company """

    queryset = Company.objects.none()
    permission_classes = [
        UserCanAddCompanyPermission,
    ]

    def post(self, request, format=None):
        serializer = AddCompanySerializer(data=request.data)
        if serializer.is_valid() and request.user.is_authenticated():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    """ API endpoint to get user base info """
    serializer_class = UserSerializer
    permission_classes = [
        SafeMethodsOnlyPermission,
    ]

    def get_queryset(self):
        user = self.request.user
        return User.objects.filter(id=user.id)


class CountryViewSet(viewsets.ModelViewSet):
    """ API endpoint to get user base info """
    serializer_class = CountrySerializer
    permission_classes = [
        SafeMethodsOnlyPermission,
    ]

    def get_queryset(self):
        users = Country.objects.all()
        return users


class InviteeUpdateView(APIView):
    """ API endpoint to get user base info """
    permission_classes = (AllowAny,)

    def post(self, request, format=None):

        serializer = UserWithEmailOnlySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(username=serializer.validated_data['email'])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PositionViewSet(viewsets.ModelViewSet):
    """ API endpoint to get positions """
    serializer_class = PositionSerializer
    permission_classes = [
        UserCanAddPositionPermission,
    ]

    def get_queryset(self):
        user = self.request.user
        return Position.objects.filter(buyer__company__operator__user=user)\
            .order_by('bought_at').order_by('-bought_at')


class SecurityViewSet(viewsets.ModelViewSet):
    """ API endpoint to get options """
    serializer_class = SecuritySerializer
    permission_classes = [
        SafeMethodsOnlyPermission,
    ]

    def get_queryset(self):
        return Security.objects.all()


class OptionPlanViewSet(viewsets.ModelViewSet):
    """ API endpoint to get options """
    serializer_class = OptionPlanSerializer
    permission_classes = [
        UserCanAddOptionPlanPermission,
    ]

    def get_queryset(self):
        user = self.request.user
        return OptionPlan.objects.filter(company__operator__user=user)


class OptionTransactionViewSet(viewsets.ModelViewSet):
    """ API endpoint to get options """
    serializer_class = OptionTransactionSerializer
    permission_classes = [
        UserCanAddOptionTransactionPermission,
    ]

    def get_queryset(self):
        user = self.request.user
        return OptionTransaction.objects.filter(
            option_plan__company__operator__user=user)
