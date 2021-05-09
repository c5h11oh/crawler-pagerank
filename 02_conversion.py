import os
import json
from urllib.parse import *

counter = int(0)
file_index_mapping = dict()
edges = dict()

# https://stackoverflow.com/questions/18262293/how-to-open-every-file-in-a-folder
for i, fn in enumerate(os.listdir('./crawled_pages/')):
    with open(os.path.join('./crawled_pages/', fn)) as f:
        f_dict = dict(json.loads( f.read()))
        for site in f_dict.keys():
            for page in f_dict[site]['page']:
                url = site + page
                if ( url in file_index_mapping.keys()):
                    index = file_index_mapping[url]
                else:
                    file_index_mapping[url] = index = counter
                    counter += 1
                del url
                
                link_arr = list()
                for link in f_dict[site]['page'][page]:
                    url = urlparse(link).netloc + urlparse(link).path
                    if ( url in file_index_mapping.keys()):
                        link_arr.append(file_index_mapping[url])
                    else:
                        link_arr.append(counter)
                        file_index_mapping[url] = counter
                        counter += 1
                    del url
                edges[index] = dict()
                edges[index]['degree'] = len(link_arr)
                edges[index]['links'] = link_arr
                del index

# store the result (edges, file_index_mapping)
edges_file = open('edges', 'w')
for index in edges.keys():
    edges_file.write(str(index) + ' ' + str(edges[index]['degree']) + ' ')
    for link_index in edges[index]['links']:
        edges_file.write(str(link_index) + ' ')
    edges_file.write('\n')
edges_file.close()

json.dump(file_index_mapping, open('file_index_mapping', 'w'))
pass
