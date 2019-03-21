from django.test import TestCase
from selenium import webdriver


class NewVisitorTest(TestCase):
    def setUp(self):
        self.browser = webdriver.Chrome()

    def tearDown(self):
        self.browser.quit()

    def test_see_browser(self):
        self.browser.get('http://localhost:8000')

        self.assertIn('Undercut', self.browser.title)
