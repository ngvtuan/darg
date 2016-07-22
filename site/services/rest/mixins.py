#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
import logging

from rest_framework import serializers

from django.utils.translation import ugettext_lazy as _

logger = logging.getLogger(__name__)


class FieldValidationMixin(object):

    def validate_number_segments(self, value):

        pattern = re.compile(r'[^0-9,\- ]')
        for part in value:

            # validate value as we have to track value...
            if pattern.findall(str(part)):
                raise serializers.ValidationError(
                    _("Invalid number segment. "
                      "Please use 1, 2, 3, 4-10.")
                )
                logger.warning("Invalid number segment: {}".format(part))

            if isinstance(part, int):
                continue

            # --- VALIDATE u'X-Z' only
            # validate that start and end of u'1-9' are valid
            start, end = part.split('-')
            if int(start) >= int(end):
                raise serializers.ValidationError(
                    _("Number Segment Range start smaller/equal then end '{}'. "
                      "Please use 1, 2, 3, 4-10.".format(part))
                )
                logger.warning("Invalid number segment: {}".format(part))

        return value
