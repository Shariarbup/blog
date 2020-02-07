from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin # for checking ekta user logged on or not
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
# Create your views here.


#<app_name>/<model_name_lowercase>_<view_type_lowercase>.html
# ../blog/post_list.html
class PostListView(ListView):
    model = Post
    template_name = 'basic_app/home.html' 
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 2


#<app_name>/<model_name_lowercase>_<view_type_lowercase>.html
# ../blog/post_list.html
class UserPostListView(ListView):
    model = Post
    template_name = 'basic_app/home.html' 
    context_object_name = 'posts'
    paginate_by = 2

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


#<app_name>/<model_name_lowercase>_<view_type_lowercase>.html (For PostDetailView)
# ../blog/post_detail.html
class PostDetailView(DetailView):
    model = Post




#<app_name>/<model_name_lowercase>_form.html (For PostCreateView)
# ../blog/post_form.html
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user # form er author er moddhe, j user request korechilo shaei user chole gelo
        return super().form_valid(form)


# UserPassesTestMixin uses for ekjon author shudhu tar post e edit korte parbe
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user # form er author er moddhe, j user request korechilo shaei user chole gelo
        return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
#post_confirm_delete.html