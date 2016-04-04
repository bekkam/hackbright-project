import doctest
import unittest

from model import connect_to_test_db, db
import server
import server_utilities as util


def load_tests(loader, tests, ignore):
    """Run doctests and file-based doctests.

    """

    tests.addTests(doctest.DocTestSuite(util))
    return tests


class UtilitiesTestCase(unittest.TestCase):
    """Unit tests for functions in utilitites file."""

    def get_distance_per_hour(self):
        assert util.get_distance_per_hour(1.2, 10) == '7.20'

    def get_lat_long(self):
        assert util.get_lat_long("Mountain View, CA") == [37.3860517, -122.0838511]

    # Add tests for queries to db


class ServerTemplatesTestCase(unittest.TestCase):
    """Integration tests: test that Flask server renders correct templates."""

    def setUp(self):

        print "(setUp ran)"
        self.client = server.app.test_client()
        server.app.config['TESTING'] = True
        connect_to_test_db(server.app)
        db.create_all()

    def tearDown(self):
        """Stub function for later."""
        print "(tearDown ran)"
        db.session.close()
        db.drop_all()

    def test_index_page(self):
        """Test that the index returns the correct html"""

        result = self.client.get('/')
        self.assertEqual(result.status_code, 200)
        self.assertIn('<h4>Login</h4>', result.data)
        self.assertIn('<h4>Register</h4>', result.data)

    def test_homepage(self):
        """Test that the homepage returns the correct html"""

        result = self.client.get('/homepage')
        self.assertEqual(result.status_code, 200)
        self.assertIn("<h3>Map a new course</h3>", result.data)

    def test_draw_course(self):
        """Test that the map page returns the correct html"""

        result = self.client.get('draw-route?start=golden+gate+park%2C+san+francisco+ca&end=24th+street+mission+bart%2C+san+francisco%2C+ca')
        self.assertEqual(result.status_code, 200)
        self.assertIn('<div id="map" style="height:500px; width: 900px;"></div>', result.data)
        self.assertIn('<div id="right-panel" style="height:500px; width: 400px;"></div>', result.data)

    def test_profile_page(self):
        """Test that the profile page returns the correct html"""

        result = self.client.get('/profile')
        self.assertEqual(result.status_code, 200)
        self.assertIn("<h2>Profile</h2>", result.data)

    def test_courses_page(self):
        """Test that the courses page returns the correct html"""

        result = self.client.get('/courses')
        self.assertEqual(result.status_code, 200)
        self.assertIn("<h2>Courses</h2>", result.data)

    def test_runs_page(self):
        """Test that the runs page returns the correct html"""

        result = self.client.get('/runs')
        self.assertEqual(result.status_code, 200)
        self.assertIn("<h2>Runs</h2>", result.data)


# class UserTestCase(unittest.TestCase):
#     """Integration tests for login/logout and registration functions."""

    # Instantiate a session

if __name__ == '__main__':
    # Run these tests if file is called like a script

    unittest.main()
