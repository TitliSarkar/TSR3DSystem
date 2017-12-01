#!/usr/bin/python
import MySQLdb
import csv
import sys
import time


# TODO: Specifify the location of path to database
path = ''
if not path:
    print("Path to database not specified")
    sys.exit(0)

# TODO: Specifiy the db password
db_password = ''
if not db_password:
    print("Database password is not specified. Couldn't connect to DB")
    sys.exit(0)

# Open database connection
db = MySQLdb.connect("localhost", "root", db_password, "ProteinDB")

# prepare a cursor object using cursor() method
cursor = db.cursor()

# execute SQL query using execute() method.
cursor.execute("SELECT VERSION()")

# Fetch a single row using fetchone() method.
data = cursor.fetchone()
print("Database version : %s " % data)


def insertCLASS_DESCRIPTION():
    with open(path + 'protein_hierarchyS2.csv', 'r') as f:
        reader = csv.reader(f, delimiter=',', quoting=csv.QUOTE_NONE)
        for row in reader:
            cathinfo = row[1].split(".")
            Class = int(cathinfo[0])
            DescriptionOfClass = row[2]
            cursor.execute(
                "SELECT * FROM compare_class_description "
                "WHERE Class = %s", [Class])
            data = cursor.fetchall()
            if len(data) == 0:
                try:
                    cursor.execute(
                        "INSERT INTO compare_class_description "
                        "(Class,DescriptionOfClass) VALUES (%s,%s)",
                        (Class, DescriptionOfClass)
                    )
                except (MySQLdb.Error, MySQLdb.Warning) as e:
                    print(e)


def insertARCHITECTURE_DESCRIPTION():
    with open(path + 'protein_hierarchyS2.csv', 'r') as f:
        reader = csv.reader(f, delimiter=',', quoting=csv.QUOTE_NONE)
        for row in reader:
            cathinfo = row[1].split(".")
            Architecture = int(cathinfo[1])
            DescriptionOfArchitecture = row[3]
            cursor.execute(
                "SELECT * FROM compare_architecture_description "
                "WHERE Architecture = %s",
                [Architecture]
            )
            data = cursor.fetchall()
            if len(data) == 0:
                try:
                    cursor.execute(
                        "INSERT INTO compare_architecture_description "
                        "(Architecture,DescriptionOfArchitecture) "
                        "VALUES (%s,%s)",
                        (Architecture, DescriptionOfArchitecture)
                    )
                except (MySQLdb.Error, MySQLdb.Warning) as e:
                    print(e)


def insertTOPOLOGYFOLD_DESCRIPTION():
    with open(path + 'protein_hierarchyS2.csv', 'r') as f:
        reader = csv.reader(f, delimiter=',', quoting=csv.QUOTE_NONE)
        for row in reader:
            cathinfo = row[1].split(".")
            TopologyFold = int(cathinfo[2])
            DescriptionOfTopologyFold = row[4]
            cursor.execute(
                "SELECT * FROM compare_topologyfold_description "
                "WHERE TopologyFold = %s",
                [TopologyFold]
            )
            data = cursor.fetchall()
            if len(data) == 0:
                try:
                    cursor.execute(
                        "INSERT INTO compare_topologyfold_description "
                        "(TopologyFold,DescriptionOfTopologyFold) "
                        "VALUES (%s,%s)",
                        (TopologyFold, DescriptionOfTopologyFold)
                    )
                except (MySQLdb.Error, MySQLdb.Warning) as e:
                    print(e)


def insertHOMOLOGYSUPERFAMILY_DESCRIPTION():
    with open(path + 'protein_hierarchyS2.csv', 'r') as f:
        reader = csv.reader(f, delimiter=',', quoting=csv.QUOTE_NONE)
        for row in reader:
            cathinfo = row[1].split(".")
            HomologySuperfamily = int(cathinfo[3])
            DescriptionOfHomologySuperfamily = row[4]
            cursor.execute(
                "SELECT * FROM compare_homologysuperfamily_description "
                "WHERE HomologySuperfamily = %s",
                [HomologySuperfamily]
            )
            data = cursor.fetchall()
            if len(data) == 0:
                try:
                    cursor.execute(
                        "INSERT INTO compare_homologysuperfamily_description "
                        "(HomologySuperfamily, "
                        "DescriptionOfHomologySuperfamily)VALUES (%s,%s)",
                        (HomologySuperfamily, DescriptionOfHomologySuperfamily)
                    )
                except (MySQLdb.Error, MySQLdb.Warning) as e:
                    print(e)


def insertPROTEIN_HIERARCHY():
    with open(path + 'protein_hierarchyS2.csv', 'r') as f:
        reader = csv.reader(f, delimiter=',', quoting=csv.QUOTE_NONE)
        for row in reader:
            Protein_ID = row[0]
            cathinfo = row[1].split(".")
            Class = int(cathinfo[0])
            Architecture = int(cathinfo[1])
            TopologyFold = int(cathinfo[2])
            HomologySuperfamily = int(cathinfo[3])
            try:
                cursor.execute(
                    "INSERT INTO compare_protein_hierarchy"
                    "(Protein_ID, Class_id, Architecture_id, "
                    "TopologyFold_id, HomologySuperfamily_id) "
                    "VALUES (%s,%s,%s,%s,%s)",
                    ([Protein_ID], [Class], [Architecture],
                     [TopologyFold], [HomologySuperfamily])
                )
            except (MySQLdb.Error, MySQLdb.Warning) as e:
                print(e)


def insertPOSITION_INFORMATION():
    with open(path + 'position_informationS2.csv', 'r') as f:
        reader = csv.reader(f, delimiter=',', quoting=csv.QUOTE_NONE)
        for row in reader:
            fname = row[0]
            aminoAcidName = row[1]
            seqid = int(row[2])
            xCord = float(row[3])
            yCord = float(row[4])
            zCord = float(row[5])
            try:
                cursor.execute(
                    "INSERT INTO compare_position_information"
                    "(Protein_ID_id, AminoAcid_Name, Seq_ID, "
                    "X_COORD, Y_COORD, Z_COORD) " +
                    "VALUES (%s,%s,%s,%s,%s,%s)",
                    ([fname], [aminoAcidName], [seqid], [xCord], [yCord], [zCord])
                )
            except (MySQLdb.Error, MySQLdb.Warning) as e:
                print(e)


def insertSIMILARITY_INFORMATION():
    with open(path + 'similarity_informationS2.csv', 'r') as f:
        reader = csv.reader(f, delimiter=',', quoting=csv.QUOTE_NONE)
        for row in reader:
            Protein_Id1 = row[0]
            Protein_Id2 = row[1]
            Sim = row[2]
            try:
                cursor.execute(
                    "INSERT INTO compare_similarity_information"
                    "(Protein_ID1_id, Protein_ID2_id,"
                    " Similarity_Value) VALUES (%s,%s,%s)",
                    ([Protein_Id1], [Protein_Id2], [Sim])
                )
            except (MySQLdb.Error, MySQLdb.Warning) as e:
                print(e)


start_time = time.clock()
insertCLASS_DESCRIPTION()
insertARCHITECTURE_DESCRIPTION()
insertTOPOLOGYFOLD_DESCRIPTION()
insertHOMOLOGYSUPERFAMILY_DESCRIPTION()
insertPROTEIN_HIERARCHY()
insertPOSITION_INFORMATION()
insertSIMILARITY_INFORMATION()

db.commit()
db.close()
end_time = time.clock()

print("Program execution time: " + str(round(end_time - start_time, 4)))
