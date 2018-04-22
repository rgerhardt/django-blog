from test_plus import TestCase


class AboutViewGet(TestCase):

    def setUp(self):
        self.response = self.get('about')

    def test_success_status_code(self):
        self.response_200(self.response)

    def test_template(self):
        self.assertTemplateUsed(self.response, 'core/about.html')