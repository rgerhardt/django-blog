from django.shortcuts import resolve_url as r

from mixer.backend.django import mixer
from test_plus import TestCase

from blog.core.forms import CommentForm
from blog.core.models import Post


class CommentAddViewGet(TestCase):
    def setUp(self):
        self.valid_post = mixer.blend(Post)
        self.resp = self.get('add_comment_to_post', pk=self.valid_post.pk)

    def test_return_success_status_code(self):
        self.response_200(self.resp)

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'core/comment_form.html')

    def test_form(self):
        form = self.resp.context.get('form', None)

        self.assertIsNotNone(form)
        self.assertTrue(isinstance(form, CommentForm))

    def test_contains_csrf_token(self):
        self.assertContains(self.resp, 'csrfmiddlewaretoken')

    def test_context(self):
        self.assertInContext('post')


class CommentAddViewPostNotFound(TestCase):
    def setUp(self):
        self.resp = self.get('add_comment_to_post', pk=0)

    def test_return_not_found_status_code(self):
        self.response_404(self.resp)


class CommentAddViewValidPost(TestCase):
    def setUp(self):
        self.valid_post = mixer.blend(Post)
        self.data = {
            'title': 'Title 1',
            'text': 'Text 1',
            'author': 'Mario'
        }

        self.resp = self.post(
            'add_comment_to_post',
            data=self.data,
            pk=self.valid_post.pk
        )

    def test_redirect(self):
        expected = r('post_list')
        self.assertRedirects(self.resp, expected)

    def test_post_has_comment(self):
        self.valid_post.refresh_from_db()
        self.assertEqual(1, self.valid_post.comments.count())


class CommentAddViewInvalidPost(TestCase):
    def setUp(self):
        self.valid_post = mixer.blend(Post)
        self.data = {}

        self.resp = self.post(
            'add_comment_to_post',
            data=self.data,
            pk=self.valid_post.pk
        )

    def test_return_success_status_code(self):
        self.response_200(self.resp)

    def test_form_has_errors(self):
        form = self.resp.context['form']
        self.assertTrue(form.errors)