from django.conf import settings
from django.contrib.auth import get_user_model

from shareholder.models import Shareholder, Company, Operator, Position
from rest_framework import serializers

from utils.user import make_username

User = get_user_model()

class CompanySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Company
        fields = ('pk', 'name')

    def create(self, validated_data):

        name = validated_data.get("name")
        user = self.context.get("request").user

        company, created = Company.objects.get_or_create(name=name)
        operator, created = Operator.objects.get_or_create(company=company, user=user)

        return company

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
        fields = ('pk', 'user', 'number', 'company', 'share_percent', 'share_count',)

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

class PositionSerializer(serializers.HyperlinkedModelSerializer):
    buyer = ShareholderSerializer(many=False)
    seller = ShareholderSerializer(many=False)
    bought_at = serializers.DateTimeField() # e.g. 2015-06-02T23:00:00.000Z

    class Meta:
        model = Position
        fields = ('pk', 'buyer', 'seller', 'bought_at', 'sold_at', 'count', 'value')

    def create(self, validated_data):
        """ adding a new position and handling nested data """

        # prepare data
        user = self.context.get("request").user
        company = user.operator_set.all()[0].company
        buyer = Shareholder.objects.get(
            company=company, 
            user__email=validated_data.get("buyer").get("user").get("email")
        )
        
        kwargs = {
            "buyer": buyer,
            "bought_at": validated_data.get("bought_at"),
            "value": validated_data.get("value"),
            "count": validated_data.get("count"),
        }

        position = Position.objects.create(**kwargs)

        return position
