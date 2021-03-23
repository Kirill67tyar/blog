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

    title = CharField(max_length=250, verbose_name='Название')#, primary_key=True)
    # unique_for_date - значит, что django будет предотвращать формирование одинаковых слагов
    # в одну и ту жу дату (в данном случае publish)
    slug = SlugField(max_length=250, unique_for_date= 'publish', verbose_name='URL_названия')
    author = ForeignKey(User, on_delete=CASCADE, related_name='blog_posts', verbose_name='Автор')
    body = TextField(verbose_name='Содержимое статьи')
    created = DateTimeField(auto_now_add=True, verbose_name='Создано')
    updated = DateTimeField(auto_now=True, verbose_name='Изменено')
    # timezone.now - возвращает текущую дату и время, но с учетом часового пояса
    # как datetime.now()
    publish = DateTimeField(default=timezone.now, verbose_name='Опубликовано')
    status = CharField(max_length=10, choices=STATUS_CHOICES, default='draft', verbose_name='Статус')
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ('-publish',)
        # db_table дает возможность задать свое имя таблицы (по умодчанию - blog_post (application_model))
        # db_table = 'blog_post_custom'
        # unique_together = 'title', 'slug',

    # если в поле модули указать primary_key=True, то это поле будет primary_key
    # по умолчанию primary_key - id



# консольная команда sqlmigrate application number_migration like
#     python manage.py sqlmigrate 0003
#     очень полезная команда. она не делает миграции в бд, и дает возможность посмотреть
#     какой sql запрос будет при миграции в бд. какой sql запрос для создания таблицы в бд
    """
    $ python manage.py sqlmigrate blog 0001
    BEGIN;
--
-- Create model Post
--
CREATE TABLE "blog_post_custom" ("title" varchar(250) NOT NULL PRIMARY KEY, "slug" varchar(250) NOT NULL, 
"body" text NOT NULL, "created" datetime NOT NULL, "updated" datetime NOT NULL, "publish" datetime NOT NULL,
"status" varchar(10) NOT NULL,
"author_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE INDEX "blog_post_custom_slug_95392f12" ON "blog_post_custom" ("slug");
CREATE INDEX "blog_post_custom_author_id_34d1c811" ON "blog_post_custom" ("author_id");
COMMIT;
    """