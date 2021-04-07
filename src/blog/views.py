from django.conf import settings
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Count
from django.shortcuts import render, HttpResponse, get_object_or_404
from django.views import View
from django.views.generic import ListView
from django.core.mail import send_mail
from blog.models import Post, Comment, Tag
from blog.forms import EmailPostForm, CommentForm


def experiments(request):
    obj = get_object_or_404(Post, id=1)
    post_url = request.build_absolute_uri(obj.get_absolute_url())
    # # 1 ----------------------------------------------------------------
    # print(f'\n\n--------------------------------------------\n'
    #       f'request.build_absolute_uri(obj.get_absolute_url() = {post_url}\n'
    #       f'obj.get_absolute_url() = {obj.get_absolute_url()}\n'
    #       f'path = {request.path}\n'
    #       f'path_info = {request.path_info}\n'
    #       f'get_host = {request.get_host()}\n'
    #       f'get_full_path_info = {request.get_full_path_info()}\n'
    #       f'get_full_path = {request.get_full_path()}\n'
    #       f'---------------------------------------------\n\n')
    # #  ----------------------------------------------------------------
    # # 2 ----------------------------------------------------------------
    # print('\n\n--------------------------------------------\n',
    #       *dir(request),
    #       '---------------------------------------------\n\n',sep='\n')
    # # 3 ----------------------------------------------------------------
    # print('\n\n--------------------------------------------\n',
    #       request.method,
    #       request.get_port,
    #       request.get_raw_uri(),
    #       request.headers,
    #       request.body,
    #       '---------------------------------------------\n\n',sep='\n')
    return HttpResponse('Check console')


def concat_and_send_email(request, post, data):
    """
        Функция ответственна за конкатенацию и отправку сообщения
        возвращает True
        принимает 3 аргумента где:
            request - HTTP request с методом post
            post - экземпляр модели Post
            data - cleaned_data
    """
    username = request.user.username
    post_url = request.build_absolute_uri(post.get_absolute_url())
    title = f'{username} ({data["email"]}) recommends you reading {post.title}'
    body = f'Read {post.title} at {post_url} \n\n {username}\'s comments:\n {data["comments"]}'
    # send_mail(title, body, settings.EMAIL_HOST_USER, [data['to']])
    sent = True
    return sent



def post_list(request, tag_slug=None):
    qs = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        qs = tag.posts.annotate(count_posts=Count('title')).all()
    paginator = Paginator(qs, 2)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    nothing = f"По тегу \"{tag}\" ничего не найдено"
    something = f"По тегу \"{tag}\" найдено {qs.count()} постов"
    report = f'{something if qs.count() else nothing}'
    context = {
        'page_obj': page_obj,
        'tag': tag,
        'report': report,
    }
    return render(request, 'blog/list.html', context=context)


def post_retrieve(request, year, month, day, slug):
    kwargs = {
        'publish__year': year,
        'publish__month': month,
        'publish__day': day,
        'slug': slug,
    }
    obj = get_object_or_404(Post.published, **kwargs)
    comments = obj.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = obj
            new_comment.save()
    else:
        comment_form = CommentForm()

    # Здесь мы реализуем рекоммендуемые статьи, по статьям по одинаковым тегам ------
    post_tags_ids = obj.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=obj.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags'))
    # здеь мы сортируем статьи по количеству тегов и берем первые 4 статьи
    similar_posts = similar_posts.order_by('-same_tags', '-publish')[:4]
    # Здесь мы реализуем рекоммендуемые статьи, по статьям по одинаковым тегам ------


    context = {
        'obj': obj,
        'comments': comments,
        # 'new_comment': new_comment,
        'comment_form': comment_form,
        'similar_posts': similar_posts,
    }
    return render(request, 'blog/retrieve.html', context=context)

# send_mail('check',
# "I'm checking sending messages from kirillbogomolov.ric@gmail.com",
# 'kirillbogomolov.ric@gmail.com',
# ['kirillbogomolov.ric@gmail.com', 'kirillbogomolov.ric@yandex.ru',],
# fail_silently=False)

    # если мы введем некорректные данные (не число) в get параметр ?page= то
    # пагинатор перейдет на первую страницы
    # если мы примем в get параметр (query string) число большее, чем страниц у нас есть -
    # то попадем на последнюю страницу
    # все это благодаря тому, что мы используем метод get_page()
    # но можно использовать метод page() и нам придется вручную отлавливать PageNotAnInteger и EmptyPage


def post_share(request, post_id):
    """
        обратоботчик принимающий post и get запросы для отправки
        вызывает функцию concat_and_send_email(request, post, data)
        где post - экземпляр модели Post
        data - cleaned_data
    """

    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False
    # print('\n\n--------------------------------------------\n',
    #       request.method,
    #       request.get_port,
    #       request.get_raw_uri(),
    #       request.headers,
    #       request.body,
    #       '---------------------------------------------\n\n',sep='\n')
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            sent = concat_and_send_email(request=request, post=post, data=data)


    # elif request.method == 'GET':
    else:
        form = EmailPostForm()
    context = {
        'form': form,
        'sent': sent,
        'post': post,
    }
    return render(request, 'blog/share.html', context=context)




class PostListView(ListView):

    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 2
    template_name = 'blog/list.html'
