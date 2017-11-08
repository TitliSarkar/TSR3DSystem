# -*- coding: utf-8 -*-
# django imports
from django.shortcuts import render
from django.views.generic.list import ListView

# app import
from compare.models import SIMILARITY_INFORMATION
from compare.models import PROTEIN_HIERARCHY
from compare.models import CLASS_DESCRIPTION
from compare.models import ARCHITECTURE_DESCRIPTION
from compare.models import TOPOLOGYFOLD_DESCRIPTION
from compare.models import HOMOLOGYSUPERFAMILY_DESCRIPTION

from compare.helper import get_hierarchy_list


class CompareByProteinID(ListView):
    model = PROTEIN_HIERARCHY
    template_name = "compare_by_pid_home.html"


def compare_by_protein_id_result(request):
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
                Protein_ID1_id=protein_compared,
                Protein_ID2_id=protein)

            if not similarity_info_queryset:
                continue

            similarity_value = similarity_info_queryset[0].Similarity_Value

            hierarchy_result = PROTEIN_HIERARCHY.objects.get(
                Protein_ID=protein)

            class_result = CLASS_DESCRIPTION.objects.get(
                Class=hierarchy_result.Class_id)

            architecture_result = ARCHITECTURE_DESCRIPTION.objects.get(
                Architecture=hierarchy_result.Architecture_id)

            topology_result = TOPOLOGYFOLD_DESCRIPTION.objects.get(
                TopologyFold=hierarchy_result.TopologyFold_id)

            homology_result = HOMOLOGYSUPERFAMILY_DESCRIPTION.objects.get(
                HomologySuperfamily=hierarchy_result.HomologySuperfamily_id)

            row_val.append({
                'ProtId': protein,
                'similarity': similarity_value,
                'class': hierarchy_result.Class_id,
                'class_desc': class_result.DescriptionOfClass,
                'archi': hierarchy_result.Architecture_id,
                'archi_desc': architecture_result.DescriptionOfArchitecture,
                'topfold': hierarchy_result.TopologyFold_id,
                'topfold_desc': topology_result.DescriptionOfTopologyFold,
                'homsup': hierarchy_result.HomologySuperfamily_id,
                'homsup_desc': homology_result.DescriptionOfHomologySuperfamily
            })

        context['protein_details_list'] = row_val
    return render(request, 'compare_by_pid_result.html', context)


class CompareByHierarchy(ListView):
    model = PROTEIN_HIERARCHY
    template_name = "compare_by_hl_home.html"


def compare_by_hierarchy_result(request):
    context = {}

    if request.method == "GET":
        context['no_result_found'] = True

    if request.method == "POST":
        row_val = []
        protein_list = []
        protein_id = request.POST["list1"]
        class_id = int(request.POST["classes"])
        architecture = int(request.POST["architectures"])
        topology = int(request.POST["topfolds"])
        homology = int(request.POST["homologies"])

        if architecture == 0 or topology == 0 or homology == 0:
            hierarchy_list = get_hierarchy_list(
                class_id, architecture, topology, homology)

            for hierarchy in hierarchy_list:
                hierarchy_result = PROTEIN_HIERARCHY.objects.filter(
                    Class=hierarchy[0],
                    Architecture_id=hierarchy[1],
                    TopologyFold_id=hierarchy[2],
                    HomologySuperfamily_id=hierarchy[3])

                for hresult in hierarchy_result:
                    protein_list.append(hresult.Protein_ID)
        else:
            hierarchy_result = PROTEIN_HIERARCHY.objects.filter(
                Class=class_id, Architecture=architecture,
                TopologyFold=topology,
                HomologySuperfamily=homology)

            for hresult in hierarchy_result:
                protein_list.append(hresult.Protein_ID)

        for protein in protein_list:
            similarity_info_queryset = SIMILARITY_INFORMATION.objects.filter(
                Protein_ID1_id=protein_id,
                Protein_ID2_id=protein)

            if not similarity_info_queryset:
                continue

            similarity_value = similarity_info_queryset[0].Similarity_Value

            hierarchy_result = PROTEIN_HIERARCHY.objects.get(Protein_ID=protein)

            class_result = CLASS_DESCRIPTION.objects.get(
                Class=hierarchy_result.Class_id)

            architecture_result = ARCHITECTURE_DESCRIPTION.objects.get(
                Architecture=hierarchy_result.Architecture_id)

            topology_result = TOPOLOGYFOLD_DESCRIPTION.objects.get(
                TopologyFold=hierarchy_result.TopologyFold_id)

            homology_result = HOMOLOGYSUPERFAMILY_DESCRIPTION.objects.get(
                HomologySuperfamily=hierarchy_result.HomologySuperfamily_id)

            row_val.append({
                'ProtId': protein,
                'similarity': similarity_value,
                'class': hierarchy_result.Class_id,
                'class_desc': class_result.DescriptionOfClass,
                'archi': hierarchy_result.Architecture_id,
                'archi_desc': architecture_result.DescriptionOfArchitecture,
                'topfold': hierarchy_result.TopologyFold_id,
                'topfold_desc': topology_result.DescriptionOfTopologyFold,
                'homsup': hierarchy_result.HomologySuperfamily_id,
                'homsup_desc': homology_result.DescriptionOfHomologySuperfamily
            })

        context['protein_compared'] = protein_id
        context['protein_details_list'] = row_val
    return render(request, 'compare_by_hl_result.html', context)
