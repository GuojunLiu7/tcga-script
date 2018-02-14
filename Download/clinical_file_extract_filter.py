def split_tag(element):
  sep = "}"
  t = element.tag.split(sep, 1)[1]
  return(t)

def read_element_text(mydict, element):
  key = split_tag(element)
  if type(element.text) == type(None):
    mydict[key] = "NotApplicable"
  else:
    mydict[key] = element.text
  return(mydict)
def extract_filter(y, root):
  method_name = y.replace("-", "")
  possibles = globals().copy()
  possibles.update(locals())
  method = possibles.get(method_name)
  if not method:
    raise NotImplementedError("Method %s not implemented" % method_name)
  d = method(root)
  return(d)
#class ClinicalExtract(object):
def TCGABRCA(root):
	mydict = {}
	clinical_index = [11, 14]
  #   clinical_index = [11, 14, 26, 37, 40, 41, 43, 44, 46, 49, 50, 51, 52, 53, 56, 59, 64, 66, 67, 68, 69, 74, 75, 84, 85, 30, 39, 42, 48, 62, 63, 70, 71, 76, 77, 78, 80, 81, 82, 86, 87, 89, 90, 91, 92, 93, 94]
	for i in clinical_index:
  		mydict = read_element_text(mydict, root[1][i])
    
	return(mydict)


