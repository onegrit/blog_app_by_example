from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView

from blog.models import Post


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'  # default variable is object_list
    paginate_by = 3
    template_name = 'blog/post/list.html'  # specify template
    object_list = Post.published.all()


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, status='published', publish__year=year, publish__month=month,
                             publish__day=day)

    return render(request, 'blog/post/detail.html', {'post': post})
