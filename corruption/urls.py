from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'corruption.views.home'),
    url(r'^(?P<case_id>\d+)/$', 'corruption.views.view_case'),
    
    #Admin
    url(r'^admin/$', 'corruption.views.admin'),
    url(r'^admin/(?P<case_id>\d+)/$', 'corruption.views.admin_view_case'),
    url(r'^admin/(?P<case_id>\d+)/delete/$', 'corruption.views.admin_del_case'),
    
    #Articles
    url(r'^admin/article/$', 'corruption.views.admin_article'),
    url(r'^admin/article/(?P<article_id>\d+)/$',
        'corruption.views.admin_view_article'),
    url(r'^admin/article/(?P<article_id>\d+)/delete/$',
        'corruption.views.admin_del_article'),
    
)