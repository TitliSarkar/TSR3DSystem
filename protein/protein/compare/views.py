from django.shortcuts import render
from django.db import connection
from django.http import HttpResponse
from .models import SIMILARITY_INFORMATION
from .models import PROTEIN_HIERARCHY
from .models import CLASS_DESCRIPTION
from .models import ARCHITECTURE_DESCRIPTION
from .models import TOPOLOGYFOLD_DESCRIPTION
from .models import HOMOLOGYSUPERFAMILY_DESCRIPTION
from .models import ALL_PROTEINS
import pandas as pd
from django.db.models import Min
from django.db.models.aggregates import Count


def display(request):
    if request.method=="POST":
	if "Choice_1" in request.POST:
	    #return HttpResponse("Choice 1 selected")
	    return render(request, 'compare/choice1.html') ###### request from 'form1.html'
	elif "Choice_2" in request.POST:
	    #return HttpResponse("Choice 2 selected")
	    return render(request, 'compare/choice2.html')
	elif "Choice_3" in request.POST:
		return render(request, 'compare/choice3.html')


def display_1(request):
    if request.method=="POST":
	s1 = request.POST["list1"]
	s2 = request.POST.getlist("list2")
	print s1,s2,str(s2[0])
	context = {}
	context['s1'] = s1
	## Uncomment the below lines to access the database and make the queries
	context['i']=[]
	for i in s2:
	    try:
		res = SIMILARITY_INFORMATION.objects.get(Protein_ID1_id=str(s1), Protein_ID2_id=str(i))
		sim = res.Similarity_Value
		res1 = PROTEIN_HIERARCHY.objects.get(Protein_ID=str(i))
		#details = [res1.Class_id + res1.Architecture_id + res1.TopologyFold_id + res1.HomologySuperfamily_id]
		context['i'].append({'ProtId':str(i),
		                     'similarity':str(sim),
		                     'class':str(res1.Class_id),
		                     'archi':str(res1.Architecture_id),
		                     'topfold':str(res1.TopologyFold_id),
		                     'homsup':str(res1.HomologySuperfamily_id)})
	    except SIMILARITY_INFORMATION.DoesNotExist,PROTEIN_HIERARCHY.DoesNotExist:
		print "-----No Match Found-----"
	    except SIMILARITY_INFORMATION.MultipleObjectsReturned, PROTEIN_HIERARCHY.MultipleObjectsReturned:
		print "-----MultipleMatchesFound-----"
	print context
    #return HttpResponse("Thanks for your choices!! Your Choices are:<br>PDB from list1 : %s<br>PDB from list2 : %s"%(s1,s2))
    return render(request, 'compare/response.html', context) #using dic as vehicle to show reaults


def display_2(request):
    if request.method == "POST":
	s1 = request.POST["list1"]
	cl = request.POST["classes"]
	ar = request.POST["architectures"]
	lst = []
	if ar=='0':
	    if cl=='1':
		lst = [(1,25,40,70)]
	    elif cl=='2':
		lst = [(2,30,30,40),(2,30,200,10),(2,30,200,20),(2,30,800,10),(2,30,1010,10),(2,130,10,10)]
	    elif cl=='3':
		lst = [(3,10,50,40),(3,20,200,10),(3,20,200,20),(3,30,30,40),(3,30,200,10),(3,30,200,20),(3,30,800,10),(3,30,1010,10),(3,90,1200,10),(3,90,810,10)]

	tf = request.POST["topfolds"]
        if tf=='0':
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
	    qry = PROTEIN_HIERARCHY.objects.filter(Class_id=int(cls), Architecture_id=int(arc), TopologyFold_id=int(tfd), HomologySuperfamily_id=int(hsy))
	    print qry
	    for k in qry:
		s2.append(k.Protein_ID)

	if ar != '0' and tf != '0' and hs != '0':
            print "---2---"
	    qry = PROTEIN_HIERARCHY.objects.filter(Class_id=int(cl), Architecture_id=int(ar), TopologyFold_id=int(tf), HomologySuperfamily_id=int(hs))
            print ("qry= ",qry)
            #s2 = []
            for k in qry:
                s2.append(k.Protein_ID)

	context = {}
	print s2
	context['s1'] = s1
    ## Uncomment the below lines to access the database and make the queries
	context['i'] = []
	for i in s2:
	    try:
		res = SIMILARITY_INFORMATION.objects.get(Protein_ID1_id=str(s1), Protein_ID2_id=str(i))
		sim = res.Similarity_Value
		res1 = PROTEIN_HIERARCHY.objects.get(Protein_ID=str(i))
		# details = [res1.Class_id + res1.Architecture_id + res1.TopologyFold_id + res1.HomologySuperfamily_id]
		context['i'].append({'ProtId':str(i),
			            'similarity':str(sim),
			            'class':str(res1.Class_id),
			            'archi':str(res1.Architecture_id),
			            'topfold':str(res1.TopologyFold_id),
			            'homsup':str(res1.HomologySuperfamily_id)})  ###### 'context' is a dictionary
	    except SIMILARITY_INFORMATION.DoesNotExist, PROTEIN_HIERARCHY.DoesNotExist:
		print "-----No Match Found-----"
	    except SIMILARITY_INFORMATION.MultipleObjectsReturned, PROTEIN_HIERARCHY.MultipleObjectsReturned:
		print "-----MultipleMatchesFound-----"
	print context
    return render(request, 'compare/response.html', context)  # using dic as vehicle to show reaults


## QUERT TYPE 2 ------------------>
## Input: a set of protein ids , Output: Commom keys, by clicking on each keys, show list of all protein_ids having it and other details too
### use of Group by and having clause -  complex queries in Django
def display_3(request):
    if request.method=="POST":
	s = request.POST.getlist("list3")
	print s
	context = {}
	context['i']=[]

	'''for i in range(1, len(s)):
		try:
			resultKeys = resultKeys & PKmat.loc[s[i][1:]]
		except IndexError:
			print ("Index error")
	keyset = resultKeys.index.values[resultKeys.nonzero()]
	'''
	#qs = ALL_PROTEINS.objects.filter(Protein_ID_id__in=s) \    ## will be needing later for implementing thtough original lage table in database
	qs = ALL_PROTEINSTEST.objects.filter(Protein_ID_id__in=s) \
		.distinct() \
		.values('Protein_Key')\
		.annotate(key_count=Count('Protein_Key')) \
		.filter(key_count=len(s)) \
		.order_by('Protein_Key')

	print qs
	for dict in qs:
		context['i'].append(dict.get('Protein_Key'))
		print type(dict)
		#context['j'].append('abc')
	print i, context
    return render(request, 'compare/response1.html', context) #using dic as vehicle to show reaults
