from django.shortcuts import resolve_url as r

from mixer.backend.django import mixer
from test_plus import TestCase

from blog.core.models import Post


class DeletePostViewGet(TestCase):
    def setUp(self):
        self.user = self.make_user('user')
        self.valid_post = mixer.blend(Post)

        with self.login(username=self.user.username):
            self.resp = self.get('post_remove', pk=self.valid_post.pk)

    def test_return_success_status_code(self):
        self.response_200(self.resp)

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'core/post_confirm_delete.html')

    def test_view_has_crsf(self):
        self.assertContains(self.resp, 'csrfmiddlewaretoken')

    def test_login_required(self):
        self.assertLoginRequired('post_remove', pk=self.valid_post.pk)


class DeletePostViewPost(TestCase):
    def setUp(self):
        self.user = self.make_user()
        self.valid_post = mixer.blend(Post)
        self.valid_post.publish()

        with self.login(username=self.user.username):
            self.resp = self.post('post_remove', pk=self.valid_post.pk)

    def test_remove_post_from_db(self):
        self.assertFalse(Post.objects.exists())

    def test_redirect_after_post(self):
        expected = r('post_list')
        self.assertRedirects(self.resp, expected)
