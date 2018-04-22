from django.shortcuts import resolve_url as r

from mixer.backend.django import mixer
from test_plus import TestCase

from blog.core.models import Post, Comment


class PostModel(TestCase):
    def setUp(self):
        self.post = mixer.blend(Post)

    def test_create(self):
        self.assertTrue(Post.objects.exists())

    def test_get_absolute_url(self):
        expected = r('post_detail', pk=self.post.pk)
        self.assertEqual(expected, self.post.get_absolute_url())

    def test_publish(self):
        self.post.publish()
        post = Post.objects.first()
        self.assertTrue(post.published)

    def test_has_comments(self):
        self.post.comments.create(
            author='Author 1',
            text='Post'
        )
        self.assertEqual(1, self.post.comments.count())

    def test_post_str_equal_to_post_title(self):
        self.assertEqual(self.post.title, str(self.post))