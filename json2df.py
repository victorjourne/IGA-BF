# -*- coding: utf-8 -*-
import os, sys
import pandas as pd
import re

import locale
import datetime
locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')
DATE_FORMAT = "%d %B %Y"

json_path = sys.argv[1]
output_path = sys.argv[2]

print('Read %s json output'% json_path)
df = pd.read_json(json_path)
xlsx_path = json_path.replace('.json','.xlsx')
print('Write %s xlsx output'% xlsx_path)
df['author'] = df['author'].str.replace('Auteur : ','')

df['date'] = df['date'].apply(lambda x: datetime.datetime.strptime(x, DATE_FORMAT).date())

df.to_excel(os.path.join(output_path,xlsx_path), index=False)

#import pdb; pdb.set_trace()
