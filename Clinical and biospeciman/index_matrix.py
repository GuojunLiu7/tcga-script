import requests
import json
import csv
import pandas as pd

url = "https://api.gdc.cancer.gov/files"
root = "X:\\Su Lab\\TCGA\\Data\\Download\\"


cols = ["file_id", "case_id", "sample_id"]
rows = []

def file_filter(t):
	fields = [
	"cases.case_id",
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
	sample_id = data['cases'][0]['samples'][0]['sample_id']
	rows = []
	rows.append([file_id, case_id, sample_id])
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
	#tumor_name = tumor_names[y].replace("['", "").replace("']", "")
	#filedir = root + y
	#os.chdir(filedir)
	main_df = read_file_list(main_df, y)
	#main_df = read_manifest(y, main_df)
	output_path = "X:\\Su Lab\\TCGA\\Data\\Matrix\\" + y + '-index-matrix'
	#if not os.path.exists(output_path):
		#os.makedirs(output_path)
	main_df = main_df.set_index("file_id")
	main_df.to_csv(output_path + ".csv", sep = '\t')
	main_df = pd.DataFrame()
	print("index matrix generated:" + y)	


if __name__ == '__main__':
	#main_df = pd.DataFrame()
	# get project list
	#project_list = [x.replace('\n', '') for x in open('X:\\Su Lab\\TCGA\\Script\\Download\\TCGA_project_list.txt').readlines()]
	#project_list = ['TCGA-SARC', 'TCGA-SKCM', 'TCGA-STAD', 'TCGA-TGCT', 'TCGA-THCA', 'TCGA-THYM', 'TCGA-UCEC', 'TCGA-UCS', 'TCGA-UVM']
	## get project 
	#with open("X:\\Su Lab\\TCGA\\Script\\Download\\TCGA_project_library.txt") as f:
		#tumor_names = dict(x.rstrip().split(None, 1) for x in f)
	
	y = "TCGA-BRCA"
	main_df = write_matrix(y)
	#print(main_df)
	'''
	y = "TCGA-BRCA"
	file_list = [x.replace('\n', '') for x in open(root + y + "\\" + y + ".txt").readlines()]
	for i in file_list:
		df = clinic_matrix(i)
		print(df)
	'''


	