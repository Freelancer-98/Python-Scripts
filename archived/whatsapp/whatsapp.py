import re
import time
import pandas as pd
import dateutil
import matplotlib.pyplot as plt
import unicodecsv as csv

class Whatsapp:
  def __init__(self,file):
    self.filename=file

  def open_file(self):
    x = open(self.filename,'r',encoding="utf8")
    y = x.read()
    content = y.splitlines()
    return content

  def ismessage(self,str):
    result = re.search(r'^[0-9]{2}\/[0-9]{2}\/[0-9]{4},\s[0-9]{2}:[0-9]{2}', str)
    date = ''
    hour = ''
    minute = ''
    name = ''
    if result:
      name_start = str.find("-")+2
      first_colon = str.find(":")
      name_end = str.find(":", first_colon+1)
      if (name_end == -1):
        name_end=len(str)
      name=str[name_start:name_end]
      message=str[name_end+1:]
      date=result.group().split(", ")[0]
      hour=result.group().split(", ")[1].split(":")[0]
      minute=result.group().split(", ")[1].split(":")[1]
    else:
      message=str
    return (date,hour,minute,name,message)

whatsapp=Whatsapp("Whatsapp1.txt")
content=whatsapp.open_file()
dataByDay=[]
dateMapping={}
members=set()
day = 0
date = ''
hour = ''
minute = ''
name = ''
for i in content:
  data = whatsapp.ismessage(i)
  if data[0]!='':
    date = data[0]
    hour = data[1]
    minute = data[2]
    name = data[3]
    if "added" not in name and "changed" not in name and "removed" not in name and "left" not in name and "+" not in name and "group" not in name:
      if name not in members:
        members.add(name)
      # print(date,hour,minute,name,data[-1])
      temp={}
      temp["date"] = date
      temp["day"] = day
      temp["time"] = int(hour)*60+int(minute)
      temp["name"] = name
      temp["message"] = data[-1]


      if date in dateMapping.keys():
        dataByDay.append(temp)
      else:
        day+=1
        # since day is changing need to update
        temp["day"] = day
        dataByDay.append(temp)
        dateMapping[date]=day
# for date in dataByDay.keys():
#   print(date)
for i in members:
  print (i)
# f = open('whatsAppData.csv','w')
# w = csv.DictWriter(f,dataByDay.keys())
# w.writerow(dataByDay)
# f.close()
# print (dataByDay[1])
keys = dataByDay[0].keys()
with open('whatsAppData.csv', 'wb') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(dataByDay)
