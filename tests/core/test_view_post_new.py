
from django.shortcuts import resolve_url as r

from test_plus import TestCase

from blog.core.forms import PostForm
from blog.core.models import Post


class PostNewGet(TestCase):
    def setUp(self):
        self.user = self.make_user()

        with self.login(username=self.user):
            self.resp = self.get('post_new')

    def test_return_success_status_code(self):
        self.response_200(self.resp)

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'core/post_form.html')

    def test_csrf(self):
        self.assertContains(self.resp, 'csrfmiddlewaretoken')

    def test_form_used(self):
        form = self.resp.context.get('form', None)

        self.assertIsNotNone(form)
        self.assertTrue(isinstance(form, PostForm))


class PostNewLoginRequired(TestCase):
    def test_login_required(self):
        self.assertLoginRequired('post_new')


class PostNewValidPost(TestCase):
    def setUp(self):
        self.user = self.make_user()
        self.data = {
            'title': 'title',
            'summary': 'summary',
            'text': 'text'
        }

        with self.login(username=self.user):
            self.resp = self.post('post_new', data=self.data)

    def test_redirect(self):
        expected_url = r('post_detail', pk=1)
        self.assertRedirects(self.resp, expected_url)

    def test_create_post(self):
        self.assertTrue(Post.objects.exists())

    def test_post(self):
        post = Post.objects.first()

        self.assertEquals(post.author, self.user)
        self.assertEquals(post.title, 'title')
        self.assertEquals(post.text, 'text')


class PostNewInvalidPost(TestCase):
    def setUp(self):
        self.user = self.make_user()
        self.data = {}

        with self.login(username=self.user):
            self.resp = self.post('post_new', data=self.data)

    def test_return_success_status_code(self):
        self.response_200(self.resp)

    def test_form_has_erros(self):
        form = self.resp.context['form']
        self.assertTrue(form.errors)