import markdown
from django.db.models import Q
from markdown.extensions.toc import TocExtension
from django.utils.text import slugify
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post,Category,Tag
from django.views.generic import  ListView,DetailView
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from pure_pagination import *
from django.contrib import messages
import re

def search(request):
    q = request.GET.get('q')
    if not q:
        error_msg = "请输入关键词"
        messages.add_message(request,messages.ERROR,error_msg,extra_tags='danger')
        return redirect('blog:index')

    post_list = Post.objects.filter(Q(title__icontains=q) | Q(body__icontains=q))
    return render(request,'blog/index.html',{'post_list' : post_list})

class IndexView(PaginationMixin,ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    #指定paginate_by属性后开启分页功能其值代表每一页包含多少篇文章
    paginate_by = 10

class ArchiveView(PaginationMixin,ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'

    #指定paginate_by属性后开启分页功能其值代表每一页包含多少篇文章
    paginate_by = 10

    def get_queryset(self):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        return super(ArchiveView,self).get_queryset().filter(created_time__year=year,created_time__month=month)

class CategoryView(PaginationMixin,ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'

    #指定paginate_by属性后开启分页功能其值代表每一页包含多少篇文章
    paginate_by = 10

    def get_queryset(self):
        cate = get_object_or_404(Category,pk = self.kwargs.get('pk'))
        return super(CategoryView,self).get_queryset().filter(category=cate)

class TagView(PaginationMixin,ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'

    #指定paginate_by属性后开启分页功能其值代表每一页包含多少篇文章
    paginate_by = 10

    def get_queryset(self):
        tag = get_object_or_404(Tag,pk = self.kwargs.get('pk'))
        return super(TagView,self).get_queryset().filter(tags=tag)

class PostDetailView(DetailView):
    # 这些属性的含义和 ListView 是一样的
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'



    def get(self,request,*args,**kwargs):
        # 覆写 get 方法的目的是因为每当文章被访问一次，就得将文章阅读量 +1
        # get 方法返回的是一个 HttpResponse 实例
        # 之所以需要先调用父类的 get 方法，是因为只有当 get 方法被调用后，
        # 才有 self.object 属性，其值为 Post 模型实例，即被访问的文章 post
        response = super(PostDetailView,self).get(request,*args,**kwargs)

        # 将文章阅读量 +1
        # 注意 self.object 的值就是被访问的文章 post
        self.object.increase_views()

        # 视图必须返回一个 HttpResponse 对象
        return response


