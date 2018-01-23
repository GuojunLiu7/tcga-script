import xml.etree.ElementTree as ET


def split_tag(element):
  sep = "}"
  t = element.tag.split(sep, 1)[1]
  return(t)

def biospeciman_list(file):
  samplelist = []
  xml = ET.parse(file)
  root_element = xml.getroot()
  u = root_element[1][8]
  for sample in u:
    dict_temp = {}
    for element in sample:
      dict_temp[split_tag(element)] = element.text
    #print(dict_temp)
    samplelist.append(dict_temp)
  return(samplelist)

import pandas as pd
d = biospeciman_list('test2.xml')
#print(d)
df = pd.DataFrame(d)
print(df)



