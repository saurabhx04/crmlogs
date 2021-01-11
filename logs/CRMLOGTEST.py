import re
import os
import time
import pandas as pd
from datetime import datetime

start = time.time()
dfError = pd.DataFrame()
APPServer = 'NA'
DBFail = 'NA'
ErrorMSG = 'NA'
WarnMSG = 'NA'
wp = 'NA'
PID = 'NA'

mypath = r"C:\Users\singhs113\projects\crmlogs\logs"
for path, subdirs, files in os.walk(mypath):
    # With this for loop getting work process names and puttinh it into name variable

    for name in files:
        if re.search(r'(dev_..)(.*)', name, re.IGNORECASE) is not None:

            print("Reading Work Process files = "+ name)
            f = open(os.path.join(path, name), 'r')
            data = f.read()

            # With this if statement getting Application server names and putting it in to APPServer variable
            # Pattern is variable where where we are putting a logic where it captures the data between
            # 2 timestamps and saving into data variable

            if re.search(r'(Destination: )(\w+)', data, re.IGNORECASE) is not None:
                APPServer = re.search(r'(Destination: )(\w+)', data, re.IGNORECASE).group(2)
            pattern = "([a-zA-Z]{3} [a-zA-Z]{3} \d{2} \d{2}:\d{2}:\d{2} \d{4})(.*?)(?=[a-zA-Z]{3} [a-zA-Z]{3} \d{2} \d{2}:\d{2}:\d{2} \d{4})"
            mappedFile = re.findall(pattern, data, re.DOTALL)

            if re.search(r'(Connect to database failed)', data, re.IGNORECASE) is not None:
                DBFail = re.search(r'(Connect to database failed)', data, re.IGNORECASE).group(0)
            pattern = "([a-zA-Z]{3} [a-zA-Z]{3} \d{2} \d{2}:\d{2}:\d{2} \d{4})(.*?)(?=[a-zA-Z]{3} [a-zA-Z]{3} \d{2} \d{2}:\d{2}:\d{2} \d{4})"
            mappedFile = re.findall(pattern, data, re.DOTALL)

            print(DBFail)

            # searching and saving Process ID in PID variable

            if re.search(r'(pid)(\s+)(\d+)', data, re.DOTALL):
                PID = re.search(r'(pid)(\s+)(\d+)',data,re.DOTALL).group(3)

            print("PID =" + PID)

            # get_errors function is searching through the pattern and formatting timestamps and getting all the
            # errors and warnings , timestamps, PID , Work process names and saving it to the List a and
            # returning the same through the function.

            def get_errors(x):
                a = []
                string = ''.join(x)
                WarnMSG = 'NA'

                if re.search(r'[a-zA-Z]{3} [a-zA-Z]{3} \d{2} \d{2}:\d{2}:\d{2} \d{4}', string, re.DOTALL):
                    timestamp = re.search(r'[a-zA-Z]{3} [a-zA-Z]{3} \d{2} \d{2}:\d{2}:\d{2} \d{4}', string,
                                          re.DOTALL).group(0)
                    old_date = datetime.strptime(timestamp, "%c")
                    new_date = old_date.strftime("%m/%d/%Y")
                    new_time = old_date.strftime("%X")

                if re.search(r'(\** ERROR =>)', string, re.DOTALL) is not None:

                    ErrorMSG = re.search(r'(\** ERROR =>)(.*)', string, re.DOTALL).group(0)
                    if re.search(r'(\** WARNING =>)', string, re.DOTALL) is not None:
                        ErrorMSG = re.search(r'(\** WARNING =>)(.*)', string, re.DOTALL).group(0)


                    a = ["NA", "NA", "NA", "NA", "NA", "NA"]
                    a[0] = new_date
                    a[1] = new_time
                    a[2] = name
                    a[3] = PID
                    a[4] = APPServer
                    a[5] = ErrorMSG
                    #a[6] = WarnMSG

                return a


            # Mapping and putting all the data in Dataframe

            out = map(get_errors, mappedFile)
            out = list(filter(None, out))
            f.close()
            error = pd.DataFrame(out, columns=["DATE", "TIME", "WORK PROCESS", "PID", "APPSERVER", "ERRORS/WARNINGS"])
            dfError = dfError.append(error, ignore_index=True)  # print(len(out[0]))


# Just calculating and printing the execution time of this code and printing into the console

now1 = datetime.now()
current_time = now1.strftime("%H:%M:%S")
print("Extraction completed at " + current_time)
print("--Total Time Taken %s mintues" % ((time.time() - start) / 60))

dfError

print(dfError)

# Putting the same data frame above and getting the output into the excel file.

now = datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
with pd.ExcelWriter("Crmerrors_"+now+".xlsx") as writer:
    dfError.to_excel(writer, sheet_name='Errors', engine='xlsxwriter', index=False)