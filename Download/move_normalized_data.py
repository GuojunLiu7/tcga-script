import os
import shutil

from string import Template


url_legacy = "https://api.gdc.cancer.gov/legacy/"

projects = "projects"

url_project = url_legacy + projects


def copy_normalized_data(y):
	normalized_count = 0
	src = src_template.substitute(t = y)
	dest = dest_template.substitute(t = y)

	for root, dirs, files in os.walk(src):
		for file in files:
			filesrc = os.sep.join([root, file])
			if file.endswith(".htseq.counts"):
				if not os.path.exists(dest):
					os.makedirs(dest)
				shutil.copyfile(filesrc, dest + '\\' + y + '_' + file)
				normalized_count += 1
	print(y + ":" + str(normalized_count))


if __name__=='__main__':
	data_dir = "X:\\Su Lab\\TCGA\\Data"	
	os.makedirs(data_dir + "\\Normalized_data")
	src_template = Template("X:\\Su Lab\\TCGA\\Data\\Download\\$t")
	dest_template = Template("X:\\Su Lab\\TCGA\\Data\\Normalized_data\\$t")

	import gdc_project

	project_list = gdc_project.write_project_library(url_project, "TCGA")
	for y in project_list:
		copy_normalized_data(y)