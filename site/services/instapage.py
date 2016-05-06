"""
handle instpage leads
"""
import requests

from django.conf import settings


class InstapageSubmission(object):

    token = None
    access_token = None
    base_url = 'https://app.instapage.com/api/1/submission/'

    def __init__(self):
        self.token = settings.INSTAPAGE_TOKEN
        self.access_token = settings.INSTAPAGE_ACCESS_TOKEN

    def _get_value_by_field_name(self, field_names, exclude_field_names='XXX'):
        """ checks for string inside seld.data.dict"""

        if isinstance(field_names, list):
            for field_name in field_names:
                r = self._get_value_by_field_name(
                    field_name, exclude_field_names)
                if r:
                    return r
            return False

        for field in self.data.get('data').get('fields'):
            if field_names in field.get('name') and \
                exclude_field_names not in field.get('name'):
                return field.get('value')

        return None

    def _get_place_query_string(self):
        s1 = self._get_value_by_field_name(['Adresse', 'Musterstadt'], 'Email')
        s2 = [
            self._get_value_by_field_name('Strasse'),
            self._get_value_by_field_name('Hausnummer'),
            self._get_value_by_field_name('Stadt')
        ]
        if s1:
            return s1
        if None not in s2:
            return s2[0] + u' ' + s2[1] + u', ' + s2[2]

        return None

    def get(self, submission_id):
        """
        get lead data based on submission id, which gets send
        to the app when redirected from form via instapage landingpage:
        """

        headers = {
            'TOKEN': self.token,
            'ACCESS': self.access_token,
        }
        url = "{}{}".format(self.base_url, submission_id)
        res = requests.get(url, headers=headers)
        data = res.json()

        self.data = data
        return data

    def get_address(self, submission_id):
        """ get address from response """

        res = self.get(submission_id)
        address = res["data"]["fields"][0]["value"]
        return address
