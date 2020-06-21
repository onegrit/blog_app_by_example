from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone
from taggit.managers import TaggableManager


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')


class Post(models.Model):
    STATUS_CHOICE = (
        ('draft', 'Draft'),
        ('published', 'Published')
    )
    title = models.CharField(max_length=250)
    """
        You have added the unique_for_date parameter to this field so that you can build URLs for posts using there
        publish date and slug. Django will prevent multiple posts from having the same slug for a given date.
    """
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    """
        This field defines a many-to-many relationship, meaning that each post is written by a user, and a user can write
        any number of posts. The on_delete parameter specifies the behavior to adopt when  referenced object is deleted. 
        当被引用的对象-user被删除时，数据库会删除所有与该User相关的posts
        此外，使用related_name还指定了反向关系（user-post）的名字，当从1端(User）访问post时，默认是user对象.post_set，指定related_name
        后，使用blog_posts替代了默认的post_set QuerySet名称
    """
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    body = models.TextField()
    # This datetime indicates when the post was published.
    publish = models.DateTimeField(default=timezone.now)
    # 创建时间：每次新建一个对象时，会自动添加时间戳
    created = models.DateTimeField(auto_now_add=True)
    # 更新时间： 帖子最后一次更新时间，当保存一个对象时，会自动更新时间戳
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICE, default='draft')
    tags = TaggableManager()
    """
    添加自定义manager前，需要显示地声明默认manager是谁
    """
    objects = models.Manager()  # The default manager
    published = PublishedManager()  # Our custom manager.

    class Meta:
        ordering = ['-publish']  # 降序排序：日期由近及远

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.publish.year, self.publish.month, self.publish.day, self.slug])


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'
