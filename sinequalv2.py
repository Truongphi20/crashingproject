import numpy as np
import math

def check_int(num_tex): #Check xem text có phải số hay không
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

def Make_bpts(bpt,biens): #Tao ma tran bat phuog trinh cho một bất phương trình 

	dau = -1
	if  len(bpt.split(">=")) == 2: #Dau = -1 khi <=, dau =1 khi >=, dau = 2 khi == 
		dau = 1
	elif len(bpt.split("==")) == 2:
		dau = 2
	#print(dau)

	if dau == 1:
		he_bpt = bpt.split(">=")[0]
		fi = bpt.split(">=")[1]
	elif len(bpt.split("<=")) == 2:
		he_bpt = bpt.split("<=")[0]
		fi = bpt.split("<=")[1]
	else:
		he_bpt = bpt.split("==")[0]
		fi = bpt.split("==")[1]
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

	rs = []
	if dau == 1 or dau == -1:
		rs = [np.array(bpt_final)*dau]
	else:
		rs = [np.array(bpt_final),np.array(bpt_final)*-1]

	return rs

def mak_hebpt_matrix(he_bpt_list,biens): #Tao matrix he so bat phuong trinh cho hệ bất phương trình
	matri = []
	for i in range(len(he_bpt_list)):
		#print(i)
		matri.extend(Make_bpts(he_bpt_list[i],biens))
	matri = np.array(matri)
	return matri

def truy_nguon(he_bpt): # Truy nguồn gốc từ phương trình hay từ bpt
    nguon_goc = []
    for i in he_bpt:
        if len(i.split("<=")) == 2 or len(i.split(">=")) == 2:
            nguon_goc.append(0)
        else:
            nguon_goc.extend([1,1])
    return nguon_goc

#biens = ["a","b","P","c","G","k"] # Khai báo tên biến
#cuctri = [0,0,1,0,-1,0]	# Khai báo biến có phải cực trị (0: không phải, 1: cực đại, -1: cực tiểu)

def order_bien(bien,cuctri): # Tìm ra thứ tự triệt tiêu biến
    bien_lis = []
    cuctri_lis = []
    for i in range(len(cuctri)):
        if cuctri[i] == 0:
            bien_lis.append(i)
        else:
            cuctri_lis.append(i)
    return bien_lis + cuctri_lis

#print(order_bien(biens,cuctri))

def tieu_bien(index,he,nguon_goc): # Tiêu biến mang index tương ứng trong hệ

    # Tạo hàm cong các thành phần giữa hai list {[1,2],[10,20]} -> [10,40] 
    cong_2list = lambda l1,l2: [l1[i]+l2[i] for i in range(len(l1))]

    # Tạo một hàm tiêu biến với đầu vào là hệ bất phương trình và index tiêu biến, đầu ra là hệ sau tiêu biến

    index_cd = [i for i in range(len(he)) if he[i][index] > 0] #Index cac hang duong
    index_ca = [i for i in range(len(he)) if he[i][index] < 0] #Index cac hang am

    index_d = index_cd[0] # index của gốc dương 
    #print(index_d)

    index_a = index_ca[0] # index của gốc âm
    #print(index_a) 

    he_moi = []
    for k in range(len(he)):
        if k != index_d:
            if he[k][index] > 0:
                he_moi.append(cong_2list(he[k]*abs(he[index_a][index]/he[k][index]),he[index_a]))
            elif he[k][index] < 0:
                he_moi.append(cong_2list(he[k]*abs(he[index_d][index]/he[k][index]),he[index_d]))
            else:
                he_moi.append(he[k])
    #print(np.array(he_moi))
    return np.array(he_moi)

#print(tieu_bien(order[0],he))

def giai_bien(index,order,he,nguon_goc): # Giải ra list hệ tiêu biến của biến cần tìm với index tương ứng
    lap = [he]
    for  i in range(len(order)):
        if order[i] != index:  
            lap.append(tieu_bien(order[i],lap[-1],nguon_goc))
    return lap

def phogia(index,tieu_bien3): #từ index của biến còn lại và hàm tiêu biến xuất ra list giá trị 
    max_bien = []
    min_bien = []
    for i in range(len(tieu_bien3)):
        if tieu_bien3[i][index] > 0:
            min_bien.append(-tieu_bien3[i][-1]/ tieu_bien3[i][index])
        elif tieu_bien3[i][index] < 0:
            max_bien.append(-tieu_bien3[i][-1]/ tieu_bien3[i][index])
    #print(max_bien)
    #print(min_bien)

    max_bien_value = math.floor(min(max_bien))
    #print(max_bien_value)

    min_bien_value = math.ceil(max(min_bien))
    #print(min_bien_value)

    return list(range(min_bien_value,max_bien_value+1))

#pho_gia_tri = phogia(index_giai,tieu_bien3)
#print(pho_gia_tri)

def thay_nghiem(he, indexes, vals): # Thay nghiem o cac bien voi index tuong ung de tao ra pho nghiem gia

	he_the = he.tolist()

	for i in range(len(indexes)):
		for k in range(len(he_the)):
			for j in range(len(he_the[0])):
				if j == indexes[i]:
					he_the[k][-1] += vals[i]*he_the[k][j] 
					he_the[k][j] = 0 # Thay xong cho bang 0
	return np.array(he_the)

def tach_key(string): #Tach key lop tren thanh key lop duoi {/10/3/2} --> [/10/3/2,/3/2,/2]
	bac = string.count("/")
	#print(bac)

	rs = []
	for i in range(1,bac+1):
		rs.append("/"+ string.split("/",i)[-1])
	return rs

def order_tl(order): #Tao list of list order tich luy {[0,3,4,5] --> [[5],[4,5],[3,4,5],[0,3,4,5]]}
	rs = []
	for i in range(1,len(order)+1):
		rs.append(order[(len(order)-i):(len(order)):])
	#print(rs)
	return rs

#print(order_tl([0,3,4,5]))


#print(tach_key("/10/3/2"))

#index = [0,2]
#vals = [2,1]
#print(thay_nghiem(he,index,vals))


def Tra_kq_ct(lib_nghiem,order): #Tra ket qua nghiem co cuc tri
	list_key_rs = [i for i in lib_nghiem if len(i.split("/")) == len(order)+1]
	#print(list_key_rs)

	rs_final = []
	key_rs = []
	rs = []
	for j in range(len(list_key_rs)):
		key_rs = tach_key(list_key_rs[j])
		#print(key_rs)

		rs = [lib_nghiem[i] for i in key_rs]
		#print(rs)
		rs_final.append(rs)

	return rs_final

#print(Tra_kq_ct(lib_nghiem,order))

def Tim_key_ct(lib_htb,lib_nghiem,order,choice_key): # Ham giai ra tat ca bien khi thay key cua bien cuc tri

	key1 = [choice_key]

	for m in range(len(key1)):
		he_bpt1 = thay_nghiem(lib_htb[-2],order_tl(order)[0],[lib_nghiem[i] for i in tach_key(key1[m])]) #Thay bien
		#print(he_bpt1)

		pho1 = phogia(order[-2],he_bpt1) #Tim pho
		#print(pho1)

		if len(pho1) != 0:
			for i in range(len(pho1)):
				lib_nghiem["/" + str(i) + key1[m]] = pho1[i]

	#print(lib_nghiem)

	if len(pho1) != 0:
		for t in range(2,len(order)):
			key2 = [i for i in lib_nghiem if i.count("/") == t]
			if len(key2) == 0:
				break

			for m in range(len(key2)):
				he_bpt1 = thay_nghiem(lib_htb[-t-1],order_tl(order)[t-1],[lib_nghiem[i] for i in tach_key(key2[m])]) #Thay bien
				#print(he_bpt1)

				pho2 = phogia(order[-t-1],he_bpt1) #Tim pho
				#print(pho2)

				if len(pho2) != 0:
					for i in range(len(pho2)):
						lib_nghiem["/" + str(i) + key2[m]] = pho2[i]
			if len(pho2) == 0:
				break

	#print(lib_nghiem)

	# Tra ket qua
	kq = Tra_kq_ct(lib_nghiem,order)
	#print(kq)

	return kq

def Giai_bpt(lib_htb,order,cuctri): # giai he bpt

	pho = phogia(order[-1],lib_htb[-1]) # Pho cua bien cuc tri
	#print(pho)

	lib_nghiem = {"/"+str(i):pho[i] for i in range(len(pho))} #Them vao thu vien
	#print(lib_nghiem)

	if sum(cuctri) == 1 or sum(cuctri) == -1: # Co cuc tri
		for i in range(len(pho)):
			if sum(cuctri) == -1: # Cuc tieu
				choice_key = "/"+str(i)
			elif sum(cuctri) == 1: # Cuc dai
				choice_key = "/"+str(len(pho)-i-1)
			rs = Tim_key_ct(lib_htb,lib_nghiem,order,choice_key)
			if len(rs) != 0:
				break
	elif sum(cuctri) == 0: # Khong co cuc tri
		for i in range(len(pho)):
			choice_key = "/"+str(i)
			rs = Tim_key_ct(lib_htb,lib_nghiem,order,choice_key)
			#print(rs)

	if check_order(order) == 1:
		rs = [rv_order(order,i) for i in rs]
	return rs
#print(Giai_ct(lib_htb,order,cuctri))

def Giai_he_bpt(he_bpt,biens,cuctri): # Tao he truy xuat giai he bpt

	nguon_goc = truy_nguon(he_bpt) # Nguon goc tu phuong trinh (1) hay bpt (0)
	#print(nguon_goc)

	he = re_order_ma(mak_hebpt_matrix(he_bpt,biens),nguon_goc) # Tao ma tran tu he bpt
	#print(he)

	order = order_bien(biens,cuctri) # Thu tu giai, uu tien giai bien cuc tri truoc
	print(order)
	#print(order_tl(order))
	#____________________

	##Giai 

	lib_htb = giai_bien(order[-1],order,he,nguon_goc) # Thu vien he tieu bien
	#print(lib_htb)

	return Giai_bpt(lib_htb,order,cuctri)

def rv_order(order,rs):
	rs_orders = rs[:]
	for i in range(len(order)):
		#print(rs)
		rs_orders[order[i]] = rs[i]
	return rs_orders

#print(rv_order(order,rs))

def check_order(order): # Check order co thay doi tt do cuc tri khong (0: khong, 1: co)
	k = 0
	for i in range(1,len(order)):
		if order[i]-order[i-1] != 1:
			k = 1 
	return k
#print(check_order([2,3,0,1]))

def re_order_ma(he,nguon_goc): # Sap xep lai thu tu hang, bt truoc, cuc tri sau
	bt = [he[i] for i in range(len(nguon_goc)) if nguon_goc[i] == 0]
	#print(bt)
	ct = [he[i] for i in range(len(nguon_goc)) if nguon_goc[i] == 1]
	#print(ct)

	rs = np.array(bt+ct)
	#print(rs)
	return rs


'''
#_______input______
biens = ["m","g","h","c"] # Khai báo tên biến
cuctri = [0,0,0,0]	# Khai báo biến có phải cực trị (0: không phải, 1: cực đại, -1: cực tiểu)
he_bpt = ["2*m+5*g+7*h+10*c<=1000","2*m+5*g+10*h+15*c<=500", "4*m+8*g+11*h+19*c==978",
			"m>=1","g>=1","h>=1","c>=1"]

print(Giai_he_bpt(he_bpt,biens,cuctri))
'''

"""
biens = ["a","b","G"] # Khai báo tên biến
cuctri = [0,0,1]	# Khai báo biến có phải cực trị (0: không phải, 1: cực đại, -1: cực tiểu)
he_bpt = ["2*a+b<=600","a+b>=0","a-b>=1","a+b-G==0"]

print(Giai_he_bpt(he_bpt,biens,cuctri))
"""


