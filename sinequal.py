import numpy as np
from big_lib import *

def check_int(num_tex): #Check xem text cos phai so hay khong
	res = False
	if num_tex.isnumeric() == True:
		res = True
	else:
		if num_tex.lstrip('-').isdigit() == True:
			res = True
	return res

#print(check_int("d3"))

def check_int_list(num_tex_list): #Check xem co phai list so hay khong
	res = True
	for element in num_tex_list:
		if check_int(element) == False:
			res = False
	return res

def find_index_int_list(listb): #Tim index cua list so trong list lon
	for i in range(len(listb)):
		if check_int_list(listb[i]) == True:
			break
	return i

def Make_bpts(bpt,biens): #Tao ma tran bat phuog trinh

	dau = -1
	if  len(bpt.split(">=")) == 2: #Dau = -1 khi <=, dau =1 khi >=
		dau = 1
	#print(dau)

	if dau == 1:
		he_bpt = bpt.split(">=")[0]
		fi = bpt.split(">=")[1]
	else:
		he_bpt = bpt.split("<=")[0]
		fi = bpt.split("<=")[1]
	#print(he_bpt)
	#print(fi)

	he_duong = he_bpt.split("+")
	#print(he_duong)

	he_duong_filter = []
	for i in he_duong:
		he_duong_filter.append(i.split("-")[0])
	he_duong_filter[:] = [x for x in he_duong_filter if x] #Xoa thanh phan rong
	#print(he_duong_filter)


	he_am = he_bpt.split("-")
	if he_am[0][1::] != "-":
		he_am.pop(0)
	#print(he_am)

	he_am_filter = []
	for i in he_am:
		he_am_filter.append("-" + i.split("+")[0])
	he_am_filter[:] = [x for x in he_am_filter if x]
	#print(he_am_filter)

	total = he_duong_filter + he_am_filter
	#print(total)

	dic = []
	for i in range(len(total)):
		tem = []
		#print("*" in total[i])
		if ("*" in total[i]) == False:
			if total[i][0] == "-":
				tem = ["-1",total[i][1:]]
			else:
				tem = ["1",total[i]]
		else:
			tem = total[i].split("*")
		
		dic.append(tem)

	#print(dic)

	dic.append(dic.pop(find_index_int_list(dic)))

	#print(dic)

	#print(dic[-1][0].lstrip('-').isdigit())
	#dic[-1][0] = str(int(dic[-1][0])*int(dic[-1][1])) 


	bpt_final = [0]*len(biens)
	#print(bpt_final)


	for i in range(len(dic)):
		#print(i)
		index = -1
		for k in range(len(biens)):
			#print(k)
			if dic[i][1] == biens[k]:
				index = k
				bpt_final[index] = int(dic[i][0])

		#print(index)
	bpt_final.append(-int(fi))
	#print(bpt_final)

	bpt_final = np.array(bpt_final)*dau
	#print(type(bpt_final))

	return bpt_final

def mak_hebpt_matrix(he_bpt_list,biens): #Tao matrix he so bat phuong trinh
	matri = []
	for i in range(len(he_bpt_list)):
		#print(i)
		matri.append(Make_bpts(he_bpt_list[i],biens))
	matri = np.array(matri)
	return matri

def giaihebpt(he_bpt,biens):
	matrix = mak_hebpt_matrix(he_bpt,biens)
	#print(matrix)
	try:
		results =  solvebdtpro(matrix)
		#print(results)
	except IndexError:
		results = "No solution"
	#print(results)
	return results

"""
biens = ["a1","a2","b1","b2","c1","c2","d1","d2","x0","y0","n0"]
bpt = "+a1+c1+d1-a2-c2-d2+4<=0"	
print(Make_bpt(bpt,biens))
"""

#Example
"""
he_bpt = ["-b1+b2-c1+c2+d1-d2+0>=0","-b1+b2-c1+c2+d1-d2+0<=0",
			"-a1+a2-c1+c2+d1-d2+0>=0","-a1+a2-c1+c2+d1-d2+0<=0",
			"a1+0>=0","a1-1<=0",
			"a2+0>=0","a2-0<=0",
			"b1+0>=0","b1-1<=0",
			"b2+0>=0","b2-0<=0",
			"c1+0>=0","c1-1<=0",
			"c2+0>=0","c2-1<=0",
			"d1+0>=0","d1-1<=0",
			"d2+0>=0","d2-0<=0",]
biens = ["a1","a2","b1","b2","c1","c2","d1","d2"]
print(giaihebpt(he_bpt,biens))
"""

biens = ["a","b","c","d","e","f","g","h"] #Đặt ẩn là hiệu số thời gian của các công việc theo thứ tụ

he_bpt = [
    # Các hiệu số phải lớn hơn hoặc bằng 0
    "a>=0","b>=0","c>=0","d>=0",
    "e>=0","f>=0","g>=0","h>=0",
    # Thời gian rút ngắn phải nằm trong phạm vi đề bài cho
    "a-1<=0","b-2<=0","c-1<=0","d-1<=0",
    "e-2<=0","f-1<=0","g-3<=0","h-1<=0",
    # Thời gian hoàn thành sau rút ngắn của các đường không Gantt phải bé hơn hoặc bằng đường Gantt
    "-e-g+f+6>=0","-a-c-e+b+d+1>=0"    
]
print(giaihebpt(he_bpt,biens))