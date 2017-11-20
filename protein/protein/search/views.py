# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.db.models.aggregates import Count
from django.db.models import Q
from django.views.generic.list import ListView

from compare.models import ALL_PROTEINS
from compare.models import POSITION_INFORMATION
from compare.models import PROTEIN_HIERARCHY

import time


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
    protein_keys_list = []
    protein_keys_dict = {}
    user_protein_list = request.POST.getlist("list3")
    context['protein_list'] = user_protein_list

    protein_key_queryset = ALL_PROTEINS.objects.filter(
        Protein_ID_id__in=user_protein_list)\
        .distinct()\
        .values('Protein_Key')\
        .annotate(key_count=Count('Protein_Key'))\
        .filter(key_count__gte=len(user_protein_list))\
        .order_by('Protein_Key')

    for query in protein_key_queryset:
        protein_keys_list.append(query.get('Protein_Key'))

    for key in protein_keys_list:
        qs_desc_list = []
        for prot in user_protein_list:
            qs_desc_list.append(ALL_PROTEINS.objects.filter(
                Q(Protein_Key=str(key))
                & Q(Protein_ID_id=str(prot)))
                .order_by('Protein_ID_id', 'Key_coourence_no'))
        protein_keys_dict[str(key)] = qs_desc_list

    end = time.clock()
    context['time'] = round(end - start, 4)
    context['protein_keys_list'] = protein_keys_list
    context['protein_keys_dict'] = protein_keys_dict

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

    return render(request, 'search_by_pid_seq_search.html', context)


def search_by_protein_id_seq_step2(request):
    start = time.clock()
    context = {}
    if request.method == 'POST':
        protein_key_list = []
        pid_list = []
        protein_keys_dict = {}
        seq_list = request.POST.getlist("list4_1")
        context['seq_list'] = seq_list

        pos_info_queryset = POSITION_INFORMATION.objects.filter(
            Seq_ID__in=seq_list)\
            .distinct().values('Protein_ID').order_by('Protein_ID')

        for dict in pos_info_queryset:
            pid_list.append(dict.get('Protein_ID'))

        all_proteins_queryset = ALL_PROTEINS.objects.filter(
            Protein_ID_id__in=pid_list)\
            .distinct()\
            .values('Protein_Key')\
            .order_by('Protein_Key')\
            .distinct()

        for dict in all_proteins_queryset:
            protein_key_list.append(dict.get('Protein_Key'))

        for key in protein_key_list:
            protein_keys_dict[str(key)] = ALL_PROTEINS.objects.filter(
                Q(Protein_Key=str(key)))\
                .order_by('Protein_ID_id', 'Key_coourence_no')

        context['protein_keys_list'] = protein_key_list
        context['protein_keys_dict'] = protein_keys_dict

    end = time.clock()
    context['time'] = round(end - start, 4)
    return render(request, 'search_by_pid_seq_search_result.html', context)
