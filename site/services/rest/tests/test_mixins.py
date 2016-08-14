#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.test import TestCase
from rest_framework import serializers

from services.rest.mixins import FieldValidationMixin


class FieldValidationMixinTestCase(TestCase):

    def test_validate_number_segments(self):

        mixin = FieldValidationMixin()

        # good input
        segments = [1, 2, 3, 4, u'5-10']
        self.assertEqual(mixin.validate_number_segments(segments), segments)

        # char input
        segments = [1, 2, 3, 4, u'5-10a']
        with self.assertRaises(serializers.ValidationError):
            mixin.validate_number_segments(segments), segments

        # char input
        segments = [1, 2, 3, 4, u'10-5']
        with self.assertRaises(serializers.ValidationError):
            mixin.validate_number_segments(segments), segments
