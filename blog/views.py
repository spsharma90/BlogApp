from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import Posts
from django.conf import settings
from django.views.generic import (
    ListView, 
    DetailView, 
    CreateView,
    UpdateView,
    DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

# posts= [
#     {
#         'author': 'CoreyMS',
#         'title': 'Blog Post 1',
#         'content': 'First post content',
#         'date_posted': 'August 27,2018'
#     },
#     {
#         'author': 'John Doe',
#         'title': 'Blog Post 2',
#         'content': 'Second post content',
#         'date_posted': 'September 30,2018'
#     }
# ]

# Function based view logic

# def home(request):
#     # context= {
#     #     'posts': posts
#     # }
#     PostsList = Posts.objects.all()

#     return render(request,'blog/home.html',{'posts':PostsList})

def print_settings(request):
    specific_settings = ['STATIC_ROOT', 'STATIC_URL', 'MEDIA_ROOT', 'MEDIA_URL']
    
    settings_dict = {}

    # Loop through each specific setting and get its value
    for name in specific_settings:
        settings_dict[name] = getattr(settings, name, 'Not Found')  # Use 'Not Found' if the setting is missing


    # Pass the list to the template and render it
    return render(request, 'blog/print.html', {'data': settings_dict})
    
# Class based view logic

class PostListView(ListView):
    model = Posts
    # default view name  <app>/<model>_<viewtype>.html
    template_name = 'blog/home.html'   
    context_object_name = 'posts' 
    ordering = ['-date_posted']
    paginate_by = 5

class UserPostListView(ListView):
    model = Posts
    # default view name  <app>/<model>_<viewtype>.html
    template_name = 'blog/user_posts.html'   
    context_object_name = 'posts' 
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User,username=self.kwargs.get('username'))
        return Posts.objects.filter(author=user).order_by('-date_posted')

class PostDetailView(DetailView):
    model = Posts
    
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Posts
    fields = ['title','content']
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form) 

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Posts
    fields = ['title','content']
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin,DeleteView):
    model = Posts
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

def about(request):
    return render(request,'blog/about.html',{'title':'About'})
