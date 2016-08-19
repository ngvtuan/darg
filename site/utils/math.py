#!/usr/bin/python
# -*- coding: utf-8 -*-
# implement some tuned fast custom logic


def substract_list(origin, substract):
    """
    example: db tells us that user bought shares 1, 2, 2, 3, 4 and also sold
    1, 2, 2. we need to know that he now owns 3, 4 for 10m item

    learned from here:
    http://openbookproject.net/thinkcs/python/english3e/list_algorithms.html#alice-in-wonderland-again

    lists need to be sorted and can contain duplicates
    """
    result = []
    xi = 0  # @origin
    yi = 0  # @subscract

    len_substract = len(substract)
    len_origin = len(origin)

    while True:
        # reached end of substract, append rest of origin, return
        if yi >= len_substract:
            result.extend(origin[xi:])
            return result

        # reached end of origin, return
        if xi >= len_origin:
            return result

        # step throught the values
        if origin[xi] == substract[yi]:
            # equal values, next one pls
            yi += 1
            xi += 1
        elif origin[xi] > substract[yi]:
            yi += 1
        else:
            result.append(origin[xi])
            xi += 1
