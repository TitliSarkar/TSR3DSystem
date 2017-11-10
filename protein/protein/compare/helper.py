import csv

from protein.settings import HIERARCHY_FILE


def read_hierarchy_csv_file():
    csv_dump = []
    f = open(HIERARCHY_FILE, 'r')
    reader = csv.reader(f)
    for row in reader:
        csv_dump.append(row)
    f.close()
    return csv_dump


def get_hierarchy_list(class_id, architecture, topology, homology):
    csv_list = read_hierarchy_csv_file()
    if architecture == 0 and topology == 0 and homology == 0:
        hierarchy_list = [row for row in csv_list if str(class_id) in row]

    if architecture != 0 and topology == 0 and homology == 0:
        hierarchy_list = [row for row in csv_list
                          if str(class_id)
                          and str(architecture) in row]

    if architecture != 0 and topology != 0 and homology == 0:
        hierarchy_list = [row for row in csv_list
                          if str(class_id)
                          and str(architecture)
                          and str(topology) in row]
    return hierarchy_list
