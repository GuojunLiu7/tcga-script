import os
import requests
import json
import re
from string import Template

data_dir = "X:\Su Lab\TCGA\Data"

url_http = "https://api.gdc.cancer.gov/"


projects = "projects"
files = "files"
cases ="cases"
annotations = "annotations"
dataa = "data"

url_project = url_http + projects
url_case = url_http + cases
url_data = url_http + dataa
url_files = url_http + files


import gdc_project
'''
['TCGA-ACC', 'TCGA-BLCA', 'TCGA-BRCA', 'TCGA-CESC', 'TCGA-CHOL', 'TCGA-COAD', 'TCGA-DLBC', 'TCGA-ESCA', 'TCGA-GBM', 'TCGA-HNSC', 'TCGA-KICH', 'TCGA-KIRC', 'TCGA-KIRP', 'TCGA-LAML', 'TCGA-LGG', 'TCGA-LIHC', 'TCGA-LUAD', 'TCGA-LUSC', 'TCGA-MESO', 'TCGA-OV', 'TCGA-PAAD', 'TCGA-PCPG', 'TCGA-PRAD', 'TCGA-READ', 'TCGA-SARC', 'TCGA-SKCM', 'TCGA-STAD', 'TCGA-TGCT', 'TCGA-THCA', 'TCGA-THYM', 'TCGA-UCEC', 'TCGA-UCS', 'TCGA-UVM']
'''
project_list = gdc_project.write_project_library(url_project, "TCGA")


os.chdir(data_dir)
folder_template = Template('\Download\$t')
file_template = Template("$t.txt")
data_endpt = "https://api.gdc.cancer.gov/data"
for y in project_list:
	x = folder_template.substitute(t = y)
	z = file_template.substitute(t = y)
	#os.mkdir(data_dir + x)
	os.chdir(data_dir + x)
	id_list = []
	id_list = gdc_project.gdc_request(id_list, url_files, gdc_project.file_extract, gdc_project.files_filter, y)
	with open(z, 'w') as f:
		for key in sorted(id_list):
			print("%s" % (key), file = f)
		#print (sorted(id_list), file = f)
	
	params = {"ids": id_list}

	response = requests.post(data_endpt, data = json.dumps(params), headers = {"Content-Type": "application/json"})

	response_head_cd = response.headers["Content-Disposition"]

	file_name = re.findall("filename=(.+)", response_head_cd)[0]

	with open(file_name, "wb") as output_file:
   		output_file.write(response.content)
	print(y + ": Downloaded")