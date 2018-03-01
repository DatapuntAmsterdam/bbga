# Python
import os

from datetime import date

from rest_framework.test import APITestCase

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
                             'application/json',
                             'Wrong Content-Type for {}'.format(url))

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

            self.assertEqual(
                response['Content-Type'],
                'application/json',
                'Wrong Content-Type for {}'.format(url))

    def test_latest_filter(self):
        """
        test latest filtering
        """
        path = 'bbga/cijfers'
        params = '?jaar=latest&gebiedcode15=STAD&variabele=BEV0_3'
        url = '/{}/{}'.format(path, params)

        response = self.client.get(url)

        self.assertEqual(
            response.status_code, 200,
            'Wrong response code for {}'.format(url))

        self.assertIn('count', response.data,
                      msg='No count attribute in {}'.format(url))

        self.assertTrue(response.data['count'] > 0,
                        msg='Wrong result count for {}'.format(url))

        latest = response.data['results'][0]['jaar']
        year_now = date.today().year

        self.assertTrue(
            latest >= year_now-2,
            msg="Testdata is too old (latest year={})".format(latest))

        for year in range(year_now-2, latest+1):
            models.Cijfers.objects.get(jaar=year, variabele='BEV0_3').delete()

        response = self.client.get(url)

        self.assertTrue(response.data['count'] > 0,
                        msg='Wrong result count for {}'.format(url))

        old = response.data['results'][0]['jaar']

        self.assertEqual(year_now - 3, old)

    def test_latest_njaar_filter(self):
        nyears = '-3'
        path = 'bbga/cijfers'
        params = f'?jaar={nyears}&gebiedcode15=STAD&variabele=BEV0_3'
        url = '/{}/{}'.format(path, params)

        response = self.client.get(url)

        self.assertEqual(
            response.status_code, 200,
            'Wrong response code for {}'.format(url))

        self.assertIn(
            'count', response.data,
            msg='No count attribute in {}'.format(url))

        self.assertTrue(
            response.data['count'] == 3,
            msg='Wrong result count for {}'.format(url))

        year_now = date.today().year

        latest = response.data['results'][0]['jaar']
        year_now = date.today().year

        self.assertTrue(
            latest >= year_now-2,
            msg="Testdata is too old (latest year={})".format(latest))

    def test_data(self):
        """
        Health is only ok (200) with more the 1.000.000 records.
        so we should expect bad health on test set
        """
        response = self.client.get('/status/data')

        self.assertEqual(
            response.status_code, 500,
            'Wrong response code for /status/data')
