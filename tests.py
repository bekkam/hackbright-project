import server
import server_utilities
import unittest
import doctest


def load_tests(loader, tests, ignore):
    """Run doctests and file-based doctests.

    """

    tests.addTests(doctest.DocTestSuite(server_utilities))
    tests.addTests(doctest.DocFileSuite("tests.txt"))
    return tests


class RunSafeUnitTestCase(unittest.TestCase):
    """Unit tests: discrete code testing."""

    def get_distance_per_hour(self):
        assert server_utilities.get_distance_per_hour(1.2, 10) == '7.20'

    # Add tests for queries to db


class RunSafeTestCase(unittest.TestCase):
    """Integration tests: testing Flask server."""

    def setUp(self):
        print "(setUp ran)"
        self.client = server.app.test_client()
        server.app.config['TESTING'] = True

    def tearDown(self):
        """Stub function for later."""
        print "(tearDown ran)"

    def test_home_page(self):
        """Test that the homepage returns the correct html"""

        result = self.client.get('/')
        self.assertEqual(result.status_code, 200)
        self.assertIn('<h3>Map a new route</h3>', result.data)
        self.assertIn('<h3>Search for a saved route</h3>', result.data)

    # def test_profile_page(self):
    #     """Test that the profile page returns the correct html"""

    #     result = self.client.get('/profile')
    #     self.assertEqual(result.status_code, 200)
    #     self.assertIn("<h2>Profile</h2>", result.data)

    def test_draw_route(self):
        """Test that the map page returns the correct html"""

        result = self.client.get('draw-route?start=golden+gate+park%2C+san+francisco+ca&end=24th+street+mission+bart%2C+san+francisco%2C+ca')
        self.assertEqual(result.status_code, 200)
        self.assertIn('<div id="map" style="height:500px; width: 900px;"></div>', result.data)
        self.assertIn('<div id="right-panel" style="height:500px; width: 400px;"></div>', result.data)
        self.assertIn('<input type="checkbox" name="streetlight-data-heatmap" id="heatmap">', result.data)
        self.assertIn('<input type="checkbox" name="streetlight-data" id="marker-checkbox">', result.data)
        self.assertIn('<h4>Save this Route: </h4>', result.data)
        self.assertIn("<h4>I've Run this Route: </h4>", result.data)

    # def test_routes_page(self):
    #     """Test that the routes page returns the correct html"""

    #     result = self.client.get('/routes')
    #     self.assertEqual(result.status_code, 200)
        # self.assertIn("<h2>Profile</h2>", result.data)

if __name__ == '__main__':
    # Run these tests if file is called like a script

    unittest.main()
