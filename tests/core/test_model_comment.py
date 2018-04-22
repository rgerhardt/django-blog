from django.shortcuts import resolve_url as r

from mixer.backend.django import mixer
from test_plus import TestCase

from blog.core.models import Comment


class CommentModelTest(TestCase):
    def setUp(self):
        self.comment = mixer.blend(Comment)

    def test_create(self):
        self.assertTrue(Comment.objects.exists())

    def test_get_absolute_url(self):
        expected = r('post_list')
        self.assertEqual(expected, self.comment.get_absolute_url())

    def test_approve(self):
        self.comment.approve()
        comment = Comment.objects.first()
        self.assertTrue(comment.approved_comment)

    def test_disapprove(self):
        self.comment.disapprove()
        comment = Comment.objects.first()
        self.assertFalse(comment.approved_comment)

    def test_st(self):
        self.assertEqual(self.comment.text, str(self.comment))