#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import re

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


def inflate_segments(segments):
    """
    change all shortened segments u'1-10' into [1,2 ..., 10]
    """
    def to_list(segment):
        if isinstance(segment, unicode):
            start, end = segment.split('-')
            return range(int(start), int(end)+1)

        return segment

    nested_segments = [to_list(segment)for segment in segments]
    flattened_segments = []
    for segment in nested_segments:
        if isinstance(to_list(segment), int):
            flattened_segments.append(segment)
        if isinstance(to_list(segment), list):
            flattened_segments.extend(segment)

    return flattened_segments


def deflate_segments(segments):
    """
    inverted inflate_segments method
    """
    start = None
    advance = None
    deflated_segments = []

    # attention: writes to list backwards elements
    for segment in segments:
        if start is None:
            start = segment
            advance = segment
            continue
        elif advance and segment == advance + 1:
            advance = segment
            # on last element write range before continue
            if segment == segments[-1]:
                deflated_segments.append(u'{}-{}'.format(start, advance))
            continue

        # write single int
        if start == advance:
            deflated_segments.append(start)
        else:
            deflated_segments.append(u'{}-{}'.format(start, advance))

        # on last element detect and write lonely int
        if segment == segments[-1] and segment > advance + 1:
            deflated_segments.append(segment)

        # start over
        start = segment
        advance = segment

    return deflated_segments
