from django.template.defaultfilters import truncatewords
from django.contrib.syndication.views import Feed
from blog.models import Post


class LatestPostsFeed(Feed):
    title = 'Мой блог'
    link = '/blog/'
    description = 'Новые посты моего блога'

    def items(self):
        return Post.published.all()[:5]

    def item_title(self, item):
        return item.title


    def item_description(self, item):
        return truncatewords(item, 30)
