import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
#import seaborn as sns
from lifelines import KaplanMeierFitter
from lifelines.statistics import logrank_test

def filedir(y, key):
	root = "X:\\Su Lab\\TCGA\\Data\\Matrix\\"
	filedir = root + y + "-" + key + "-matrix.csv"
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
	matrix = matrix[matrix['duration']!="NotApplicable"]
	return(matrix)


def kmplot(df_high, df_low, ax):
	kmf_high = KaplanMeierFitter()
	kmf_low = KaplanMeierFitter()
	try:
		kmf_high.fit(durations = df_high.duration, event_observed = df_high.event, label = 'High: n = ' + str(len(df_high)))
		kmf_low.fit(durations = df_low.duration, event_observed = df_low.event, label = "Low: n = " + str(len(df_low)))
	except ValueError:
		return
	kmf_high.plot(ax = ax, color = "red", show_censors=True,  ci_show=False)
	kmf_low.plot(ax = ax, color = "black", show_censors=True, ci_show=False)
	statistics_result = logrank_test(df_high.duration, df_low.duration, event_observed_A = df_high.event, event_observed_B = df_low.event)
	p_value = statistics_result.p_value
	ax.set_xlabel('Time (months)')
	ax.set_ylabel('Probability')
	ax.text(0.95, 0.02, 'logrank P = ' + str('%.4f' % p_value), verticalalignment='bottom', horizontalalignment='right', transform=ax.transAxes,
        color = 'black', fontsize = 11)
	plt.legend(loc=3)
	#plt.show()
def divide_into_two(gene_matrix, index_matrix, t):
	specific_gene_matrix = gene_matrix[['bcr_sample_barcode', t]]
	key = ['bcr_sample_barcode']
	in1 = index_matrix.set_index(key).index
	in2 = specific_gene_matrix.set_index(key).index
	specific_gene_matrix = specific_gene_matrix[in2.isin(in1)]
	gene_cutoff = specific_gene_matrix[t].quantile(0.5)
	high_index = specific_gene_matrix[specific_gene_matrix[t] > gene_cutoff]
	low_index = specific_gene_matrix[specific_gene_matrix[t] < gene_cutoff]
	ihigh = high_index.set_index(key).index
	ilow = low_index.set_index(key).index
	df_high = index_matrix[in1.isin(ihigh)]
	df_low = index_matrix[in1.isin(ilow)]
	#print(gene_cutoff)
	return(df_high, df_low)


def save_fig(total_matrix, gene_matrix, t, ARS, plottitle, filetitle):
	df_high, df_low = divide_into_two(gene_matrix, total_matrix, t)
	fig = plt.figure()
	fig.suptitle(('Expression of ' + str(ARS) + ' in breast cancer'), fontsize = 13)
	ax = plt.subplot(111)
	ax.set_title(plottitle)
	plt.ylim(0.2, 1)
	kmplot(df_high, df_low, ax)
	fig.savefig('X:\\Su Lab\\TCGA\\Data\\Plot\\' + y + "\\" + ARS + "\\" + y + '-' + ARS + '-' + filetitle + '.png')
	print(plottitle + ' Done')
	#plt.show()
	
def breast_cancer_series(y, t, ARS, total_matrix):
	#os.mkdir('X:\\Su Lab\\TCGA\\Data\\Plot\\' + y + "\\" + ARS)
	
	matrix_normal = total_matrix[total_matrix['sample_type'] == "Solid Tissue Normal"]
	save_fig(matrix_normal, gene_matrix, t, ARS, "Solid tissue normal", "normal_tissue")

	matrix_meta = total_matrix[total_matrix['sample_type'] == "Metastatic"]
	save_fig(matrix_meta, gene_matrix, t, ARS, "Metastatic", "metastatic")	
	'''
	# primary tumor
	matrix_primary = total_matrix[total_matrix['sample_type'] == "Primary Tumor"]
	save_fig(matrix_primary, gene_matrix, t, ARS, "Primary tumor", "primary_tumor")

	# ========================================
	# estrogen receptor positive
	matrix_erpos = matrix_primary[matrix_primary['breast_carcinoma_estrogen_receptor_status'] == 'Positive']
	save_fig(matrix_erpos, gene_matrix, t, ARS, "Primary tumor: estrogen receptor positive", "primary_tumor_er+")
	# estrogen receptor negative
	matrix_erneg = matrix_primary[matrix_primary['breast_carcinoma_estrogen_receptor_status'] == 'Negative']
	save_fig(matrix_erneg, gene_matrix, t, ARS, "Primary tumor: estrogen receptor negative", "primary_tumor_er-")
	# --------------------------
	# progesterone receptor positive
	matrix_prpos = matrix_primary[matrix_primary['breast_carcinoma_progesterone_receptor_status'] == 'Positive']
	save_fig(matrix_prpos, gene_matrix, t, ARS, "Primary tumor: progesterone receptor positive", "primary_tumor_pr+")
	# progesterone receptor negative
	matrix_prneg = matrix_primary[matrix_primary['breast_carcinoma_progesterone_receptor_status'] == 'Negative']
	save_fig(matrix_prneg, gene_matrix, t, ARS, "Primary tumor: progesterone receptor negative", "primary_tumor_pr-")
	# --------------------------
	# her2 positive
	matrix_her2pos = matrix_primary[matrix_primary['lab_proc_her2_neu_immunohistochemistry_receptor_status'] == 'Positive']
	save_fig(matrix_her2pos, gene_matrix, t, ARS, "Primary tumor: her2 IHC positive", "primary_tumor_her2+")
	# her2 negative
	matrix_her2neg = matrix_primary[matrix_primary['lab_proc_her2_neu_immunohistochemistry_receptor_status'] == 'Negative']
	save_fig(matrix_her2neg, gene_matrix, t, ARS, "Primary tumor: her2 IHC negative", "primary_tumor_her2-")
	# --------------------------
	# triple negative
	matrix_3neg = matrix_primary[matrix_primary['lab_proc_her2_neu_immunohistochemistry_receptor_status'] == 'Negative']
	matrix_3neg = matrix_3neg[matrix_3neg['breast_carcinoma_estrogen_receptor_status'] == 'Negative']
	matrix_3neg = matrix_3neg[matrix_3neg['breast_carcinoma_progesterone_receptor_status'] == 'Negative']
	save_fig(matrix_3neg, gene_matrix, t, ARS, "Primary tumor: triple negative", "primary_tumor_3neg")
	# triple positive
	matrix_3pos = matrix_primary[matrix_primary['lab_proc_her2_neu_immunohistochemistry_receptor_status'] == 'Positive']
	matrix_3pos = matrix_3pos[matrix_3pos['breast_carcinoma_estrogen_receptor_status'] == 'Positive']
	matrix_3pos = matrix_3pos[matrix_3pos['breast_carcinoma_progesterone_receptor_status'] == 'Positive']
	save_fig(matrix_3pos, gene_matrix, t, ARS, "Primary tumor: triple positive", "primary_tumor_3pos")
	#=================================================================
	# mirometastasis positive
	matrix_mmspos = matrix_primary[matrix_primary['cytokeratin_immunohistochemistry_staining_method_micrometastasis_indicator'] == 'YES']
	save_fig(matrix_mmspos, gene_matrix, t, ARS, "Primary tumor: micrometastasis indicator positive", "primary_tumor_mms+")
	# mirometastasis negative
	matrix_mmsneg = matrix_primary[matrix_primary['cytokeratin_immunohistochemistry_staining_method_micrometastasis_indicator'] == 'NO']
	save_fig(matrix_mmsneg, gene_matrix, t, ARS, "Primary tumor: micrometastasis indicator negative", "primary_tumor_mms-")
	#==============================================================
	# stage
	# stage i
	matrix_i = matrix_primary[matrix_primary['tumor_stage'].str.startswith('stage i') == True]
	matrix_i = matrix_i[matrix_i['tumor_stage'].str.startswith('stage ii') == False]
	matrix_i = matrix_i[matrix_i['tumor_stage'].str.startswith('stage iv') == False]
	save_fig(matrix_i, gene_matrix, t, ARS, "Primary tumor: stage I", "primary_tumor_stage_i")
	# stage ii
	matrix_ii = matrix_primary[matrix_primary['tumor_stage'].str.startswith('stage ii') == True]
	matrix_ii = matrix_ii[matrix_ii['tumor_stage'].str.startswith('stage iii') == False]
	save_fig(matrix_ii, gene_matrix, t, ARS, "Primary tumor: stage II", "primary_tumor_stage_ii")	
	# stage iii
	matrix_iii = matrix_primary[matrix_primary['tumor_stage'].str.startswith('stage iii') == True]
	save_fig(matrix_iii, gene_matrix, t, ARS, "Primary tumor: stage III", "primary_tumor_stage_iii")
	
	# stage iv
	matrix_iv = matrix_primary[matrix_primary['tumor_stage'].str.startswith('stage iv') == True]
	save_fig(matrix_iv, gene_matrix, t, ARS, "Primary tumor: stage IV", "primary_tumor_stage_iv")
	#==============================================================
	# Pathology
	# T
	# TX
	matrix_TX = matrix_primary[matrix_primary['pathologic_T'].str.startswith('TX') == True]
	save_fig(matrix_TX, gene_matrix, t, ARS, "Primary tumor: pathologic TX", "primary_tumor_tx")
	# T0
	matrix_T0 = matrix_primary[matrix_primary['pathologic_T'].str.startswith('T0') == True]
	save_fig(matrix_T0, gene_matrix, t, ARS, "Primary tumor: pathologic T0", "primary_tumor_t0")
	# T1
	matrix_T1 = matrix_primary[matrix_primary['pathologic_T'].str.startswith('T1') == True]
	save_fig(matrix_T1, gene_matrix, t, ARS, "Primary tumor: pathologic T1", "primary_tumor_t1")
	# T2
	matrix_T2 = matrix_primary[matrix_primary['pathologic_T'].str.startswith('T2') == True]
	save_fig(matrix_T2, gene_matrix, t, ARS, "Primary tumor: pathologic T2", "primary_tumor_t2")
	# T3
	matrix_T3 = matrix_primary[matrix_primary['pathologic_T'].str.startswith('T3') == True]
	save_fig(matrix_T3, gene_matrix, t, ARS, "Primary tumor: pathologic T3", "primary_tumor_t3")
	# T4
	matrix_T4 = matrix_primary[matrix_primary['pathologic_T'].str.startswith('T4') == True]
	save_fig(matrix_T4, gene_matrix, t, ARS, "Primary tumor: pathologic T4", "primary_tumor_t4")
	# N
	#NX
	matrix_NX = matrix_primary[matrix_primary['pathologic_N'].str.startswith('NX') == True]
	save_fig(matrix_NX, gene_matrix, t, ARS, "Primary tumor: pathologic NX", "primary_tumor_nx")
	#N0
	matrix_N0 = matrix_primary[matrix_primary['pathologic_N'].str.startswith('N0') == True]
	save_fig(matrix_N0, gene_matrix, t, ARS, "Primary tumor: pathologic N0", "primary_tumor_n0")
	#N1
	matrix_N1 = matrix_primary[matrix_primary['pathologic_N'].str.startswith('N1') == True]
	save_fig(matrix_N1, gene_matrix, t, ARS, "Primary tumor: pathologic N1", "primary_tumor_n1")
	#N2
	matrix_N2 = matrix_primary[matrix_primary['pathologic_N'].str.startswith('N2') == True]
	save_fig(matrix_N2, gene_matrix, t, ARS, "Primary tumor: pathologic N2", "primary_tumor_n2")
	#N3
	matrix_N3 = matrix_primary[matrix_primary['pathologic_N'].str.startswith('N3') == True]
	save_fig(matrix_N3, gene_matrix, t, ARS, "Primary tumor: pathologic N3", "primary_tumor_n3")
	# M
	#MX
	matrix_MX = matrix_primary[matrix_primary['pathologic_M'].str.startswith('MX') == True]
	save_fig(matrix_MX, gene_matrix, t, ARS, "Primary tumor: pathologic MX", "primary_tumor_mx")
	#M0
	matrix_M0 = matrix_primary[matrix_primary['pathologic_M'].str.startswith('M0') == True]
	save_fig(matrix_M0, gene_matrix, t, ARS, "Primary tumor: pathologic M0", "primary_tumor_m0")
	# M1
	matrix_M1 = matrix_primary[matrix_primary['pathologic_M'].str.startswith('M1') == True]
	save_fig(matrix_M1, gene_matrix, t, ARS, "Primary tumor: pathologic M1", "primary_tumor_m1")
	'''

if __name__ == '__main__':
	y = "TCGA-BRCA"

	plt.rcParams.update({'figure.max_open_warning': 0})
	pd.options.mode.chained_assignment = None

	gene_matrix = pd.read_csv(filedir(y, "gene_reindex"), sep = '\t')
	total_matrix = pd.read_csv(filedir(y ,"total"), sep = '\t')
	total_matrix = reshape_matrix_for_km(total_matrix)
	with open("X:\\Su Lab\\TCGA\\Data\\Plot\\" + y + "\\" + "genelist.txt") as f:
	    for line in f:
	       (ARS, t) = line.split()
	       breast_cancer_series(y, t, ARS, total_matrix)
	       print("================= " + ARS + " Done!!! ================")
	
	
	#print(gene_id[SARS])

'''
t = "ENSG00000031698.11"
	ARS = "SARS"
	
	
'''
'''	# Self-defined filter
def custom_filter(matrix):
	matrix = matrix[matrix['sample_type'] == "Primary Tumor"]
	matrix = matrix[matrix['pathologic_M'].str.startswith('M1') == True]
	#matrix = matrix[matrix['tumor_stage'].str.startswith('stage iii') == False]
	#matrix = matrix[matrix['tumor_stage'].str.startswith('stage iv') == False]
	#matrix = matrix[matrix['tumor_stage'].str.startswith('stage iv') == True]
	#matrix = matrix[matrix['tumor_stage'].str.startswith('stage ii') == False]
	#matrix = matrix[matrix['tumor_stage'].str.startswith('stage iv') == False]
	# breast_carcinoma_estrogen_receptor_status
	# breast_carcinoma_progesterone_receptor_status
	# cytokeratin_immunohistochemistry_staining_method_micrometastasis_indicator
	# her2_immunohistochemistry_level_result
	# lab_proc_her2_neu_immunohistochemistry_receptor_status
	# pathologic_T
	return(matrix)

if __name__ == '__main__':
	y = "TCGA-BRCA"
	t = "ENSG00000031698.11"
	gene_matrix = pd.read_csv(filedir(y, "gene_reindex"), sep = '\t')
	total_matrix = pd.read_csv(filedir(y ,"total"), sep = '\t')
	total_matrix = custom_filter(total_matrix)
	total_matrix = reshape_matrix_for_km(total_matrix)
	df_high, df_low = divide_into_two(gene_matrix, total_matrix, t)
	fig = plt.figure()
	fig.suptitle('Expression of SARS in breast cancer', fontsize = 13)
	ax = plt.subplot(111)
	ax.set_title('Primary tumor: pathologic M1')
	plt.ylim(0.2, 1)
	kmplot(df_high, df_low)
	#plt.show()
	fig.savefig('X:\\Su Lab\\TCGA\\Data\\Plot\\' + y + "\\" + y + '-SARS' + '-primary_tumor-pathological_M1.png')
'''