import re
import numpy as np
import math
import sympy
from fractions import Fraction
import itertools

#Chuyen trinh tu ve dang chinh tac (vd: ij-qq -> +i+j-q-q)
def split(word):
    return [char for char in word]

def solve(s, t):  # Dan xen hai string
      res=""
      i=0
      m=min(len(s),len(t))
      while i <(m):
         res+=s[i]+t[i]
         i+=1
      return res+s[i:]+t[i:]

def Convert_ct(sequence):   # Chuyen trinh tu thanh dang chuan tac 
	if sequence[0] != '-':
		sequence = '+'+ sequence
	dau = {'++':'+','+-':'-','-+':'-','--':'+'}
	sequence = re.sub('({})'.format('|'.join(map(re.escape, dau.keys()))), lambda m: dau[m.group()], sequence)
	
	chara_ct = {'+':'1', '-':'0'}
	rem_ct = sequence.maketrans(chara_ct)
	sequence = sequence.translate(rem_ct)

	ctw = re.split(r'[1 0]',sequence) 
	ctw = list(filter(None, ctw))

	lengh = []
	for i in range(len(ctw)):
		lengh.append(len(ctw[i]))

	dau_ct = split(re.sub('\D', '', sequence))

	word = ''.join(ctw)

	dau_list = []
	for i in range(len(dau_ct)):
		dau_list.append(dau_ct[i]*lengh[i])

	dau_list = ''.join(dau_list)
	sequence = solve(dau_list,word)

	chara_ctr = {'1':'+', '0':'-'}
	rem_ctr = sequence.maketrans(chara_ctr)
	sequence = sequence.translate(rem_ctr)
	return sequence

#Phien ma y_sequence
def trans(sequence):
	guide = {'i':'j','j':'i','q':'-q'}
	transTable = sequence.maketrans(guide)
	sequence = sequence.translate(transTable)

	dau = {'++':'+','+-':'-','-+':'-','--':'+'}
	sequence = re.sub('({})'.format('|'.join(map(re.escape, dau.keys()))), lambda m: dau[m.group()], sequence)
	return sequence

#Phien ma nhi phan

def anp(sequence):
	anp_table = {'i':'1','j':'0','p':'1','q':'1'}
	anp_trans = sequence.maketrans(anp_table)
	sequence = sequence.translate(anp_trans)
	return sequence

def laydau(sequence): # Lay dau cua trinh tu
	chara = {'i':'', 'j':'', 'p':'', 'q':''}
	rem = sequence.maketrans(chara)
	sequence = sequence.translate(rem)
	return sequence

def hoanviv(liststr):	# Tao list hoan vi vong trinh tu
	lay = []
	for k in range(len(liststr)):
		dau_tem = []
		for i in range(len(liststr)):
			dau_tem.append(liststr[i-k])
		lay.append(dau_tem)
	return lay

def laychu(sequence): # Lay chu cua trinh tu
	chara = {'+':'', '-':''}
	rem = sequence.maketrans(chara)
	sequence = sequence.translate(rem)
	return sequence

# Chuyen string thanh matrix
def Convert(string):
    list1=[]
    list1[:0]=string
    return list1

# Tinh trinh tu the nang
def nhan(np,dau):  # Tinh dau cua nhi phan
	if dau == '+':
		value=int(np)
	else:
		value = int('-'+ np)
	return value

def tn(np_list,dau_list):  # Tinh the nang cua list
	tn_list = [0]
	for i in range(len(np_list)):
		tn_list.append(tn_list[i] + nhan(np_list[i],dau_list[i]))
	del tn_list[0]
	return tn_list


# Tim nghiem
def index_ng(tn_list):  #Lay index cua nghiem
	index_list = []
	for i in range(len(tn_list)):
		if tn_list[i] == 0:
			index_list.append(i)
	return index_list

def check_ng(nghiem_1,ng_list): # check xem thanh phan co trong list hay khong
	ans = 'no'
	for i in ng_list:
		if nghiem_1 == i:
			ans = 'yes'
	return ans

def check_ng_pro(nghiem_1,ng_list): # check xem thanh phan co trong multilist hay khong
	ans = 'no'
	for i in ng_list:
		for k in i:
			if nghiem_1 == k:
				ans = 'yes'
	return ans

def tra_ng(nghiem_1,ng_list):
	tra = []
	for i in ng_list:
		if check_ng(nghiem_1,i) == 'yes':
			tra = i
	return tra

def del_index(del_list, index_list): # Xoa thanh phan phan trong list dua vaof list index
	somelist = [i for j, i in enumerate(del_list) if j not in index_list]
	return somelist

def ng(np_list,dau_list): # Xuat nghiem cua trinh tu
	nghiem = []
	for i in range(len(np_list)-1):
		nghiem.append([0] + tn(np_list[i+1:],dau_list[i+1:]))
	dong_ng = []
	for i in range(len(nghiem)):
		dong_ng.append([x+i for x in index_ng(nghiem[i])])

	
	del_list = []
	for i in range(len(dong_ng)-1):
		for k in range(i+1,len(dong_ng)):
			if check_ng(dong_ng[k][0],dong_ng[i]) == 'yes':
				del_list.append(k)
	dong_ng = del_index(dong_ng,del_list)

	if check_ng_pro(len(np_list)-1,dong_ng) != 'yes':
		dong_ng.append([len(np_list)-1])
	return dong_ng
 
def max_val(nghiem_list):  # Tim gia tri lon nhat trong list bac 2
	l = 0
	for list_con in nghiem_list:
		for ele in list_con:
			if ele > l:
				l = ele 
	return l

def extractDigits(lst):  # Chuyen list thanh list of list
    res = []
    for el in lst:
        sub = el.split(', ')
        res.append(sub)
      
    return(res)

def sao(nghiem_list): # Xuat gian do sao tu list nghiem
	sao_list = extractDigits(['a']*len(nghiem_list))
	length = max_val(nghiem_list)
	for i in range(len(nghiem_list)):
		for k in range(length+1): 
			if check_ng(k,nghiem_list[i]) == 'yes':
				sao_list[i].append('*')
			else:
				sao_list[i].append(".")
	for list_con in sao_list:
		del list_con[0]
	return sao_list

def seri_list(lista): # Xuat seri stt cua list
	listp = []
	for i in range(1,len(lista)+1):
		listp.extend([i])
	return listp

def listToString(s): #Chuyen list thanh string
    
    # initialize an empty string
    str1 = "" 
    
    # traverse in the string  
    for ele in s: 
        str1 += ele  
    
    # return string  
    return str1 

def count_so(list_1,list_2): #Tao list so luong chu so lon nhat giua hai list 
	long_1 = []
	long_2 = []
	max_chos = []
	for i in list_1:
		long_1.append(len(str(i)))

	for i in list_2:
		long_2.append(len(str(i)))


	for i in range(len(list_2)):
		max_chos.append(max(long_1[i],long_2[i]))

	return max_chos

def tra_tn(list_index, list_tn): #Chuyen tu list_index thanh list the nang
	tra_tn = []
	for i in list_index:
		tra_tn.append(list_tn[i])
	return tra_tn

def trich_ng(ng_list, list_nghiem): #Trich list nghiem
	res = []
	for k in list_nghiem:
		if check_ng(ng_list[0],k) == "yes":
			res = k
	return res

def count_lan(val,k_step,list_tn): # Dem so lan di qua gia tri val trong k step trong list tn
	lan = 0
	for i in range(1,k_step):
		if list_tn[0-i] == val:
			lan += 1
	return lan

def check_start(start_index, step, x_tn_list, y_tn_list): # Check xem co di qua goc hay khong
	a = ''
	for i in range(1,step):
		if (x_tn_list[start_index-i] == 0) and (y_tn_list[start_index-i] == 0):
			a = "pass"
		else:
			a= "notpass"
	return a  

def luong(x_np_ma,x_dau_ma,x_nghiem,checkv,x_tn,y_tn): # Tinh luong cua trinh tu
	luong = []

	# Xac dinh nghiem 0
	for i in range(len(x_np_ma)-1):
		if x_np_ma[i] == '1' :
			luong.append("a")
		else:
			if x_dau_ma[i+1] == x_dau_ma[i]:
				luong.append("0")
			else:
				luong.append("b")

	if x_np_ma[-1] == '1' :
			luong.append("a")
	else:
		if checkv == 1:
			if x_dau_ma[0] == x_dau_ma[-1]:
				luong.append("0")
			else:
				luong.append("b")
		else:
			if x_dau_ma[-1] == '-':
				luong.append("b")
			else:
				luong.append('0')

	#Xac dinh nghiem 0 cua 1

	for i in range(len(luong)-1):
		if luong[i] == 'a':
			if x_dau_ma[i+1] == x_dau_ma[i]:
				luong[i] = "a"
			else:
				luong[i] = "0"

	if checkv == 1:
		if luong[-1] == 'a':
			if x_dau_ma[0] == x_dau_ma[-1]:
				luong[-1] = "a"
			else:
				luong[-1] = "0"
	else:
		if luong[-1] == "0" and x_dau_ma[-1] == '+':
			luong[-1] = '0'
		else: 
			luong [-1] = 'a'
	
	for i in range(len(luong)):
		if luong[i] == 'b':
			luong[i] = 'a'
	
	# Xac dinh nghiem 1 va -1

	x_nghiem_k0 = []
	for i in range(len(x_nghiem)):
		x_nghiem_k0_lay = []
		for k in range(len(x_nghiem[i])):
			if luong[x_nghiem[i][k]] != '0':
				x_nghiem_k0_lay.append(x_nghiem[i][k])
		x_nghiem_k0.append(x_nghiem_k0_lay)
	x_nghiem_k0 = [ele for ele in x_nghiem_k0 if ele != []] # Xoa list rong trong list

	x_nghiem_np = []
	for i in x_nghiem_k0:
		lay_nghiem = []
		if x_tn[i[0]] > 0:
			for k in range(len(i)):
				if (k % 2) == 0:
					lay_nghiem.append("+")
				else:
					lay_nghiem.append("-")
		else:
			if x_tn[i[0]] < 0:
				for k in range(len(i)):
					if (k % 2) == 0:
						lay_nghiem.append("-")
					else:
						lay_nghiem.append("+")
			else:
				la = []
				k_lis = []
				
				x_ng_0 = trich_ng(i,x_nghiem)
				x_tn_0 = tra_tn(x_ng_0,x_tn)
			
				for k in range(1,len(x_tn)-1):
					if x_tn[i[0]-k] != 0:
						la.append(x_tn[i[0]-k])
						k_lis.append(k)
				
				
				step_hv = count_lan(0,k_lis[0],x_tn)
				

				if (check_start(i[0],k_lis[0],x_tn,y_tn) == "pass") and (luong[-1] != '0'): 
					x_nghiem_k0[x_nghiem_k0.index(i)] = hoanviv(i)[step_hv]

				if la[0] > 0:
					for k in range(len(i)):
						if (k % 2) == 0:
							lay_nghiem.append("-")
						else:
							lay_nghiem.append("+")
					
				else:
					for k in range(len(i)):
						if (k % 2) == 0:
							lay_nghiem.append("+")
						else:
							lay_nghiem.append("-")
					
		x_nghiem_np.append(lay_nghiem)
	

	for i in range(len(x_nghiem_k0)):
		for k in range(len(x_nghiem_k0[i])):
				if luong[x_nghiem_k0[i][k]] == "a":
					luong[x_nghiem_k0[i][k]] = x_nghiem_np[i][k]

	return luong

def xuat_luong(y_tn,luong): #Tinh gia tri luong
	replace_dau = []
	for i in luong:
		if i == '0':
			replace_dau.append('+0*')
		else:
			replace_dau.append(i)

	ket_hop = eval(listToString([val for pair in zip(replace_dau, map(str,y_tn)) for val in pair])) 
	return ket_hop


def Tim_tn(x_sequence): # Chuyen ve list [x_tn, y_tn]
	x_sequence = Convert_ct(x_sequence)
	y_sequence= trans(x_sequence)
	x_ck =  x_sequence.replace("+","")
	x_ck =  x_ck.replace("-","")

	y_ck =  y_sequence.replace("+","")
	y_ck =  y_ck.replace("-","")

	x_np = anp(x_ck)
	y_np = anp(y_ck)

	x_dau = laydau(x_sequence)
	y_dau = laydau(y_sequence)

	y_tn = tn(y_np,y_dau)
	x_tn = tn(x_np,x_dau)

	list_tn = [x_tn,y_tn]
	return list_tn

def checkv(x_tn, y_tn):	# La duong hay vong khep kin (1 la circle, 0 la path)
	checkv = 0
	if y_tn[-1] == 0 and x_tn[-1] == 0:
		checkv = 1
	return checkv

"""
Giải hệ bất phương trình:
Giải các hệ bất phương trình lớn hơn bằng có dạng như:

	2x -  y + z >= 0
	 x + 2y - z >= 0
	-x +  y + z >= 0

Tìm khoảng giá trị của x,y,z.
"""

def numrowpls(lista,column): # Tra ve STT hang co gia tri duong o 1 cot
	la = []
	for i in range(len(lista)):
		if lista[i,column] > 0:
			la.append(i)
	#print(la)
	return la

def numrowmis(lista,column): # Tra ve STT hang co gia tri am o 1 cot
	la = []
	for i in range(len(lista)):
		if lista[i,column] < 0:
			la.append(i)
	#print(la)
	return la

def hoanviv(liststr):	# Tao list hoan vi vong trinh tu
	lay = []
	for k in range(len(liststr)):
		dau_tem = []
		for i in range(len(liststr)):
			dau_tem.append(liststr[i-k])
		lay.append(dau_tem)
	return lay

#print(hoanviv([0,1,2,3,4]))


def inequal(matrix): #giai he bat phuong trinh tim ra khoang bien doi thay the listk = [[k1,k2,k3,k4],[k5,k6,k7,k8]]

	#print(matrix)
	#print("________")


	maximum = []
	minimum = []


	for v in range(len(matrix[0])-2):


		#print(v)

		max_val = max(np.max(matrix[:,v]),abs(np.min(matrix[:,v])))
		#print("max: "+str(max_val))

		listpls = numrowpls(matrix,v)
		listminus = numrowmis(matrix,v)

		#print("listplus: "+ str(listpls))
		#print("listminus: "+ str(listminus))


		listminus_ma = []
		for i in range(len(listminus)):
			listminus_ma.append(max_val/abs(matrix[listminus[i],v])*matrix[listminus[i],:])
		listminus_ma = np.array(listminus_ma)

		#print("listminus: "+ str(listminus_ma))

		listpls_ma = []
		for i in range(len(listpls)):
			listpls_ma.append(max_val/abs(matrix[listpls[i],v])*matrix[listpls[i],:])
		listpls_ma = np.array(listpls_ma)

		#print("listplus: "+ str(listpls_ma))

		listpls_ma_new = listpls_ma + listminus_ma[0,:]
		#print(listpls_ma_new)

		listminus_ma_new = listminus_ma + listpls_ma[0,:]
		#print(listminus_ma_new)

		list_ma_com = np.vstack((listminus_ma_new,listpls_ma_new))
		#print(list_ma_com)

		new_array = [tuple(row) for row in list_ma_com]
		uniques = np.unique(new_array, axis=0)
		#print(uniques)


		#Dieu chinh lai matrix, xoa cac hang da xet
		liscom = listpls + listminus
		#print(liscom)

		matrix = np.delete(matrix,liscom,0)
		matrix = np.vstack((matrix,uniques))

		#print("")
		#print(matrix)
		#print("__..__..___")

	#print("")
	#print(matrix)

	# Tim max value
	maxi = []
	for i in range(len(matrix)):
		if matrix[i,-2] < 0:
			maxi.append(-matrix[i,-1]/matrix[i,-2])
	
	if len(maxi) == 0:
		maxo = "~"
	else:
		maxo = min(maxi)
	maximum.append(maxo)

	# Tim min value

	mini = []
	for i in range(len(matrix)):
		if matrix[i,-2] > 0:
			mini.append(-matrix[i,-1]/matrix[i,-2])
	
	if len(mini) == 0:
		mino = "~"
	else:
		mino = max(mini)
	minimum.append(mino)

	#print("_______")

	#print(maximum)
	#print(minimum)

	kq = []
	
	kq.append(minimum[len(maximum)-1])
	kq.append(maximum[len(maximum)-1])


	return(kq)



def range2num(list_range): #Chuyen range list to listnum
	dower = int(math.ceil(list_range[0]))
	#print(dower)

	upper = int(math.floor(list_range[1]))
	#print(upper)

	listn = list(range(dower,upper+1))
	#print(listn)

	return listn


def findrangema(matrix): # Range cua bien ngoai bia
	ranges = inequal(matrix)
	#print(ranges)

	list0 = range2num(ranges)
	return list0 

def findmatrix(matrix,i): # Rut gon bien ngoai cung voi gia tri i
	

	matrix_tem = matrix[:,[-2,-1]]
	#print(matrix_tem)

	matrix_tem_col = matrix_tem[:,0]*i+matrix_tem[:,1]
	#print(matrix_tem_col)

	matrix = np.delete(matrix,[-1,-2],1)
	matrix = np.column_stack((matrix,matrix_tem_col))

	return matrix

def messyrange(range1,matrix): # Dua vao range cua bien ngoai bia cua matrix, tim range cua bien tiep theo

	totalist1 = []
	totalmatrix = []

	index_range = range1[0:len(range1)-1]
	#print(index_range[0])

	for i in range(len(range1[-1])):
		

		range2 = []
		range2.append(index_range[0]+1)
		range2.append(i)
		range2.extend(index_range)
		range2.append(findrangema(findmatrix(matrix[-1],range1[-1][i])))


		#print(matrix2)

		totalist1.append(range2)	
	
	return totalist1


def messymatrix(range1,matrix): # Dua vao range cua bien ngoai bia cua matrix, tim matrix cua bien tiep theo

	
	totalist1 = []
	totalmatrix = []

	index_range = range1[0:len(range1)-1]
	#print(index_range[0])

	for i in range(len(range1[-1])):
		
		matrix2 =[]
		matrix2.append(index_range[0]+1)
		matrix2.append(i)
		matrix2.extend(index_range)
		matrix2.append(findmatrix(matrix[-1],range1[-1][i]))
		

		#print(matrix2)

		totalmatrix.append(matrix2)

	
	
	return totalmatrix

def displaylist(lista): #bieu dien cac thanh phan list theo hang
	for i in range(len(lista)):
		print(i)
		print(lista[i])
		print("____")

def listToStringpro(s): #Chuyen list thanh string
    
    # initialize an empty string
    str1 = "" 
    
    # traverse in the string  
    for ele in s: 
        str1 += "-"+str(ele)  
    
    # return string  
    return str1 


def situation_num(listk): #Tra ve so truong hop dong dang
	
	listk = listk.tolist()
	matrix = np.array([[-2,0,0,1,0,listk[0][0]],
						[0,0,-2,0,-1,listk[0][1]],
						[1,0,1,0,1,listk[0][2]],
						[1,0,0,-1,-1,listk[0][3]],
						[0,-2,0,-1,0,listk[1][0]],
						[0,0,0,0,1,listk[1][1]],
						[0,1,0,1,0,listk[1][2]],
						[0,1,1,0,0,listk[1][3]]])

	#print(matrix)


	range1 = [0,0,findrangema(matrix)]
	matrix = [0,0,matrix]

	#print(range1)
	totalist0 = range1

	totalist1 = messyrange(range1,matrix)
	totalmatrix1 = messymatrix(range1,matrix)



	#displaylist(totalist1)
	#print(totalmatrix1)
	#print(len(totalist1))

	totalist2 = []
	totalmatrix2 = []
	for i in range(len(totalist1)):
		totalist2_tem  = []
		totalmatrix2_tem = []

		totalist2_tem = messyrange(totalist1[i],totalmatrix1[i])
		totalmatrix2_tem = messymatrix(totalist1[i],totalmatrix1[i])

		totalist2.extend(totalist2_tem)
		totalmatrix2.extend(totalmatrix2_tem)

	#displaylist(totalist2)
	#print(len(totalist2))


	totalist3 = []
	totalmatrix3 = []
	for i in range(len(totalist2)):
		totalist3_tem  = []
		totalmatrix3_tem = []

		totalist3_tem = messyrange(totalist2[i],totalmatrix2[i])
		totalmatrix3_tem = messymatrix(totalist2[i],totalmatrix2[i])

		totalist3.extend(totalist3_tem)
		totalmatrix3.extend(totalmatrix3_tem)

	#displaylist(totalist3)
	#print(len(totalist3))

	totalist4 = []
	totalmatrix4 = []
	for i in range(len(totalist3)):
		totalist4_tem  = []
		totalmatrix4_tem = []

		totalist4_tem = messyrange(totalist3[i],totalmatrix3[i])
		totalmatrix4_tem = messymatrix(totalist3[i],totalmatrix3[i])

		totalist4.extend(totalist4_tem)
		totalmatrix4.extend(totalmatrix4_tem)

	#displaylist(totalist4)
	#print(len(totalist4))


	database = totalist1 + totalist2 + totalist3 + totalist4
	database.insert(0, totalist0)


	# Xuat database
	"""
	textfile = open("database.txt", "w")
	for element in database:
	    textfile.write(str(element) + "\n")
	textfile.close()
	"""

	#Tinh co bao nhieu truong hop
	situa_value = 0
	for i in totalist4:
		situa_value += len(i[-1])
	#print("Số trường hợp: " + str(situa_value))
	return situa_value


def solvebdt(listk): # Giai he bat dang thuc de thu he so 5 vecto co so cho phep bien doi 

	listk = listk.tolist()

	matrix = np.array([[-2,0,0,1,0,listk[0][0]],
						[0,0,-2,0,-1,listk[0][1]],
						[1,0,1,0,1,listk[0][2]],
						[1,0,0,-1,-1,listk[0][3]],
						[0,-2,0,-1,0,listk[1][0]],
						[0,0,0,0,1,listk[1][1]],
						[0,1,0,1,0,listk[1][2]],
						[0,1,1,0,0,listk[1][3]]])

	#print(matrix)


	range1 = [0,0,findrangema(matrix)]
	matrix = [0,0,matrix]

	#print(range1)
	totalist0 = range1

	totalist1 = messyrange(range1,matrix)
	totalmatrix1 = messymatrix(range1,matrix)



	#displaylist(totalist1)
	#print(totalmatrix1)
	#print(len(totalist1))

	totalist2 = []
	totalmatrix2 = []
	for i in range(len(totalist1)):
		totalist2_tem  = []
		totalmatrix2_tem = []

		totalist2_tem = messyrange(totalist1[i],totalmatrix1[i])
		totalmatrix2_tem = messymatrix(totalist1[i],totalmatrix1[i])

		totalist2.extend(totalist2_tem)
		totalmatrix2.extend(totalmatrix2_tem)

	#displaylist(totalist2)
	#print(len(totalist2))


	totalist3 = []
	totalmatrix3 = []
	for i in range(len(totalist2)):
		totalist3_tem  = []
		totalmatrix3_tem = []

		totalist3_tem = messyrange(totalist2[i],totalmatrix2[i])
		totalmatrix3_tem = messymatrix(totalist2[i],totalmatrix2[i])

		totalist3.extend(totalist3_tem)
		totalmatrix3.extend(totalmatrix3_tem)

	#displaylist(totalist3)
	#print(len(totalist3))

	totalist4 = []
	totalmatrix4 = []
	for i in range(len(totalist3)):
		totalist4_tem  = []
		totalmatrix4_tem = []

		totalist4_tem = messyrange(totalist3[i],totalmatrix3[i])
		totalmatrix4_tem = messymatrix(totalist3[i],totalmatrix3[i])

		totalist4.extend(totalist4_tem)
		totalmatrix4.extend(totalmatrix4_tem)

	#displaylist(totalist4)
	#print(len(totalist4))


	database = totalist1 + totalist2 + totalist3 + totalist4
	database.insert(0, totalist0)


	# Xuat database
	"""
	textfile = open("database.txt", "w")
	for element in database:
	    textfile.write(str(element) + "\n")
	textfile.close()
	"""

	#Tinh co bao nhieu truong hop
	situa_value = 0
	for i in totalist4:
		situa_value += len(i[-1])
	#print("Số trường hợp: " + str(situa_value))

	#Trả về giá trị trong database
	complete_index = []
	for i in range(len(totalist4)):
		for k in range(len(totalist4[i][-1])):
			complete_index.append([5,k] + totalist4[i][0:len(totalist4[i])-1])


	#displaylist(complete_index)
	#print(len(complete_index))

	# Tạo thu vien (tách và chuyển index và array thành dictionary)

	lib ={}
	for i in range(len(database)):
		lib[listToStringpro(database[i][0:len(database[i])-1])] = database[i][-1]
	#print(lib)

	# Nhan ket qua 
	## Tra ve he so cua 5 vecto
	response_list = []
	for k in range(len(complete_index)):
		
		index = complete_index[k]

		response = []
		for i in range(0,len(index)-2,2):
			#print(i)
			response.append(lib[listToStringpro(index[i+2:])][index[i+1]])
		#print(k)
		#print(response)
		#print("____")

		response_list.append(response)

	#displaylist(response_list)
	return response_list

## Tra ve matrix chuyen doi

"""
listk = np.array([[1,2,3,4],[5,6,7,8]])

displaylist(solvebdt(listk))
#print(situation_num(listk))
"""

def calnon(sequence): #Chuyen ve dang string chinh tac (ai+bj+cp+dq)
	sequence_ct = Convert_ct(sequence)

	dau_seq = Convert(laydau(sequence_ct)[::-1])
	chu_seq = Convert(laychu(sequence_ct)[::-1])

	listchar = ["i","j","p","q"]
	ber = []
	for k in listchar:
		num = 0
		for i in range(len(chu_seq)):
			if chu_seq[i] == k:
				if dau_seq[i] == "+":
					num += 1
				else:
					num += -1
		ber.append(num)

	dau =[]
	for i in ber:
		if i >= 0:
			dau.append("+")
		else:
			dau.append("")

	string = ""
	for i in range(len(dau)):
		string += dau[i] + str(ber[i]) + listchar[i]

	return string

def num_cal(sequence): #Chuyen ve list he so cua dang chinh tac [a,b,c,d]
	sequence_ct = Convert_ct(sequence)

	dau_seq = Convert(laydau(sequence_ct)[::-1])
	chu_seq = Convert(laychu(sequence_ct)[::-1])

	listchar = ["i","j","p","q"]
	ber = []
	for k in listchar:
		num = 0
		for i in range(len(chu_seq)):
			if chu_seq[i] == k:
				if dau_seq[i] == "+":
					num += 1
				else:
					num += -1
		ber.append(num)

	return(ber)

def dau_cal(sequence): #Chuyen ve list dau chinh tac [+,+,-,+)
	sequence_ct = Convert_ct(sequence)

	dau_seq = Convert(laydau(sequence_ct)[::-1])
	chu_seq = Convert(laychu(sequence_ct)[::-1])

	listchar = ["i","j","p","q"]
	ber = []
	for k in listchar:
		num = 0
		for i in range(len(chu_seq)):
			if chu_seq[i] == k:
				if dau_seq[i] == "+":
					num += 1
				else:
					num += -1
		ber.append(num)

	dau =[]
	for i in ber:
		if i >= 0:
			dau.append("+")
		else:
			dau.append("-")


def phandau(sequence): #Phan thanh hai nhom cong-tru rieng (ij-pi+pq-j -> ijpq-ijp)
	sequence_ct = Convert_ct(sequence)

	dau_seq = Convert(laydau(sequence_ct)[::-1])
	chu_seq = Convert(laychu(sequence_ct)[::-1])

	chu_cong=[]
	for i in range(len(dau_seq)):
		if dau_seq[i] == "+":
			chu_cong.append(chu_seq[i])

	chu_tru= []
	for i in range(len(dau_seq)):
		if dau_seq[i] == "-":
			chu_tru.append(chu_seq[i])

	chu_final = calnon(listToString(chu_cong))+calnon("-"+listToString(chu_tru))

	return(chu_final)

def phandau_ef(sequence): #Phan thanh matran he so cua hai nhom cong-tru ( ij-pi+pq-j -> [[1,1,1,1],[1,1,1,0]] )
	sequence_ct = Convert_ct(sequence)

	dau_seq = Convert(laydau(sequence_ct)[::-1])
	chu_seq = Convert(laychu(sequence_ct)[::-1])


	chu_cong=[]
	for i in range(len(dau_seq)):
		if dau_seq[i] == "+":
			chu_cong.append(chu_seq[i])


	chu_tru= []
	for i in range(len(dau_seq)):
		if dau_seq[i] == "-":
			chu_tru.append(chu_seq[i])

	if len(chu_tru) == 0:
		chu_final = [num_cal(listToString(chu_cong)),[0,0,0,0]]	 
	else:
		if len(chu_cong) ==0:
			chu_final = [[0,0,0,0],num_cal(listToString(chu_tru))]	
		else:	
			chu_final = [num_cal(listToString(chu_cong)),num_cal(listToString(chu_tru))]

	return(np.array(chu_final))

def phandau_ef_dau(sequence): #Phan thanh ma tran he so cua hai nhom cong-tru co dau tru (ij-pi+pq-j -> [[1,1,1,1],[-1,-1,-1,0]] )
	sequence_ct = Convert_ct(sequence)

	dau_seq = Convert(laydau(sequence_ct)[::-1])
	chu_seq = Convert(laychu(sequence_ct)[::-1])

	chu_cong=[]
	for i in range(len(dau_seq)):
		if dau_seq[i] == "+":
			chu_cong.append(chu_seq[i])

	chu_tru= []
	for i in range(len(dau_seq)):
		if dau_seq[i] == "-":
			chu_tru.append(chu_seq[i])

	num_tru = num_cal(listToString(chu_tru))
	for i in range(len(num_tru)):
		num_tru[i] = -num_tru[i]
	chu_final = [num_cal(listToString(chu_cong)),num_tru]

	return(np.array(chu_final))


def check_list_int(lista): #Kiem tra trong list co float hay khong? (0 la nhan, 1 la loai)
	kq = 0
	for i in lista:
		#print(i.is_integer())
		if i.is_integer() == False:
			kq += 1
	#print(kq)
	kqt = 0
	if kq > 0:
		kqt = 1
	return kqt

def check_multi_int(multi_matrix): #Kiem tra trong ma tran co float hay khong
	kq = 0
	for i in range(len(multi_matrix)):
		if check_list_int(multi_matrix[i,:]) == 1:
			kq += 1
	kqt = 0
	if kq > 0:
		kqt = 1
	return kqt

def sum_array(array): # Tinh tong cac thanh phan trong array
	sum = 0
	for i in range(len(array)):
		for k in range(len(array[i])):
			sum += array[i,k]
	return sum

def path_num(array): # Tinh so con duong dong dang cua array
	tich = 1
	for i in range(len(array)):
		for k in range(len(array[i])):
			tich = tich*math.factorial(array[i,k])
	path = int(math.factorial(sum_array(array))/tich)
	return path

def stringwhile(ex): # Chuyen array (ma trận thức) ve dang string don thuan (vd: [1,0,1,1][0,2,0,1]) -> ipq-jjq)

	char = {0:"i",1:"j",2:"p",3:"q"}

	sre = ""
	for i in range(len(ex)):
		dau = "+"
		if i/2 != 0:
			dau = "-"
		for k in range(len(ex[0])):
			sre += ex[i][k]*(dau + char[k])
	return sre	

def liststring(ex): #Chuyen string ve dang list de hoan vi (+i+p+q-j-j-q -> ['+i', '+p', '+q', '-j', '-j', '-q'])
	str_tem = stringwhile(ex)
	#print(str_tem)

	str_tem1 = Convert(str_tem)

	str_tem2 = []
	for i in range(0,len(str_tem1),2):
		str_tem2.append(str(str_tem1[i])+str(str_tem1[i+1]))
	return str_tem2

def dongdang(ex): # Xuất các con đường đồng dạng của 1 ma trận thức

	listne = liststring(ex)
	per_list = list(itertools.permutations(listne))
	for i in range(len(per_list)):
		per_list[i] = list(per_list[i])

	# print(len(per_list))

	per_list.sort()
	final_list = list(per_list for per_list,_ in itertools.groupby(per_list))
	#print(len(final_list))

	final_str_list = []
	for i in final_list:
		final_str_list.append(listToString(i))
	return final_str_list

"""
a1 = -phandau_ef("ii")+phandau_ef("pq")
a2 = a1[[1,0],:]

#print("a1 là: "+str(a1))
#print("a2 là: "+str(a2))

a5 = -phandau_ef("q-i")+phandau_ef("i-p")
a6 = a5[[1,0],:]

#print("a5 là: "+str(a5))
#print("a6 là: "+str(a6))

a3 = -phandau_ef("jj")+phandau_ef("p-q")
a4 = a3[[1,0],:]

#print("a3 là: "+str(a3))
#print("a4 là: "+str(a4))

a7 = -phandau_ef("j+q")+phandau_ef("p-j")
a8 = a7[[1,0],:]

#print("a7 là: "+str(a7))
#print("a8 là: "+str(a8))

total = [a1,a2,a3,a4,a5,a6,a7,a8]

matrix_full = []
for j in range(len(total[0])):
	matrix_part = []
	for i in range(0,4):
		hang = []
		for k in range(len(total)):
			hang.append(total[k][j,i])
		matrix_part.append(hang)
	matrix_full.extend(matrix_part)

#print(matrix_full)

r_value = len(total[0][0])

matrix_full_ranged = []
for i in range(r_value):
	matrix_full_ranged.append(matrix_full[i])
	matrix_full_ranged.append(matrix_full[4+i])
matrix_full_ranged = np.array(matrix_full_ranged)
#print(matrix_full_ranged)

rankma = np.linalg.matrix_rank(matrix_full_ranged)
#print("Hang cua ma tran la: "+ str(rankma))

matrix_thang = sympy.Matrix(matrix_full_ranged).rref()
matrix_thang = np.array(matrix_thang[0])
#print("Ma tran bac thang: ")
#print(matrix_thang)


matrix_full_ranged_order = matrix_full_ranged[[0,1,2,3,4,5,6,7],:]
#matrix_full_ranged_order = matrix_full_ranged[[0,2,4,6,7,1,3,5],:] #Bỏ 3 trận 2,4,6 (1,3,5) và lấy các ma trận còn lại làm gốc 
#print("Ma tran ban dau la:")
#print(matrix_full_ranged_order)

 #Tinh nghiem


#Chon 5 ma tran dau lam ma tran goc
he = matrix_full_ranged_order[:5,:5]
bien = 1*matrix_full_ranged_order[:5,7]


#print(he)
#print(np.linalg.matrix_rank(he))
#print(bien)

nghiem = np.linalg.solve(he,bien)

#print("nghiem cua pt la: "+ str(nghiem))

#Tinh thu xem sao
he_test=matrix_full_ranged_order[:8,:5]
#print(he_test)

test = np.dot(he_test,nghiem)
#print("Giai he coi thu: " + str(test))

a1_ma = np.array(a1)
a2_ma = np.array(a2)
a3_ma = np.array(a3)
a4_ma = np.array(a4)
a5_ma = np.array(a5)
a6_ma = np.array(a6)
a7_ma = np.array(a7)
a8_ma = np.array(a8)

#print(a1_ma)
#print(a2_ma)
#print(-1*a1_ma+1*a2_ma-0*a3_ma+0*a4_ma-2*a5_ma+0*a6_ma+1*a7_ma+1*a8_ma)
"""	

def tuyenchon(hv):
	#Tuyển chọn biến để bỏ (bien bỏ phải thỏa mãn hệ số của nó = 1 và hai bien kia bằng 0 trong hệ) 
	#hv = np.array([[-1,1,1,-1,-2,0,0,2],[-1,1,-1,1,-2,0,2,0],[1,-1,0,0,1,-1,0,0]])
	print(hv)
	print("")
	print("_________________________")

	check_1 = 0
	check_0 = 0
	check_v = 0
	tt_cot0 =[]
	tt_cot1 =[]
	tt_cotv =[]
	for t in range(0,len(hv[0])-2):
		for j in range(t+1,len(hv[0])-1):
			for v in range(j+1,len(hv[0])):
				take_he = np.transpose(hv[:,[t,j,v]])
				print("STT: " + str(t+1) + str(j+1) + str(v+1))
				print("Det: "+ str(np.linalg.det(take_he)))

				if np.linalg.det(take_he) != 0:
					take_bien = np.array([[1,0,0],[0,1,0],[0,0,1]])
					#print(take_bien)

					take_nghiem_hv = []
					for k in range(len(take_bien)):
						take_nghiem = np.linalg.solve(take_he,take_bien[k])  
						for i in range(len(take_nghiem)):
							take_nghiem[i] = str(round(take_nghiem[i],2))
							#print(Fraction(str(round(take_nghiem[i],2)))
						take_nghiem_hv.append(take_nghiem)
					take_nghiem_hv = np.array(take_nghiem_hv)

					#print(take_nghiem_hv)

					take_pt_hv = []
					for i in range(len(take_nghiem_hv)):
						take_pt = np.dot(take_nghiem_hv[i,:],hv)
						take_pt_hv.append(take_pt)
					take_pt_hv = np.array(take_pt_hv)

					print(take_pt_hv)
					print("Check: "+ str(check_multi_int(take_pt_hv)))


					if check_multi_int(take_pt_hv) == 0:
						tt_cot0.append(str(t+1) + str(j+1) + str(v+1))
						check_0 += 1
					else:
						tt_cot1.append(str(t+1) + str(j+1) + str(v+1))
						check_1 += 1

					print("_________________________")
				
				else:
					check_v += 1
					tt_cotv.append(str(t+1) + str(j+1) + str(v+1))
					print("Vo nghiem")
					print("_________________________")

	print("Tổng số nhận là: " + str(check_0))
	print("Tổng số loại là: " + str(check_1))
	print("Tổng số vô nghiệm là: " + str(check_v))
	print("_________________________")
	print("")
	print("STT các cột nhận: " + str(tt_cot0))
	print("")
	print("STT các cột loại: " + str(tt_cot1))
	print("")
	print("STT các cột vô nghiệm: " + str(tt_cotv))

	# Sau tuyển chọn: bỏ a4,a6 và a8.


# 5 ma tran nguyen to

def FindAlterMatrix(listk): #Tìm và tạo list ma trận thức đồng dạng với một ma thức cho trước     

	a1 = -phandau_ef("ii")+phandau_ef("pq")
	a2 = a1[[1,0],:]
	a3 = -phandau_ef("jj")+phandau_ef("p-q")
	a4 = -phandau_ef("q-i")+phandau_ef("i-p")
	a5 = -phandau_ef("j+q")+phandau_ef("p-j")


	a1 = np.array(a1)
	a2 = np.array(a2)
	a3 = np.array(a3)
	a4 = np.array(a4)
	a5 = np.array(a5)

	#print(a1)

	# Tinh so ma tran dong dang
	#listk = np.array([[1,1,0,1],[0,0,0,0]])
	#print(listk)



	#print("Số ma trận đồng dạng là: "+str(situation_num(listk)))

	# Tao list cac ma tran dong dang
	vectors_list = solvebdt(listk)
	#print(vectors_list)

	alter_matrix = []
	for i in range(len(vectors_list)):
		tran_ma = vectors_list[i][0]*a1+vectors_list[i][1]*a2+vectors_list[i][2]*a3+vectors_list[i][3]*a4+vectors_list[i][4]*a5
		alter_matrix.append(listk+tran_ma)

	#displaylist(alter_matrix)


	# Tính tổng số đường đi đồng dạng
	#print(sum_array(listk))
	#print(path_num(listk))

	path_num_total = 0
	for i in range(len(alter_matrix)):
		path_num_total += path_num(alter_matrix[i])

	#print("Tổng số đường đi đồng dạng: " + str(path_num_total))


	# Chuyển ma trận thức thành chuỗi (vd: [1,0,1,1][0,2,0,1]) -> ipq-jjq)
	#ex = np.array([[1,0,1,1],[0,2,0,1]])


	return alter_matrix


def FindAlterPath(listk): #Tìm số lượng con đường đồng dạng      

	a1 = -phandau_ef("ii")+phandau_ef("pq")
	a2 = a1[[1,0],:]
	a3 = -phandau_ef("jj")+phandau_ef("p-q")
	a4 = -phandau_ef("q-i")+phandau_ef("i-p")
	a5 = -phandau_ef("j+q")+phandau_ef("p-j")


	a1 = np.array(a1)
	a2 = np.array(a2)
	a3 = np.array(a3)
	a4 = np.array(a4)
	a5 = np.array(a5)

	#print(a1)

	# Tinh so ma tran dong dang
	#listk = np.array([[1,1,0,1],[0,0,0,0]])
	#print(listk)



	#print("Số ma trận đồng dạng là: "+str(situation_num(listk)))

	# Tao list cac ma tran dong dang
	vectors_list = solvebdt(listk)
	#print(vectors_list)

	alter_matrix = []
	for i in range(len(vectors_list)):
		tran_ma = vectors_list[i][0]*a1+vectors_list[i][1]*a2+vectors_list[i][2]*a3+vectors_list[i][3]*a4+vectors_list[i][4]*a5
		alter_matrix.append(listk+tran_ma)

	#displaylist(alter_matrix)


	# Tính tổng số đường đi đồng dạng
	#print(sum_array(listk))
	#print(path_num(listk))

	path_num_total = 0
	for i in range(len(alter_matrix)):
		path_num_total += path_num(alter_matrix[i])


	"""#Viec ghi ra file txt có thể ảnh hưởng đến tố độ xử lý 
	# Ghi ra tất cả con đường đồng dạng
	alter_path = []
	for i in alter_matrix:
		alter_path.extend(dongdang(i))
	#displaylist(alter_path)

	## Xuat file txt ghi tat ca con duong dong dang 
		
	textfile = open("total_path.txt", "w")
	for i in range(len(alter_path)):
		if ((i+1) % 6) == 0:
		    textfile.write(str(alter_path[i]) + "\n")
		else:
			textfile.write(str(alter_path[i]) + "\t")
	textfile.close()	
	"""

	return path_num_total
	
"""#Test 
listk = np.array([[2,0,0,8],[2,0,0,0]])
#listk = phandau_ef("ijp-iijp")

print(FindAlterMatrix(listk))
print("Số ma trận đồng dạng là: "+str(situation_num(listk)))
print("Số con đường đồng dạng là: "+str(FindAlterPath(listk)))
"""


def Tim_tn_path(Start_point, path): # Xac dinh cac toa do cua cac diem tren con duong
	tn = Tim_tn(path)
	#print(tn)
	tn_x = [Start_point[0]]
	tn_y = [Start_point[1]]
	for i in range(len(tn[0])):
		tn_x.append(tn[0][i]+Start_point[0])
		tn_y.append(tn[1][i]+Start_point[1])
	
	#print(tn_y)
	#print(tn_x)

	toa = []
	for i in range(len(tn_x)):
		tem = []
		tem.append(tn_x[i])
		tem.append(tn_y[i])
		toa.append(tem)
	#print(toa)
	return toa


def check_toado(toa_do_1,toa_do_2): #Check 2 toa do co trung nhau hay khong, trung = 1, khong trung = 0
	rs = 0
	if toa_do_1 == toa_do_2:
		rs = 1
	return rs

#print(check_toado([1,3],[1,3]))

def check_lap_path(S,exam): #Check xem con duong co bi tu trung hay khong, trung = 1, khong trung = 0
	toa = Tim_tn_path(S,exam)

	rs = []
	for i in range(len(toa)):
		rs1 = []
		for k in range(len(toa)):
			rs1.append(check_toado(toa[i],toa[k]))
		rs.append(rs1)
	#print(rs)

	sum_lista = []
	for i in range(len(rs)):
		sum_lista.append(sum_list(rs[i]))
	#print(sum_lista)

	if toa[0] == toa[-1]:
		sum_lista[0] = sum_lista[0] - 1
		sum_lista[-1] = sum_lista[-1] -1

	maxa = max(sum_lista)
	#print(maxa)

	final = 0
	if maxa > 1: 
		final = 1
	#print(final)

	return(final)


#S = [2,1]
#exam = "+p+j+i+q-p-j"

#print(check_lap_path(S,exam))


def Path_Nonreturn(Vector,step): #Tu vecto va step tim cac con duong di sao cho moi diem chi di qua 1 lan
	paths = VectorToPath(Vector,step)
	#print(paths)

	fill_in_paths = []
	for i in range(len(paths)):
		if check_lap_path([0,0],paths[i]) == 0:
			fill_in_paths.append(paths[i])
	#print(len(fill_in_paths))
	return fill_in_paths

#print(Path_Nonreturn([0,0],3))

def the(Start_point,path,x_or_y,value): # Tu path khi x bang 1 gia thi se thu duoc cac gia tri y tuong ung
	tn = Tim_tn(path)

	tn_x = [Start_point[0]]
	tn_y = [Start_point[1]]
	for i in range(len(tn[0])):
		tn_x.append(tn[0][i]+Start_point[0])
		tn_y.append(tn[1][i]+Start_point[1])
	
	#print(tn_y)
	#print(tn_x)

	sort = []
	if x_or_y == "x":
	 	for i in range(len(tn_y)):
	 		if tn_x[i] == value:
	 			sort.append(tn_y[i])
	else:
	 	if x_or_y == "y":
	 		for i in range(len(tn_x)):
		 		if tn_y[i] == value:
		 			sort.append(tn_x[i])
	return sort


#print(the([1,0],"+i+j+i+j","x",3))	#Thay x = 3 tim cac gia tri y

def TaoHeBpt(matrix_equaltion): #Tạo hệ bất phương trình

	he_bpt = []
	for k in range(len(matrix_equaltion)):
		he_bpt_tem = []
		for i in range(len(matrix_equaltion[k,:])-1):
			tem = []
			if matrix_equaltion[k,i] < 0:
				tem = matrix_equaltion[k,:].tolist()
				#print(tem)
				
			else:
				if matrix_equaltion[k,i] > 0:
					tem = (-1*matrix_equaltion[k,:]).tolist()
			if len(tem) != 0:
				tem[i] = 0
			he_bpt_tem.append(tem)
			he_bpt_tem = [x for x in he_bpt_tem if x]

		#he_bpt_tem = np.array(he_bpt_tem)
		#print(he_bpt_tem)
		he_bpt.extend(he_bpt_tem)

	he_bpt = np.array(he_bpt)
	return(he_bpt)

def TaoHeBpt_pro(matrix_equaltion): #Tao he bat phuong trinh tu phuong trinh

	he_bpt = []
	for i in range(len(matrix_equaltion)):
		he_bpt.append(matrix_equaltion[i,:])
		he_bpt.append(-1*(matrix_equaltion[i,:]))

	for k in range(len(matrix_equaltion[0])-1):
		ze = np.array([0]*len(matrix_equaltion[0]))
		#print(ze)

		ze[k] = 1
		he_bpt.append(ze)

	he_bpt = np.array(he_bpt)

	return he_bpt


def inequal_check(matrix): #giai he bat phuong trinh tim ra khoang bien doi thay the listk = [[k1,k2,k3,k4],[k5,k6,k7,k8]]
	#print(matrix)
	#print("________")


	maximum = []
	minimum = []

	v_list = []
	for v in range(len(matrix[0])-2):


		#print(v)

		max_val = max(np.max(matrix[:,v]),abs(np.min(matrix[:,v])))
		#print("max: "+str(max_val))


		listpls = numrowpls(matrix,v)
		listminus = numrowmis(matrix,v)

		#print("listplus: "+ str(listpls))
		#print("listminus: "+ str(listminus))

		if len(listminus) != 0 and len(listpls) != 0:
			v_list.append(v) 
			listminus_ma = []
			for i in range(len(listminus)):
				listminus_ma.append(max_val/abs(matrix[listminus[i],v])*matrix[listminus[i],:])
			listminus_ma = np.array(listminus_ma)

			#print("listminus: "+ str(listminus_ma))

			listpls_ma = []
			for i in range(len(listpls)):
				listpls_ma.append(max_val/abs(matrix[listpls[i],v])*matrix[listpls[i],:])
			listpls_ma = np.array(listpls_ma)

			#print("listplus: "+ str(listpls_ma))

			listpls_ma_new = listpls_ma + listminus_ma[0,:]
			#print(listpls_ma_new)

			listminus_ma_new = listminus_ma + listpls_ma[0,:]
			#print(listminus_ma_new)

			list_ma_com = np.vstack((listminus_ma_new,listpls_ma_new))
			#print(list_ma_com)

			new_array = [tuple(row) for row in list_ma_com]
			uniques = np.unique(new_array, axis=0)
			#print(uniques)


			#Dieu chinh lai matrix, xoa cac hang da xet
			liscom = listpls + listminus
			#print(liscom)

			matrix = np.delete(matrix,liscom,0)
			matrix = np.vstack((matrix,uniques))

			#print("")
			#print(matrix)
			#print("__..__..___")
		else:
			v_list.append("break")
			break
	return v_list


def solvebdtpro(matrix): # Giai he bat dang thuc de tim 8 he so 

	lengtha = len(matrix[0])-1
	#print(lengtha)

	range1 = [0,0,findrangemapro(matrix)]
	matrix = [0,0,matrix]

	#print(range1)
	totalist0 = range1
	#print(range1)

	totalist1 = messyrangepro(range1,matrix)
	totalmatrix1 = messymatrix(range1,matrix)



	#displaylist(totalist1)
	#print(totalmatrix1)
	#print(len(totalist1))

	database = []
	database.append(totalist1)
	datamatrix = []
	datamatrix.append(totalmatrix1)
	
	#print(database[-1])

	for v in range(2,lengtha):
		#print(v)
		totalist2 = []
		totalmatrix2 = []
		for i in range(len(database[-1])):
			#print("-"+str(i))
			totalist2_tem  = []
			totalmatrix2_tem = []

			totalist2_tem = messyrangepro(database[-1][i],datamatrix[-1][i])
			totalmatrix2_tem = messymatrix(database[-1][i],datamatrix[-1][i])

			totalist2.extend(totalist2_tem)
			totalmatrix2.extend(totalmatrix2_tem)

		database.append(totalist2)
		#print(database[-1])
		datamatrix.append(totalmatrix2)

	#displaylist(totalist2)
	#print(len(totalist2))

	database_new = [ item for elem in database for item in elem]

	database_new.insert(0, totalist0)


	# Xuat database
	"""
	textfile = open("database.txt", "w")
	for element in database:
	    textfile.write(str(element) + "\n")
	textfile.close()
	"""

	#Tinh co bao nhieu truong hop
	situa_value = 0
	for i in database[-1]:
		situa_value += len(i[-1])
	#print("Số trường hợp: " + str(situa_value))

	#Trả về giá trị trong database
	complete_index = []
	for i in range(len(database[-1])):
		for k in range(len(database[-1][i][-1])):
			complete_index.append([5,k] + database[-1][i][0:len(database[-1][i])-1])


	#displaylist(complete_index)
	#print(len(complete_index))

	# Tạo thu vien (tách và chuyển index và array thành dictionary)

	lib ={}
	for i in range(len(database_new)):
		lib[listToStringpro(database_new[i][0:len(database_new[i])-1])] = database_new[i][-1]
	#print(lib)

	# Nhan ket qua 
	## Tra ve he so cua 5 vecto
	response_list = []
	for k in range(len(complete_index)):
		
		index = complete_index[k]

		response = []
		for i in range(0,len(index)-2,2):
			#print(i)
			response.append(lib[listToStringpro(index[i+2:])][index[i+1]])
		#print(k)
		#print(response)
		#print("____")

		response_list.append(response)

	#displaylist(response_list)
	return response_list

def check_am(lista): #Check list chua so am khong.
	res = 0
	for i in lista:
		if i < 0:
			res = 1
	return res

def list2ma(lista): #Chuyen list ve ma tran thuc
	duong = []
	am = []
	for i in range(len(lista)):
		if (i % 2) != 0:
			am.append(lista[i])
		else:
			duong.append(lista[i])
	ma = np.array([duong,am])
	return ma


def findrangemapro(matrix): # Range cua bien ngoai bia
	ranges = inequal(matrix)
	#print(ranges)

	list0 = range2numpro(ranges)
	return list0 

def range2numpro(list_range): #Chuyen range list to listnum
	if list_range[0] == "~":
		dower = 0
	else:
		if list_range[0] >= 0:
			dower = int(math.ceil(list_range[0]))
		else:
			dower = 0
	#print(dower)

	upper = int(math.floor(list_range[1]))
	#print(upper)

	listn = list(range(dower,upper+1))
	#print(listn)

	return listn

def messyrangepro(range1,matrix): # Dua vao range cua bien ngoai bia cua matrix, tim range cua bien tiep theo

	totalist1 = []
	totalmatrix = []

	index_range = range1[0:len(range1)-1]
	#print(index_range[0])

	for i in range(len(range1[-1])):
		

		range2 = []
		range2.append(index_range[0]+1)
		range2.append(i)
		range2.extend(index_range)
		range2.append(findrangemapro(findmatrix(matrix[-1],range1[-1][i])))


		#print(matrix2)

		totalist1.append(range2)	
	
	return totalist1

def sum_list(lista): #Tinh tong cac so trong list
	sum = 0
	for i in range(len(lista)):
		sum += lista[i]
	return sum

def nummin_step(vector): #Tim so buoc di toi thieu cua 1 vector
	a = abs(vector[0])
	b = abs(vector[1])

	mean = min(a,b)
	bos = max(abs(a-mean),abs(b-mean))

	return mean+bos

#print(nummin_step([-3,2]))

"""
#Tuyển chọn biến để bỏ (bien bỏ phải thỏa mãn hệ số của nó = 1 và hai bien kia bằng 0 trong hệ) 
hv = np.array([[1,1,1,1,1,1,1,1],[1,-1,0,0,1,-1,1,-1],[0,0,1,-1,1,-1,-1,1]])
#tuyenchon(hv)
"""

"""Chọn 248"""


# Tim he bat phuong trinh

def VectorToPath(vector,step): #Từ số bước để đi và vector cho trước tìm các con đường khả dĩ 
	##Tạo hệ phương trình (.... = 0)

	x_val = vector[0]
	y_val = vector[1]

	matrix_equaltion = np.array([[1,1,1,1,1,1,1,1,-step],
								 [ 1,-1,0,0,1,-1,1,-1,-x_val],
								 [ 0,0,1,-1,1,-1,-1,1,-y_val]])
	#print(matrix_equaltion)

	##Tạo hệ bất phương trình

	he_bpt = TaoHeBpt_pro(matrix_equaltion)
	#print(he_bpt)


	#Tìm thứ tự thích hợp
	"""
	##Giai hệ bất phương trình (.... >= 0)
	#he_bpt = he_bpt[:,[1,7,4,6,5,0,2,8,3]]
	#print(he_bpt)

	#print(inequal_check(he_bpt[:,[6, 1, 0, 7, 4, 5, 2, 3, 8]]))

	##Chon lọc
	he_bpt_hv_index = list(itertools.permutations(list(range(len(he_bpt[0])-1))))
	#print(len(he_bpt_hv_index))
	#displaylist(he_bpt_hv_index)


	for i in range(len(he_bpt_hv_index)):
			he_bpt_hv_index[i] = list(he_bpt_hv_index[i])
			he_bpt_hv_index[i].append(len(he_bpt[0])-1)


	#displaylist(he_bpt_hv_index)


	rs_list = []
	for i in range(len(he_bpt_hv_index)):
		rs_list.append(inequal_check(he_bpt[:,he_bpt_hv_index[i]]))

	#displaylist(rs_list)

	#Lọc kết quả
	order_choise = []
	for i in range(len(rs_list)):
		if check_ng("break",rs_list[i]) == "no":
			order_choise.append(he_bpt_hv_index[i])
	#displaylist(order_choise) 


	## Xuat file txt ghi tat ca con duong dong dang 

	textfile = open("order_choise_v1.txt", "w")
	for i in range(len(order_choise)):
		if ((i+1) % 6) == 0:
		    textfile.write(str(order_choise[i]) + "\n")
		else:
			textfile.write(str(order_choise[i]) + "\t")
	textfile.close()	
	"""
	"""
	## Loc cac truong hop co 2 can
	#print(inequal(he_bpt[:,[5, 7, 4, 2, 0, 1, 6, 3, 8]]))

	order_choise_v2 = []
	for i in range(len(order_choise)):
		#print(inequal(he_bpt[:,order_choise[i]]))
		if check_ng("~",inequal(he_bpt[:,order_choise[i]])) == "no":
			order_choise_v2.append([order_choise[i],inequal(he_bpt[:,order_choise[i]])])
	displaylist(order_choise_v2)

	## Xuat file txt ghi tat ca con duong dong dang 

	textfile = open("order_choise_v2.txt", "w")
	for i in range(len(order_choise_v2)):
		textfile.write(str(order_choise_v2[i]) + "\n")
	textfile.close()

	"""

	# Thay đổi thứ tự giải bpt
	#orderchoise = [2, 3, 0, 5, 7, 4, 1, 6, 8]

	he_bpt_reorder = he_bpt

	# Tìm cac ma thức thỏa mãn điều kiện bpt
	resulte = solvebdtpro(he_bpt_reorder)
	#print(resulte)

	"""
	# Loc ra cac ma thuc tong bang step
	resulte_sorted = []
	for i in range(len(resulte)):
		if sum(resulte[i]) == step:
			resulte_sorted.append(resulte[i])
	#print(resulte_sorted)
	resulte = resulte_sorted
	"""
	"""
	# reoderchoise
	reoderchoise =[]
	for i in range(len(orderchoise)):
		for k in range(len(orderchoise)):
			if orderchoise[k] == i:
				reoderchoise.append(k)
	del reoderchoise[-1]
	#print(reoderchoise)

	reorder_list = []
	for k in resulte:
		k = [k[i] for i in reoderchoise]
		reorder_list.append(k)
	print(reorder_list)
	"""
	# Chuyen tu list sang ma thuc
	sort_ma = []
	for k in resulte:
		sort_ma.append(list2ma(k))
	#print(sort_ma)

	#Tinh so con duong dong dang
	path_num_total = 0
	for i in range(len(sort_ma)):
		path_num_total += path_num(sort_ma[i])

	#print("Tổng số đường đi đồng dạng: " + str(path_num_total))
	
	# Ghi ra tất cả con đường
	alter_path = []
	for i in sort_ma:
		alter_path.extend(dongdang(i))
	#displaylist(alter_path)

	## Xuat file txt ghi tat ca con duong dong dang 
	"""
	textfile = open("paths.txt", "w")
	for i in range(len(alter_path)):
		if ((i+1) % 6) == 0:
		    textfile.write(str(alter_path[i]) + "\n")
		else:
			textfile.write(str(alter_path[i]) + "\t")
	textfile.close()
	"""

	return alter_path

""" #Check time
for i in range(100):
	print("_______"+str(i)+"_______")
	start = time.time()
	VectorToPath([3,3],i)
	end = time.time()
	print("Time run: "+str(end-start))
"""

#print(VectorToPath([0,1],2))