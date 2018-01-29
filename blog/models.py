from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.urls.base import reverse
from taggit.managers import TaggableManager


class Rash(models.Manager):
    def get_queryset(self):
        return super(Rash, self).get_queryset().filter(status='draft')


class Post(models.Model):
    objects = models.Manager()
    rash = Rash()
    Status_choice = (
        ('draft', 'Draft'),
        ('published', 'Published')
    )
    title = models.CharField(max_length=250, unique_for_date='publish')
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(choices=Status_choice, max_length=10, default='draft')
    tag = TaggableManager()

    class Meta:
        ordering = ['-publish']

    def get_absolute_url(self):
        return reverse('blog:detail', args=[self.publish.year,
                                            self.publish.strftime('%m'),
                                            self.publish.strftime('%d'),
                                            self.slug])

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created']

    def __str__(self):
        return 'Comment by {} on {}'.format(self.name, self.post)
