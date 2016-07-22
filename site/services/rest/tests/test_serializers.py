#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.test import RequestFactory, TestCase

from services.rest.serializers import PositionSerializer
from shareholder.generators import PositionGenerator


class PositionSerializerTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    def test_is_valid(self):

        def serialize(segments):
            position = PositionGenerator().generate(number_segments=segments)
            url = reverse('position-detail', kwargs={'pk': position.id})
            request = self.factory.get(url)
            # prepare data
            data = PositionSerializer(position, context={'request': request}).data
            # clear bad datetimedata
            data['buyer']['user']['userprofile']['birthday'] = None
            data['seller']['user']['userprofile']['birthday'] = None
            data['bought_at'] = '2014-01-01T10:00'
            return PositionSerializer(data=data, context={'request': request})

        serializer = serialize([1, 3, 4, u'6-9', 33])
        res = serializer.is_valid()
        self.assertEqual(res, True)
