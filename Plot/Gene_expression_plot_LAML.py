import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import json
#import seaborn as sns
from lifelines import KaplanMeierFitter
from lifelines.statistics import logrank_test
from pandas import ExcelWriter
from textwrap import wrap

cols = ["gene", "subgroup", "total_number", "favorable_5_year", "favorable_10_year", "logrank_P"]
def filedir(y, key):
	root = "X:\\Su Lab\\TCGA\\Data\\Matrix\\"
	filedir = root + y + "\\" + y + "-" + key + "-matrix.csv"
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


def kmplot(df_high, df_low, ax):
	kmf_high = KaplanMeierFitter()
	kmf_low = KaplanMeierFitter()
	try:
		kmf_high.fit(durations = df_high.duration, event_observed = df_high.event, label = 'High: n = ' + str(len(df_high)))
		kmf_low.fit(durations = df_low.duration, event_observed = df_low.event, label = "Low: n = " + str(len(df_low)))
	except ValueError:
		return("NA", "0", "0", "0", "0")
	kmf_high.plot(ax = ax, color = "red", show_censors=True,  ci_show=False)
	kmf_low.plot(ax = ax, color = "black", show_censors=True, ci_show=False)
	statistics_result = logrank_test(df_high.duration, df_low.duration, event_observed_A = df_high.event, event_observed_B = df_low.event)
	p_value = statistics_result.p_value
	ax.set_xlabel('Time (months)')
	ax.set_ylabel('Probability')
	ax.text(0.95, 0.02, 'logrank P = ' + str('%.4f' % p_value), verticalalignment='bottom', horizontalalignment='right', transform=ax.transAxes,
        color = 'black', fontsize = 11)
	plt.legend(loc=3)
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

def save_fig(summary_index, total_matrix, gene_matrix, t, ARS, plottitle, filetitle, tumor_name):
	df_high, df_low, total_number = divide_into_two(gene_matrix, total_matrix, t)
	
	fig = plt.figure()
	fig.suptitle("\n".join(wrap(('Expression of ' + str(ARS) + ' in ' + tumor_name))), fontsize = 13)
	fig.subplots_adjust(top = 0.85)
	ax = plt.subplot(111)
	ax.set_title("\n".join(wrap(plottitle)), fontsize = 11)
	plt.ylim(0, 1)
	p_value, hm5, hm10, lm5, lm10 = kmplot(df_high, df_low, ax)
	favorable5y = survival_compare(hm5, lm5)
	favorable10y = survival_compare(hm10, lm10)
	df = pd.DataFrame()
	rows = []
	rows.append([ARS, plottitle, total_number, favorable5y, favorable10y, p_value])
	df = pd.DataFrame(rows, columns = cols)
	summary_index = summary_index.append(df)
	fig.savefig('X:\\Su Lab\\TCGA\\Data\\Plot\\' + y + "\\" + ARS + "\\" + y + '-' + ARS + '-' + filetitle + '.png')
	plt.close("all")
	return(summary_index)

	
def extract_filter(y, t, ARS, total_matrix, summary_index, tumor_name):
	os.mkdir('X:\\Su Lab\\TCGA\\Data\\Plot\\' + y + "\\" + ARS)
	
	matrix_normal = total_matrix[total_matrix['sample_type'] == "Solid Tissue Normal"]
	summary_index = save_fig(summary_index, matrix_normal, gene_matrix, t, ARS, "Solid Tissue Normal", "normal_tissue", tumor_name)

	matrix_meta = total_matrix[total_matrix['sample_type'] == "Metastatic"]
	summary_index = save_fig(summary_index, matrix_meta, gene_matrix, t, ARS, "Metastatic", "metastatic", tumor_name)	
	
	# primary tumor
	matrix_primary = total_matrix[total_matrix['sample_type'] == "Primary Tumor"]
	summary_index = save_fig(summary_index, matrix_primary, gene_matrix, t, ARS, "Primary Tumor", "primary_tumor", tumor_name)
	matrix_primary = total_matrix[total_matrix['sample_type'] == "Primary Blood Derived Cancer - Peripheral Blood"]
	summary_index = save_fig(summary_index, matrix_primary, gene_matrix, t, ARS, "Primary Blood Derived Cancer", "primary_blood_tumor", tumor_name)
	# ============================================================
	matrix_male = matrix_primary[matrix_primary['gender'] == "male"]
	summary_index = save_fig(summary_index, matrix_male, gene_matrix, t, ARS, "Primary Blood Derived Cancer: Male", "gender_male", tumor_name)
	matrix_female = matrix_primary[matrix_primary['gender'] == "female"]
	summary_index = save_fig(summary_index, matrix_female, gene_matrix, t, ARS, "Primary Blood Derived Cancer: Female", "gender_female", tumor_name)
	#=====================================
	matrix_i = matrix_primary[matrix_primary['tumor_stage'].str.startswith('stage i') == True]
	matrix_i = matrix_i[matrix_i['tumor_stage'].str.startswith('stage ii') == False]
	matrix_i = matrix_i[matrix_i['tumor_stage'].str.startswith('stage iv') == False]
	summary_index = save_fig(summary_index, matrix_i, gene_matrix, t, ARS, "Primary Blood Derived Cancer: Stage I", "primary_tumor_stage_i", tumor_name)
	matrix_ii = matrix_primary[matrix_primary['tumor_stage'].str.startswith('stage ii') == True]
	matrix_ii = matrix_ii[matrix_ii['tumor_stage'].str.startswith('stage iii') == False]
	summary_index = save_fig(summary_index, matrix_ii, gene_matrix, t, ARS, "Primary Blood Derived Cancer: Stage II", "primary_tumor_stage_ii", tumor_name)	
	matrix_iii = matrix_primary[matrix_primary['tumor_stage'].str.startswith('stage iii') == True]
	summary_index = save_fig(summary_index, matrix_iii, gene_matrix, t, ARS, "Primary Blood Derived Cancer: Stage III", "primary_tumor_stage_iii", tumor_name)
	matrix_iv = matrix_primary[matrix_primary['tumor_stage'].str.startswith('stage iv') == True]
	summary_index = save_fig(summary_index, matrix_iv, gene_matrix, t, ARS, "Primary Blood Derived Cancer: Stage IV", "primary_tumor_stage_iv", tumor_name)

	# =========from count file
	with open("X:\\Su Lab\\TCGA\\Data\\Matrix\\" + y + "\\" + y + "-clinical-count.json") as json_file:
		d = json.load(json_file)
		for ele in d:
			if ("first_degree_relative" not in ele) and ("year" not in ele):
				category = d[ele]
				for item in category:
					if (category[item] > 10) and (item != "NotApplicable") and (len(category) < 10):
						try:
							matrix_ele = matrix_primary[matrix_primary[ele] == item]
							summary_index = save_fig(summary_index, matrix_ele, gene_matrix, t, ARS, ("Primary Blood Derived Cancer: " + ele.replace("_", " ").title() + " " + item.title()), (ele.replace(" ", "_").replace("/", "_").replace("<", "less_than").replace("=", "").replace(">", "more_than").replace(":","_") + "_" + (item.replace(" ", "_").replace("/", "_").replace("<", "less_than").replace("=", "").replace(">", "more_than").replace(":","_")).lower()), tumor_name)
						except TypeError:
							continue
	return(summary_index)


if __name__ == '__main__':
	# project_list = ['TCGA-ACC', 'TCGA-BLCA', 'TCGA-BRCA', 'TCGA-CESC', 'TCGA-CHOL', 'TCGA-COAD', 'TCGA-DLBC', 'TCGA-ESCA', 'TCGA-GBM', 'TCGA-HNSC', 'TCGA-KICH', 'TCGA-KIRC', 'TCGA-KIRP', 'TCGA-LAML', 'TCGA-LGG', 'TCGA-LIHC', 'TCGA-LUAD', 'TCGA-LUSC', 'TCGA-MESO', 'TCGA-OV', 'TCGA-PAAD', 'TCGA-PCPG', 'TCGA-PRAD', 'TCGA-READ', 'TCGA-SARC', 'TCGA-SKCM', 'TCGA-STAD', 'TCGA-TGCT', 'TCGA-THCA', 'TCGA-THYM', 'TCGA-UCEC', 'TCGA-UCS', 'TCGA-UVM']
	project_list = ['TCGA-LAML']

	for y in project_list:


		with open("X:\\Su Lab\\TCGA\\Script\\Download\\TCGA_project_library.txt") as f:
			tumor_names = dict(x.rstrip().split(None, 1) for x in f)
		tumor_name = tumor_names[y].replace("['", "").replace("']", "")

		os.mkdir('X:\\Su Lab\\TCGA\\Data\\Plot\\' + y)

		plt.rcParams.update({'figure.max_open_warning': 0})
		pd.options.mode.chained_assignment = None

		gene_matrix = pd.read_csv(filedir(y, "gene_reindex"), sep = '\t')
		total_matrix = pd.read_csv(filedir(y ,"total"), sep = '\t')
		total_matrix = reshape_matrix_for_km(total_matrix)
		#print(total_matrix)
		
		summary_index = pd.DataFrame()

		with open("X:\\Su Lab\\TCGA\\Data\\Plot\\" + "genelist.txt") as f:
		    for line in f:
		       (ARS, t) = line.split()
		       summary_index = extract_filter(y, t, ARS, total_matrix, summary_index, tumor_name)
		       print("================= " + ARS + " Done!!! ================")

		summary_index.reset_index()
		writer = pd.ExcelWriter("X:\\Su Lab\\TCGA\\Data\\Plot\\" + y + "\\" + y + "-summary.xlsx")
		summary_index.to_excel(writer, 'Sheet1')
		writer.save()
		print(y + " summary index written")
	
