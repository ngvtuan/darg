#!/usr/bin/python
# -*- coding: utf-8 -*-

from random import choice
from string import ascii_uppercase

def random_hash(digits=4):
    hash = ''.join(choice(ascii_uppercase) for i in range(12))
    return hash[:digits]
