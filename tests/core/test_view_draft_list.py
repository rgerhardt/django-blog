from datetime import timedelta

from mixer.backend.django import mixer
from test_plus import TestCase

from django.utils import formats
from django.utils import timezone

from blog.core.models import Post


class DraftListViewGet(TestCase):
    def setUp(self):
        self.user = self.make_user()
        self.published_post = mixer.blend(Post)
        self.published_post.publish()

        self.unpublished_post1 = mixer.blend(Post)
        self.unpublished_post1.created_date = timezone.now() - timedelta(days=3)
        self.unpublished_post1.save()

        self.unpublished_post2 = mixer.blend(Post)
        self.unpublished_post2.created_date = timezone.now() - timedelta(days=2)
        self.unpublished_post2.save()

        with self.login(username=self.user.username):
            self.resp = self.get('post_draft_list')

    def test_return_success_status_code(self):
        self.response_200(self.resp)

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'core/post_draft_list.html')

    def test_unpublished_posts_in_context(self):
        post_list = self.resp.context.get('post_list', None)

        self.assertIsNotNone(post_list)

        self.assertEqual(len(list(post_list)), 2)
        self.assertIn(self.unpublished_post1, post_list)
        self.assertIn(self.unpublished_post2, post_list)

    def test_unpublished_posts_order(self):
        expected = [self.unpublished_post1, self.unpublished_post2]
        post_list = self.resp.context.get('post_list', None)

        self.assertListEqual(expected, list(post_list))

    def test_html_content(self):
        contents = (
            (1, 'created: {}'.format(formats.date_format(self.unpublished_post1.created_date))),
            (1, self.unpublished_post1.title),
            (1, self.unpublished_post1.text),
            (1, self.unpublished_post1.get_absolute_url()),
            (1, 'created: {}'.format(formats.date_format(self.unpublished_post2.created_date))),
            (1, self.unpublished_post2.title),
            (1, self.unpublished_post2.text),
            (1, self.unpublished_post2.get_absolute_url()),
        )

        for times, content in contents:
            with self.subTest():
                self.assertContains(self.resp, content, times)


class DraftListViewEmptyList(TestCase):
    def setUp(self):
        self.user = self.make_user()
        with self.login(username=self.user.username):
            self.resp = self.get('post_draft_list')

    def test_content(self):
        self.assertContains(self.resp, 'No post found!')


class DraftListViewLoginRequired(TestCase):
    def test_login_required(self):
        self.assertLoginRequired('post_draft_list')