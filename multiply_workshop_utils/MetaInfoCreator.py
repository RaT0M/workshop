#!/usr/bin/python

import json
import os
import subprocess
import sys

in_dir = sys.argv[1]
data_type = sys.argv[2]
out_dir = sys.argv[3]
out_name = sys.argv[4]
dir_content = os.listdir(in_dir)
datasets = {}
dataset_list = []
mcd43_h21v09_polygon = 'POLYGON(30.3449669452828 -10.0030362620852, 29.8878502699691 -0.0000385080169377221,' \
                       '40.0118919785422 0.00342024304742925, 40.6239580927438 -9.9998919197506,' \
                       '30.3449669452828 -10.0030362620852)'
for path in dir_content:
    if os.path.isfile(in_dir + '/' + path):
        # result = os.system('sh /home/tonio/snap/bin/gpt Info '+  in_dir + '/'+ path + ' > out.txt')
        result = os.system('sh gpt Info '+  in_dir + '/'+ path + ' > out.txt')
        if result == 0:
            dataset = {}
            dataset['data_type'] = data_type
            dataset['name'] = path
            output = open('out.txt', 'r+')
            for info in output.readlines():
                info = info.replace('\n', '')
                if info.split('=')[0] == 'startTime' or info.split('=')[0] == 'start_time':
                    if not info.split('=')[1] == 'null':
                        dataset['start_time'] = info.split('=')[1]
                if info.split('=')[0] == 'stopTime' or info.split('=')[0] == 'end_time' or \
                        info.split('=')[0] == 'endTime' or info.split('=')[0] == 'stop_time':
                    if not info.split('=')[1] == 'null':
                        dataset['end_time'] = info.split('=')[1]
                if info.split('=')[0] == 'polygon':
                    if not info.split('=')[1] == 'null':
                        dataset['spatial_coverage'] = info.split('=')[1]
                    elif 'h21v09' in path:
                        dataset['spatial_coverage'] = mcd43_h21v09_polygon
            # os.remove('out.txt')
            dataset_list.append(dataset)
datasets['datasets'] = dataset_list
with open(out_dir +'/' + out_name, 'w') as out_file:
    json.dump(datasets, out_file)
