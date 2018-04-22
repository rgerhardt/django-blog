from django.shortcuts import resolve_url as r

from mixer.backend.django import mixer
from test_plus import TestCase

from blog.core.forms import PostForm
from blog.core.models import Post


class PostEditViewAuthenticatedUserGet(TestCase):
    def setUp(self):
        self.user = self.make_user('user')
        self.post = mixer.blend(Post)

        with self.login(username=self.user.username):
            self.resp = self.get('post_edit', pk=self.post.id)

    def test_return_status_code_200(self):
        self.response_200(self.resp)

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'core/post_form.html')

    def test_csrf(self):
        self.assertContains(self.resp, "csrfmiddlewaretoken")

    def test_has_form(self):
        form = self.resp.context['form']
        self.assertIsInstance(form, PostForm)


class PostEditViewAnonymousUserGet(TestCase):
    def setUp(self):
        self.post = mixer.blend(Post)
        self.resp = self.get('post_edit', pk=self.post.pk)

    def test_redirect_to_login(self):
        expected = r('login')
        self.response_302(self.resp)
        self.assertIn(expected, self.resp.url)


class PostEditViewNotFoundGet(TestCase):
    def setUp(self):
        self.user = self.make_user('user')

        with self.login(username=self.user.username):
            self.resp = self.get('post_edit', pk=0)

    def test_not_found(self):
        self.response_404(self.resp)


class PostEditViewValidPost(TestCase):
    def setUp(self):
        self.user = self.make_user('user')
        self.valid_post = mixer.blend(Post, title='title')
        data = {
            'title': 'title 1',
            'author': self.user.id,
            'summary': 'summary',
            'text': '123',
        }

        with self.login(username=self.user.username):
            url = r('post_edit', pk=self.valid_post.id)
            self.resp = self.client.post(url, data=data)

    def test_return_success_status_code(self):
        self.response_302(self.resp)

    def test_redirect_to_post_detail(self):
        expected = r('post_detail', pk=self.valid_post.id)
        self.assertEqual(self.resp.url, expected)

    def test_update_post(self):
        self.valid_post.refresh_from_db()
        self.assertEqual(self.valid_post.title, 'title 1')


class PostEditViewInvalidPost(TestCase):
    def setUp(self):
        self.user = self.make_user('user')
        self.valid_post = mixer.blend(Post)
        with self.login(username=self.user.username):
            url = r('post_edit', pk=self.valid_post.id)
            self.resp = self.client.post(url, data={})

    def test_return_success_status_code(self):
        self.response_200(self.resp)

    def test_form_erros(self):
        form = self.resp.context['form']
        self.assertTrue(form.errors)