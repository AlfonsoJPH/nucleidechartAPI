import unittest
import tracemalloc
import io
import json
from app import create_app

tracemalloc.start()

class FlaskApiTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = create_app().app
        cls.client = cls.app.test_client()
        cls.client.testing = True

    def test_generar_tabla(self):
        with io.BytesIO(b'Mass Number,Atomic Number,A Element,Isomer,Mass Excess,Mass Excess uncertainty,Isomer Excitation Energy,Isomer Excitation Energy uncertainty,Origin of Excitation Energy,Isom.Unc,Isom.Inv,Half-life,Half-life unit,Half-life uncertainty,Spin and Parity,Ensdf year,Year of Discovery,Decay Modes and their Intensities\n001,0010,1H,,7288.971064,0.000013,,,,,,stbl,,,1/2+*,06,1920,IS=99.9855 78\n') as test_csv:
            response = self.client.post('/gen_table/', data={
                'sessionID': 'test-session-id',
                'source': (test_csv, 'test.csv')
            }, content_type='multipart/form-data')

            self.assertEqual(response.status_code, 200)
            self.assertIn('Content-Disposition', response.headers)
            self.assertTrue(response.headers['Content-Disposition'].startswith('attachment'))

    def test_check_config(self):
        with io.BytesIO(json.dumps({"key": "value"}).encode()) as config_file:
            response = self.client.post('/get_config/', data={
                'sessionID': 'test-session-id',
                'config': (config_file, 'config.json')
            }, content_type='multipart/form-data')

            self.assertEqual(response.status_code, 200)
            self.assertIn('Content-Disposition', response.headers)
            self.assertTrue(response.headers['Content-Disposition'].startswith('attachment'))

    def test_generar_element_box(self):
        with io.BytesIO(b'some,csv,data\n') as test_csv:
            response = self.client.post('/gen_element_box/', data={
                'sessionID': 'test-session-id',
                'element_box': '1H',
                'source': (test_csv, 'test.csv')
            }, content_type='multipart/form-data')

            self.assertEqual(response.status_code, 200)
            self.assertIn('Content-Disposition', response.headers)
            self.assertTrue(response.headers['Content-Disposition'].startswith('attachment'))

if __name__ == '__main__':
    unittest.main()
