#Python
import os
from unittest.mock import Mock
# Packages
from rest_framework.test import APITestCase
from django.http import HttpResponse
# Project
from bbga_data import import_data
from bbga_data import models


class BrowseDatasetsTestCase(APITestCase):
    """
    Verifies that browsing the API works correctly.
    """
    datasets = [
        'bbga/meta',
        'bbga/cijfers',
    ]

    extra_sets = [
        'bbga/variabelen',
        'bbga/themas',
        'bbga/groepen',
    ]

    def setUp(self):
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        meta_csv = os.path.join(BASE_DIR, 'tests/test_data/metadata_utf8.csv')
        cijfers_csv = os.path.join(
            BASE_DIR, 'tests/test_data/bbga_tableau.csv')

        import_data.import_meta_csv(meta_csv, 'bbga_data_meta')
        import_data.import_variable_csv(cijfers_csv, 'bbga_data_cijfers')

    def test_lists(self):
        for url in self.datasets:
            response = self.client.get('/{}/'.format(url))

            self.assertEqual(
                response.status_code, 200,
                'Wrong response code for {}'.format(url))

            self.assertEqual(response[
                'Content-Type'],
                'application/json', 'Wrong Content-Type for {}'.format(url))

            self.assertIn(
                'count', response.data, 'No count attribute in {}'.format(url))

            self.assertNotEqual(
                response.data['count'], 0,
                'Wrong result count for {}'.format(url))

    def test_extra(self):
        for url in self.extra_sets:
            response = self.client.get('/{}/'.format(url))

            self.assertEqual(
                response.status_code, 200,
                'Wrong response code for {}'.format(url))

            self.assertEqual(response[
                'Content-Type'],
                'application/json', 'Wrong Content-Type for {}'.format(url))

    def test_latest_filter(self):
        """
        test latest filtering
        """
        url = 'bbga/cijfers'
        params = '?jaar=latest&gebiedcode15=STAD&variabele=BEV0_3'

        response = self.client.get('/{}/{}'.format(url, params))

        self.assertEqual(
            response.status_code, 200,
            'Wrong response code for {}'.format(url))

        self.assertIn(
                'count', response.data, 'No count attribute in {}'.format(url))

        self.assertNotEqual(
                response.data['count'], 0,
                'Wrong result count for {}'.format(url))

        latest = response.data['results'][0]['jaar']

        c1 = models.Cijfers.objects.get(jaar=latest, variabele='BEV0_3')
        c2 = models.Cijfers.objects.get(jaar=latest - 1, variabele='BEV0_3')
        c3 = models.Cijfers.objects.get(jaar=latest - 2, variabele='BEV0_3')

        c1.delete()
        c2.delete()
        c3.delete()

        response = self.client.get('/{}/{}'.format(url, params))

        old = response.data['results'][0]['jaar']

        self.assertEqual(latest - 3, old)

        # check for 2016
        #
        # models.
        # remove object jaar and jaar-1

        # get latests

        # = jaar - 3

    def test_health(self):
        """
        Health is only ok (200) with more the 1.000.000 records.
        so we should expect bad health on test set
        """
        response = self.client.get('/status/health')

        self.assertEqual(
            response.status_code, 500,
            'Wrong response code for health')
