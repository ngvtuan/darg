from rest_framework import viewsets

from services.rest.serializers import ShareholderSerializer
from shareholder.models import Shareholder

class ShareholderViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    # FIXME filter by user perms
    queryset = Shareholder.objects.all()
    serializer_class = ShareholderSerializer
