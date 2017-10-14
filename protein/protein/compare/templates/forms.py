from django.forms.models import ModelForm
from django import forms
from django.db.models import Q

from compare.models import SIMILARITY_INFORMATION
from compare.models import PROTEIN_HIERARCHY

compare_protein_id_fields = ['Protein_ID']


class CompareProteinIDForm(ModelForm):
    class Meta:
        model = PROTEIN_HIERARCHY
        fields = 
