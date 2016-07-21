#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
import logging

from rest_framework import serializers

from django.utils.translation import ugettext_lazy as _

logger = logging.getLogger(__name__)


class FieldValidationMixin(object):

    def validate_number_segments(self, value):

        # validate value as we have to track value...
        pattern = re.compile(r'[^0-9,\- ]')
        for part in value:
            if pattern.findall(str(part)):
                raise serializers.ValidationError(
                    _("Invalid number segment. "
                      "Please use 1, 2, 3, 4-10.")
                )
                logger.warning("Invalid number segment: {}".format(part))
        return value
