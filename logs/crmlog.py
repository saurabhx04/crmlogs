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
daaa = 'NA'
mypath = r"C:\Users\singhs113\Desktop\crmlogs\logs"
for path, subdirs, files in os.walk(mypath):
    for name in files:
        if re.search(r'(dev_..)(.*)', name, re.IGNORECASE) is not None:
            DBName = re.search(r'(dev_..)(.*)', name, re.IGNORECASE).group(1)
            f = open(os.path.join(path, name), 'r', encoding='utf-8')
            for i in f.readlines():
                if re.search(r'[a-zA-Z]{3} [a-zA-Z]{3} \d{2} \d{2}:\d{2}:\d{2} \d{4}', i):
                    timestamp = re.search(r'[a-zA-Z]{3} [a-zA-Z]{3} \d{2} \d{2}:\d{2}:\d{2} \d{4}',i).group(0)
                    old_date = datetime.strptime(timestamp, "%c")
                    new_date = old_date.strftime("%m/%d/%Y")
                    new_time = old_date.strftime("%X")
                    a = ["NA", "NA", "NA", "NA"]
                #if re.search(r'\d{4}-\d{2}-\d{2}', i) is not None:
                # if re.search(r'\w{3}\s\w{3}\s\d{1}\s\d{2}:\d{2}:\d{2}\s\d{4}', i) is not None:
                #     d = re.search(r'\w{3}\s\w{3}\s\d{1}\s\d{2}:\d{2}:\d{2}\s\d{4}', i).group(0)
                #     daaa = d
                #     old_date = datetime.strptime(d, '%Y-%m-%d')
                #     new_date = old_date.strftime('%m/%d/%Y')
                    a[0] = new_date
                    # print(d)
                    # print(old_date)
                if re.search(r'\d{error}', i) is not None:
               #if re.search(r'\d{2}:\d{2}:\d{2}', i) is not None:
                    a[1] = re.search(r'\d{error}:\d{2}:\d{2}', i).group(0)
                    # print(a[1])
                if re.search(r'\d{sapcrpprp...}', i) is not None:
                    a[2] = re.search(r'(\sE[A-Z]{3}R\s)(.*)', i).group(0)
                    # if re.search(r'(Caused by:\s)(.*)',i) is not None:
                    # a[4] = re.search(r'(Caused by:\s)(.*)',i).group(0)
                    a[3] = DBName
                    if len(set(a[1:4])) > 1:
                    data.append(a)
            f.close()

print("--Total Time Taken %s mintues" % ((time.time() - start) / 60))
print(daaa)
print(old_date)

#print(data)

# df = pd.DataFrame(data)
# df.columns = ["DATE", "TIMESTAMP", "APP ERROR DETAILS", "APPLICATION HOSTNAME"]
# df.to_csv("crm_logs.csv", index=False)
