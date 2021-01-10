import re
import os
import time
import pandas as pd
from datetime import datetime

start = time.time()
dfError = pd.DataFrame()
APPServer = 'NA'
DBFail = 'NA'
mypath = r"C:\Users\singhs113\Desktop\crmlogs\logs"
for path, subdirs, files in os.walk(mypath):
    for name in files:
        if re.search(r'(dev_..)(.*)', name, re.IGNORECASE) is not None:
            # if re.search(r'(dev_..)(.*)', name, re.IGNORECASE) is not None:
            #     WorkProcess = re.search(r'(dev_..)(.*)', name, re.IGNORECASE).group(2).rstrip('.')

        #if re.search(r'dev_.*.log$', name, re.IGNORECASE) is not None:
            # WorkProcess = [name]
            print(name)
            # if re.search(r'(>sapcrmprp...)(.*?\.)', name, re.IGNORECASE) is not None:
            # #if re.search(r'(dev_..)(.*?\.)', name, re.IGNORECASE) is not None:
            #     APPServer = re.search(r'(>sapcrmprp...)(.*?\.)', name, re.IGNORECASE).group(2).rstrip('.')
            #     print("Appserver Name = " + APPServer)
            f = open(os.path.join(path, name), 'r')
            data = f.read()

            if re.search(r'(Destination: )(\w+)', data, re.IGNORECASE) is not None:
                APPServer = re.search(r'(Destination: )(\w+)', data, re.IGNORECASE).group(2)
            pattern = "([a-zA-Z]{3} [a-zA-Z]{3} \d{2} \d{2}:\d{2}:\d{2} \d{4})(.*?)(?=[a-zA-Z]{3} [a-zA-Z]{3} \d{2} \d{2}:\d{2}:\d{2} \d{4})"
            mappedFile = re.findall(pattern, data, re.DOTALL)

            if re.search(r'(Connect to database failed)', data, re.IGNORECASE) is not None:
                DBFail = re.search(r'(Connect to database failed)', data, re.IGNORECASE).group(0)
            pattern = "([a-zA-Z]{3} [a-zA-Z]{3} \d{2} \d{2}:\d{2}:\d{2} \d{4})(.*?)(?=[a-zA-Z]{3} [a-zA-Z]{3} \d{2} \d{2}:\d{2}:\d{2} \d{4})"
            mappedFile = re.findall(pattern, data, re.DOTALL)

            # if re.search(r'(Destination: )(\w+)', data, re.IGNORECASE) is not None:
            #     APPServer = re.search(r'(Destination: )(\w+)', data, re.IGNORECASE).group(2)
            # pattern = "([a-zA-Z]{3} [a-zA-Z]{3} \d{2} \d{2}:\d{2}:\d{2} \d{4})(.*?)(?=[a-zA-Z]{3} [a-zA-Z]{3} \d{2} \d{2}:\d{2}:\d{2} \d{4})"
            # mappedFile = re.findall(pattern, data, re.DOTALL)

            print(DBFail)


            def get_errors(x):
                a = []
                string = ''.join(x)


                if re.search(r'[a-zA-Z]{3} [a-zA-Z]{3} \d{2} \d{2}:\d{2}:\d{2} \d{4}', string, re.DOTALL):
                    timestamp = re.search(r'[a-zA-Z]{3} [a-zA-Z]{3} \d{2} \d{2}:\d{2}:\d{2} \d{4}', string,
                                          re.DOTALL).group(0)
                    old_date = datetime.strptime(timestamp, "%c")
                    new_date = old_date.strftime("%m/%d/%Y")
                    new_time = old_date.strftime("%X")
                #if re.search(r'(ERROR)', string, re.DOTALL) is not None:
                if re.search(r'(ERROR)(\w+)', string, re.DOTALL) is not None:
                #if re.search(r'(WARNING:.*?)(?=ORA-\d+)', string, re.DOTALL) is not None:
                    a = ["NA", "NA", "NA", "NA", "NA"]
                    a[0] = new_date
                    a[1] = new_time
                    a[2] = APPServer
                    a[3] = re.search(r'(ERROR)(\w+)', string, re.DOTALL).group(0)
                    a[4] = re.search(r'(WARNING:.*?)', string, re.DOTALL)
                    #a[5] = WorkProcess
                    # a[3] = re.search(r'(ERROR.*?)(ORA-\d+)', string, re.DOTALL).group(1)
                    # a[4] = re.search(r'(ERROR.*?)(ORA-\d+)', string, re.DOTALL).group(2)
                return a


            out = map(get_errors, mappedFile)
            out = list(filter(None, out))
            f.close()
            error = pd.DataFrame(out, columns=["DATE", "TIME", "APPSERVER", "ERRORS", "WARNINGS"])
            dfError = dfError.append(error, ignore_index=True)  # print(len(out[0]))
# w = datetime.now().time()
# now = datetime. now().time()


now1 = datetime.now()

current_time = now1.strftime("%H:%M:%S")
# print("Current Time =", current_time)


# print("now =", now)
# print("type(now) =", type(now))
print("Extraction completed at " + current_time)
print("--Total Time Taken %s mintues" % ((time.time() - start) / 60))



dfError
print(dfError)
#
# now = datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
# with pd.ExcelWriter("Crmerrors_"+now+".xlsx") as writer:
#     dfError.to_excel(writer, sheet_name='Errors', engine='xlsxwriter', index=False)