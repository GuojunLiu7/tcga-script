import xml.etree.ElementTree as ET
import pandas as pd
import os

def split_tag(element):
  sep = "}"
  t = element.tag.split(sep, 1)[1]
  return(t)

def clinical_dict(file):
  tree = ET.parse(file)
  root = tree.getroot()
  mydict = {}
  for element in root:
    value1 = split_tag(element)
    if type(element.text) == type(None):
      mydict[value1] = "N/A"
    elif (type(element.text) != type(None)) and (element.text.startswith('\n') == True):
      mydict[value1] = "Next_level"
    else: 
      mydict[value1] = element.text
    for ele2 in element.findall('.//'):
      value2 = split_tag(element) + "-" + split_tag(ele2)
      if type(ele2.text) == type(None):
        mydict[value2] = "N/A"
      elif (type(ele2.text) != type(None)) and (ele2.text.startswith('\n') == True):
        mydict[value2] = "Next_level"
      else: 
        mydict[value2] = ele2.text
      for ele3 in ele2.findall('.//'):
        value3 = split_tag(element) + "-" + split_tag(ele2) + "-" + split_tag(ele3)
        if type(ele3.text) == type(None):
          mydict[value3] = "N/A"
        elif (type(ele3.text) != type(None)) and (ele3.text.startswith('\n') == True):
          mydict[value3] = "Next_level"
        else: 
          mydict[value3] = ele3.text
        for ele4 in ele3.findall('.//'):
          value4 = split_tag(element) + "-" + split_tag(ele2) + "-" + split_tag(ele3) + "-" + split_tag(ele4)
          if type(ele4.text) == type(None):
            mydict[value4] = "N/A"
          elif (type(ele4.text) != type(None)) and (ele4.text.startswith('\n') == True):
            mydict[value4] = "Next_level"
          else: 
            mydict[value4] = ele4.text
          for ele5 in ele4.findall('.//'):
            value5 = split_tag(element) + "-" + split_tag(ele2) + "-" + split_tag(ele3) + "-" + split_tag(ele4) + "-" + split_tag(ele5)
            if type(ele5.text) == type(None):
              mydict[value5] = "N/A"
            elif (type(ele5.text) != type(None)) and (ele5.text.startswith('\n') == True):
              mydict[value5] = "Next_level"
            else: 
              mydict[value5] = ele5.text

            
  return(mydict)

def get_clinical_df(file):
  d = clinical_dict(file)
  #print(d)
  df = pd.DataFrame([d], columns=d.keys())
  return(df)

def clinical_matrix(y, main_df):
  src = "X:\\Su Lab\\TCGA\\Data\\Download\\" + y + "-Clinical"
  for root, dirs, files in os.walk(src):
    for file in files:
      filesrc = os.sep.join([root, file])
      if file.endswith(".xml"):
        df = get_clinical_df(filesrc)
        main_df = main_df.append(df)
  return(main_df)

def write_clinical_matrix(y):
  main_df = pd.DataFrame()
  main_df = clinical_matrix(y, main_df)
  output_path = "X:\\Su Lab\\TCGA\\Data\\Matrix\\" + y + '-clinical-matrix'
  #bcr_sample_barcode
  main_df = main_df.set_index('patient-bcr_patient_uuid')
  

  #print(main_df)
  main_df.to_csv(output_path + ".csv", sep = '\t')
  main_df = pd.DataFrame()
  print("matrix generated:" + y)

if __name__ == '__main__':
  y = "TCGA-BRCA"
  write_clinical_matrix(y)
  #main_df = pd.DataFrame()
  #main_df = clinical_matrix(y, main_df)
  #print(main_df)
