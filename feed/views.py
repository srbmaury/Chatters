from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.conf import settings
from django.urls import reverse
from django.shortcuts import render, redirect
from .models import post

# Create your views here.

class PostListView(LoginRequiredMixin, ListView):
    model = post
    template_name = 'feed/home.html'
    ordering = ['-datetime']


class PostCreateView(LoginRequiredMixin, CreateView):
    model = post
    fields = ['text']
    success_url = '/'

    def form_valid(self, form):
        form.instance.uname = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = post
    fields = ['text']
    success_url = '/'

    def form_valid(self, form):
        form.instance.uname = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.uname:
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.uname:
            return True
        return False

def show_profile(request, username):
    user = User.objects.get(username = username)
    posts_list = []
    for posts in post.objects.all():
        if posts.uname == user:
            posts_list.append(posts)
    posts_list.sort(key=lambda x: x.datetime, reverse=True)

    context = {
        'user': user,
        'posts_list': posts_list,
    }
    return render(request, 'accounts/show_profile.html', context)

def LikeView(request, pk):
    curr_post = get_object_or_404(post, id=request.POST.get('post_id'))
    if request.user in curr_post.likes.all():
        messages.error(request, 'You have already liked this post')
        return redirect(request.META['HTTP_REFERER'])
    else:
        curr_post.likes.add(request.user)
    curr_post.save()
    return redirect(request.META['HTTP_REFERER'])

