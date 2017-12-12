# -*- coding: utf-8 -*-
from django.conf.urls import url

from search import views
from search.views import SearchByProteinID
from search.views import SearchByProteinIDAndSeq
from search.views import SearchProteinKey


urlpatterns = [
    url(r'^proteinid/$',
        SearchByProteinID.as_view(),
        name="search_by_pid_home"),

    url(r'^proteinid/result/$',
        views.search_by_protein_id,
        name='search_by_pid_result'),

    url(r'^proteinid-seq/$',
        SearchByProteinIDAndSeq.as_view(),
        name="search_by_pid_seq_home"),

    url(r'^protenid-seq/seq/result/$',
        views.search_by_protein_id_seq_step2,
        name='search_by_pid_seq_search_result'),

    url(r'^proteinkey/(?P<pk>[0-9]+)/$',
        SearchProteinKey.as_view(),
        name="search_protein_key"),
]
