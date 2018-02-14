'''
Goal: get badic information from gdc api, including: 
"file_id", "case_id", "gender", "year_of_birth", "race", "ethnicity", "year_of_death", "sample_type", "sample_id", "classification_of_tumor", "tumor_grade", "tissue_of_origin", "days_to_last_follow_up", "primary_diagnosis", "tumor_stage", "days_to_birth", "age_at_diagnosis", "vital_status", "morphology", "days_to_death", "prior_malignancy", "progression_or_recurrence"
=> generate a basic-matrix
'''

import requests
import json
import csv
import pandas as pd
import os
url = "https://api.gdc.cancer.gov/files"
root = "/home/yuwang/SuLab/TCGA/Data/Download/"


cols = ["file_id", "case_id", "gender", "year_of_birth", "race", "ethnicity", "year_of_death", "sample_type", "sample_id", "classification_of_tumor", "tumor_grade", "tissue_of_origin", "days_to_last_follow_up", "primary_diagnosis", "tumor_stage", "days_to_birth", "age_at_diagnosis", "vital_status", "morphology", "days_to_death", "prior_malignancy", "progression_or_recurrence"]
rows = []

def file_filter(t):
	fields = [
	"cases.demographic.ethnicity", 
	"cases.demographic.gender",
	"cases.demographic.race",
	"cases.demographic.year_of_birth",
	"cases.demographic.year_of_death",
	"cases.case_id",
	"cases.diagnoses.age_at_diagnosis",
	"cases.diagnoses.classification_of_tumor",
	"cases.diagnoses.days_to_birth",
	"cases.diagnoses.days_to_death",
	"cases.diagnoses.days_to_last_follow_up",
	"cases.diagnoses.morphology",
	"cases.diagnoses.primary_diagnosis",
	"cases.diagnoses.prior_malignancy",
	"cases.diagnoses.progression_or_recurrence",
	"cases.diagnoses.tissue_or_organ_of_origin",
	"cases.diagnoses.tumor_grade",
	"cases.diagnoses.tumor_stage",
	"cases.diagnoses.vital_status",
	"cases.samples.sample_type",
	"cases.samples.sample_id"
	]
	fields = ','.join(fields)
	filters = {
		"op": "and",
		"content":[
			{
			"op": "in",
			"content":{
			"field": "file_id",
			"value": [t]
				}
			}
			]
			}
	params = {
		"filters": json.dumps(filters),
		"fields": fields,
		"format": "JSON",
		#"from": num_count
		}
	return(params)

def clinic_matrix(t):
	r = requests.get(url, params = file_filter(t)).json()
	data = r['data']['hits'][0]
	file_id = data['id']
	case_id = data['cases'][0]['case_id']
	samples = data['cases'][0]['samples']
	try:
		diagnoses = data['cases'][0]['diagnoses']
	except KeyError:
		diagnoses = [{'classification_of_tumor': "NotApplicable", 'tumor_grade': "NotApplicable", 'tissue_or_organ_of_origin': "NotApplicable", 'days_to_last_follow_up': "NotApplicable", 'primary_diagnosis':"NotApplicable", 'tumor_stage': "NotApplicable", 'days_to_birth': "NotApplicable", 'age_at_diagnosis': "NotApplicable", 'vital_status': "NotApplicable", 'morphology': "NotApplicable", 'days_to_death': "NotApplicable", 'prior_malignancy': "NotApplicable", 'progression_or_recurrence': "NotApplicable"}]

	try:
		demographic = data['cases'][0]['demographic']
	except KeyError:
		demographic = {'gender': "NotApplicable", 'year_of_birth': "NotApplicable", 'race': "NotApplicable", 'ethnicity': "NotApplicable", 'year_of_death': "NotApplicable"}

	rows = []
	rows.append([file_id, case_id, *list(demographic.values()), *list(samples[0].values()), *list(diagnoses[0].values())])
	df = pd.DataFrame(rows, columns = cols)
	return(df)

def read_file_list(main_df, y):
	file_list = [x.replace('\n', '') for x in open(root + y + "\\" + y + ".txt").readlines()]
	for i in file_list:
		df = clinic_matrix(i)
		
		main_df = main_df.append(df)
	return(main_df)

def write_matrix(y):
	main_df = pd.DataFrame()
	#os.mkdir("/home/yuwang/SuLab/TCGA/Data/Matrix/" + y )
	#tumor_name = tumor_names[y].replace("['", "").replace("']", "")
	#filedir = root + y
	#os.chdir(filedir)
	main_df = read_file_list(main_df, y)
	#main_df = read_manifest(y, main_df)
	output_path = "/home/yuwang/SuLab/TCGA/Data/Matrix/" + y + "/" + y + '-basic-matrix'
	#if not os.path.exists(output_path):
		#os.makedirs(output_path)
	main_df = main_df.set_index("file_id")
	main_df.to_csv(output_path + ".csv", sep = '\t')
	main_df = pd.DataFrame()
	print(y + ": Basic matrix generated")	


if __name__ == '__main__':
	main_df = pd.DataFrame()
	# get project list
	#project_list = [x.replace('\n', '') for x in open('home\\yuwang\\SuLab\\TCGA\\Script\\Download\\TCGA_project_list.txt').readlines()]
	## get project 
	#with open("/home/yuwang/SuLab/TCGA/Script/Download/TCGA_project_library.txt") as f:
		#tumor_names = dict(x.rstrip().split(None, 1) for x in f)
	#project_list = ['TCGA-ACC', 'TCGA-BLCA', 'TCGA-BRCA', 'TCGA-CESC', 'TCGA-CHOL', 'TCGA-COAD', 'TCGA-DLBC', 'TCGA-ESCA', 'TCGA-GBM', 'TCGA-HNSC', 'TCGA-KICH', 'TCGA-KIRC', 'TCGA-KIRP', 'TCGA-LAML', 'TCGA-LGG', 'TCGA-LIHC', 'TCGA-LUAD', 'TCGA-LUSC', 'TCGA-MESO', 'TCGA-OV', 'TCGA-PAAD', 'TCGA-PCPG', 'TCGA-PRAD', 'TCGA-READ', 'TCGA-SARC', 'TCGA-SKCM', 'TCGA-STAD', 'TCGA-TGCT', 'TCGA-THCA', 'TCGA-THYM', 'TCGA-UCEC', 'TCGA-UCS', 'TCGA-UVM']
	project_list = ['TCGA-UCEC', 'TCGA-UCS', 'TCGA-UVM']

	for y in project_list:
		write_matrix(y)


	