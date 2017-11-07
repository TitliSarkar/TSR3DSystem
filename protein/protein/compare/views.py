from django.db.models import Min
from django.db.models.aggregates import Count
from django.shortcuts import render
from django.db import connection
from django.db.models import Q
from django.http import HttpResponse
from django.http import Http404
from django.utils.translation import ugettext as _
from django.views.generic.edit import FormMixin
from django.views.generic.list import ListView

import pandas as pd

from compare.models import SIMILARITY_INFORMATION
from compare.models import PROTEIN_HIERARCHY
from compare.models import CLASS_DESCRIPTION
from compare.models import ARCHITECTURE_DESCRIPTION
from compare.models import TOPOLOGYFOLD_DESCRIPTION
from compare.models import HOMOLOGYSUPERFAMILY_DESCRIPTION
from compare.models import ALL_PROTEINS
from compare.models import POSITION_INFORMATION


class CompareByProteinID(ListView):
    model = PROTEIN_HIERARCHY
    template_name = "choice1.html"


def display_1(request):
    context = {}

    if request.method == "GET":
        context['no_result_found'] = True

    if request.method == "POST":
        row_val = []
        protein_compared = request.POST["list1"]
        protein_list = request.POST.getlist("list2")
        context['protein_compared'] = protein_compared

        for protein in protein_list:
            similarity_info_queryset = SIMILARITY_INFORMATION.objects.filter(
                Protein_ID1_id=str(protein_compared),
                Protein_ID2_id=str(protein))

            print(similarity_info_queryset)

            if not similarity_info_queryset:
                context['no_result_found'] = True
                return render(request, 'response.html', context)

            similarity_value = similarity_info_queryset[0].Similarity_Value

            hierarchy_result = PROTEIN_HIERARCHY.objects.get(
                Protein_ID=str(protein))

            class_result = CLASS_DESCRIPTION.objects.get(
                Class=hierarchy_result.Class_id)

            architecture_result = ARCHITECTURE_DESCRIPTION.objects.get(
                Architecture=hierarchy_result.Architecture_id)

            topology_result = TOPOLOGYFOLD_DESCRIPTION.objects.get(
                TopologyFold=hierarchy_result.TopologyFold_id)

            homology_result = HOMOLOGYSUPERFAMILY_DESCRIPTION.objects.get(
                HomologySuperfamily=hierarchy_result.HomologySuperfamily_id)

            row_val.append({
                'ProtId': str(protein),
                'similarity': str(similarity_value),
                'class': str(hierarchy_result.Class_id),
                'class_desc': str(class_result.DescriptionOfClass),
                'archi': str(hierarchy_result.Architecture_id),
                'archi_desc': str(architecture_result.DescriptionOfArchitecture),
                'topfold': str(hierarchy_result.TopologyFold_id),
                'topfold_desc': str(topology_result.DescriptionOfTopologyFold),
                'homsup': str(hierarchy_result.HomologySuperfamily_id),
                'homsup_desc': str(homology_result.DescriptionOfHomologySuperfamily)
            })

        context['protein_details_list'] = row_val
    return render(request, 'response.html', context)


def display_2(request):
    if request.method == "POST":
        s1 = request.POST["list1"]
        cl = request.POST["classes"]
        ar = request.POST["architectures"]
        lst = []
        if ar == '0':
            if cl == '1':
                lst = [(1,25,40,70)]
            elif cl=='2':
                lst = [(2,30,30,40),(2,30,200,10),(2,30,200,20),(2,30,800,10),(2,30,1010,10),(2,130,10,10)]
            elif cl=='3':
                lst = [(3,10,50,40), (3,20,200,10), (3,20,200,20),
                        (3,30,30,40), (3,30,200,10), (3,30,200,20),
                        (3,30,800,10), (3,30,1010,10), (3,90,1200,10),
                        (3,90,810,10)]

        tf = request.POST["topfolds"]
        if tf == '0':
            if cl=='1' and ar=='25':
                lst = [(1,25,40,70)]
            if cl=='2':
                if ar=='30':
                    lst = [(2,30,30,40),(2,30,200,10),(2,30,200,20),(2,30,800,10),(2,30,1010,10)]
                elif ar=='130':
                    lst = [(2,130,10,10)]
            if cl=='3':
                if ar=='10':
                    lst = [(3,10,50,40)]
                elif ar=='20':
                    lst = [(3,20,200,10),(3,20,200,20)]
                elif ar=='30':
                    lst = [(3,30,30,40),(3,30,200,10),(3,30,200,20),(3,30,800,10),(3,30,1010,10)]
                elif ar=='90':
                    lst = [(3,90,1200,10),(3,90,810,10)]

        hs = request.POST["homologies"]
        hs = str(hs)

        if hs=='0':
            if cl=='1' and ar=='25':
                lst = [(1,25,40,70)]
            if cl=='2':
                if ar=='30':
                    if tf=='30':
                        lst = [(2,30,30,40)]
                    elif tf=='200':
                        lst = [(2,30,200,10),(2,30,200,20)]
                    elif tf=='800':
                        lst = [(2,30,800,10)]
                    elif tf=='1010':
                        lst = [(2,30,1010,10)]
                    elif ar=='130':
                        lst = [(2,130,10,10)]
            if cl=='3':
                if ar=='10':
                    lst = [(3,10,50,40)]
                elif ar=='20':
                    lst = [(3,20,200,10),(3,20,200,20)]
                elif ar=='30':
                    if tf=='30':
                        lst = [(3,30,30,40)]
                    elif tf=='200':
                        lst = [(3,30,200,10),(3,30,200,20)]
                    elif tf=='800':
                        lst = [(3,30,800,10)]
                    elif tf=='1010':
                        lst = [(3,30,1010,10)]
                elif ar=='90':
                    if tf=='1200':
                        lst = [(3,90,1200,10)]
                    elif tf=='810':
                        lst = [(3,90,810,10)]
        qry = []
        print ("lst= ",lst)
        s2 = []
        for i in lst:
            cls = i[0]
            arc = i[1]
            tfd = i[2]
            hsy = i[3]
            print "---1---"
            qry = PROTEIN_HIERARCHY.objects.filter(Class_id=int(cls), Architecture_id=int(arc), TopologyFold_id=int(tfd),
                    HomologySuperfamily_id=int(hsy))
            print qry
            for k in qry:
                s2.append(k.Protein_ID)

        if ar != '0' and tf != '0' and hs != '0':
            print "---2---"
            qry = PROTEIN_HIERARCHY.objects.filter(Class_id=int(cl), Architecture_id=int(ar), TopologyFold_id=int(tf), HomologySuperfamily_id=int(hs))
            print ("qry= ",qry)
            # s2 = []
            for k in qry:
                s2.append(k.Protein_ID)

        context = {}
        print s2
        context['s1'] = s1
        # Uncomment the below lines to access the database and make the queries
        context['i'] = []
        for i in s2:
            try:
                res = SIMILARITY_INFORMATION.objects.get(
                    Protein_ID1_id=str(s1),
                    Protein_ID2_id=str(i))
                sim = res.Similarity_Value
                res1 = PROTEIN_HIERARCHY.objects.get(Protein_ID=str(i))
                context['i'].append({'ProtId':str(i),
                    'similarity':str(sim),
                    'class':str(res1.Class_id),
                    'archi':str(res1.Architecture_id),
                    'topfold':str(res1.TopologyFold_id),
                    'homsup':str(res1.HomologySuperfamily_id)})
            except SIMILARITY_INFORMATION.DoesNotExist, PROTEIN_HIERARCHY.DoesNotExist:
                print "-----No Match Found-----"
            except SIMILARITY_INFORMATION.MultipleObjectsReturned, PROTEIN_HIERARCHY.MultipleObjectsReturned:
                print "-----MultipleMatchesFound-----"
        print context
    return render(request, 'response.html', context)  # using dic as vehicle to show reaults


