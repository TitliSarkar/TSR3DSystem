from django.conf.urls import url
from django.views.generic import TemplateView

from compare import views
from compare.views import CompareByProteinID


urlpatterns = [
    url(r'^proteinid/$',
        CompareByProteinID.as_view(),
        name="compare_by_pid_home"),

    url(r'^byprotienid/result/$',
        views.display_1,
        name='compare_by_pid_result'),

    url(r'^byhierarchy/$',
        TemplateView.as_view(template_name='choice2.html'),
        name="compare_by_hl_home"),

    url(r'^byhierarchy/result/$',
        views.display_2,
        name='compare_by_hl_result'),
]
