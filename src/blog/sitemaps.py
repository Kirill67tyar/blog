from django.contrib.sitemaps import Sitemap
from blog.models import Post



class PostSitemap(Sitemap):

    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return Post.published.all()

    def lastmod(self, obj):
        return obj.updated

# этот наш сайт по сути и представляет карту сайта
# changefreq - чатстота обновления страниц
# priority - степень их совпадения с тематикой сайта (максимально - 1). Хз че значит
# метод items() - будет отображать объекты, которые будут отображаться в тематике сайта
# скорее всего для этого метода, для объектов модели нужно определить get_absolute_url()

# Здесь вообще про карты сайта, то это такое:
# https://convertmonster.ru/blog/seo-blog/sitemap-xml-chto-takoe-karta-sajta-html/#:~:text=%D0%9A%D0%B0%D1%80%D1%82%D0%B0%20%D1%81%D0%B0%D0%B9%D1%82%D0%B0%20(sitemap)%20%E2%80%94%20%D1%8D%D1%82%D0%BE,%D0%BD%D0%B0%20%D0%B2%D1%81%D0%B5%20%D0%B2%D0%B0%D0%B6%D0%BD%D1%8B%D0%B5%20%D1%81%D1%82%D1%80%D0%B0%D0%BD%D0%B8%D1%86%D1%8B%20%D1%81%D0%B0%D0%B9%D1%82%D0%B0.
# так же гугли "карта сайта"

# Здесь конкретно в для работы и настройки карты сайта на django:
# https://docs.djangoproject.com/en/3.1/ref/contrib/sitemaps/