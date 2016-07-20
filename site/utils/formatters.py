#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import logging

logger = logging.getLogger(__name__)


def string_list_to_json(string):
    """
    takes string and converts into list: "1,2,3,4-10"
    to [1,2,3,u'4-10']
    """
    # validate first
    pattern = re.compile(r'[^0-9,\- ]')
    if pattern.findall(string):
        raise ValueError('invalid characters in segments list')

    parts = string.split(",")
    res = []
    for part in parts:
        part = part.strip()
        if part.count('-') == 1:
            res.append(unicode(part))
        elif part.count('-') == 0 and len(part) > 0:
            res.append(int(part))
        else:
            logger.warning('attempt to add badly formatted number segment',
                           extra={'string': part})

    return res
