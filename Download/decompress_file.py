# Extract files
import os


#Decompress .tar.gz
def decompress_targz():
	import tarfile
	for root, dirs, files in os.walk("X:\Su Lab\TCGA\Data\Download\TCGA-BRCA-Clinical"):
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
	
	for root, dirs, files in os.walk("X:\Su Lab\TCGA\Data\Download"):
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



decompress_targz()

