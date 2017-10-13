from django.conf.urls import url
from django.views.generic import TemplateView

from compare import views

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='general/compare.html')),
    url(r'^protienid/$', views.display_1, name='compare_by_pid'),
    url(r'^hierarchylevel/$', views.display_2, name='compare_by_hl'),
    url(r'^protienid/$', views.display_3, name='search_by_pid'),
]
