# -*- coding: utf-8 -*-

import csv
import json
from collections import defaultdict

dict_map = {}

with open("dictionary.txt", 'r',encoding='utf8') as dict_file:
    lines = dict_file.readlines()
    for row in lines:
        j_row = json.loads(row)
        dict_map[j_row["character"]] = j_row

"""
    Example:
    '鲣': {'character': '鲣', 'definition': 'skipjack, bonito', 'pinyin': ['jiān'], 'decomposition': '⿰鱼坚', 'etymology': {'type': 'pictophonetic', 'phonetic': '坚', 'semantic': '鱼', 'hint': 'fish'}, 'radical': '鱼
    ', 'matches': [[0], [0], [0], [0], [0], [0], [0], [0], [1], [1], [1], [1], [1], [1], [1]]}
"""

hsk5_word_list = []
with open("HSK5_freqorder.txt", 'r',encoding='utf8') as csvfile:
    freader = csv.reader(csvfile, delimiter='\t')
    for row in freader:
        simplified_character = row[0]
        hsk5_word_list.append(simplified_character)


word_to_neighbours_dict = defaultdict(list)
for word in hsk5_word_list:
    # print('word')
    # print(word)
    # add relationship between word and it's components
    word_to_neighbours_dict[word] = list(word)
    for hanzi in word:
        # consider single hanzi in word to lookup in the dictionary
        dict_entry_for_hanzi = dict_map[hanzi]
        hanzi_decomposition = dict_entry_for_hanzi['decomposition']
        #print('hanzi_decomposition')
        #print(hanzi_decomposition)
        
        for component in hanzi_decomposition:
            o = ord(component)
            if o in range(11904, 12246) or o in range(19968, 40960):
                # it's a radical
                # print('radical')
                # print(component)
                word_to_neighbours_dict[word].append(component)
                # print('dict_entry_for_radical')
                # print(dict_entry_for_radical)
                # hanzi_to_neighbours_dict[component].append(list(word))
                pass

            if o in range(12272, 12284):
                # it's a position
                # print('position component')
                # print(component)
                pass

node_set = set()
relationship_set = set()
node_id = 1

for source in word_to_neighbours_dict.keys():
    # add source to nodes
    # out_nodes_file.write(str(node_id)+","+source+'\n')
    node_set.add(source)
    # node_id = node_id + 1
    if len(word_to_neighbours_dict[source]) > 1:
        for dest in word_to_neighbours_dict[source]:
            # add dest to nodes ...
            node_set.add(dest)
            # out_nodes_file.write(str(node_id)+","+dest+'\n')
            # node_id = node_id + 1
            # ...and add the relationship too
            # out_relationships_file.write(source+","+dest+'\n')
            relationship_set.add((source, dest))

node_to_id_map = {}
node_counter = 1
with open("nodes.csv", 'w',encoding='utf8') as out_nodes_file:
    out_nodes_file.write('id,name\n')
    for node in node_set:
        out_nodes_file.write(str(node_counter)+","+node+'\n')
        node_to_id_map[node] = node_counter
        node_counter = node_counter + 1

with open("edges.csv", 'w',encoding='utf8') as out_relationships_file:
    out_relationships_file.write('source_id,target_id\n')
    for relationship in relationship_set:
        source = relationship[0]
        dest = relationship[1]
        if source != dest:
            source_id = node_to_id_map[source]
            dest_id = node_to_id_map[dest]
            out_relationships_file.write(str(dest_id)+","+str(source_id)+'\n')
        
"""
word_to_index_map = {}
with open("HSK5_freqorder.txt", 'r',encoding='utf8') as csvfile:
    freader = csv.reader(csvfile, delimiter='\t')
    i = 1
    with open("nodes.csv","w",encoding='utf8') as node_file:
        node_file.write('id,word\n')
        for row in freader:
            simplified_character = row[0]
            word_to_index_map[simplified_character] = i
            node_file.write(str(i)+","+simplified_character+'\n')
            i = i + 1
    node_file.close()
"""