import re
from datetime import datetime
import os
import time
import pandas as pd

from os.path import isfile, join
from os import listdir

start = time.time()
DBName = 'NA'
data = []
mypath = r"C:\Users\singhs113\Desktop\MQ\logs"
for path, subdirs, files in os.walk(mypath):
    for name in files:
        if re.search(r'(sapappprp..)(.*)', name, re.IGNORECASE) is not None:
            DBName = re.search(r'(sapappprp..)(.*)', name, re.IGNORECASE).group(1)
            f = open(os.path.join(path, name), 'r', encoding='utf-8')
            for i in f.readlines():
                a = ["NA", "NA", "NA", "NA"]
                if re.search(r'\d{4}-\d{2}-\d{2}', i) is not None:
                    d = re.search(r'\d{4}-\d{2}-\d{2}', i).group(0)
                    old_date = datetime.strptime(d, '%Y-%m-%d')
                    new_date = old_date.strftime('%m/%d/%Y')
                    a[0] = new_date
                if re.search(r'\d{2}:\d{2}:\d{2}', i) is not None:
                    a[1] = re.search(r'\d{2}:\d{2}:\d{2}', i).group(0)
                if re.search(r'(\sE[A-Z]{3}R\s)(.*)', i) is not None:
                    a[2] = re.search(r'(\sE[A-Z]{3}R\s)(.*)', i).group(0)
                    # if re.search(r'(Caused by:\s)(.*)',i) is not None:
                    # a[4] = re.search(r'(Caused by:\s)(.*)',i).group(0)
                    a[3] = DBName
                if len(set(a[1:4])) > 1:
                    data.append(a)
            f.close()

print("--Total Time Taken %s mintues" % ((time.time() - start) / 60))





df = pd.DataFrame(data)
df.columns= ["DATE","TIMESTAMP","APP ERROR DETAILS","APPLICATION HOSTNAME"]
df.to_csv("hybrisapp_logs.csv", index=False)

print(df)