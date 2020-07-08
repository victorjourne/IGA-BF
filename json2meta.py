# -*- coding: utf-8 -*-
import os, sys, json
import pandas as pd
import re
from pathlib import Path
import locale
import datetime
locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')
DATE_FORMAT = "%d %B %Y"

json_path = sys.argv[1]
output_path = sys.argv[2]

print('Read %s json output'% json_path)
df = pd.read_json(json_path)
for _, row in df.iterrows():
    path_meta =  Path(output_path) / 'meta' / row['file']
    path_meta = path_meta.with_suffix('').with_suffix('.json') # replace extension
    row['date'] =  datetime.datetime.strptime(row['date'], DATE_FORMAT).date()
    row['date'] = str(row['date'])

    row['author'] = row['author'].replace('Auteur : ','')

    row['author'] = re.split(' - |- | -| et ', row['author'])
    if row['author'] != [''] :
        #row['author'] = [{'name': val} for val in row['author']]
        pass
    else:
        row['author'] = []
    #import pdb; pdb.set_trace()
    row['author'] = ', '.join(row['author'])
    with open(str(path_meta) , 'w', encoding='utf-8') as f:
        json.dump(row.to_dict(), f, ensure_ascii=False)
