import pandas as pd

root = "X:\\Su Lab\\TCGA\\Data\\"
y = "TCGA-BRCA"


def csv2matrix(y, csv):
	csvdir = root + "Matrix\\" + y +"-" + csv + "-matrix.csv"
	csv_matrix = pd.read_csv(csvdir, sep = '\t', encoding = 'utf-8')
	csv_matrix = pd.DataFrame(csv_matrix)
	return(csv_matrix)

def combine_row(index_matrix, clinical_matrix, biospecimen_matrix, row):
	file_id = row[0]
	case_id = row[1]
	sample_id = row[8]
	df_index = (index_matrix.loc[index_matrix['file_id'] == file_id])
	df_clinic = (clinical_matrix.loc[clinical_matrix['bcr_patient_uuid'] == case_id])
	df1 = pd.merge(df_index, df_clinic, left_on = "case_id", right_on = "bcr_patient_uuid") 
	

	df_bio = (biospecimen_matrix.loc[biospecimen_matrix['bcr_sample_uuid'] == sample_id])
	df2 = pd.merge(df1, df_bio, left_on = "sample_id", right_on = "bcr_sample_uuid")
	
	return(df2)
'''
def combine_row(index_matrix, clinical_matrix, biospecimen_matrix, row):
	file_id = row[0]
	case_id = row[1]
	sample_id = row[8]
	df_index = (index_matrix.loc[index_matrix['file_id'] == file_id])
	df_clinic = (clinical_matrix.loc[clinical_matrix['bcr_patient_uuid'] == case_id])
	df1 = pd.merge(df_index, df_clinic, left_on = "case_id", right_on = "bcr_patient_uuid") 
	

	df_bio = (biospecimen_matrix.loc[biospecimen_matrix['bcr_sample_uuid'] == sample_id])
	df2 = pd.merge(df1, df_bio, left_on = "sample_id", right_on = "bcr_sample_uuid")
	return(df2)
'''
def generate_total_clinic_matrix(main_df, y):
	index_matrix = csv2matrix(y, "basic")
	clinical_matrix = csv2matrix(y, "clinical")
	biospecimen_matrix = csv2matrix(y, "biospecimen")
	for index, row in index_matrix.iterrows():
		df = combine_row(index_matrix, clinical_matrix, biospecimen_matrix, row)
		main_df = main_df.append(df)
	return(main_df)

def write_total_matrix(y):
	main_df = pd.DataFrame()
	main_df = generate_total_clinic_matrix(main_df, y)
	output_path = "X:\\Su Lab\\TCGA\\Data\\Matrix\\" + y + '-total-matrix'
	main_df = main_df.set_index("bcr_sample_barcode")
	main_df.to_csv(output_path + ".csv", sep = '\t')
	print("total matrix generated:" + y)

if __name__ == '__main__':
	#main_df = pd.DataFrame()
	# get project list
	#project_list = [x.replace('\n', '') for x in open('X:\\Su Lab\\TCGA\\Script\\Download\\TCGA_project_list.txt').readlines()]
	#project_list = ['TCGA-SARC', 'TCGA-SKCM', 'TCGA-STAD', 'TCGA-TGCT', 'TCGA-THCA', 'TCGA-THYM', 'TCGA-UCEC', 'TCGA-UCS', 'TCGA-UVM']
	## get project 
	#with open("X:\\Su Lab\\TCGA\\Script\\Download\\TCGA_project_library.txt") as f:
		#tumor_names = dict(x.rstrip().split(None, 1) for x in f)
	
	y = "TCGA-BRCA"
	write_total_matrix(y)



