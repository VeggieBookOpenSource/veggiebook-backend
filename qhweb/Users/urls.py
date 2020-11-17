from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin

admin.autodiscover()
from qhmobile import views

urlpatterns = patterns('',
                       # Examples:
                       url(r'^qhmobile/', include('qhmobile.urls')),

                       url(r'^admin/qhmobile/recipe/preview/(?P<id>\d+)/(?P<language>\w\w)/$', views.getRecipe,
                           name='getRecipe'),
                       url(r'^admin/qhmobile/recipe/mobilePreview/(?P<language>\w\w)/(?P<id>\d+)/$',
                           views.previewMobileRecipe),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^support/$', views.support_page),
                       url(r'^privacyPolicy/$', views.privacy_policy)

                       )
