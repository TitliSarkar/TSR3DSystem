from django.conf.urls import url
from django.views.generic import TemplateView

from compare import views

urlpatterns = [
    url(r'^proteinid/$',
        TemplateView.as_view(template_name='choice1.html'),
        name="compare_by_pid_home"),
    url(r'^byprotienid/result/$',
        views.display_1,
        name='compare_by_pid_result'),

    url(r'^proteinid/$',
        TemplateView.as_view(template_name='choice2.html'),
        name="compare_by_hl_home"),
    url(r'^byhierarchy/result/$',
        views.display_2,
        name='compare_by_hl_result'),

    url(r'^search_keys/proteinid/$',
        TemplateView.as_view(template_name='choice3.html'),
        name="search_by_pid_home"),
    url(r'^search_keys/proteinid/result/$',
        views.display_3,
        name='search_by_pid_result'),

    url(r'^search_keys/protein_seq/$',
        TemplateView.as_view(template_name='choice4.html'),
        name="search_by_pid_seq_home"),
    url(r'^search_keys/protein_seq/result/$',
        views.display_4,
        name='search_by_pid_seq_result'),
]
