from shareholder.models import Shareholder
from rest_framework import serializers

class ShareholderSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.StringRelatedField()
    company = serializers.StringRelatedField()

    class Meta:
        model = Shareholder
        fields = ('user', 'number', 'company')


