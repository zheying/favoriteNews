from django.conf.urls import patterns, include, url
# from django.contrib import admin
import settings
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'favoriteNews.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # url(r'^admin/', include(admin.site.urls)),

    url(r'^login/', 'server.views.login', name='login'),
    url(r'^news/', 'server.views.getNews', name='getNews'),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.STATICFILES_DIRS, 'show_indexes': True}),
    url(r'^view_news/(?P<news_id>\d+)/$', 'server.views.viewNews', name='viewNews')
)
