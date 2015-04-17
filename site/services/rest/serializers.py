from django.conf import settings
from django.contrib.auth import get_user_model

from shareholder.models import Shareholder, Company, Operator
from rest_framework import serializers

from utils.user import make_username

User = get_user_model()

class CompanySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Company
        fields = ('pk', 'name')

class OperatorSerializer(serializers.HyperlinkedModelSerializer):
    company = CompanySerializer(many=False, read_only=True)

    class Meta:
        model = Operator
        fields = ('id', 'company')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    operator_set = OperatorSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'operator_set',)

class ShareholderSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer(many=False)
    company = CompanySerializer(many=False,  read_only=True)

    class Meta:
        model = Shareholder
        fields = ('user', 'number', 'company')

    def create(self, validated_data):

        # existing or new user
        user = self.context.get("request").user

        #FIXME: assuming one company per user
        company = user.operator_set.all()[0].company

        # get unique username
        username = make_username(
            validated_data.get("user").get("first_name"),
            validated_data.get("user").get("last_name"),
            validated_data.get("user").get("email")
        )

        # save user
        shareholder_user, created= User.objects.get_or_create(
            email=validated_data.get("user").get("email"), 
            defaults={
                "username": username,
                "first_name":validated_data.get("user").get("first_name"),
                "last_name":validated_data.get("user").get("last_name"),
            })

        # save shareholder
        shareholder, created = Shareholder.objects.get_or_create(
            user=shareholder_user,
            company=company,
            defaults={"number": validated_data.get("number")},
        )

        return shareholder
