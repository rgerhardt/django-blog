from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.http.response import JsonResponse
from django.contrib.auth.decorators import login_required
from blog.core.models import Post, Comment
from django.utils import timezone
from blog.core.forms import PostForm, CommentForm


from django.views import generic


from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin


class PostListView(generic.ListView):
    model = Post

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.published_posts().order_by('-published_at')
        return qs


class AboutView(generic.TemplateView):
    template_name = 'core/about.html'


class PostDetailView(generic.DetailView):
    model = Post


class PostUpdateView(LoginRequiredMixin, generic.UpdateView):
    form_class = PostForm
    model = Post


class PostDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Post
    success_url = reverse_lazy('post_list')


def add_comment_view(request, pk):
    post = get_object_or_404(Post, pk=pk)
    form = CommentForm()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()

            return redirect(comment.get_absolute_url())

    return render(
        request,
        'core/comment_form.html',
        context=dict(form=form, post=post)
    )

@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return JsonResponse({}, status=204)


@login_required
def comment_disapprove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.disapprove()
    return JsonResponse({}, status=204)


@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)


class NewPostView(LoginRequiredMixin, generic.CreateView):
    model = Post
    form_class = PostForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()

        return redirect(self.get_success_url())


class DraftListView(LoginRequiredMixin, generic.ListView):
    template_name = 'core/post_draft_list.html'

    def get_queryset(self):
        return Post.objects.unpublished_posts().order_by('created_date')