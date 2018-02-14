'''
No Plot, only matrix
'''
from __future__ import print_function
import pandas as pd
import numpy as np

import os
import json
#import seaborn as sns
from lifelines import KaplanMeierFitter
from lifelines.statistics import logrank_test
from pandas import ExcelWriter

cols = ["gene", "subgroup", "total_number", "favorable_5_year", "favorable_10_year", "logrank_P"]
limit = 10
def filedir(y, key):
	root = "/home/yuwang/SuLab/TCGA/Data/Matrix/"
	filedir = root + y + "/" + y + "-" + key + "-matrix.csv"
	return(filedir)
def is_number(s):
	if pd.isnull(s):
		return False
	else:
		try:
			float(s)
			return True
		except ValueError:
			return False
		except TypeError:
			return False
def event(c):
	if c['vital_status'] == "dead":
		return 1
	elif c['vital_status'] == "alive":
		return 0
def duration(c):
	if is_number(c['days_to_death']) == True:
		t = 12*(float(c['days_to_death'])*4/(365*3 + 366))
		return t
	elif is_number(c['year_of_birth']) == True and is_number(c['age_at_diagnosis']) == True and is_number(c['days_to_death']) == False:
		t = 12*(2018 - float(c['year_of_birth']) - (float(c['age_at_diagnosis'])*4/(365*3 + 366)))
		return t
	else:
		return "NotApplicable"
def reshape_matrix_for_km(matrix):
	matrix['duration'] = matrix.apply(duration, axis = 1)
	matrix['event'] = matrix.apply(event, axis = 1)
	try:
		matrix = matrix[matrix['duration']!="NotApplicable"]
	except:
		matrix = matrix
	return(matrix)


def kmplot(df_high, df_low):
	kmf_high = KaplanMeierFitter()
	kmf_low = KaplanMeierFitter()
	try:
		kmf_high.fit(durations = df_high.duration, event_observed = df_high.event, label = 'High: n = ' + str(len(df_high)))
		kmf_low.fit(durations = df_low.duration, event_observed = df_low.event, label = "Low: n = " + str(len(df_low)))
	except ValueError:
		return("NA", "0", "0", "0", "0")

	statistics_result = logrank_test(df_high.duration, df_low.duration, event_observed_A = df_high.event, event_observed_B = df_low.event)
	p_value = statistics_result.p_value
                                       
	hm5 = kmf_high.predict(60)
	hm10 = kmf_high.predict(120)
	lm5 = kmf_low.predict(60)
	lm10 = kmf_low.predict(120)
	return(p_value, hm5, hm10, lm5, lm10)
	
def divide_into_two(gene_matrix, index_matrix, t):
	specific_gene_matrix = gene_matrix[['bcr_sample_barcode', t]]
	key = ['bcr_sample_barcode']
	in1 = index_matrix.set_index(key).index
	in2 = specific_gene_matrix.set_index(key).index
	total_number = len(index_matrix)
	specific_gene_matrix = specific_gene_matrix[in2.isin(in1)]
	gene_cutoff = specific_gene_matrix[t].quantile(0.5)
	high_index = specific_gene_matrix[specific_gene_matrix[t] > gene_cutoff]
	low_index = specific_gene_matrix[specific_gene_matrix[t] < gene_cutoff]
	ihigh = high_index.set_index(key).index
	ilow = low_index.set_index(key).index
	df_high = index_matrix[in1.isin(ihigh)]
	df_low = index_matrix[in1.isin(ilow)]
	#print(gene_cutoff)
	return(df_high, df_low, total_number)

def survival_compare(h, l):
	if h>l:
		return("high")
	elif h<l:
		return("low")
	else:
		return("NA")

def save_fig(y, summary_index, total_matrix, gene_matrix, t, ARS, plottitle, filetitle, tumor_name):
	df_high, df_low, total_number = divide_into_two(gene_matrix, total_matrix, t)

	p_value, hm5, hm10, lm5, lm10 = kmplot(df_high, df_low)
	if hm10 > lm10:
		p_value = p_value
	if hm10 < lm10:
		p_value = 0 - p_value
	favorable5y = survival_compare(hm5, lm5)
	favorable10y = survival_compare(hm10, lm10)
	df = pd.DataFrame()
	rows = []
	rows.append([ARS, plottitle, total_number, favorable5y, favorable10y, p_value])
	df = pd.DataFrame(rows, columns = cols)
	df['project'] = y
	df['disease'] = tumor_name
	summary_index = summary_index.append(df)
	
	return(summary_index)

	
def extract_filter(y, t, ARS, total_matrix, summary_index, tumor_name):
	matrix_normal = total_matrix[total_matrix['sample_type'] == "Solid Tissue Normal"]
	if len(matrix_normal) > limit:
		summary_index = save_fig(y, summary_index, matrix_normal, gene_matrix, t, ARS, "Solid Tissue Normal", "normal_tissue", tumor_name)

	matrix_meta = total_matrix[total_matrix['sample_type'] == "Metastatic"]
	if len(matrix_meta) > limit:
		summary_index = save_fig(y, summary_index, matrix_meta, gene_matrix, t, ARS, "Metastatic", "metastatic", tumor_name)	
	
	# primary tumor
	matrix_primary = total_matrix[total_matrix['sample_type'] == "Primary Tumor"]
	if y != "TCGA-LAML":
		if len(matrix_primary) > limit:
			summary_index = save_fig(y, summary_index, matrix_primary, gene_matrix, t, ARS, "Primary Tumor", "primary_tumor", tumor_name)
	else:
		matrix_primary = total_matrix[total_matrix['sample_type'] == "Primary Blood Derived Cancer - Peripheral Blood"]
		if len(matrix_primary) > limit:
			summary_index = save_fig(y, summary_index, matrix_primary, gene_matrix, t, ARS, "Primary Blood Derived Cancer", "primary_blood_cancer", tumor_name)

	# ============================================================
	matrix_male = matrix_primary[matrix_primary['gender'] == "male"]
	if len(matrix_male) > limit:
		if y == "TCGA-LAML":
			summary_index = save_fig(y, summary_index, matrix_male, gene_matrix, t, ARS, "Primary Blood Derived Cancer: Male", "primary_blood_cancer_gender_male", tumor_name)
		else:
			summary_index = save_fig(y, summary_index, matrix_male, gene_matrix, t, ARS, "Primary Tumor: Male", "primary_tumor_gender_male", tumor_name)
	matrix_female = matrix_primary[matrix_primary['gender'] == "female"]
	if len(matrix_female) > limit:
		if y == "TCGA-LAML":
			summary_index = save_fig(y, summary_index, matrix_female, gene_matrix, t, ARS, "Primary Blood Derived Cancer: Female", "primary_blood_cancer_gender_female", tumor_name)
		else:
			summary_index = save_fig(y, summary_index, matrix_female, gene_matrix, t, ARS, "Primary Tumor: Female", "primary_tumor_gender_female", tumor_name)
	#=====================================
	matrix_i = matrix_primary[matrix_primary['tumor_stage'].str.startswith('stage i') == True]
	matrix_i = matrix_i[matrix_i['tumor_stage'].str.startswith('stage ii') == False]
	matrix_i = matrix_i[matrix_i['tumor_stage'].str.startswith('stage iv') == False]
	if len(matrix_i) > limit:
		if y == "TCGA-LAML":
			summary_index = save_fig(y, summary_index, matrix_i, gene_matrix, t, ARS, "Primary Blood Derived Cancer: Stage I", "primary_blood_cancer_stage_i", tumor_name)
		else:
			summary_index = save_fig(y, summary_index, matrix_i, gene_matrix, t, ARS, "Primary Tumor: Stage I", "primary_tumor_stage_i", tumor_name)
	matrix_ii = matrix_primary[matrix_primary['tumor_stage'].str.startswith('stage ii') == True]
	matrix_ii = matrix_ii[matrix_ii['tumor_stage'].str.startswith('stage iii') == False]
	if len(matrix_ii) > limit:
		if y == "TCGA-LAML":
			summary_index = save_fig(y, summary_index, matrix_ii, gene_matrix, t, ARS, "Primary Blood Derived Cancer: Stage II", "primary_blood_cancer_stage_ii", tumor_name)
		else:
			summary_index = save_fig(y, summary_index, matrix_ii, gene_matrix, t, ARS, "Primary Tumor: Stage II", "primary_tumor_stage_ii", tumor_name)	
	matrix_iii = matrix_primary[matrix_primary['tumor_stage'].str.startswith('stage iii') == True]
	if len(matrix_iii) > limit:
		if y == "TCGA-LAML": 
			summary_index = save_fig(y, summary_index, matrix_iii, gene_matrix, t, ARS, "Primary Blood Derived Cancer: Stage III", "primary_blood_cancer_stage_iii", tumor_name)
		else:
			summary_index = save_fig(y, summary_index, matrix_iii, gene_matrix, t, ARS, "Primary Tumor: Stage III", "primary_tumor_stage_iii", tumor_name)

	matrix_iv = matrix_primary[matrix_primary['tumor_stage'].str.startswith('stage iv') == True]
	if len(matrix_iv) > limit:
		if y == "TCGA-LAML":
			summary_index = save_fig(y, summary_index, matrix_iv, gene_matrix, t, ARS, "Primary Blood Derived Cancer: Stage IV", "primary_blood_cancer_stage_iv", tumor_name)
		else:
			summary_index = save_fig(y, summary_index, matrix_iv, gene_matrix, t, ARS, "Primary Tumor: Stage IV", "primary_tumor_stage_iv", tumor_name)


	# =========from count file
	with open("/home/yuwang/SuLab/TCGA/Data/Matrix/" + y + "/" + y + "-clinical-count.json") as json_file:
		d = json.load(json_file)
		for ele in d:
			if ("first_degree_relative" not in ele) and ("year" not in ele):
				category = d[ele]
				for item in category:
					if (category[item] > limit) and (item != "NotApplicable") and (len(category) < 10):
						try:
							matrix_ele = matrix_primary[matrix_primary[ele] == item]
							if y == "TCGA-LAML":
								summary_index = save_fig(y, summary_index, matrix_ele, gene_matrix, t, ARS, ("Primary Blood Derived Cancer: " + ele.replace("_", " ").title() + " " + item.title()), "primary_blood_cancer_"+(ele.replace(" ", "_").replace("/", "_").replace("<", "less_than").replace("=", "").replace(">", "more_than").replace(":","_") + "_" + (item.replace(" ", "_").replace("/", "_").replace("<", "less_than").replace("=", "").replace(">", "more_than").replace(":","_")).lower()), tumor_name)
							else:
								summary_index = save_fig(y, summary_index, matrix_ele, gene_matrix, t, ARS, ("Primary Tumor: " + ele.replace("_", " ").title() + " " + item.title()), "primary_tumor_" + (ele.replace(" ", "_").replace("/", "_").replace("<", "less_than").replace("=", "").replace(">", "more_than").replace(":","_") + "_" + (item.replace(" ", "_").replace("/", "_").replace("<", "less_than").replace("=", "").replace(">", "more_than").replace(":","_")).lower()), tumor_name)

						except TypeError:
							continue
	return(summary_index)


def write_index(y, summary_index):
	
	with open("/home/yuwang/SuLab/TCGA/Data/Plot/" + "genelist.txt") as f:
	    for line in f:
	       (ARS, t) = line.split()
	       summary_index = extract_filter(y, t, ARS, total_matrix, summary_index, tumor_name)
	       
	return(summary_index)

if __name__ == '__main__':
	# project_list = ['TCGA-ACC', 'TCGA-BLCA', 'TCGA-BRCA', 'TCGA-CESC', 'TCGA-CHOL', 'TCGA-COAD', 'TCGA-DLBC', 'TCGA-ESCA', 'TCGA-GBM', 'TCGA-HNSC', 'TCGA-KICH', 'TCGA-KIRC', 'TCGA-KIRP', 'TCGA-LAML', 'TCGA-LGG', 'TCGA-LIHC', 'TCGA-LUAD', 'TCGA-LUSC', 'TCGA-MESO', 'TCGA-OV', 'TCGA-PAAD', 'TCGA-PCPG', 'TCGA-PRAD', 'TCGA-READ', 'TCGA-SARC', 'TCGA-SKCM', 'TCGA-STAD', 'TCGA-TGCT', 'TCGA-THCA', 'TCGA-THYM', 'TCGA-UCEC', 'TCGA-UCS', 'TCGA-UVM']
	project_list = ['TCGA-ACC', 'TCGA-BLCA', 'TCGA-BRCA', 'TCGA-CESC', 'TCGA-CHOL', 'TCGA-COAD', 'TCGA-DLBC', 'TCGA-ESCA', 'TCGA-GBM', 'TCGA-HNSC', 'TCGA-KICH', 'TCGA-KIRC', 'TCGA-KIRP', 'TCGA-LAML', 'TCGA-LGG', 'TCGA-LIHC', 'TCGA-LUAD', 'TCGA-LUSC', 'TCGA-MESO', 'TCGA-OV', 'TCGA-PAAD', 'TCGA-PCPG', 'TCGA-PRAD', 'TCGA-READ', 'TCGA-SARC', 'TCGA-SKCM', 'TCGA-STAD', 'TCGA-TGCT', 'TCGA-THCA', 'TCGA-THYM', 'TCGA-UCEC', 'TCGA-UCS', 'TCGA-UVM']
	summary_index = pd.DataFrame()
	with open("/home/yuwang/SuLab/TCGA/Script/Download/TCGA_project_library.txt") as l:
		tumor_names = dict(x.rstrip().split(None, 1) for x in l)
	for y in project_list:
		tumor_name = tumor_names[y].replace("['", "").replace("']", "")
		gene_matrix = pd.read_csv(filedir(y, "gene_reindex"), sep = '\t')
		total_matrix = pd.read_csv(filedir(y ,"total"), sep = '\t')
		total_matrix = reshape_matrix_for_km(total_matrix)
		total_matrix = total_matrix[total_matrix['vital_status'] != "not reported"]
		summary_index = write_index(y, summary_index)
		#print(summary_index)
		print("================= " + y + " Done!!! ================")

	summary_index.reset_index()
	output_path = "/home/yuwang/SuLab/TCGA/Data/Plot/total_summary"
	summary_index.to_csv(output_path + ".csv", sep = '\t')
  	
  	print("total summary index written")
  	'''
	writer = pd.ExcelWriter("/home/yuwang/SuLab/TCGA/Data/Plot/" + "total-summary-v2.xlsx")
	summary_index.to_excel(writer, 'Sheet1')
	writer.save()
	print("total summary index written")
	'''
