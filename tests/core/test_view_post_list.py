import datetime

from django.utils import timezone

from mixer.backend.django import mixer
from test_plus import TestCase

from blog.core.models import Post, Comment


class PostListGet(TestCase):
    def setUp(self):
        self.post1 = mixer.blend(Post, title='Post 1', summary='Summary 1')
        self.post1.publish()
        self.comment = mixer.blend(Comment, post=self.post1, approved_comment=True)

        self.post2 = mixer.blend(Post, title='Post 2', summary='Summary 2')
        self.post2.publish()

        self.post3 = mixer.blend(Post)
        self.post3_created_date = timezone.now() + datetime.timedelta(days=1)

        self.response = self.get('post_list')

    def test_response_status_code(self):
        self.response_200(self.response)

    def test_template(self):
        self.assertTemplateUsed(self.response, 'core/post_list.html')

    def test_post_list_in_context(self):
        self.assertInContext('post_list')

    def test_only_list_published_posts(self):
        post_list = self.response.context['post_list']
        self.assertIn(self.post1, post_list)
        self.assertIn(self.post2, post_list)

    def test_post_list_should_order_by_desc_create_date(self):
        post_list = self.response.context['post_list']
        self.assertListEqual(list(post_list), [self.post2, self.post1])

    def test_content(self):
        contents = (
            (1, 'Post 1'),
            (1, 'Summary 1'),
            (1, 'href="/post/1"'),
            (1, 'Comments: 1'),
            (1, 'Post 2'),
            (1, 'Summary 2'),
            (1, 'href="/post/2"'),
            (1, 'Comments: 0'),
            (2, 'Published on: {}'.format(self.post1.published_at.strftime('%d %b %Y'))),
        )

        for times, content in contents:
            with self.subTest():
                self.assertContains(self.response, content, times)


class EmptyPostListGet(TestCase):
    def setUp(self):
        self.response = self.get('post_list')

    def test_response_status_code(self):
        self.response_200(self.response)

    def test_content(self):
        self.assertContains(self.response, 'No post found!')