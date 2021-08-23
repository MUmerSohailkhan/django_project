from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from .models import post
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.contrib.auth.models import User


# Create your views here.


def home(request):
    context={
        'posts':post.objects.all()
    }
    return render(request,'blog/home.html',context)


class postlistview(ListView):
    model=post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 3

class Userpostlistview(ListView):
    model=post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    paginate_by = 3

    def get_queryset(self):
        user=get_object_or_404(User,username=self.kwargs.get('username'))
        return post.objects.filter(author=user).order_by('-date-posted')

class postdetailview(DetailView):
    model=post
    template_name = 'blog/post_detail.html'


class postdeleteview(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model=post
    success_url = '/blog'

    def test_func(self):
        post=self.get_object()
        if self.request.user == post.author:
            return True
        return False

class postcreateview(LoginRequiredMixin,CreateView):
    model=post
    fields = ['title','content']
    def form_valid(self, form):
        form.instance.author=self.request.user
        return super().form_valid(form)


class postupdateview(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model=post
    fields = ['title','content']
    def form_valid(self, form):
        form.instance.author=self.request.user
        return super().form_valid(form)

    def test_func(self):
        post=self.get_object()
        if self.request.user == post.author:
            return True
        return False

def about(request):
    return render(request,'blog/about.html',{'title':'about'})