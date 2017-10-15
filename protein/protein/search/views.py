# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.db.models.aggregates import Count
from django.db.models import Q

from compare.models import ALL_PROTEINS
from compare.models import POSITION_INFORMATION


def display_3(request):
    """
    Input: A set of protein ids
    Output: Commom keys, by clicking on each keys, show list of all protein_ids
    having it and other details too
    """
    context = {}
    s = request.POST.getlist("list3")
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
    qs_desc_list = []
    for key in db_rows:
        for prot in s:
            qs_desc_list.append(ALL_PROTEINS.objects.filter(
                Q(Protein_Key=str(key)) &
                Q(Protein_ID_id=str(prot)))
                .order_by('Protein_ID_id', 'Key_coourence_no'))
    context['j'] = qs_desc_list
    return render(request, 'response1.html', context)


def display_4(request):
    context = {}
    pid = request.POST["list4"]
    seq_id_queryset = POSITION_INFORMATION.objects.filter(
        Protein_ID_id=str(pid)).values('Seq_ID')
    context['i'] = seq_id_queryset
    return render(request, 'response2.html', context)
