# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.db.models.aggregates import Count
from django.db.models import Q
from django.views.generic.list import ListView

from compare.models import ALL_PROTEINS, ALL_PROTEINS_BIG
from compare.models import ALL_PROTEINS_BIG_UNINDEXED
from compare.models import POSITION_INFORMATION
from compare.models import PROTEIN_HIERARCHY

import time
from collections import Counter


class SearchByProteinID(ListView):
    model = PROTEIN_HIERARCHY
    template_name = 'search_by_pid_home.html'


def search_by_protein_id(request):
    """
    Input: A set of protein ids
    Output: Commom keys, by clicking on each keys, displays
    list of all protein_ids having it and other details too
    """
    start = time.clock()
    context = {}
    protein_key_list = []
    user_protein_list = request.POST.getlist("list3")

    if not user_protein_list and "small_table" in request.POST:
        user_protein_list = ['1a06', '1cdk', '1muo', '2src']

    context['protein_list'] = user_protein_list

    if "small_table" in request.POST:
        all_proteins_table = ALL_PROTEINS
    elif "big_indexed_table" in request.POST:
        all_proteins_table = ALL_PROTEINS_BIG
    elif "big_unindexed_table" in request.POST:
        all_proteins_table = ALL_PROTEINS_BIG_UNINDEXED
    else:
        all_proteins_table = ALL_PROTEINS

    protein_key_queryset = all_proteins_table.objects.filter(
        Protein_ID_id__in=user_protein_list)\
        .distinct()\
        .values('Protein_Key')\
        .annotate(key_count=Count('Protein_Key'))\
        .filter(key_count__gte=len(user_protein_list))\
        .order_by('Protein_Key')

    for query in protein_key_queryset:
        protein_key_list.append(query.get('Protein_Key'))

    sub_query = all_proteins_table.objects.filter(
        Protein_Key__in=protein_key_list)\
        .distinct()\
        .values_list('Protein_ID', 'Protein_Key')

    sub_query_list = [entry for entry in sub_query]

    d = {}
    cnt = Counter(elem[0] for elem in sub_query_list)
    for key, value in cnt.items():
        d[key] = value

    pro_list = filter(lambda x: x[1] >= len(protein_key_list), d.items())
    proteins = []
    for i in range(len(pro_list)):
        proteins.append(pro_list[i][0])

    end = time.clock()
    context['time'] = round(end - start, 4)
    context['common_keys'] = protein_key_list
    context['proteins'] = proteins
    context['protein_key_list'] = protein_key_list

    return render(request, 'search_by_pid_result.html', context)


class SearchByProteinIDAndSeq(ListView):
    model = PROTEIN_HIERARCHY
    template_name = "search_by_pid_seq_home.html"


def search_by_protein_id_seq_step1(request):
    context = {}
    if request.method == 'POST':
        pid = request.POST.get("list4")
        seq_id_queryset = POSITION_INFORMATION.objects.filter(
            Q(Protein_ID=str(pid)))\
            .values('Seq_ID')
        context['seq_list'] = seq_id_queryset
        context['pid'] = pid

    return render(request, 'search_by_pid_seq_search.html', context)


def search_by_protein_id_seq_step2(request):
    start = time.clock()
    context = {}
    if request.method == 'POST':
        protein_key_list = []
        pid_list = []
        seq_list = request.POST.getlist("list4_1")
        context['pid'] = request.POST.get('pid', '1a06')
        context['seq_list'] = seq_list

        pos_info_queryset = POSITION_INFORMATION.objects.filter(
            Seq_ID__in=seq_list)\
            .distinct().values('Protein_ID').order_by('Protein_ID')

        for dict in pos_info_queryset:
            pid_list.append(dict.get('Protein_ID'))

        if "small_table" in request.POST:
            all_proteins_table = ALL_PROTEINS
        elif "big_indexed_table" in request.POST:
            all_proteins_table = ALL_PROTEINS_BIG
        elif "big_unindexed_table" in request.POST:
            all_proteins_table = ALL_PROTEINS_BIG_UNINDEXED
        else:
            all_proteins_table = ALL_PROTEINS

        all_proteins_queryset = all_proteins_table.objects.filter(
            Protein_ID_id__in=pid_list)\
            .distinct()\
            .values('Protein_Key')\
            .order_by('Protein_Key')\
            .distinct()

        for dict in all_proteins_queryset:
            protein_key_list.append(int(dict.get('Protein_Key')))

        sub_query = all_proteins_table.objects.filter(
            Protein_Key__in=protein_key_list)\
            .distinct()\
            .values_list('Protein_ID', 'Protein_Key')

        sub_query_list = [entry for entry in sub_query]

        d = {}
        cnt = Counter(elem[0] for elem in sub_query_list)
        for key, value in cnt.items():
            d[key] = value

        pro_list = filter(lambda x: x[1] >= len(protein_key_list), d.items())
        proteins = []
        for i in range(len(pro_list)):
            proteins.append(pro_list[i][0])

        context['common_keys'] = protein_key_list
        context['proteins'] = proteins
        context['protein_keys_list'] = protein_key_list
    end = time.clock()
    context['time'] = round(end - start, 4)
    return render(request, 'search_by_pid_seq_search_result.html', context)
