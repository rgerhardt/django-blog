from blog.core.forms import PostForm
from test_plus import TestCase


class PostFormTest(TestCase):
    def test_form_has_fields(self):
        form = PostForm()
        expected = ['title', 'summary', 'text']
        self.assertSequenceEqual(expected, list(form.fields))