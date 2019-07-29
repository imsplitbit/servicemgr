import unittest
import json
from svcmgr import create_app
from svcmgr.models import db


class ServicesTestCase(unittest.TestCase):
    """This class represents the services test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.first_svc_name = 'sonarr'
        self.second_svc_name = 'radarr'
        self.first_svc = {'name': self.first_svc_name}

        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_service_creation(self):
        """Test API can create a service (POST request)"""
        res = self.client().post('/api/v0/services/{}'.format(self.first_svc_name))
        self.assertEqual(res.status_code, 201)
        self.assertIn(self.first_svc_name, str(res.data))

    def test_service_get_after_create(self):
        """Test API can create a service and fetch that service. (POST, GET)"""
        res = self.client().post('/api/v0/services/{}'.format(self.first_svc_name))
        self.assertEqual(res.status_code, 201)
        self.assertIn(self.first_svc_name, str(res.data))
        res = self.client().get('/api/v0/services/{}'.format(self.first_svc_name))
        self.assertEqual(res.status_code, 200)
        self.assertIn(self.first_svc_name, str(res.data))

    def test_service_get_not_found(self):
        """Test API returns proper error when service not found (GET)"""
        res = self.client().get('/api/v0/services/{}'.format(self.first_svc_name))
        self.assertEqual(res.status_code, 404)
        data = json.loads(res.data)
        self.assertIn('error', data.keys())


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
