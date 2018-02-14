import pandas as pd
import numpy as np
import os


root = "/home/yuwang/SuLab/TCGA/Data/Download/"

def files_filter(file_id):
	fields = [
	"annotations.case_id",
	]
	fields = ','.join(fields)
	filters = {
	"op": "and",
	"content":[
		{
		"op": "in",
		"content":{
		"field": "file_id",
		"value": [file_id]
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

def read_manifest(y, main_df):
	file = root + y + "/MANIFEST.txt"
	t = pd.read_csv(file, sep = '\t', encoding = 'utf-8')
	#total_count = t.shape[0]
	t = t.values
	for i in t:
		fuuid = i[0]
		fname = root + y + "/" + i[1]
		fdir = fname[:-3]
		df = pd.read_csv(fdir, sep = '\t', names = ["gene_id", fuuid])
		df = df.rename(columns = {'gene_id':'index'})
		df = df.T
		header = df.iloc[0]
		df = df[1:]
		df.columns = header
		df = df.reset_index()
		df = df.rename(columns = {'index':'file_id'})
		#print(fuuid + " ：appended")
		main_df = main_df.append(df)
	return(main_df)


if __name__ == '__main__':
	# get project list
	#project_list = [x.replace('\n', '') for x in open('X:\\Su Lab\\TCGA\\Script\\Download\\TCGA_project_list.txt').readlines()]
	# get project 
	#with open("X:\\Su Lab\\TCGA\\Script\\Download\\TCGA_project_library.txt") as f:
	#	tumor_names = dict(x.rstrip().split(None, 1) for x in f)
	# 'TCGA-OV', 'TCGA-PAAD', 'TCGA-PCPG', 'TCGA-PRAD', 'TCGA-READ', 'TCGA-SARC', 'TCGA-SKCM', 'TCGA-STAD', 'TCGA-TGCT', 'TCGA-THCA', 'TCGA-THYM', 'TCGA-UCEC', 'TCGA-UCS', 'TCGA-UVM'
	project_list = ['TCGA-ACC','TCGA-OV', 'TCGA-PAAD', 'TCGA-PCPG', 'TCGA-PRAD', 'TCGA-READ', 'TCGA-SARC', 'TCGA-SKCM', 'TCGA-STAD', 'TCGA-TGCT', 'TCGA-THCA', 'TCGA-THYM', 'TCGA-UCEC', 'TCGA-UCS', 'TCGA-UVM']
	for y in project_list:
		
		main_df = pd.DataFrame()
		#tumor_name = tumor_names[y].replace("['", "").replace("']", "")
		filedir = root + y
		os.chdir(filedir)
		main_df = read_manifest(y, main_df)
		output_path = "/home/yuwang/SuLab/TCGA/Data/Matrix/" + y + '-gene-matrix'
		#if not os.path.exists(output_path):
			#os.makedirs(output_path)
		
		#main_df = main_df.reset_index()
		#main_df = main_df.rename(columns = {'gene_id':'file_id'})
		

		#print(main_df)
		main_df.to_csv(output_path + ".csv", sep = '\t')
		main_df = pd.DataFrame()
		print("Gene matrix generated:" + y)

'''	
		





file = "X:\\Su Lab\\TCGA\\Data\\Download\\" + "TCGA-ACC" + "\\MANIFEST.txt"
Y = pd.DataFrame()
t = pd.read_csv(file, sep = '\t', encoding ='utf-8')
t = t.values
#for y in t:
#	print(y[0], y[1])


t1 = "X:\\Su Lab\\TCGA\\Data\\Download\\" + "TCGA-ACC\\" + t[0][1]
t1 = t1[:-3]
x1 = "test1"
m1 = pd.read_csv(t1, sep = '\t', names = ["gene_id", x1])
m1 = m1.set_index("gene_id")
print(m1)
Y = Y.join(m1, how = "outer")

t2 = "X:\\Su Lab\\TCGA\\Data\\Download\\" + "TCGA-ACC\\" + t[1][1]
t2 = t2[:-3]
x2 = "test2"
m2 = pd.read_csv(t2, sep = '\t', names = ["gene_id", x2])
m2 = m2.set_index("gene_id")
print()
Y = Y.join(m2, how = "outer")
#t = t.shape[0]
print(Y)

'''

