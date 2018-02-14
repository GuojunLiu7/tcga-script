import xml.etree.ElementTree as ET
import pandas as pd
import os
import json

#clinical_matrix = pd.read_csv(csvdir, sep = '\t', encoding = 'utf-8')
#clinical_matrix = pd.DataFrame(clinical_matrix)

def read_value(number):
  try:
    t = idx_sorted[number]
  except:
    t = None
  return(t)

def write_count(filedir, y):
  counts = {}
  clinical_matrix = pd.read_csv(filedir, sep = '\t', encoding = 'utf-8')
  clinical_matrix = pd.DataFrame(clinical_matrix)
  for col in (clinical_matrix.drop(['bcr_patient_uuid', 'bcr_patient_barcode'], axis=1)):
    t = clinical_matrix[col].value_counts().to_dict()
    counts[col] = t 
  output = "/home/yuwang/SuLab/TCGA/Data/Matrix/" + y + "/" + y +"-" + "clinical-count.json"
  with open(output,"w") as f:
    json.dump(counts,f)
  print(y + ": item counted")


