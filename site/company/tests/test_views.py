#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.utils.translation import gettext as _

from shareholder.generators import (
    CompanyGenerator, SecurityGenerator,
    OperatorGenerator, DEFAULT_TEST_DATA)


class CompanyDetailViewTestCase(TestCase):

    def setUp(self):
        self.client = Client()

    def test_numbered_shares(self):

        company = CompanyGenerator().generate()
        SecurityGenerator().generate(
            company=company, track_numbers=True)
        operator = OperatorGenerator().generate(company=company)

        self.client.login(username=operator.user.username,
                          password=DEFAULT_TEST_DATA.get('password'))

        res = self.client.get(reverse(
            'company', kwargs={'company_id': company.id}))

        self.assertEqual(res.status_code, 200)
        self.assertTrue(
            _('tracking security numbers for owners enabled. segments:') in res.content)
