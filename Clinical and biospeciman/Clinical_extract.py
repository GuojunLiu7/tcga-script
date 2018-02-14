'''
Goal:
Extract clinical information into clinical matrix,
specific filter for each project is documented clinical_file_extract_filter.py
run clinical_count
'''

import xml.etree.ElementTree as ET
import pandas as pd
import os
import clinical_file_extract_filter
import Clinical_count

def get_clinical_df(file, y):
  tree = ET.parse(file)
  root = tree.getroot()
  d = clinical_file_extract_filter.extract_filter(y, root)
  df = pd.DataFrame([d], columns=d.keys())

  df['bcr_patient_uuid'] = df.bcr_patient_uuid.str.lower()
  return(df)

def clinical_matrix(y, main_df):
  src = "/home/yuwang/SuLab/TCGA/Data/Download/" + y + "-Clinical"
  for root, dirs, files in os.walk(src):
    for file in files:
      filesrc = os.sep.join([root, file])
      if file.endswith(".xml"):
        df = get_clinical_df(filesrc, y)
        main_df = main_df.append(df)

  return(main_df)

def write_clinical_matrix(y):
  main_df = pd.DataFrame()
  main_df = clinical_matrix(y, main_df)
  output_path = "/home/yuwang/SuLab/TCGA/Data/Matrix/" + y + "/" + y + '-clinical-matrix'
  main_df = main_df.set_index('bcr_patient_uuid')
  main_df.to_csv(output_path + ".csv", sep = '\t')
  main_df = pd.DataFrame()
  print(y + ": Clinical matrix generated")
  return(output_path)

if __name__ == '__main__':
  #project_list = ['TCGA-ACC', 'TCGA-BLCA', 'TCGA-BRCA', 'TCGA-CESC', 'TCGA-CHOL', 'TCGA-COAD', 'TCGA-DLBC', 'TCGA-ESCA', 'TCGA-GBM', 'TCGA-HNSC', 'TCGA-KICH', 'TCGA-KIRC', 'TCGA-KIRP', 'TCGA-LAML', 'TCGA-LGG', 'TCGA-LIHC', 'TCGA-LUAD', 'TCGA-LUSC', 'TCGA-MESO', 'TCGA-OV', 'TCGA-PAAD', 'TCGA-PCPG', 'TCGA-PRAD', 'TCGA-READ', 'TCGA-SARC', 'TCGA-SKCM', 'TCGA-STAD', 'TCGA-TGCT', 'TCGA-THCA', 'TCGA-THYM', 'TCGA-UCEC', 'TCGA-UCS', 'TCGA-UVM']
  #project_list = ['TCGA-ACC', 'TCGA-BLCA', 'TCGA-CESC']
  #for y in project_list:
  y = "TCGA-UVM"
  filedir = write_clinical_matrix(y) + ".csv"
  Clinical_count.write_count(filedir, y)
