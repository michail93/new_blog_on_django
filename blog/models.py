from django.db import models

# Create your models here.

from django.utils import timezone
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django import forms
from taggit.managers import TaggableManager


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')



class Post(models.Model):
    STATUS_CHOICES=(
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title=models.CharField(max_length=250)
    slug=models.SlugField(max_length=250, unique_for_date='publish')
    author=models.ForeignKey(User, related_name='blog_posts')
    body=models.TextField()
    publish=models.DateTimeField(default=timezone.now)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    status=models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    tags=TaggableManager()

    class Meta:
        ordering=('-publish', )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail',
                       args=[self.publish.year,
                             self.publish.strftime('%m'),
                             self.publish.strftime('%d'),
                             self.slug])

    # если добавляются рукописные/custom менеджеры моделей,
    # то стандартный экземпляр objects модели Manager
    # нужно определять явно
    objects=models.Manager()
    # если "published=PublishedManager()" определить выше "objects=models.Manager()",
    # то в Django administration не будут отображаться объекты модели Post
    published=PublishedManager()



class EmailPostForm(forms.Form):
    name=forms.CharField(max_length=25)
    email=forms.EmailField()
    to=forms.EmailField()
    comments=forms.CharField(required=False,
                             widget=forms.Textarea)



class Comment(models.Model):
    post=models.ForeignKey(Post, related_name='comments')
    name=models.CharField(max_length=80)
    email=models.EmailField()
    body=models.TextField()
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    active=models.BooleanField(default=True)
    class Meta:
        ordering=('created',)
    def __str__(self):
        return 'Comment by {} on {}'.format(self.name, self.post)



class CommentForm(forms.ModelForm):
    class Meta:
        model=Comment
        fields=('name', 'email', 'body')
