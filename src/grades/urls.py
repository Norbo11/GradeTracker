from django.conf.urls import patterns, url
from django.views.generic.base import RedirectView

from grades import views
from grades.forms import LoginForm


urlpatterns = patterns('',
    url(r'^$', RedirectView.as_view(url='home/', permanent=True)),
    url(r'^home/$', views.HomeView.as_view()),
    url(r'^subjects/$', views.SubjectListView.as_view()),
    url(r'^subjects/delete/(?P<subject_id>[0-9]+)$', views.SubjectDeleteView.as_view()),

    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'grades/login.html', 'authentication_form': LoginForm}),
    url(r'^logout/$', 'django.contrib.auth.views.logout_then_login'),
    url(r'^register/$', views.RegisterView.as_view()),
)