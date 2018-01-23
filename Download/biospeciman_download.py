import requests
import json
import os
import re

url_files = "https://api.gdc.cancer.gov/files"
data_dir = "X:\Su Lab\TCGA\Data"

def files_filter(num_count, project_id):
	fields = [
	"file_id"
	]
	fields = ','.join(fields)
	filters = {
	"op": "and",
	"content":[
		{
		"op": "in",
		"content":{
		"field": "cases.project.project_id",
		"value": [project_id]
			}
		},
		{
		"op": "in",
		"content":{
		"field": "data_category",
		"value": ['Biospecimen']
			}
		}
		
		]
	 }
	 	# Here a GET is used, so the filter parameters should be passed as a JSON string.
	params = {
	"filters": json.dumps(filters),
	"fields": fields,
	"format": "JSON",
	"from":num_count
	}
	return(params)

import gdc_project

y = "TCGA-BRCA"
#os.mkdir(data_dir + "\\Download\\" + y + "-Biospecimen")
biospeciman_dir = data_dir + "\\Download\\" + y + "-Biospecimen"
os.chdir(data_dir + "\\Download\\" + y + "-Biospecimen")
file_dir = biospeciman_dir + "\\" + y + "-Biospecimen.txt"
biospeciman_list = []
#r = requests.get(url_files, params = files_filter(0, y)).json()

biospeciman_list = gdc_project.gdc_request(biospeciman_list, url_files, gdc_project.file_extract, files_filter, y)
with open(file_dir, 'w') as f:
	for key in sorted(biospeciman_list):
		print("%s" % (key), file = f)
#print(biospeciman_list)

def file_download(list)
	data_endpt = "https://api.gdc.cancer.gov/data"
	params = {"ids": biospeciman_list}
	response = requests.post(data_endpt, data = json.dumps(params), headers = {"Content-Type": "application/json"})
	response_head_cd = response.headers["Content-Disposition"]
	file_name = re.findall("filename=(.+)", response_head_cd)[0]
	with open(file_name, "wb") as output_file:
			output_file.write(response.content)

#file_download(biospeciman_list)			
#print(y + ": Downloaded")

