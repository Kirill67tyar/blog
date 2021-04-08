from django.contrib.sitemaps import Sitemap
from blog.models import Post



class PostSitemap(Sitemap):

    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return Post.published.all()

    def lastmod(self, obj):
        return obj.updated

# этот наш класс по сути и представляет карту сайта
# changefreq - чатстота обновления страниц
# priority - степень их совпадения с тематикой сайта (максимально - 1). Хз че значит
# метод items() - будет отображать объекты, которые будут отображаться в тематике сайта
# скорее всего для этого метода, для объектов модели нужно определить get_absolute_url()

# Для своей карты сайта через django затрагиваем три файла:
# 1) settings.py - установка приложений 'django.contrib.sites','django.contrib.sitemaps',
# и поледующая миграция в db
# 2) sitemaps.py - создаем новый файл в приложении(!) реализуем класс выше (наследуемся от Sitemap)
# 3) urls.py (корневой) - делаем там специальный path для sitemap, смотри какой.

# Здесь конкретно для работы и настройки карты сайта на django:
# https://docs.djangoproject.com/en/3.1/ref/contrib/sitemaps/

# Также смотри книгу Django (Антонио Меле) 78 стр.

# Здесь вообще про карты сайта, что это такое:
# https://convertmonster.ru/blog/seo-blog/sitemap-xml-chto-takoe-karta-sajta-html/#:~:text=%D0%9A%D0%B0%D1%80%D1%82%D0%B0%20%D1%81%D0%B0%D0%B9%D1%82%D0%B0%20(sitemap)%20%E2%80%94%20%D1%8D%D1%82%D0%BE,%D0%BD%D0%B0%20%D0%B2%D1%81%D0%B5%20%D0%B2%D0%B0%D0%B6%D0%BD%D1%8B%D0%B5%20%D1%81%D1%82%D1%80%D0%B0%D0%BD%D0%B8%D1%86%D1%8B%20%D1%81%D0%B0%D0%B9%D1%82%D0%B0.
# так же гугли "карта сайта"



# ниже шаблон и разъяснение что такое карта сайта:
"""
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
 <url>
  <loc>http://mysite.ru/</loc>
  <lastmod>2014-09-18T18:54:13+04:00</lastmod>
  <changefreq>always</changefreq>
  <priority>1.0</priority>
 </url>
 <url>
  <loc>http://mysite.ru/category/</loc>
  <lastmod>2014-09-18T18:57:09+04:00</lastmod>
  <changefreq>hourly</changefreq>
  <priority>0.8</priority>
 </url>
 <url>
  <loc>http://mysite.ru/page/</loc>
  <lastmod>2014-09-18T18:59:37+04:00</lastmod>
  <changefreq>daily</changefreq>
  <priority>0.6</priority>
 </url>
</urlset>
Где используются следующие обязательные теги:

<urlset> — родительский тег, в него заключаются все url-адреса;
<url> — тег, в котором указываются сведения о конкретном url-адресе;
<loc> — в данном теге указывается непосредственно url.
Далее, следуют необязательные теги:

<lastmod> — этот тег заключает в себе дату последнего изменения страницы;
<changefreq> — тег используется, чтобы указать насколько часто изменяется страница: always, hourly, daily, weekly, monthly, yearly, never;
<priority> — указывает приоритет определенной страницы, относительно других страниц сайта от 0,1 – низкий приоритет, до 1 – высокий приоритет.
Так же, в файле карты сайта в формате xml должно содержаться указание на пространство имен языка XML:
xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
"""
