from blog.core.forms import CommentForm
from test_plus import TestCase


class CommentFormTest(TestCase):
    def test_form_has_fields(self):
        form = CommentForm()
        expected = ['author', 'text']
        self.assertListEqual(expected, list(form.fields))