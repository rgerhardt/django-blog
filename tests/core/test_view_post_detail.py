from mixer.backend.django import mixer
from test_plus import TestCase

from django.shortcuts import resolve_url as r
from django.utils import formats
from django.utils import timezone

from blog.core.models import Post, Comment


class PostDetailGet(TestCase):
    def setUp(self):
        self.post = mixer.blend(Post, title='Post', text='Text')
        self.resp = self.get('post_detail', pk=self.post.pk)

    def test_response_status_code(self):
        self.response_200(self.resp)

    def test_post_object_in_context(self):
        self.assertInContext('post')
        self.assertContext('post', self.post)

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'core/post_detail.html')

    def test_has_add_comment_view_link(self):
        expected = r('add_comment_to_post', pk=self.post.pk)
        self.assertContains(self.resp, expected)


class PostDetailGetPostWithoutComments(TestCase):
    def setUp(self):
        self.post = mixer.blend(Post, title='Post', text='Text')
        self.resp = self.get('post_detail', pk=self.post.pk)

    def test_content(self):
        self.assertContains(self.resp, 'No comments found!')


class PostDetailAuthenticatedUserGet(TestCase):
    def setUp(self):
        self.user = self.make_user('user')

        self.post = mixer.blend(Post, title='Post 1', text='Text')
        self.comment_approved = mixer.blend(Comment, text='Comment 1', author='Author 1', post=self.post)
        self.comment_approved.approve()
        self.comment_disapproved = mixer.blend(Comment, text='Comment 2', author='Author 2', post=self.post)

        self.published_post = mixer.blend(Post)
        self.published_post.publish()

        with self.login(username=self.user.username):
            self.resp = self.get('post_detail', pk=self.post.pk)

    def test_show_last_update_date_if_post_is_published(self):
        response = self.get('post_detail', pk=self.published_post.pk)
        expected = formats.date_format(self.published_post.published_at)
        self.assertContains(response, expected)

    def test_show_publish_link_if_post_is_not_published(self):
        expected = r('post_publish', pk=self.post.pk)
        self.assertContains(self.resp, expected)

    def test_show_action_post_links_if_user_is_authenticated(self):
        links = [
            r('post_edit', pk=self.post.pk),
            r('post_remove', pk=self.post.pk)
        ]

        for link in links:
            with self.subTest():
                self.assertContains(self.resp, link)

    def test_show_approve_comment_link_if_comment_is_not_approved(self):
        approve_link = r('comment_approve', pk=self.comment_disapproved.pk)
        self.assertContains(self.resp, approve_link)

    def test_show_disapprove_comment_link_if_comment_is_approved(self):
        disapprove_link = r('comment_disapprove', pk=self.comment_approved.pk)
        self.assertContains(self.resp, disapprove_link)

    def test_html_content(self):
        contents = (
            ('Post 1'),
            ('Text'),
            ('Comment 1'),
            ('Author 1'),
            (formats.date_format(self.comment_approved.created_date)),
            ('Comment 2'),
            ('Author 2'),
            (formats.date_format(self.comment_disapproved.created_date)),
        )

        for content in contents:
            with self.subTest():
                self.assertContains(self.resp, content)


class PostDetailUnauthenticatedUserGet(TestCase):
    def setUp(self):
        self.post_without_comments = mixer.blend(Post, title='Post 1', text='Text')
        self.post = mixer.blend(Post, title='Post 2', text='Text')
        self.comment_approved = mixer.blend(Comment, text='Comment 1', author='Author 1', post=self.post)
        self.comment_approved.approve()
        self.comment = mixer.blend(Comment, text='Comment 2', author='Author 2', post=self.post)

        self.resp = self.get('post_detail', pk=self.post.pk)

    def test_show_approved_comments_only(self):
        self.assertContains(self.resp, self.comment_approved.text)
        self.assertNotContains(self.resp, self.comment.text)

    def test_hide_action_post_links(self):
        links = [
            r('post_edit', pk=self.post.pk),
            r('post_remove', pk=self.post.pk)
        ]

        for link in links:
            with self.subTest():
                self.assertNotContains(self.resp, link)


class PostDetailNotFound(TestCase):
    def test_not_found(self):
        response = self.get('post_detail', pk=1)
        self.response_404(response)