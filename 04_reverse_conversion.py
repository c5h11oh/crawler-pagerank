import json
import io
import numpy

pagerank = open('./pagerank', 'r')
mapping = open('./file_index_mapping', 'r')
mp = json.loads(mapping.read())
mp_arr = numpy.empty(len(mp), dtype=object)
for k in mp:
    mp_arr[mp[k]] = k
pr_arr = numpy.empty(len(mp), dtype=object)
for line in pagerank:
    tmp = line.split(' ')
    pr_arr[int(tmp[0])] = float(tmp[1])
    pass
pr_arr, mp_arr = zip(*sorted(zip(pr_arr, mp_arr), reverse=True))
pr_name = open('pagerank_with_name', 'w')
for i in range(len(mp)):
    pr_name.write(str(pr_arr[i]) + '\t' + mp_arr[i] + '\n')
pass
