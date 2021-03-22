from django.contrib.auth.models import User
from django.db.models import \
    (CharField, TextField, Model,
    DateTimeField, ForeignKey, SlugField, CASCADE)
from django.db import models
from django.utils import timezone



class Post(Model):
    
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    title = CharField(max_length=250, verbose_name='Название')
    slug = SlugField(max_length=250, unique_for_date= 'publish', verbose_name='URL_названия')
    author = ForeignKey(User, on_delete=CASCADE, related_name='blog_posts', verbose_name='Автор')
    body = TextField(verbose_name='Содержимое статьи')
    created = DateTimeField(auto_now_add=True, verbose_name='Создано')
    updated = DateTimeField(auto_now=True, verbose_name='Изменено')
    publish = DateTimeField(default=timezone.now, verbose_name='Опубликовано')
    status = CharField(max_length=10, choices=STATUS_CHOICES, default='draft', verbose_name='Статус')
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ('-publish',)
        # unique_together = 'title', 'slug',