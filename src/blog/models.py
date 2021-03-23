from django.contrib.auth.models import User
from django.db.models import \
    (CharField, TextField, Model,
    DateTimeField, ForeignKey, SlugField, Manager, CASCADE)
from django.db import models
from django.utils import timezone



class PublishManager(Manager):

    def get_queryset(self):
        return super().get_queryset().filter(status='published')


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

    # мой кастомный менеджер - показывает и все фильтрует все опубликованные посты (status='published')
    # важный момент - при определении кастомного менеджера, если хочешь сохранить
    # и старый менеджер тоже, то необходимо его явно определять objects = Manager()
    objects = Manager()
    published = PublishManager()



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

# Важно, ORM Django совместима с SQLite, MySQL, PostgreSQL, Oracle.
# https://docs.djangoproject.com/en/3.1/ref/databases/
# В django можно настроить работу с несколькими СУБД одновременно


# Когда мы создаем объект модели - Post(author__id=1, title='re' ...)
# мы сохраняем этот объект в памяти. А вызывая метод save() у этого объекта
# мы делаем SQL запрос INSERT в бд, вот так то.
# ! НО, если мы измененм аттрибут экземпляра модели (какое-ниюудь поле), то метод save()
# вызовет SQL-выражение UPDATE
# Все изменения, которые мы делаем для объекта в памяти не вызываются до тех пор, пока
# не вызвовется метод save(). Работая с объектом через ORM мы работаем в памяти
# вызывая метод save(commit=True) мы делаем SQL-запрос INSERT или UPDATE
# Post.objects.all() - это SQL-запрос SELECT * FROM blog_post;
# но этот sql запрос будет выполняться не тогда, когда мы присвоим переменную,
# а тогда, когда мы ее явно вызовем. Когда делаем непосредственное обращение к элементам QuerySet
# это потому, что объекты запросов в django ленивые.
# метод delete() тоже вызовет SQL-запрос