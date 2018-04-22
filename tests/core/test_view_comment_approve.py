from django.shortcuts import resolve_url as r

from mixer.backend.django import mixer
from test_plus import TestCase

from blog.core.models import Post, Comment


class CommentApproveViewGet(TestCase):
    def setUp(self):
        self.user = self.make_user()
        self.comment = mixer.blend(Comment, post=mixer.blend(Post))

        with self.login(username=self.user.username):
            self.resp = self.get('comment_approve', pk=self.comment.pk)

    def test_return_no_content_status_code(self):
        self.response_204(self.resp)

    def test_content_type(self):
        expected = 'application/json'
        self.assertEqual(self.resp['Content-Type'], expected)

    def test_approve_comment(self):
        comment = Comment.objects.get(pk=self.comment.post.pk)
        self.assertTrue(comment.approved_comment)


class CommentApproveViewNotFound(TestCase):
    def test_not_found_status_code(self):
        resp = self.get('comment_approve', pk=-1)
        self.response_404(resp)


class CommentApproveViewLoginRequired(TestCase):
    def setUp(self):
        self.comment = mixer.blend(Comment, post=mixer.blend(Post))

    def test_login_requerired(self):
        self.assertLoginRequired('comment_approve', pk=self.comment.pk)


