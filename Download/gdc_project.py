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
# Project filter
def project_filter(num_count, program_name):
	fields = [
	"project_id",
	"disease_type",
	"program.name"
	]

	fields = ','.join(fields)

	filters = {
	"op":"and",
	"content":[
	{
	"op":"in",
	"content":{
	"field":"program.name",
	"value":[program_name]
		}
	}
	]
	}

	
	params = {
		"filters": json.dumps(filters),
		"fields": fields,
		"from": num_count
		}

	return(params)

def files_filter(num_count, project_id):
	fields = [
	"file_id",
	"tags"
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
		"field": "access",
		"value": ["open"]
			}
		},
		{
		"op": "in",
		"content":{
		"field": "analysis.workflow_type",
		"value": ["HTSeq - Counts"]
		}	
		}
		]
	 }
	 #Change data filter => rsem. is the old form of seq data.

	# Here a GET is used, so the filter parameters should be passed as a JSON string.
	params = {
	"filters": json.dumps(filters),
	"fields": fields,
	"format": "JSON",
	"from": num_count
	}
	return(params)

# Get project list and disease 
def project_extract(library, project_hits):
	a = json.loads(json.dumps(project_hits))
	b = {y['project_id']:y['disease_type'] for y in a if 'project_id' in y}
	x = library.update(b)
	return (library)

def file_extract(id_list, project_hits):
	a = json.loads(json.dumps(project_hits))
	for y in a:
		x = id_list.append(y['file_id'])
	return (id_list)

def gdc_pagination(request_data, library, url, extract, filter, gdc_id):
	params_page = request_data['pagination']['page']
	total_page = request_data['pagination']['pages']
	num_count = 0
	while params_page in range(1, total_page+1) and request_data['pagination']['count'] > 0:
		params_page = request_data['pagination']['page']
		num_count = request_data['pagination']['from'] + request_data['pagination']['count']
		request = requests.get(url, params = filter(num_count, gdc_id)).json()
		request_data = request['data']
		request_hits = request_data['hits']
		library = extract(library, request_hits)
	return (library) 	


def gdc_request(library, url, extract, filter, gdc_id):
	gdc_request = requests.get(url, params = filter(0, gdc_id)).json()
	request_data = gdc_request['data']
	library = extract(library, request_data['hits'])
	library = gdc_pagination(request_data, library, url, extract, filter, gdc_id)
	return(library)


def write_project_library(url, program_name):
	library = {} 
	project_library = gdc_request(library, url, project_extract, project_filter, program_name)
	project_list = sorted(project_library)
	#with open('TCGA_project_list.txt', 'w') as t:
	#	for key in project_list:
	#		print("%s" % (key), file = t)
	#with open('TCGA_project_library.txt', 'w') as f:
	#	for key in sorted(project_library):
	# 		print ("%s  %s" % (key, project_library[key]), file = f)
	return(project_list)