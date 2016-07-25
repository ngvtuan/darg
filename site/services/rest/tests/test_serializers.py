#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.test import RequestFactory, TestCase

from services.rest.serializers import PositionSerializer
from shareholder.generators import (OperatorGenerator, PositionGenerator,
                                    TwoInitialSecuritiesGenerator)
from utils.formatters import human_readable_segments


class PositionSerializerTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    def test_is_valid(self):
        """
        position serializer handling numbered shares
        """
        def serialize(segments):
            position = PositionGenerator().generate(number_segments=segments)
            url = reverse('position-detail', kwargs={'pk': position.id})
            request = self.factory.get(url)
            # prepare data
            data = PositionSerializer(
                position, context={'request': request}).data
            # clear bad datetimedata
            data['buyer']['user']['userprofile']['birthday'] = None
            data['seller']['user']['userprofile']['birthday'] = None
            data['bought_at'] = '2014-01-01T10:00'
            return PositionSerializer(data=data, context={'request': request})

        serializer = serialize([1, 3, 4, u'6-9', 33])
        res = serializer.is_valid()
        self.assertEqual(res, True)

    def test_create_capital_increase_numbered_shares(self):
        """
        position serializer handling numbered shares while doing a capital
        increase
        """
        def serialize(segments):
            operator = OperatorGenerator().generate()
            company = operator.company
            securities = TwoInitialSecuritiesGenerator().generate(
                company=company)
            security = securities[1]
            security.track_numbers = True
            security.save()
            position = PositionGenerator().generate(
                company=company, number_segments=segments, save=False,
                security=security, count=8)

            url = reverse('position-detail', kwargs={'pk': position.id})
            request = self.factory.get(url)
            request.user = operator.user

            # prepare data
            position.seller = None
            position.buyer = None
            # get test data dict
            data = PositionSerializer(
                position, context={'request': request}).data
            # clear bad datetimedata
            data['bought_at'] = '2014-01-01T10:00'
            del data['seller'], data['buyer']
            # feed data into serializer
            return PositionSerializer(data=data, context={'request': request})

        segments = [1, 3, 4, u'6-9', 33]
        serializer = serialize(human_readable_segments(segments))
        serializer.is_valid()
        position = serializer.create(serializer.validated_data)
        self.assertEqual(
            [1, u'3-4', u'6-9', 33],
            position.security.number_segments)
