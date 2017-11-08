from django.conf.urls import url

from compare import views
from compare.views import CompareByProteinID
from compare.views import CompareByHierarchy


urlpatterns = [
    url(r'^proteinid/$',
        CompareByProteinID.as_view(),
        name="compare_by_pid_home"),

    url(r'^byprotienid/result/$',
        views.display_1,
        name='compare_by_pid_result'),

    url(r'^byhierarchy/$',
        CompareByHierarchy.as_view(),
        name="compare_by_hl_home"),

    url(r'^byhierarchy/result/$',
        views.display_2,
        name='compare_by_hl_result'),
]
