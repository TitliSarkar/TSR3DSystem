# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.db.models.aggregates import Count
from django.db.models import Q
from django.views.generic.list import ListView

from compare.models import ALL_PROTEINS
from compare.models import POSITION_INFORMATION
from compare.models import PROTEIN_HIERARCHY


class SearchByProteinID(ListView):
    model = PROTEIN_HIERARCHY
    template_name = 'choice3.html'


def display_3(request):
    """
    Input: A set of protein ids
    Output: Commom keys, by clicking on each keys, show list of all protein_ids
    having it and other details too
    """
    context = {}
    s = request.POST.getlist("list3")
    context['s'] = s
    qs = ALL_PROTEINS.objects.filter(Protein_ID_id__in=s) \
        .distinct()\
        .values('Protein_Key')\
        .annotate(key_count=Count('Protein_Key')) \
        .filter(key_count__gte=len(s)) \
        .order_by('Protein_Key')

    db_rows = []
    for dict in qs:
        db_rows.append(dict.get('Protein_Key'))
    context['i'] = db_rows
    keys_dict = {}
    for key in db_rows:
        qs_desc_list = []
        for prot in s:
            qs_desc_list.append(ALL_PROTEINS.objects.filter(
                Q(Protein_Key=str(key)) &
                Q(Protein_ID_id=str(prot)))
                .order_by('Protein_ID_id', 'Key_coourence_no'))
        keys_dict[str(key)] = qs_desc_list

    context['j'] = keys_dict
    print(context['j'])
    return render(request, 'response1.html', context)


class SearchByProteinIDAndSeq(ListView):
    model = PROTEIN_HIERARCHY
    template_name = "choice4.html"


def display_4_step1(request):
    context = {}
    if request.method == 'POST':
        pid = request.POST.get("list4")
        seq_id_queryset = POSITION_INFORMATION.objects.filter(
            Q(Protein_ID=str(pid))).values('Seq_ID')
        context['i'] = seq_id_queryset
    return render(request, 'choice4_1.html', context)


def display_4_step2(request):
    context = {}
    if request.method == 'POST':
        seq_list = request.POST.getlist("list4_1")
        context['seq_list'] = seq_list
        qs = POSITION_INFORMATION.objects.filter(Seq_ID__in=seq_list)\
            .distinct().values('Protein_ID').order_by('Protein_ID')
        pid_list = []
        for dict in qs:
            pid_list.append(dict.get('Protein_ID'))

        qs = ALL_PROTEINS.objects.filter(Protein_ID_id__in=pid_list)\
            .values('Protein_ID_id', 'Protein_Key')\
            .order_by('Protein_Key')\
            .distinct()
        context['i'] = qs
        print(context['i'])
    return render(request, 'response2.html', context)
