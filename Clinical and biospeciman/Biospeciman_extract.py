'''
Extract biospeciman information under sample level, and keep samplet_type, bcr_sample_barcode_bcr_sample_uuid under a "-biospecimen-matrix"
'''
import xml.etree.ElementTree as ET
import pandas as pd
import os

def split_tag(element):
  sep = "}"
  t = element.tag.split(sep, 1)[1]
  return(t)

def biospeciman_list(file):
  samplelist = []
  xml = ET.parse(file)
  root_element = xml.getroot()
  u = root_element[1][8]
  biospecimen_index = [19, 20]
  for sample in u:
    dict_temp = {}
    for i in biospecimen_index:
      ele = sample[i]
      if (type(ele.text) != type(None)) and (ele.text.startswith('\n')):
        dict_temp[split_tag(ele)] = "OMITTED"
      elif type(ele.text) == type(None):
        dict_temp[split_tag(ele)] = "NotApplicable"
      else:
        dict_temp[split_tag(ele)] = ele.text
    #print(dict_temp)
    samplelist.append(dict_temp)
  return(samplelist)


def get_df(link):
  d = biospeciman_list(link)
  #print(d)
  df = pd.DataFrame(d)
  df['bcr_sample_uuid'] = df.bcr_sample_uuid.str.lower()
  return(df)


def biospecimen_matrix(y, main_df):
  src = "/home/yuwang/SuLab/TCGA/Data/Download/" + y + "-Biospecimen"
  for root, dirs, files in os.walk(src):
    for file in files:
      filesrc = os.sep.join([root, file])
      if file.endswith(".xml"):
        df = get_df(filesrc)
        main_df = main_df.append(df)
  return(main_df)

def write_matrix(y):
  main_df = pd.DataFrame()
  main_df = biospecimen_matrix(y, main_df)
  output_path = "/home/yuwang/SuLab/TCGA/Data/Matrix/" + y + "/" + y + '-biospecimen-matrix'
  #bcr_sample_barcode
  main_df = main_df.set_index('bcr_sample_uuid')
  

  #print(main_df)
  main_df.to_csv(output_path + ".csv", sep = '\t')
  main_df = pd.DataFrame()
  print("biospecimen matrix generated:" + y)

if __name__ == '__main__':
  project_list = ['TCGA-ACC', 'TCGA-BLCA', 'TCGA-BRCA', 'TCGA-CESC', 'TCGA-CHOL', 'TCGA-COAD', 'TCGA-DLBC', 'TCGA-ESCA', 'TCGA-GBM', 'TCGA-HNSC', 'TCGA-KICH', 'TCGA-KIRC', 'TCGA-KIRP', 'TCGA-LAML', 'TCGA-LGG', 'TCGA-LIHC', 'TCGA-LUAD', 'TCGA-LUSC', 'TCGA-MESO', 'TCGA-OV', 'TCGA-PAAD', 'TCGA-PCPG', 'TCGA-PRAD', 'TCGA-READ', 'TCGA-SARC', 'TCGA-SKCM', 'TCGA-STAD', 'TCGA-TGCT', 'TCGA-THCA', 'TCGA-THYM', 'TCGA-UCEC', 'TCGA-UCS', 'TCGA-UVM']
  for y in project_list:
    write_matrix(y)
