from django.conf.urls import url
from django.views.generic import TemplateView

from search import views

urlpatterns = [
    url(r'^proteinid/$',
        TemplateView.as_view(template_name='choice3.html'),
        name="search_by_pid_home"),

    url(r'^proteinid/result/$',
        views.display_3,
        name='search_by_pid_result'),

    url(r'^protein_seq/$',
        TemplateView.as_view(template_name='choice4.html'),
        name="search_by_pid_seq_home"),

    url(r'^protein_seq/result/$',
        views.display_4,
        name='search_by_pid_seq_result'),
]
