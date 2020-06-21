from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView

from blog.forms import EmailPostForm, CommentForm
from blog.models import Post, Comment
from taggit.models import Tag


def post_list(request, tag_slug=None):
    object_list = Post.published.all()
    # 过滤与Tag相关的Post
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    paginator = Paginator(object_list, 3)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request,
                  'blog/post/list.html',
                  {'page': page,
                   'posts': posts,
                   'tag': tag
                   })


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'  # default variable is object_list
    paginate_by = 3
    template_name = 'blog/post/list.html'  # specify template
    object_list = Post.published.all()


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, status='published', publish__year=year, publish__month=month,
                             publish__day=day)
    # List of active comments for this post.注意：检索与本post相关的的comments
    comments = post.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':
        # A comment was posted:客户端提交了comment Form
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet.从comment Form中创建新的Comment对象
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment，为comment对象分配post
            new_comment.post = post
            # save the Comment to the database
            new_comment.save()

            # 注意：POST请求处理完成后必须redirect，否则用户刷新后会重复提交数据，原书作者代码有bug
            return redirect(post.get_absolute_url())
    else:  # 如果是GET请求就构建一个空的Comment传递给模板
        comment_form = CommentForm()
    return render(request,
                  'blog/post/detail.html',
                  {'post': post,
                   'comments': comments,
                   'new_comment': new_comment,
                   'comment_form': comment_form,
                   })


def post_share(request, post_id):
    # Retrieve post by id
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False
    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            # 发送邮件
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read {post.title}"
            message = f"Read {post.title} at {post_url} \n\n {cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'admin@myblog.com', [cd['to']])
            sent = True

            # ... send email
    else:  # 如果u不是POST请求，如是GET 请求，则构建一个空白的Form
        form = EmailPostForm()

    return render(request, 'blog/post/share.html', {'post': post, 'form': form, 'sent': sent})
