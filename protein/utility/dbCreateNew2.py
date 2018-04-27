#!/usr/bin/python
import MySQLdb
import numpy as np
import pandas as pd
import csv
import os
import glob

#path = 'E:\\Codes\\Python_Code\\Database Part\\'
path = '/home/seshagiri/Studies/IRS/Project/Database/'
# Open database connection
db = MySQLdb.connect("localhost", "root", "12345678", "ProteinDB")

# prepare a cursor object using cursor() method
cursor = db.cursor()

# execute SQL query using execute() method.
cursor.execute("SELECT VERSION()")

# Fetch a single row using fetchone() method.
data = cursor.fetchone()
print("Database version : %s " % data)

#Insert Value in tables
def insertCLASS_DESCRIPTION():
    with open(path+'protein_hierarchyS2.csv', 'r') as f:
        reader = csv.reader(f, delimiter=',', quoting=csv.QUOTE_NONE)
        for row in reader:
            cathinfo = row[1].split(".")
            Class = int(cathinfo[0])
            DescriptionOfClass = row[2]
            cursor.execute ("SELECT * FROM compare_class_description WHERE Class = %s", [Class])
            data = cursor.fetchall()
            if len(data) == 0:
                try:
                    cursor.execute("INSERT INTO compare_class_description (Class,DescriptionOfClass) VALUES (%s,%s)",
                                   (Class, DescriptionOfClass))
                except MySQLdb.Error, e:
                    print(e)
def insertARCHITECTURE_DESCRIPTION():
    with open(path+'protein_hierarchyS2.csv', 'r') as f:
        reader = csv.reader(f, delimiter=',', quoting=csv.QUOTE_NONE)
        for row in reader:
            cathinfo = row[1].split(".")
            Architecture = int(cathinfo[1])
            DescriptionOfArchitecture = row[3]
            cursor.execute("SELECT * FROM compare_architecture_description WHERE Architecture = %s", [Architecture])
            data = cursor.fetchall()
            if len(data) == 0:
                try:
                    cursor.execute(
                        "INSERT INTO compare_architecture_description (Architecture,DescriptionOfArchitecture) VALUES (%s,%s)",
                        (Architecture, DescriptionOfArchitecture))
                except MySQLdb.Error, e:
                    print(e)
def insertTOPOLOGYFOLD_DESCRIPTION():
    with open(path+'protein_hierarchyS2.csv', 'r') as f:
        reader = csv.reader(f, delimiter=',', quoting=csv.QUOTE_NONE)
        for row in reader:
            cathinfo = row[1].split(".")
            TopologyFold = int(cathinfo[2])
            DescriptionOfTopologyFold = row[4]
            cursor.execute("SELECT * FROM compare_topologyfold_description WHERE TopologyFold = %s", [TopologyFold])
            data = cursor.fetchall()
            if len(data) == 0:
                try:
                    cursor.execute(
                        "INSERT INTO compare_topologyfold_description (TopologyFold,DescriptionOfTopologyFold) VALUES (%s,%s)",
                        (TopologyFold, DescriptionOfTopologyFold))
                except MySQLdb.Error, e:
                    print(e)

def insertHOMOLOGYSUPERFAMILY_DESCRIPTION():
    with open(path+'protein_hierarchyS2.csv', 'r') as f:
        reader = csv.reader(f, delimiter=',', quoting=csv.QUOTE_NONE)
        for row in reader:
            cathinfo = row[1].split(".")
            HomologySuperfamily = int(cathinfo[3])
            DescriptionOfHomologySuperfamily = row[4]
            cursor.execute("SELECT * FROM compare_homologysuperfamily_description WHERE HomologySuperfamily = %s", [HomologySuperfamily])
            data = cursor.fetchall()
            if len(data) == 0:
                try:
                    cursor.execute(
                        "INSERT INTO compare_homologysuperfamily_description (HomologySuperfamily,DescriptionOfHomologySuperfamily) VALUES (%s,%s)",
                        (HomologySuperfamily, DescriptionOfHomologySuperfamily))
                except MySQLdb.Error, e:
                    print(e)

def insertPROTEIN_HIERARCHY():
    with open(path+'protein_hierarchyS2.csv', 'r') as f:
        reader = csv.reader(f, delimiter=',', quoting=csv.QUOTE_NONE)
        for row in reader:
            Protein_ID = row[0]
            cathinfo = row[1].split(".")
            #print(cathinfo)
            Class = int(cathinfo[0])
            Architecture = int(cathinfo[1])
            TopologyFold = int(cathinfo[2])
            HomologySuperfamily = int(cathinfo[3])
            try:
                cursor.execute("INSERT INTO compare_protein_hierarchy"
                               "(Protein_ID, Class_id, Architecture_id, TopologyFold_id, HomologySuperfamily_id) "
                               "VALUES (%s,%s,%s,%s,%s)",
                               ([Protein_ID], [Class], [Architecture], [TopologyFold], [HomologySuperfamily])
                               )
            except MySQLdb.Error, e:
                print(e)

def insertALL_PROTEINS_BIG():   ## saving everything in a csv file and reading from it
    with open(path+"all_proteinsS2.csv", 'r') as f:  ## inserting in smaller test table
        reader = csv.reader(f)
        for row in reader:
            Protein_ID = str(row[0])
            Protein_Key = int(row[1])
            Key_coourence_no = int(row[2])
            aacd0 = row[3]
            position0= row[4]
            aacd1= row[5]
            position1= row[6]
            aacd2= row[7]
            position2= row[8]
            classT1= int(row[9])
            Theta= float(row[10])
            classL1= int(row[11])
            maxDist= float(row[12])
            x0= float(row[13])
            y0= float(row[14])
            z0= float(row[15])
            x1= float(row[16])
            y1= float(row[17])
            z1= float(row[18])
            x2= float(row[19])
            y2= float(row[20])
            z2= float(row[21])
            #print (Protein_ID, Protein_Key, Key_coourence_no, aacd0, position0, aacd1, position1, aacd2, position2, classT1, Theta, classL1, maxDist, x0, y0, z0, x1, y1, z1, x2, y2, z2)
            try:
                cursor.execute(
                    "INSERT INTO compare_all_proteins_big(Protein_ID_id, Protein_Key, Key_coourence_no, aacd0, position0, aacd1, position1, aacd2, position2, classT1, Theta, classL1, maxDist, x0, y0, z0, x1, y1, z1, x2, y2, z2) "
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    ([Protein_ID], [Protein_Key], [Key_coourence_no], [aacd0], [position0], [aacd1], [position1], [aacd2], [position2], [classT1], [Theta], [classL1], [maxDist], [x0], [y0], [z0], [x1], [y1], [z1], [x2], [y2], [z2])
                )
            except MySQLdb.Error, e:
                print(e)


def insertALL_PROTEINS_BIG_UNINDEXED():   ## saving everything in a csv file and reading from it
    with open(path+"all_proteinsS2.csv", 'r') as f:  ## inserting in smaller test table
        reader = csv.reader(f)
        for row in reader:
            Protein_ID = str(row[0])
            Protein_Key = int(row[1])
            Key_coourence_no = int(row[2])
            aacd0 = row[3]
            position0= row[4]
            aacd1= row[5]
            position1= row[6]
            aacd2= row[7]
            position2= row[8]
            classT1= int(row[9])
            Theta= float(row[10])
            classL1= int(row[11])
            maxDist= float(row[12])
            x0= float(row[13])
            y0= float(row[14])
            z0= float(row[15])
            x1= float(row[16])
            y1= float(row[17])
            z1= float(row[18])
            x2= float(row[19])
            y2= float(row[20])
            z2= float(row[21])
            #print (Protein_ID, Protein_Key, Key_coourence_no, aacd0, position0, aacd1, position1, aacd2, position2, classT1, Theta, classL1, maxDist, x0, y0, z0, x1, y1, z1, x2, y2, z2)
            try:
                cursor.execute(
                    "INSERT INTO compare_all_proteins_big_unindexed(Protein_ID_id, Protein_Key, Key_coourence_no, aacd0, position0, aacd1, position1, aacd2, position2, classT1, Theta, classL1, maxDist, x0, y0, z0, x1, y1, z1, x2, y2, z2) "
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    ([Protein_ID], [Protein_Key], [Key_coourence_no], [aacd0], [position0], [aacd1], [position1], [aacd2], [position2], [classT1], [Theta], [classL1], [maxDist], [x0], [y0], [z0], [x1], [y1], [z1], [x2], [y2], [z2])
                )
            except MySQLdb.Error, e:
                print(e)

def insertALL_PROTEINS():   ## saving everything in a csv file and reading from it
    with open(path+"all_proteinsS2.csv", 'r') as f:  ## inserting in smaller test table
        reader = csv.reader(f)
        for row in reader:
            Protein_ID = str(row[0])
            Protein_Key = int(row[1])
            Key_coourence_no = int(row[2])
            aacd0 = row[3]
            position0= row[4]
            aacd1= row[5]
            position1= row[6]
            aacd2= row[7]
            position2= row[8]
            classT1= int(row[9])
            Theta= float(row[10])
            classL1= int(row[11])
            maxDist= float(row[12])
            x0= float(row[13])
            y0= float(row[14])
            z0= float(row[15])
            x1= float(row[16])
            y1= float(row[17])
            z1= float(row[18])
            x2= float(row[19])
            y2= float(row[20])
            z2= float(row[21])
            #print (Protein_ID, Protein_Key, Key_coourence_no, aacd0, position0, aacd1, position1, aacd2, position2, classT1, Theta, classL1, maxDist, x0, y0, z0, x1, y1, z1, x2, y2, z2)
            try:
                cursor.execute(
                    "INSERT INTO compare_all_proteins(Protein_ID, Protein_Key, Key_coourence_no, aacd0, position0, aacd1, position1, aacd2, position2, classT1, Theta, classL1, maxDist, x0, y0, z0, x1, y1, z1, x2, y2, z2) "
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    ([Protein_ID], [Protein_Key], [Key_coourence_no], [aacd0], [position0], [aacd1], [position1], [aacd2], [position2], [classT1], [Theta], [classL1], [maxDist], [x0], [y0], [z0], [x1], [y1], [z1], [x2], [y2], [z2])
                )
            except MySQLdb.Error, e:
                print(e)
def insertPOSITION_INFORMATION():
    with open(path+'position_informationS2.csv', 'r') as f:
        reader = csv.reader(f, delimiter=',', quoting=csv.QUOTE_NONE)
        for row in reader:
            fname = row[0]
            aminoAcidName = row[1]
            seqid = int(row[2])
            #print(type(seqid))
            xCord = float(row[3])
            yCord = float(row[4])
            zCord = float(row[5])
            try:
                cursor.execute(
                        "INSERT INTO compare_position_information(Protein_ID_id, AminoAcid_Name, Seq_ID, X_COORD, Y_COORD, Z_COORD) "
                        "VALUES (%s,%s,%s,%s,%s,%s)",
                        ([fname], [aminoAcidName], [seqid], [xCord], [yCord], [zCord])
                )
            except MySQLdb.Error, e:
                print(e)
def insertSIMILARITY_INFORMATION():
    with open(path+'similarity_informationS2.csv', 'r') as f:
        reader = csv.reader(f, delimiter=',', quoting=csv.QUOTE_NONE)
        for row in reader:
            Protein_Id1 = row[0]
            Protein_Id2 = row[1]
            Sim = row[2]
            #print (Protein_Id1,Protein_Id2,Sim)
            try:
                cursor.execute("INSERT INTO compare_similarity_information(Protein_ID1_id,Protein_ID2_id,Similarity_Value) VALUES (%s,%s,%s)",
                ([Protein_Id1],[Protein_Id2],[Sim])
                )

            except MySQLdb.Error, e:
                print(e)

# insertCLASS_DESCRIPTION()
# insertARCHITECTURE_DESCRIPTION()
# insertTOPOLOGYFOLD_DESCRIPTION()
# insertHOMOLOGYSUPERFAMILY_DESCRIPTION()
# insertPROTEIN_HIERARCHY()
# insertALL_PROTEINS_BIG()
insertALL_PROTEINS_BIG_UNINDEXED()
# insertPOSITION_INFORMATION() ######
# insertSIMILARITY_INFORMATION()

db.commit()
db.close()

print ("Code End.")
