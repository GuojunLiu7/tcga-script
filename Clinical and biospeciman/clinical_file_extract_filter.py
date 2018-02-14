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

def TCGABRCA(root):
  mydict = {}
  clinical_index = [11, 14, 26, 37, 40, 41, 43, 44, 46, 49, 50, 51, 52, 53, 56, 59, 64, 66, 67, 68, 69, 74, 75, 84, 85, 30, 39, 42, 48, 62, 63, 70, 71, 76, 77, 78, 80, 81, 82, 86, 87, 89, 90, 91, 92, 93]
  for i in clinical_index:
    mydict = read_element_text(mydict, root[1][i])
  mydict = read_element_text(mydict, root[1][65][0])
  for ele in root[1][94][3][1]:
    mydict = read_element_text(mydict, ele)
  return(mydict)

def TCGAACC(root):
  mydict = {}
  clinical_index = [3, 4, 16, 17, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31]
  for i in clinical_index:
    mydict = read_element_text(mydict, root[1][i])

  mydict = read_element_text(mydict, root[1][32][1])
  mydict = read_element_text(mydict, root[1][32][2])
  for ele in root[1][32][3]:
    for ele2 in ele:
      mydict = read_element_text(mydict, ele2)

  clinical_index_2 = [0, 1, 7, 9, 12, 13]
  for j in clinical_index_2:
    mydict = read_element_text(mydict, root[1][33][j])
  for ele in root[1][33][11][1]:
    mydict = read_element_text(mydict, ele)
  mydict = read_element_text(mydict, root[1][33][16][0])
  mydict = read_element_text(mydict, root[1][33][16][1])
  mydict = read_element_text(mydict, root[1][34][0])
  return(mydict)

def TCGABLCA(root):
  mydict = {}
  mydict = read_element_text(mydict, root[1][4])
  clinical_index = [3, 4, 26, 32, 33, 34, 35, 37, 38, 40 ]
  for i in clinical_index:
    mydict = read_element_text(mydict, root[1][i])
  i = 50
  while True:
    try:
      mydict = read_element_text(mydict, root[1][i][1])
      mydict = read_element_text(mydict, root[1][i][2])
      for ele in root[1][i][3]:
        for ele2 in ele:
          mydict = read_element_text(mydict, ele2)
      mydict = read_element_text(mydict, root[1][i-5])
      mydict = read_element_text(mydict, root[1][i-4])
      mydict = read_element_text(mydict, root[1][i+1][0])
      for ele in root[1][i][3]:
        for ele2 in ele:
          mydict = read_element_text(mydict, ele2)
      t_index = [2, 3, 4, 5, 6, 7, 8, 9]
      for t in t_index:
        mydict = read_element_text(mydict, root[1][i+t])
      mydict = read_element_text(mydict, root[1][i+11][0])
      return(mydict)
    except IndexError:
      i = i+1

def TCGACESC(root):
  mydict = {}
  clinical_index = [3, 4, 13, 23, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 38, 43, 44, 45, 46, 47, 61, 62, 63, 64, 65, 79, 82]
  for i in clinical_index:
    mydict = read_element_text(mydict, root[1][i])
  mydict = read_element_text(mydict, root[1][73][0])
  mydict = read_element_text(mydict, root[1][81][1])
  mydict = read_element_text(mydict, root[1][81][2])
  for ele in root[1][81][3]:
    for ele2 in ele:
      mydict = read_element_text(mydict, ele2)
  mydict = read_element_text(mydict, root[1][86][0])
  return(mydict)

def TCGACHOL(root):
  mydict = {}
  clinical_index = [3, 4, 19, 23, 24]
  for i in clinical_index:
    mydict = read_element_text(mydict, root[1][i])
  t = []
  for ele in root[1][26][:-1]:
    key = split_tag(ele)
    t.append(ele.text)
    mydict[key] = t
  mydict = read_element_text(mydict, root[1][30][1])
  mydict = read_element_text(mydict, root[1][30][2])
  for ele in root[1][30][3]:
    for ele2 in ele:
      mydict = read_element_text(mydict, ele2)
  for ele in root[1][32]:
    mydict = read_element_text(mydict, ele)
  mydict = read_element_text(mydict, root[1][33][0])
  return(mydict)

def TCGACOAD(root):
  mydict = {}
  clinical_index = [11, 14, 58, 59, 60, 61]
  for i in clinical_index:
    mydict = read_element_text(mydict, root[1][i])
  mydict = read_element_text(mydict, root[1][25][1])
  mydict = read_element_text(mydict, root[1][25][2])
  for ele in root[1][25][3]:
    for ele2 in ele:
      mydict = read_element_text(mydict, ele2)
  for ele in root[1][26:57]:
    mydict = read_element_text(mydict, ele)
  return(mydict)

def TCGADLBC(root):
  mydict = {}
  clinical_index = [3, 4, 24, 28, 29, 30, 31]
  for i in clinical_index:
    mydict = read_element_text(mydict, root[1][i])

  clinical_index_1 = list(range(0, 14)) + [15, 17, 18, 19]
  for i in clinical_index_1:
    mydict = read_element_text(mydict, root[1][32][i])


  mydict = read_element_text(mydict, root[1][32][14][0])
  mydict = read_element_text(mydict, root[1][32][16][0])
  clinical_index_2 = list(range(3, 14)) + [0, 15, 16, 17, 18]
  for i in clinical_index_2:
    mydict = read_element_text(mydict, root[1][33][i])


  mydict = read_element_text(mydict, root[1][33][1][0])
  mydict = read_element_text(mydict, root[1][33][2][0])
  mydict = read_element_text(mydict, root[1][33][14][0])
  mydict = read_element_text(mydict, root[1][35][0])
  clinical_index_3 = [0, 1, 3, 4, 5, 6, 8, 9, 10]
  for  i in clinical_index_3:
    mydict = read_element_text(mydict, root[1][34][i])
  i = 0
  while True:
    try:
      #key = split_tag(root[1][34][2][i])
      mydict[str(root[1][34][2][i][0].text).replace(" ", "_")] = str(root[1][34][2][i][2].text)
      i = i+1
    except IndexError:
      
      return(mydict)
    
def TCGAESCA(root):
  mydict = {}
  clinical_index = [3, 4, 23] + list(range(27, 35)) + list(range(36, 42))
  for i in clinical_index:
    mydict = read_element_text(mydict, root[1][i])
  mydict = read_element_text(mydict, root[1][42][1])
  mydict = read_element_text(mydict, root[1][42][2])
  for ele in root[1][42][3]:
    for ele2 in ele:
      mydict = read_element_text(mydict, ele2)
  clinical_index_2 = [0, 1] + list(range(3, 25))
  for i in clinical_index_2:
    mydict = read_element_text(mydict, root[1][43][i])
  mydict = read_element_text(mydict, root[1][43][2][0])
  mydict = read_element_text(mydict, root[1][44][0])
  return(mydict)

def TCGAGBM(root):
  mydict = {}
  clinical_index = [2, 3, 10, 13, 23, 30, 35, 36, 37, 38]
  for i in clinical_index:
    mydict = read_element_text(mydict, root[1][i])
  mydict = read_element_text(mydict, root[1][39][0])
  #!!!
  return(mydict)

def TCGAHNSC(root):
  mydict = {}
  clinical_index = [2, 12, 15, 25] + list(range(29, 57))
  for i in clinical_index:
    mydict = read_element_text(mydict, root[1][i])
  mydict = read_element_text(mydict, root[1][58][1])
  mydict = read_element_text(mydict, root[1][58][2])
  for ele in root[1][58][3]:
    for ele2 in ele:
      mydict = read_element_text(mydict, ele2)
  return(mydict)

def TCGAKICH(root):
  mydict = {}
  clinical_index = [3, 4, 13, 14, 15, 16, 27, 28] + list(range(33, 50))
  for i in clinical_index:
    mydict = read_element_text(mydict, root[1][i])
  mydict = read_element_text(mydict, root[1][29][1])
  mydict = read_element_text(mydict, root[1][29][2])
  for ele in root[1][29][3]:
    for ele2 in ele:
      mydict = read_element_text(mydict, ele2)
  mydict = read_element_text(mydict, root[1][50][0])
  return(mydict)

def TCGAKIRC(root):
  mydict = {}
  clinical_index = [2, 11, 14, 23] + list(range(32, 52))
  for i in clinical_index:
    mydict = read_element_text(mydict, root[1][i])
  mydict = read_element_text(mydict, root[1][31][1])
  mydict = read_element_text(mydict, root[1][31][2])
  for ele in root[1][31][3]:
    for ele2 in ele:
      mydict = read_element_text(mydict, ele2)
  mydict = read_element_text(mydict, root[1][52][0])
  return(mydict)

def TCGAKIRP(root):
  mydict = {}
  clinical_index = [2, 11, 14] + list(range(33, 46)) + list(range(47, 54))
  for i in clinical_index:
    mydict = read_element_text(mydict, root[1][i])
  mydict = read_element_text(mydict, root[1][46][1])
  mydict = read_element_text(mydict, root[1][46][2])
  for ele in root[1][46][3]:
    for ele2 in ele:
      mydict = read_element_text(mydict, ele2)
  mydict = read_element_text(mydict, root[1][54][0])
  return(mydict)

def TCGALAML(root):
  mydict = {}
  clinical_index = [3, 12, 15] + list(range(25, 37)) + list(range(38, 60)) + [61, 62, 63] + [65, 66, 67, 68, 70, 71]
  for i in clinical_index:
    mydict = read_element_text(mydict, root[1][i])
  mydict = read_element_text(mydict, root[1][60][0])
  i = 0
  loop = True
  while loop:
    try:
      s = str(root[1][37][i][0].text)
      mydict[s.split(" ", 1)[0]] = s.split(" ", 1)[1]
      i = i + 1
    except IndexError:
      loop = False
  i = 0
  loop = True
  while loop:
    try:
      mydict[root[1][64][i][0].text] = root[1][64][i][1].text
      i = i + 1
    except IndexError:
      loop = False
  i = 0
  loop = True
  while loop:
    try:
      s = str(root[1][69][i][0].text)
      mydict[s.split(" ", 1)[0]] = s.split(" ", 1)[1]
      i = i + 1
    except IndexError:
      loop = False
  return(mydict)

def TCGALGG(root):
  mydict = {}
  clinical_index = [2, 11, 14, 26] + list(range(33, 70))
  for i in clinical_index:
    mydict = read_element_text(mydict, root[1][i])
  mydict = read_element_text(mydict, root[1][70][0])
  return(mydict)

def TCGALIHC(root):
  mydict = {}
  clinical_index = [3, 4, 27, 28, 34, 37, 38] + list(range(40, 63))
  for i in clinical_index:
    mydict = read_element_text(mydict, root[1][i])
  mydict = read_element_text(mydict, root[1][29][0])
  mydict = read_element_text(mydict, root[1][29][1])
  mydict = read_element_text(mydict, root[1][39][1])
  mydict = read_element_text(mydict, root[1][39][2])
  for ele in root[1][39][3]:
    for ele2 in ele:
      mydict = read_element_text(mydict, ele2)  
  mydict = read_element_text(mydict, root[1][63][0])
  mydict = read_element_text(mydict, root[1][67][0])
  return(mydict)

def TCGALUAD(root):
  mydict = {}
  clinical_index = [2, 11, 14, 26] + list(range(32, 62))
  for i in clinical_index:
    mydict = read_element_text(mydict, root[1][i])
  mydict = read_element_text(mydict, root[1][31][1])
  mydict = read_element_text(mydict, root[1][31][2])
  for ele in root[1][31][3]:
    for ele2 in ele:
      mydict = read_element_text(mydict, ele2)  
  mydict = read_element_text(mydict, root[1][62][0])
  return(mydict)

def TCGALUSC(root):
  mydict = {}
  clinical_index = [2, 11, 14, 26] + list(range(32, 60))
  for i in clinical_index:
    mydict = read_element_text(mydict, root[1][i])
  mydict = read_element_text(mydict, root[1][31][1])
  mydict = read_element_text(mydict, root[1][31][2])
  for ele in root[1][31][3]:
    for ele2 in ele:
      mydict = read_element_text(mydict, ele2)
  mydict = read_element_text(mydict, root[1][60][0])
  return(mydict)

def TCGAMESO(root):
  mydict = {}
  clinical_index = [3, 4, 17, 18, 19] + list(range(23, 32)) + [33, 34, 35, 36, 37]
  for i in clinical_index:
    mydict = read_element_text(mydict, root[1][i])
  clinical_index_2 = list(range(0, 15))
  for i in clinical_index_2:
    mydict = read_element_text(mydict, root[1][39][i])
  mydict = read_element_text(mydict, root[1][38][1])
  mydict = read_element_text(mydict, root[1][38][2])
  for ele in root[1][38][3]:
    for ele2 in ele:
      mydict = read_element_text(mydict, ele2)
  mydict = read_element_text(mydict, root[1][40][0])
  return(mydict)

def TCGAOV(root):
  mydict = {}
  clinical_index = [2, 9, 12, 22, 29, 30, 33, 34, 35, 36, 40, 41, 42, 43, 44]
  for i in clinical_index:
    mydict = read_element_text(mydict, root[1][i])
  mydict = read_element_text(mydict, root[1][45][0])
  mydict = read_element_text(mydict, root[1][32][1])
  mydict = read_element_text(mydict, root[1][32][2])
  for ele in root[1][32][3]:
    for ele2 in ele:
      mydict = read_element_text(mydict, ele2)
  return(mydict)

def TCGAPAAD(root):
  mydict = {}
  clinical_index = [3, 4, 10, 11, 13, 14, 29, 31, 32, 33, 34, 35, 37, 59, 60, 61, 62] + list(range(42, 58))
  for i in clinical_index:
    mydict = read_element_text(mydict, root[1][i])
  mydict = read_element_text(mydict, root[1][63][0])
  mydict = read_element_text(mydict, root[1][38][1])
  mydict = read_element_text(mydict, root[1][38][2])
  for ele in root[1][38][3]:
    for ele2 in ele:
      mydict = read_element_text(mydict, ele2)
  return(mydict)

def TCGAPCPG(root):
  mydict = {}
  clinical_index = [3, 4, 16, 17, 19, 23, 24, 25]
  for i in clinical_index:
    mydict = read_element_text(mydict, root[1][i])
  clinical_index_2 = list(range(0, 13))
  for i in clinical_index_2:
    mydict = read_element_text(mydict, root[1][26][i])
  mydict = read_element_text(mydict, root[1][27][0])
  return(mydict)

def TCGAPRAD(root):
  mydict = {}
  clinical_index = [9, 12, 31, 34, 35, 36, 37, 42, 43, 44, 45, 46, 47, 49, 50, 51, 52, 53]
  for i in clinical_index:
    mydict = read_element_text(mydict, root[1][i])
  i = 0
  t = []
  loop = True
  while loop:
    try:
      t.append(str(root[1][32][i].text))
      i = i+1
    except IndexError:
      mydict[split_tag(root[1][32])] = t
      loop = False
  mydict = read_element_text(mydict, root[1][38][0])
  mydict = read_element_text(mydict, root[1][41][0])
  mydict = read_element_text(mydict, root[1][54][0])
  mydict = read_element_text(mydict, root[1][48][1])
  mydict = read_element_text(mydict, root[1][48][2])
  for ele in root[1][48][3]:
    for ele2 in ele:
      mydict = read_element_text(mydict, ele2)
  for ele in root[1][48][4]:
      mydict = read_element_text(mydict, ele)
  for ele in root[1][48][5]:
      mydict = read_element_text(mydict, ele)
  return(mydict)

def TCGAREAD(root):
  mydict = {}
  clinical_index = [2, 11, 14, 26, 58, 59, 60, 61] + list(range(33, 57))
  for i in clinical_index:
    mydict = read_element_text(mydict, root[1][i])
  mydict = read_element_text(mydict, root[1][25][1])
  mydict = read_element_text(mydict, root[1][25][2])
  for ele in root[1][25][3]:
    for ele2 in ele:
      mydict = read_element_text(mydict, ele2)
  mydict = read_element_text(mydict, root[1][62][0])
  return(mydict)

def TCGASARC(root):
  mydict = {}
  clinical_index = [3, 4, 22]
  for i in clinical_index:
    mydict = read_element_text(mydict, root[1][i])
  clinical_index_2 = list(range(0,4)) + [5] + list(range(7, 18)) + list(range(19, 31))
  for i in clinical_index_2:
    mydict = read_element_text(mydict, root[1][23][i])
  for ele in root[1][23][4]:
    mydict = read_element_text(mydict, ele)
  mydict = read_element_text(mydict, root[1][23][6][0])
  mydict = read_element_text(mydict, root[1][24][0])
  return(mydict)

def TCGASKCM(root):
  mydict = {}
  clinical_index =  [3, 4, 23, 25, 26, 27, 33, 35, 36, 37, 40]
  for i in clinical_index:
    mydict = read_element_text(mydict, root[1][i])
  mydict = read_element_text(mydict, root[1][24][0])
  mydict = read_element_text(mydict, root[1][24][1])
  mydict = read_element_text(mydict, root[1][24][2][0])
  mydict = read_element_text(mydict, root[1][24][2][1])
  mydict = read_element_text(mydict, root[1][24][2][2])
  mydict = read_element_text(mydict, root[1][32][1])
  mydict = read_element_text(mydict, root[1][32][2])
  for ele in root[1][32][3]:
    for ele2 in ele:
      mydict = read_element_text(mydict, ele2)
  mydict = read_element_text(mydict, root[1][42][0])
  return(mydict)

def TCGASTAD(root):
  mydict = {}
  clinical_index = [2, 11, 14, 26, 30, 33, 34, 35, 37, 40, 41, 42, 44, 45, 46, 47, 48, 49, 50]
  for i in clinical_index:
    mydict = read_element_text(mydict, root[1][i])
  mydict = read_element_text(mydict, root[1][36][1])
  mydict = read_element_text(mydict, root[1][36][2])
  for ele in root[1][36][3]:
    for ele2 in ele:
      mydict = read_element_text(mydict, ele2)
  mydict = read_element_text(mydict, root[1][43][0])
  return(mydict)

def TCGATGCT(root):
  mydict = {}
  clinical_index = [3, 4, 27, 29, 33, 34, 36, 37] + list(range(17, 26))
  for i in clinical_index:
    mydict = read_element_text(mydict, root[1][i])
  mydict = read_element_text(mydict, root[1][26][0])
  for ele in root[1][28]:
    mydict[ele[0].text] = ele[1].text
  clinical_index_2 = [0, 1, 2, 3, 5, 6, 7, 9, 10, 11, 12, 13, 14, 15, 18, 20]
  for i in clinical_index_2:
    mydict = read_element_text(mydict, root[1][39][i])
  for ele in root[1][39][8]:
    mydict[ele[0].text] = ele[1].text
  mydict = read_element_text(mydict, root[1][39][4][0][0])
  mydict = read_element_text(mydict, root[1][39][4][0][1])
  for ele in root[1][39][16]:
    mydict = read_element_text(mydict, ele)
  for ele in root[1][39][17]:
    mydict = read_element_text(mydict, ele)
  for ele in root[1][39][19]:
    s = ele.text
    try:
      mydict[split_tag(ele) + "_" + str(s.split(" - ", 1)[0])] = s.split(" - ", 1)[1]
    except:
      mydict[split_tag(ele)] = ele.text

  mydict = read_element_text(mydict, root[1][40][0])
  mydict = read_element_text(mydict, root[1][38][1])
  mydict = read_element_text(mydict, root[1][38][2])
  for ele in root[1][38][3]:
    for ele2 in ele:
      mydict = read_element_text(mydict, ele2)
  return(mydict)

def TCGATHCA(root):
  mydict = {}
  clinical_index = [3, 4, 20, 22, 24, 25, 26, 27, 28, 29, 34, 36, 37, 38, 39, 40, 44, 45, 46, 48, 49, 50, 51]
  for i in clinical_index:
    mydict = read_element_text(mydict, root[1][i])
  mydict = read_element_text(mydict, root[1][21][0])
  mydict = read_element_text(mydict, root[1][23][0])
  mydict = read_element_text(mydict, root[1][30][0])
  mydict = read_element_text(mydict, root[1][30][1])
  mydict = read_element_text(mydict, root[1][30][2])
  mydict = read_element_text(mydict, root[1][41][1])
  mydict = read_element_text(mydict, root[1][41][2])
  mydict = read_element_text(mydict, root[1][62][0])
  for ele in root[1][41][3]:
    for ele2 in ele:
      mydict = read_element_text(mydict, ele2)
  return(mydict)
 
def TCGATHYM(root):
  mydict = {}
  clinical_index = [3, 4, 19]
  for i in clinical_index:
    mydict = read_element_text(mydict, root[1][i])
  mydict = read_element_text(mydict, root[1][26][1])
  mydict = read_element_text(mydict, root[1][26][2])
  for ele in root[1][26][3]:
    for ele2 in ele:
      mydict = read_element_text(mydict, ele2)
  clinical_index_2 = [0, 2, 3, 4, 5, 6, 7, 8]
  for i in clinical_index_2:
    mydict = read_element_text(mydict, root[1][27][i])
  mydict = read_element_text(mydict, root[1][27][1][0])
  mydict = read_element_text(mydict, root[1][28][0])
  return(mydict)

def TCGAUCEC(root):
  mydict = {}
  clinical_index = [3, 4, 13, 24, 25, 27, 33, 34, 35] + list(range(37, 57))
  for i in clinical_index:
    mydict = read_element_text(mydict, root[1][i])
  mydict = read_element_text(mydict, root[1][57][0])
  mydict = read_element_text(mydict, root[1][36][1])
  mydict = read_element_text(mydict, root[1][36][2])
  for ele in root[1][36][3]:
    for ele2 in ele:
      mydict = read_element_text(mydict, ele2)
  return(mydict)

def TCGAUCS(root):
  mydict = {}
  clinical_index = [3, 4, 27, 31] + list(range(13, 21))
  for i in clinical_index:
    mydict = read_element_text(mydict, root[1][i])
  mydict = read_element_text(mydict, root[1][36][0])
  mydict = read_element_text(mydict, root[1][34][1])
  mydict = read_element_text(mydict, root[1][34][2])
  for ele in root[1][34][3]:
    for ele2 in ele:
      mydict = read_element_text(mydict, ele2)
  for ele in root[1][35]:
    mydict = read_element_text(mydict, ele)
  return(mydict)


def TCGAUVM(root):
  mydict = {}
  clinical_index = [3, 4, 20, 24]
  for i in clinical_index:
    mydict = read_element_text(mydict, root[1][i])
  mydict = read_element_text(mydict, root[1][26][1])
  mydict = read_element_text(mydict, root[1][26][2])
  for ele in root[1][26][3]:
    for ele2 in ele:
      mydict = read_element_text(mydict, ele2)
  clinical_index_2 = [0, 1, 2, 3, 24, 25, 26] + list(range(8, 23))
  for i in clinical_index:
    mydict = read_element_text(mydict, root[1][27][i])
  mydict = read_element_text(mydict, root[1][27][4][0])

  for ele in root[1][27][5]:
    mydict[ele[0].text] = ele[1].text

  for ele in root[1][27][6]:
    s = ele.text
    try:
      mydict[split_tag(ele) + "_" + s.rsplit(" ", 1)[0]] = s.rsplit(" ", 1)[1]
    except:
      mydict[split_tag(ele)] = ele.text
  for ele in root[1][27][7]:
    s = ele.text
    try:
      mydict[split_tag(ele) + "_" + str(s.rsplit(" ", 1)[0])] = s.rsplit(" ", 1)[1]
    except:
      mydict[split_tag(ele)] = ele.text
  return(mydict)
  
