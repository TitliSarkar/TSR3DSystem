#!/usr/bin/python
import MySQLdb
import csv
import os
import sys
import time
from tqdm import tqdm


def insert_into_all_proteins_table(cursor, db_name, protein_file):
    """
    Reads the TSV file and inserts the values into the
    given all_protiens table in the database
    """
    with open(protein_file, 'r') as f:
        reader = csv.reader(f, delimiter='\t')
        for row in reader:
            Protein_ID = str(os.path.splitext(protein_file)[0])
            Protein_Key = int(row[0])
            aacd0 = str(row[1])
            position0 = str(row[2])
            aacd1 = str(row[3])
            position1 = str(row[4])
            aacd2 = str(row[5])
            position2 = str(row[6])
            classT1 = int(row[7])
            Theta = float(row[8])
            classL1 = int(row[9])
            maxDist = float(row[10])
            x0 = float(row[11])
            y0 = float(row[12])
            z0 = float(row[13])
            x1 = float(row[14])
            y1 = float(row[15])
            z1 = float(row[16])
            x2 = float(row[17])
            y2 = float(row[18])
            z2 = float(row[19])
            sql = "INSERT INTO %s"\
                " (Protein_ID_id, Protein_Key, aacd0, position0, aacd1,"\
                " position1, aacd2, position2, classT1, Theta, classL1,"\
                " maxDist, x0, y0, z0, x1, y1, z1, x2, y2, z2)"\
                " VALUES('%s', %s, '%s', %s, '%s', %s, '%s', %s,"\
                " %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)" %\
                (db_name, Protein_ID, Protein_Key, aacd0, position0,
                 aacd1, position1, aacd2, position2, classT1, Theta,
                 classL1, maxDist, x0, y0, z0, x1, y1, z1, x2, y2, z2)
            try:
                cursor.execute(sql)
            except (MySQLdb.Error, MySQLdb.Warning) as e:
                print(e)


if __name__ == "__main__":
    start_time = time.clock()

    APP_DIR = os.path.dirname(os.path.realpath(__file__))
    tsv_files = [f for f in os.listdir(APP_DIR) if f.endswith('.tsv')]

    # TODO: Fill the password of the root user in mysql
    db_password = ''
    if not db_password:
        print("Database password not specified. Couldn't connect to DB")
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

    for tsv in tqdm(tsv_files, total=len(tsv_files), unit="files"):
        insert_into_all_proteins_table(cursor, "compare_all_proteins_big", tsv)
        insert_into_all_proteins_table(cursor, "compare_all_proteins_big_unindexed", tsv)

    db.commit()
    db.close()

    end_time = time.clock()
    print("Program execution time: " + str(round(end_time - start_time, 4)))
