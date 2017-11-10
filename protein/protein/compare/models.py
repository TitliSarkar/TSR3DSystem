from __future__ import unicode_literals
from django.db import models


class CLASS_DESCRIPTION(models.Model):
    Class = models.IntegerField(primary_key=True, unique=True)
    DescriptionOfClass = models.CharField(max_length=300)


class ARCHITECTURE_DESCRIPTION(models.Model):
    Architecture = models.IntegerField(primary_key=True, unique=True)
    DescriptionOfArchitecture = models.CharField(max_length=300)


class TOPOLOGYFOLD_DESCRIPTION(models.Model):
    TopologyFold = models.IntegerField(primary_key=True, unique=True)
    DescriptionOfTopologyFold = models.CharField(max_length=300)


class HOMOLOGYSUPERFAMILY_DESCRIPTION(models.Model):
    HomologySuperfamily = models.IntegerField(primary_key=True, unique=True)
    DescriptionOfHomologySuperfamily = models.CharField(max_length=300)


class PROTEIN_HIERARCHY(models.Model):
    Protein_ID = models.CharField(primary_key=True, max_length=20, unique=True)
    Class = models.ForeignKey(
        CLASS_DESCRIPTION, to_field='Class', on_delete=models.CASCADE)
    Architecture = models.ForeignKey(
        ARCHITECTURE_DESCRIPTION, to_field='Architecture',
        on_delete=models.CASCADE)
    TopologyFold = models.ForeignKey(
        TOPOLOGYFOLD_DESCRIPTION, to_field='TopologyFold',
        on_delete=models.CASCADE)
    HomologySuperfamily = models.ForeignKey(
        HOMOLOGYSUPERFAMILY_DESCRIPTION, to_field='HomologySuperfamily',
        on_delete=models.CASCADE)


class ALL_PROTEINS(models.Model):
    Protein_ID = models.ForeignKey(
        PROTEIN_HIERARCHY,
        to_field='Protein_ID',
        on_delete=models.CASCADE)
    Protein_Key = models.IntegerField()
    Key_coourence_no = models.IntegerField(default=0)
    aacd0 = models.CharField(max_length=5, null=True)
    position0 = models.CharField(max_length=5, null=True)
    aacd1 = models.CharField(max_length=5, null=True)
    position1 = models.CharField(max_length=5, null=True)
    aacd2 = models.CharField(max_length=5, null=True)
    position2 = models.CharField(max_length=5, null=True)
    classT1 = models.IntegerField(default=0)
    Theta = models.FloatField(default=0.0)
    classL1 = models.IntegerField(default=0)
    maxDist = models.FloatField(default=0.0)
    x0 = models.FloatField(default=0.0)
    y0 = models.FloatField(default=0.0)
    z0 = models.FloatField(default=0.0)
    x1 = models.FloatField(default=0.0)
    y1 = models.FloatField(default=0.0)
    z1 = models.FloatField(default=0.0)
    x2 = models.FloatField(default=0.0)
    y2 = models.FloatField(default=0.0)
    z2 = models.FloatField(default=0.0)


class POSITION_INFORMATION(models.Model):
    Protein_ID = models.ForeignKey(
        PROTEIN_HIERARCHY,
        to_field='Protein_ID',
        on_delete=models.CASCADE)
    AminoAcid_Name = models.CharField(max_length=20)
    Seq_ID = models.CharField(max_length=5, null=True)
    X_COORD = models.FloatField(default=0.0)
    Y_COORD = models.FloatField(default=0.0)
    Z_COORD = models.FloatField(default=0.0)


class SIMILARITY_INFORMATION(models.Model):
    Protein_ID1 = models.ForeignKey(
        PROTEIN_HIERARCHY, to_field='Protein_ID',
        related_name='protein_id1',
        on_delete=models.CASCADE)
    Protein_ID2 = models.ForeignKey(
        PROTEIN_HIERARCHY, to_field='Protein_ID',
        related_name='protein_id2',
        on_delete=models.CASCADE)
    Similarity_Value = models.FloatField(default=0.0)


# extra class for test
class ALL_PROTEINSTEST(models.Model):
    Protein_ID = models.CharField(max_length=20)
    Protein_Key = models.IntegerField()
    Key_coourence_no = models.IntegerField(default=0)
    aacd0 = models.CharField(max_length=5, null=True)
    position0 = models.CharField(max_length=5, null=True)
    aacd1 = models.CharField(max_length=5, null=True)
    position1 = models.CharField(max_length=5, null=True)
    aacd2 = models.CharField(max_length=5, null=True)
    position2 = models.CharField(max_length=5, null=True)
    classT1 = models.IntegerField(default=0)
    Theta = models.FloatField(default=0.0)
    classL1 = models.IntegerField(default=0)
    maxDist = models.FloatField(default=0.0)
    x0 = models.FloatField(default=0.0)
    y0 = models.FloatField(default=0.0)
    z0 = models.FloatField(default=0.0)
    x1 = models.FloatField(default=0.0)
    y1 = models.FloatField(default=0.0)
    z1 = models.FloatField(default=0.0)
    x2 = models.FloatField(default=0.0)
    y2 = models.FloatField(default=0.0)
    z2 = models.FloatField(default=0.0)
