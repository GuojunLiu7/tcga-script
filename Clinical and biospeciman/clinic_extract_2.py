import xml.etree.ElementTree as ET

def extract_xml(link):
	tree = ET.parse(link)
	root = tree.getroot()
	mydict = {}
	sep = "}"
	for element in root:
		if (type(element.text) == type(None)) or (element.text.startswith('\n')):
			mydict[element.tag.split(sep, 1)[1]] = []
			for ele2 in element.findall('.//'):
				dicttemp1 = {}
				if (type(ele2.text) != type(None)) and (ele2.text.startswith('\n')):
					dicttemp1[ele2.tag.split(sep, 1)[1]] = []
					mydict[element.tag.split(sep, 1)[1]].append(dicttemp1.copy())
					for ele3 in ele2.findall('.//'):
						dicttemp2 = {}
						if (type(ele3.text) != type(None)) and (ele3.text.startswith('\n')):
							dicttemp2[ele3.tag.split(sep, 1)[1]] = []
							dicttemp1[ele2.tag.split(sep, 1)[1]].append(dicttemp2.copy())
							for ele4 in ele3.findall('.//'):
								dicttemp3 = {}
								if (type(ele4.text) != type(None)) and (ele4.text.startswith('\n')):
									dicttemp3[ele4.tag.split(sep, 1)[1]] = []
									dicttemp2[ele3.tag.split(sep, 1)[1]].append(dicttemp3.copy())
									for ele5 in ele4.findall('.//'):
										dicttemp4 = {}
										if (type(ele5.text) != type(None)) and (ele5.text.startswith('\n')):
											dicttemp4[ele5.tag.split(sep, 1)[1]] = []
											dicttemp3[ele4.tag.split(sep, 1)[1]].append(dicttemp4.copy())
											for ele6 in ele5.findall('.//'):
												dicttemp5 = {}
												if (type(ele6.text) != type(None)) and (ele6.text.startswith('\n')):
													dicttemp5[ele6.tag.split(sep, 1)[1]] = []
													dicttemp4[ele5.tag.split(sep, 1)[1]].append(dicttemp5.copy())
												elif type(ele6.text) == type(None):
													dicttemp5[ele6.tag.split(sep, 1)[1]] = None
													dicttemp4[ele5.tag.split(sep, 1)[1]].append(dicttemp5.copy())
												else:
													dicttemp5[ele6.tag.split(sep, 1)[1]] = ele6.text
													dicttemp4[ele5.tag.split(sep, 1)[1]].append(dicttemp5.copy())
										elif type(ele5.text) == type(None):
											dicttemp4[ele5.tag.split(sep, 1)[1]] = None
											dicttemp3[ele4.tag.split(sep, 1)[1]].append(dicttemp4.copy())
										else:
											dicttemp4[ele5.tag.split(sep, 1)[1]] = ele5.text
											dicttemp3[ele4.tag.split(sep, 1)[1]].append(dicttemp4.copy())
								elif type(ele4.text) == type(None):
									dicttemp3[ele4.tag.split(sep, 1)[1]] = None
									dicttemp2[ele3.tag.split(sep, 1)[1]].append(dicttemp3.copy())
								else:
									dicttemp3[ele4.tag.split(sep, 1)[1]] = ele4.text
									dicttemp2[ele3.tag.split(sep, 1)[1]].append(dicttemp3.copy())
						elif type(ele3.text) == type(None):
							dicttemp2[ele2.tag.split(sep, 1)[1]] = None
							dicttemp1[ele2.tag.split(sep, 1)[1]].append(dicttemp2.copy())
						else:
							dicttemp2[ele3.tag.split(sep, 1)[1]] = ele3.text
							dicttemp1[ele2.tag.split(sep, 1)[1]].append(dicttemp2.copy())
				elif type(ele2.text) == type(None):
					dicttemp1[ele2.tag.split(sep, 1)[1]] = None
					mydict[element.tag.split(sep, 1)[1]].append(dicttemp1.copy())
				else:
					dicttemp1[ele2.tag.split(sep, 1)[1]] = ele2.text
					mydict[element.tag.split(sep, 1)[1]].append(dicttemp1.copy())
		else:
			mydict[element.tag.split(sep, 1)[1]] = element.text
	return(mydict)


