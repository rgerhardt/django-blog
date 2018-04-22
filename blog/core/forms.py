from django import forms

from .models import Post, Comment


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'summary', 'text',)

        widgets = {
            'title': forms.TextInput(),
            'text': forms.Textarea(),
            'summary': forms.Textarea(attrs=dict(rows=2)),
        }


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('author', 'text',)

        widgets = {
            'author': forms.TextInput(),
            'text': forms.Textarea(),
        }
