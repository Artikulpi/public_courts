from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'account.views.profile'),
    url(r'^admin/$', 'account.views.admin'),
    url(r'^admin/new/$', 'account.views.new'),
    url(r'^admin/(?P<user_id>\d+)/$', 'account.views.view_account'),
    url(r'^admin/(?P<user_id>\d+)/delete/$', 'account.views.delete_account'),
    url(r'^admin/(?P<user_id>\d+)/password/$', 'account.views.change_password'),
    
    url(r'^register/$', 'account.views.register'),
    url(r'^register/success/$', 'account.views.register_success'),
    url(r'^confirm/(?P<username>\w+)/(?P<token>[a-f0-9]+)/$',
            'account.views.confirm'),
    
    url(r'^login/$', 'django.contrib.auth.views.login',
            {'template_name': 'account/login.html'}),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    url(r'^profile/$', 'account.views.profile'),
    url(r'^profile/edit/$', 'account.views.profile_edit'),
)
