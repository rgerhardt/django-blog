import datetime

from mixer.backend.django import mixer
from test_plus import TestCase

from django.utils import timezone

from blog.core.models import Post


class PostPublishGet(TestCase):
    def setUp(self):
        self.user = self.make_user()
        self.post = mixer.blend(Post)

    def test_redirect(self):
        with self.login(username=self.user.username):
            self.resp = self.get('post_publish', pk=self.post.pk)

        expected_url = self.post.get_absolute_url()
        self.assertRedirects(self.resp, expected_url)

    def test_publish_post(self):

        with self.login(username=self.user.username):
            self.resp = self.get('post_publish', pk=self.post.pk)

        self.post.refresh_from_db()
        self.assertTrue(self.post.published)


class PostPublishNotFound(TestCase):
    def setUp(self):
        self.user = self.make_user()

        with self.login(username=self.user.username):
            self.resp = self.get('post_publish', pk=0)

    def test_not_found_status_code(self):
        self.response_404(self.resp)


class PostPublishLoginRequired(TestCase):
    def setUp(self):
        self.post = mixer.blend(Post)

    def test_login_required(self):
        self.assertLoginRequired('post_publish', pk=self.post.pk)