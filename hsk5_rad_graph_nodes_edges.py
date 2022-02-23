# -*- coding: utf-8 -*-
import csv
import json

word_set = set()
comp_set = set()
edge_set = set()
edge_c_set = set()
dict_map = {}


#dictionary from https://raw.githubusercontent.com/skishore/makemeahanzi/master/dictionary.txt

with open("HSK5_freqorder.txt", 'r',encoding='utf8') as csvfile:
    freader = csv.reader(csvfile, delimiter='\t')
    for row in freader:
        for c in row[0]:
            word_set.add(c)

with open("dictionary.txt", 'r',encoding='utf8') as dict_file:
    lines = dict_file.readlines()
    for row in lines:
        j_row = json.loads(row)
        dict_map[j_row["character"]] = j_row

for wa_entry in word_set:
    d_entry = dict_map[wa_entry]
    if d_entry.get('etymology') != None:
        if d_entry.get('etymology').get('phonetic') != None:
            comp_set.add(d_entry.get('etymology').get('phonetic'))
            edge_set.add(d_entry.get('character')+"|"+d_entry.get('etymology').get('phonetic')+"|"+'phonetic')
            edge_c_set.add(d_entry.get('etymology').get('phonetic'))

        if d_entry.get('etymology').get('semantic') != None:
            comp_set.add(d_entry.get('etymology').get('semantic'))
            edge_set.add(d_entry.get('character')+"|"+d_entry.get('etymology').get('semantic')+"|"+'semantic')
            edge_c_set.add(d_entry.get('etymology').get('semantic'))

word_set = word_set.union(comp_set)  
word_set = word_set.union(edge_c_set) 

word_set = list(word_set)
edge_set = list(edge_set)
s_nodes = []
s_edges = []
for value in word_set:
    s_nodes.append(str(word_set.index(value)+1)+","+value+"\n")
print(s_nodes)
j = 0
for edge_str in edge_set:
    edge = edge_str.split("|")
    s_edges.append(str(edge_set.index(edge_str)+1)+","+str(word_set.index(edge[1])+1)+","+str(word_set.index(edge[0])+1)+","+edge[2]+"\n")
    j = j + 1
    
print(s_edges)

nodes_file = open("nodes.csv","w",encoding='utf8')
nodes_file.writelines(s_nodes)
nodes_file.close()

edges_file = open("edges.csv","w",encoding='utf8')
edges_file.writelines(s_edges)
edges_file.close()