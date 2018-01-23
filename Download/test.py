# goal: from file id request clinical and biospeciman file

import requests
import json
import pprint
url = "https://api.gdc.cancer.gov/files"

def files_filter(project_id):
	fields = [
	"cases.case_id",
	]
	fields = ','.join(fields)
	filters = {
	"op": "and",
	"content":[
		{
		"op": "in",
		"content":{
		"field": "file_id",
		"value": [project_id]
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
	}
	return(params)

def cases_filter(project_id):

	filters = {
	"op": "and",
	"content":[
		{
		"op": "in",
		"content":{
		"field": "cases.case_id",
		"value": [project_id]
			}
		}
		]
	 }
	 #Change data filter => rsem. is the old form of seq data.

	# Here a GET is used, so the filter parameters should be passed as a JSON string.
	params = {
	"filters": json.dumps(filters),
	"format": "JSON",
	"from":10
	}
	return(params)
file_id = "00156c51-2686-4736-88c1-c30c81ec0a12"
r = requests.get(url, params = files_filter(file_id)).json()
m = r['data']['hits'][0]['cases'][0]['case_id']
t = requests.get(url, params = cases_filter(m)).json()
pprint.pprint(t)