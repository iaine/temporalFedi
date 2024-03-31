'''
temporal sonifcation of fediverse
'''
import sys
from time import sleep

from yappyChuck import yappyChuck

def convert_time(tm):
    return tm

def jaccard (setA, setB):
    return setA.union(setB)/setA.intersection(setB)

def get_labels(label, dataset):
    labels = {"altright":0, "porn":0, "other":0}
    if label == "altright":
        labels["altright"] += 1
    elif label == "porn":
        labels["porn"] += 1
    else:
        labels["other"] += 1
    return labels


_file = sys.argv[3]

if not _file:
    print("usage: python3 temporalFedi.py <type> <data>")
    sys.exit(0)

yappy = yappyChuck()

yappy.startServer()

fh = open(_file, 'r')
data = fh.readlines()
fh.close()

# get the reasons
fh = open("blocks.csv", 'r')
bl = fh.readlines()
fh.close()

blocks = {}
for b in bl:
    blocks[b[3]]=b[2]

start_time = convert_time(data[0][2])
start_block = data[0][2].split(';')

if sys.argv[2] == "similarity":
    #listen to similairty of blocks
    for row in _file:
        _time = (convert_time(row[2]) - start_time)/1000
        jaccard_blk = jaccard(len(row[3]), start_block)
        yappy.send("chuck {0}.ck:{1}:{2}".format(row, jaccard_blk) )
        sleep(_time)
elif sys.argv[2] == "types":
    #listen to types of blocks
    for row in _file:
        _time = (convert_time(row[2]) - start_time)/1000
        falls = [reason for reason in row[3]]
        reasons = get_labels(falls)
        yappy.send("chuck {0}.ck:{1}:{2}:{3}:{4}".format(row, 
                reasons["altright"], reasons["porn"], reasons["other"] ) )
        sleep(_time)


yappy.stopServer()