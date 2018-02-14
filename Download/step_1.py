import Clinical_download
import Biospecimen_download
import Decompress_file

url_files = "https://api.gdc.cancer.gov/files"
data_dir = "/home/yuwang/SuLab/TCGA/Data"
filedir = "/home/yuwang/SuLab/TCGA/Data/Download/"

def file(y, keyword):
	t = filedir + y + "-" + keyword
	return(t)

if __name__ == '__main__':
#project_list = [x.replace('\n', '') for x in open('X:\\Su Lab\\TCGA\\Script\\Download\\TCGA_project_list.txt').readlines()]
	project_list = ['TCGA-ACC', 'TCGA-BLCA', 'TCGA-BRCA', 'TCGA-CESC', 'TCGA-CHOL', 'TCGA-COAD', 'TCGA-DLBC', 'TCGA-ESCA', 'TCGA-GBM', 'TCGA-HNSC', 'TCGA-KICH', 'TCGA-KIRC', 'TCGA-KIRP', 'TCGA-LAML', 'TCGA-LGG', 'TCGA-LIHC', 'TCGA-LUAD', 'TCGA-LUSC', 'TCGA-MESO', 'TCGA-OV', 'TCGA-PAAD', 'TCGA-PCPG', 'TCGA-PRAD', 'TCGA-READ', 'TCGA-SARC', 'TCGA-SKCM', 'TCGA-STAD', 'TCGA-TGCT', 'TCGA-THCA', 'TCGA-THYM', 'TCGA-UCEC', 'TCGA-UCS', 'TCGA-UVM']
	for y in project_list:
		Clinical_download.file_download(y)
		Decompress_file.decompress_targz(file(y, "Clinical"))
		Biospecimen_download.biospecimen_download(y)
		Decompress_file.decompress_targz(file(y, "Biospecimen"))