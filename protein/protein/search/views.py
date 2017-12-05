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
from itertools import combinations


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
        user_protein_list = ['1a06', '1muo']

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
        .values_list('Protein_ID_id', 'Protein_Key')

    sub_query_list = [entry for entry in sub_query]
    d = {}
    cnt = Counter(elem[0] for elem in sub_query_list)
    for key, value in cnt.items():
        d[key] = value

    pro_list = filter(lambda x: x[1] >= len(protein_key_list), d.items())

    proteins = []
    for i in range(len(pro_list)):
        proteins.append(pro_list[i][0])

    if not pro_list:
        proteins = user_protein_list

    context['common_keys'] = protein_key_list
    context['proteins'] = proteins
    context['protein_key_list'] = protein_key_list
    end = time.clock()
    context['time'] = round(end - start, 4)

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
        seq_list = request.POST.getlist("list4_1")
        pid = request.POST.get('pid', '1a06')
        context['pid'] = pid
        context['seq_list'] = seq_list
        pos_list = list(combinations(seq_list, 3))

        if "small_table" in request.POST:
            all_proteins_table = ALL_PROTEINS
        elif "big_indexed_table" in request.POST:
            all_proteins_table = ALL_PROTEINS_BIG
        elif "big_unindexed_table" in request.POST:
            all_proteins_table = ALL_PROTEINS_BIG_UNINDEXED
        else:
            all_proteins_table = ALL_PROTEINS

        pid_rows = all_proteins_table.objects.filter(Protein_ID_id=pid)

        key_list = []
        for positions in pos_list:
            protein_keys = pid_rows.filter(
                Q(position0__in=list(positions))
                & Q(position1__in=list(positions))
                & Q(position2__in=list(positions)))\
                .distinct()\
                .values('Protein_Key')

            for key in protein_keys:
                key_list.append(key['Protein_Key'])

        protein_key_list = set(key_list)

        sub_query = []
        for key in protein_key_list:
            row_val = all_proteins_table.objects.filter(
                Protein_Key=str(key))\
                .distinct()\
                .values('Protein_ID_id')\
                .order_by('Protein_ID_id')
            sub_query.append(row_val)

        sub_query_list = []
        for queryset in sub_query:
            for l in queryset:
                sub_query_list.append(str(l.get('Protein_ID_id')))

        d = {}
        cnt = Counter(elem for elem in sub_query_list)
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
