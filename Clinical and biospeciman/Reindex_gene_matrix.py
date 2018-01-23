import pandas as pd

root = "X:\\Su Lab\\TCGA\\Data\\"
y = "TCGA-BRCA"

def csv2matrix(y, csv):
	csvdir = root + "Matrix\\" + y +"-" + csv + "-matrix.csv"
	csv_matrix = pd.read_csv(csvdir, sep = '\t', encoding = 'utf-8')
	csv_matrix = pd.DataFrame(csv_matrix)
	return(csv_matrix)





def combine_row(temp_matrix, gene_matrix, row):
	#sample_barcode = row[0]
	file_id = row[1]
	df_temp = (temp_matrix.loc[temp_matrix['file_id'] == file_id])
	df_gene = (gene_matrix.loc[gene_matrix['file_id'] == file_id])
	df1 = pd.merge(df_temp, df_gene, left_on = "file_id", right_on = "file_id") 
	return(df1)

def reindex_gene_matrix(main_df, y):
	total_matrix = csv2matrix(y, "total")
	temp_matrix = total_matrix[['bcr_sample_barcode','file_id']]
	gene_matrix = csv2matrix(y, "gene")

	for index, row in temp_matrix.iterrows():
		df = combine_row(temp_matrix, gene_matrix, row)
		main_df = main_df.append(df)
	return(main_df)

def write_gene_matrix(y):
	main_df = pd.DataFrame()
	main_df = reindex_gene_matrix(main_df, y)
	output_path = "X:\\Su Lab\\TCGA\\Data\\Matrix\\" + y + '-gene_reindex-matrix'
	main_df = main_df.set_index("bcr_sample_barcode")
	main_df.to_csv(output_path + ".csv", sep = '\t')
	print("gene matrix reindex:" + y)

if __name__ == '__main__':
	y = "TCGA-BRCA"
	write_gene_matrix(y)