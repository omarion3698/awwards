from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import ProjectCreateView,ProjectListView,ProjectDetailView,UserProjectListView

urlpatterns=[
    url(r'^welcome$', views.welcome, name = 'awwards-welcome'),
    url(r'^$', views.home, name = 'home'),
    url(r'^review/(\d+)/$',views.review,name='review'),
    url(r'^rate/(\d+)/$',views.rate,name='rate'),
    url(r'^accounts/profile/$', views.profile, name = 'profile'),
    url(r'^api/profiles/$', views.ProfilesList.as_view()),
    url(r'^api/profile/profile-id/(?P<pk>[0-9]+)/$',views.ProfileDescription.as_view()),
    url(r'^api/projects/$', views.ProjectsList.as_view()),
    url(r'^api/project/project-id/(?P<pk>[0-9]+)/$',views.ProjectDescription.as_view()),
    url(r'^project/list$', ProjectListView.as_view(), name = 'awwards-home'),
    url(r'^project/new/$',ProjectCreateView.as_view(), name='project-create'),
    url(r'^user/(?P<username>\w+)/$', UserProjectListView.as_view(), name='user-projects'),
    url(r'^project/(?P<pk>\d+)/$',ProjectDetailView.as_view(), name='project-detail'),
    url(r'^search/', views.search_results, name='search_results'),
    url(r'^project/(?P<pk>\d+)/rating', views.rating, name='awwards-rating'),
]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
