# Extract files
import os


#Decompress .tar.gz
def decompress_targz(filedir):
	import tarfile
	for root, dirs, files in os.walk(filedir):
		for file in files:
			if file.endswith(".tar.gz"):
				fname = os.path.join(root, file)
				dirpath = os.path.join(root)
				tar = tarfile.open(fname)
				tar.extractall(path = dirpath)
				tar.close()
				print("Extract", root)


# Decompress .gz
def decompress_gzip():
	import gzip
	
	for root, dirs, files in os.walk("/home/yuwang/SuLab/TCGA/Data/Download"):
		for file in files:
			if file.endswith(".counts.gz"):
				fname = os.path.join(root, file)
				dirpath = os.path.join(root)
				outf = fname[:-3]
				inF = gzip.open(fname, "rb")
				outF = open(outf, 'wb')
				outF.write(inF.read())
				inF.close()
				outF.close()
				print("Extract:", root)


