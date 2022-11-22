"""
Imports for the functionality of users views

"""

from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic, View
from django.views.generic.edit import UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect
from .models import Post, Category, Comment
from .forms import CommentForm


class PostList(generic.ListView):
    """ Views of the list of posts fields on the home page """
    model = Post
    queryset = Post.objects.filter(status=1).order_by('-date_added')
    paginate_by = 6
    template_name = 'index.html'


class PostDetail(View):
    """ Each individual detailed posts """
    def get(self, request, slug, *args, **kwargs):
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.filter(approved=True).order_by('-date_added')
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        return render(
            request,
            "post_detail.html",
            {
                "post": post,
                "comments": comments,
                "commented": False,
                "liked": liked,
                "comment_form": CommentForm()
            },
        )
    """ Relationship between the views and backend """
    def post(self, request, slug, *args, **kwargs):
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.filter(approved=True).order_by('-date_added')
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        comment_form = CommentForm(data=request.POST)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment_form.instance.name = request.user.username
            comment_form.instance.email = request.user.email
            comment.post = post
            comment.save()
        else:
            comment_form = CommentForm()

        return render(
            request,
            "post_detail.html",
            {
                "post": post,
                "comments": comments,
                "commented": True,
                "liked": liked,
                "comment_form": CommentForm()
            },
        )


def category(request, id):

    category = get_object_or_404(Category, pk=id)

    context = {
        'category': category,
        'posts': Post.objects.filter(category=category),
    }
    return render(request, 'category.html', context)


class LikePost(View):
    """ Like and unlike posts and redirect to same post """
    def post(self, request, slug):
        post = get_object_or_404(Post, slug=slug)

        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)

        return HttpResponseRedirect(reverse('post_detail', args=[slug]))


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """ Edit/Update option in the update_comment.html """
    model = Comment
    form_class = CommentForm
    template_name = 'update_comment.html'

    """ Restrict access of users to other users comments """
    def test_func(self):
        comment = self.get_object()
        print(self.request.user.username)
        print(comment.name)
        return self.request.user.username == comment.name

    """ Success url after edit for post """
    def get_success_url(self, **kwargs):
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=self.object.post.slug)
        return reverse('post_detail', args=[post.slug])


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """ Delete option in the delete_comment.html """
    model = Comment
    template_name = 'delete_comment.html'

    """ Restrict access of users to other users comments """
    def test_func(self):
        comment = self.get_object()
        print(self.request.user.username)
        print(comment.name)
        return self.request.user.username == comment.name       
    """ Success url after delete for post """
    def get_success_url(self, **kwargs):
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=self.object.post.slug)
        return reverse('post_detail', args=[post.slug])
