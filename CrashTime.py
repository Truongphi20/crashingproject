from sinequalv2 import *
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def tim_vector(tenda,pretenda): # Tim cac vector tren giang do
	Start_point = [i for i in tenda if pretenda[tenda.index(i)] == '-'] #Tìm start point
	#print(Start_point)

	# Liệt kê các vector:
	##Thêm vector start point
	vector = [["Start",i] for i in Start_point] 
	#print(vector)

	##Thêm vector trung gian
	for i in range(len(pretenda)): 
	    if pretenda[i] != "-" and len(pretenda[i]) == 1:
	        vector.append([pretenda[i],tenda[i]])
	    elif len(pretenda[i]) > 1:
	        Stats = pretenda[i].split(",")
	        for k in range(len(Stats)):
	            vector.append([Stats[k],tenda[i]]) 
	#print(vector)

	##Tìm end point
	End_point = []
	for i in range(len(tenda)):
	    a = 0
	    for k in range(len(pretenda)):
	        if tenda[i] in pretenda[k]:
	            a += 1
	    if a == 0:
	        End_point.append(tenda[i])
	#print(End_point)

	vector.extend([[i,'End'] for i in End_point])
	#print(vector)
	return vector

def all_paths(G): # Xuat ra cac con duong
    roots = (v for v, d in G.in_degree() if d == 0)
    leaves = [v for v, d in G.out_degree() if d == 0]
    all_paths = []
    for root in roots:
        paths = nx.all_simple_paths(G, root, leaves)
        all_paths.extend(paths)
    return all_paths

def pathsf(tenda,pretenda): # Xac dinh cac con duong
	# Xac dinh cac con duong
	## Xac dinh cac vecto
	vector = tim_vector(tenda,pretenda)
	#print(vector)
	## Xac dinh cac con duong
	G = nx.DiGraph()
	G.add_edges_from(vector)
	paths = all_paths(G)
	print(lisotoString(paths))
	return paths

def Tim_gantt(paths,tenda,tg1): # Rà thời gian thực hiện dự án của các con đường 
    g_list = []
    for i in range(len(paths)):
        g_val = []
        for k in range(1,len(paths[i])-1):
            for j in range(len(tenda)):
                if tenda[j] == paths[i][k]:
                    g_val.append(tg1[j])
        g_list.append(g_val)
    return g_list

class Ganttc(): 
	def __init__(self,tenda,paths,tg1):
		self.tenda = tenda
		self.paths = paths
		self.tg1 = tg1
		self.g_list = Tim_gantt(self.paths,self.tenda,self.tg1)
    #print(g_list)

	def time(self): # Tra ve thoi gian hoan thanh du an    
		return [sum(i) for i in self.g_list]
    	#print("Thời gian hoàn thành: "+ str(g_val_list))

	def gantt(self): # Tra ve duong gantt
	    max_tg = max(self.time())
	    #print(max_tg)

	    Gantt = [self.time().index(max_tg)]
	    return Gantt

def bpt3(paths,tenda,time_ht): # bat phuong trinh cho dieu kien thu 3
	rs = []
	for k in range(len(paths)):
		tem = [0]*(len(tenda)+1)
		for i in range(len(tenda)):
			for ele in paths[k]:
				if ele == tenda[i]:
					tem[i] = -1
		tem[-1] = time_ht[k]
		rs.append(tem)
	#print(rs)
	return rs

def Taohe(index_gantt, tenda, paths, time_ht): # Tao he bat phuong trinh
	# Gia su duong 1 la duong Gantt
	zero = [] # He dieu kien cac bien lon hon hoac bang 0
	for i in range(len(tenda)):
		tem = [0]*(len(tenda)+1)
		tem[i] = 1
		zero.append(tem)
	#print(zero)

	pv = [] # He dieu kien cac bien phai nam trong pham vi de bai
	for i in range(len(tenda)):
		tem = [0]*(len(tenda)+1)
		tem[i] = -1
		tem[-1] = tg_dv[i]
		pv.append(tem)
	#print(pv)

	#index_gantt = 0 # index duong gan sau qua trinh rut gon		
	dk3 = bpt3(paths,tenda,time_ht) # Cac bpt cho dieu kien 3
	#print(dk3)

	bpt_dk3 = []
	for i in range(len(dk3)):
		if i != index_gantt:
			bpt_dk3.append([dk3[index_gantt][k] - dk3[i][k] for k in range(len(dk3[i]))])
	#print(bpt_dk3)

	he = np.array(zero + pv + bpt_dk3)
	#print(he)
	return he

def Giai_bptc(index_gantt, tenda, paths, time_ht):
	he = Taohe(index_gantt, tenda, paths, time_ht) # He bpt de giai thoi gia rut
	#print(he)

	nguon_goc = [0]*len(he)
	cuctri = [0]*len(he[0])
	order = list(range(len(tenda)))
	#print(order)

	lib_htb = giai_bien(order[-1],order,he,nguon_goc) # Thu vien he tieu bien
	#print(lib_htb)

	return Giai_bpt(lib_htb,order,cuctri)

def cp_rutz(hs_cp,cost_dv): #Tính chi phí rút ngắn của các trường hợp rút ngắn
    cp_rut = []
    for i in range(len(hs_cp)):
        a = 0
        for k in range(len(cost_dv)):
            a += hs_cp[i][k]*cost_dv[k]
        cp_rut.append(a)
    return cp_rut

def ds_lumf(paths,tenda): #Tao ds lum cho cho tg rut
	rs = []
	for path in paths:
		tem = []
		for i in range(len(tenda)):
			if tenda[i] in path:
				tem.append(i)
		rs.append(tem)
	#print(rs)
	return rs

def tg_rutz(hs_cp,lum,time_ht,index_gantt): #Tính thời gian rút ngắn của các trường hợp rút ngắn
    tg_rut = []
    for i in range(len(hs_cp)):
        a = 0
        for k in lum:
            a += hs_cp[i][k]
        tg_rut.append(max(time_ht)-time_ht[index_gantt]+a) # Tg gantt ban dau - tg gantt sau
    return tg_rut

def FindMin(tg_list,tg_rut,cp_rut):
    rs = []
    for j in range(len(tg_list)):
        index = [] #index của mốc thời gian
        for i in range(len(tg_rut)):
            if tg_rut[i] == tg_list[j]:
                index.append(i)
        #print(index)

        cp = [cp_rut[i] for i in index] # Chi phí của các index tương ứng
        #print(cp)

        cp_min = min(cp)
        #print(cp_min)

        #Index của chi phí min
        index_min = index[cp.index(cp_min)]
        #print(index_min)
        rs.append([index_min,cp_min])
    return rs

class Toithieu():## Tim chi phi toi thieu o cac moc thoi gian
	def __init__(self,tg_rut,cp_rut):
		self.tg_rut = tg_rut
		self.cp_rut = cp_rut

	def tg_list(self):
		return list(range(min(self.tg_rut),max(self.tg_rut)+1))
	#print(tg_list)

	def cp_min(self):
		cp_min_list = FindMin(self.tg_list(),self.tg_rut,self.cp_rut) #List [index của hs_cp, chi phí min]
		#print(cp_min_list)

		cp_min = [cp_min_list[i][1] for i in range(len(cp_min_list))] # Trích xuất chi phí min từ list trên
		#print("Chi phí min: "+str(cp_min))
		return cp_min

def TruyXuat(cp_val,tg_val,cp_rut,tg_rut): #Truy xuất index của mức phí và thời gian
    index1 = []
    for i in range(len(cp_rut)):
        if cp_rut[i] == cp_val:
            index1.append(i)
    
    index2 = []
    for k in index1:
        if tg_rut[k] == tg_val:
            index2.append(k)
    return index2

def dem(cp_min,pho_tg,cp_rut,tg_rut):
	index_min_lap = [] # Index của các lần lặp
	for i in range(len(cp_min)): 
	    index_min_lap.append(TruyXuat(cp_min[i],pho_tg[i],cp_rut,tg_rut))
	return index_min_lap

def PhanTich(tenda, paths, time_ht,cost_dv,ds_lum): # Phan tich truong hop la duong gantt sau rut ngan thoi gian

	index_paths = [] #index cua cac path kha di 
	tg_list = [] # pho thoi gia rut ngan
	cp_min_list = [] # chi phi rut ngan toi thieu
	hs_cp_can = [] # he so chi phi cua cac th rut ngan

	for i in range(len(paths)):
		index_gantt = i

		hs_cp = Giai_bptc(index_gantt, tenda, paths, time_ht) # So thoi gian co the giam
		#print(hs_cp[:10])
		if len(hs_cp) != 0:
			index_paths.append(i)
			cp_rut = cp_rutz(hs_cp,cost_dv) # Chi phi rut ngan cua cac truong hop
			#print(cp_rut[:10])

			tg_rut = tg_rutz(hs_cp,ds_lum[index_gantt],time_ht,index_gantt) # Thoi gian rut ngan so voi thoi gian cua duong Gantt cuoi
			#print(tg_rut[:10])

			toithieu = Toithieu(tg_rut,cp_rut) #class toi thieu
			pho_tg = toithieu.tg_list()
			#print(pho_tg) 
			tg_list.append(pho_tg) # pho thoi gian rut ngan
			
			cp_min = toithieu.cp_min() # chi phi rut ngan toi thieu o tung moc thoi gian
			cp_min_list.append(cp_min)
			#print(cp_min)

			index_min_lap = dem(cp_min,pho_tg,cp_rut,tg_rut) # Dem so lan lap cua chi phi toi thieu
			#print(index_min_lap)

			hs_cp_can.append(list(map(lambda x: list(map(lambda k: hs_cp[k],x)) ,index_min_lap)))
			#print(hs_cp_can)
	return index_paths, tg_list, cp_min_list, hs_cp_can


def phochung(tg_list): # Tao pho tg chung
	pho_min = min([i[0] for i in tg_list])
	pho_max = max([i[-1] for i in tg_list])

	pho_chung = list(range(pho_min,pho_max+1))
	#print(pho_chung)
	return pho_chung

def cpchung(pho_chung,tg_list,cp_min_list,hs_cp_can):
	cp_chung = []
	hs_cp_chung = [] # Lay he so chi phi chung theo pho chung
	for t in pho_chung:
		cp_tem = []
		hs_cp_tem = []
		for i in range(len(tg_list)):
			for k in range(len(tg_list[i])):
				if t == tg_list[i][k]:
					cp_tem.append(cp_min_list[i][k])
					hs_cp_tem.extend(hs_cp_can[i][k])
		cp_chung.append(min(cp_tem))
		hs_cp_chung.append(hs_cp_tem)

	#print(cp_chung)
	return cp_chung, hs_cp_chung

def CpFromGantt(cp_chung,index_paths,cp_min_list): # Do xem chi phi chung toi thieu den tu index cua duong Gantt nao
	cp_from_gantt = [] 
	for cp in cp_chung:
		cp_tem = []
		for i in range(len(index_paths)):
			for k in range(len(cp_min_list[i])):
				if cp == cp_min_list[i][k]:
					cp_tem.append(index_paths[i])
		cp_from_gantt.append(cp_tem)
	#print(cp_from_gantt)
	return cp_from_gantt

def ShowTGR(list, biens): # Bieu dien ket qua dang cach thuc
    inter = [val for pair in zip(list,biens) for val in pair] #Đan xen hai list thành list mới
    #print(inter)

    rs = listToStr = ''.join(map(str, inter)) # Chuyển list thành string
    #print(rs)
    return rs

def rmDoup(lista): # Loai bo thanh phan lap lai trong list
	list_rmD = []
	tem = [list_rmD.append(ele) for ele in lista if ele not in  list_rmD]
	return list_rmD

def lisotoString(listo): # Chuyen list of list thanh list string
	listo1 = [list(map(str,i)) for i in listo] #Chuyển list of list int sang list of list string
	#print(index_min_lapstr)

	listo2 = [",".join(i) for i in listo1] #Chuyển list string thành các string
	#print("Index tương ứng: "+str(index_min_laps2))
	return listo2

def flatten(l): #Chuyên list of lists thành list
    return [item for sublist in l for item in sublist]

def Bdkq(hs_cp_final,pho_chung,cp_from_gantt_display,cp_chung): #Bieu dien ket qua dang bang

	space_list = [len(i)-1 for i in hs_cp_final] # khoang cach can them vao dua vao cot max
	#print(space_list)

	pho_chung_just = flatten([[pho_chung[i]]+[""]*space_list[i] for i in range(len(pho_chung))]) #pho chung them space
	#print(pho_chung_just)

	cp_from_gantt_just = flatten([[cp_from_gantt_display[i]]+[""]*space_list[i] for i in range(len(cp_from_gantt_display))])
	#print(cp_from_gantt_just)

	cp_chung_just = flatten([[cp_chung[i]]+[""]*space_list[i] for i in range(len(cp_chung))])
	#print(cp_from_gantt_just)

	hs_cp_final_just = flatten(hs_cp_final)

	##Xuất ra bảng
	data_ct = pd.DataFrame(list(zip(pho_chung_just,cp_from_gantt_just,cp_chung_just,hs_cp_final_just)),columns=["Tg rút","Gantt","Cost","Ways"])
	#print(data_ct)

	return data_ct

def CrashTime(tenda,pretenda,tg1,tg_dv,cost_dv): #Ham tong quat
	paths = pathsf(tenda,pretenda) # Cac con duong co the di
	#print(paths)

	Gantt = Ganttc(tenda,paths,tg1) 
	#print(Gantt)

	Gantt_index = Gantt.gantt() # Tra ve duong stt cua duong Gantt hien tai
	time_ht = Gantt.time() # Thoi gian hoan thanh cac con duong
	#print(time_ht)

	ds_lum = ds_lumf(paths,tenda) # ds lum de tinh thoi gian rut gon
	#print(ds_lum)


	index_paths, tg_list, cp_min_list, hs_cp_can = PhanTich(tenda, paths, time_ht,cost_dv,ds_lum)
	#print(index_paths) # index cac path kha di
	#print(tg_list) # pho thoi gian cua cac truong hop
	#print(cp_min_list[1]) # cac chi phi min cua cac truong hop 
	#print(hs_cp_can) # cac he so chi phi o cac truong hop

	# Hop cac truong hop de tim cac truong hop sao cho chi phi cuc tieu
	pho_chung = phochung(tg_list) #pho tg giam chung
	#print(pho_chung)

	## Tao pho chi phi chung voi chi phi toi thieu o cac moc
	cp_chung, hs_cp_chung = cpchung(pho_chung,tg_list,cp_min_list,hs_cp_can)
	#print(cp_chung)
	#print(hs_cp_chung)

	hs_cp_chung_rm = [rmDoup(i) for i in hs_cp_chung]
	#print(hs_cp_chung_rm)

	## Do xem chi phi chung toi thieu den tu index cua duong Gantt nao
	cp_from_gantt = CpFromGantt(cp_chung,index_paths,cp_min_list)
	#print(cp_from_gantt)
	cp_from_gantt_display = lisotoString(cp_from_gantt)
	#print(cp_from_gantt_display)


	## Tao ket qua doc cho he so chi phi
	lower_tenda = [i.lower() for i in tenda]
	#print(lower_tenda)

	## Chuyển list cách thức thành dạng string
	hs_cp_final = list(map(lambda x: list(map(lambda y: ShowTGR(y,lower_tenda), x)), hs_cp_chung_rm))
	#print(hs_cp_final)


	data_ct = Bdkq(hs_cp_final,pho_chung,cp_from_gantt_display,cp_chung) # Bieu dien ket qua dang bang
	#print(data_ct)

	return data_ct

# Khai bao du lieu
#tenda = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'] # Ten du an
#pretenda = ['-', '-', 'A', 'B', 'C', 'C', 'D,E', 'F,G'] # Ten du an lien truoc
#tg1 = [2, 3, 2, 4, 4, 3, 5, 2] # Thoi gian hoan thanh du an bth
#tg_dv = [1, 2, 1, 1, 2, 1, 3, 1] # Thoi gian rut ngan don vi
#cost_dv = [1000.0, 2000.0, 1000.0, 1000.0, 1000.0, 500.0, 2000.0, 3000.0] # Chi phi rut ngan don vi

df = pd.read_csv('input_data.csv',sep="\t")
#print(df)

tenda = list(df.iloc[:,0])
pretenda = list(df.iloc[:,1])
tg1 = list(df.iloc[:,2])
tg_dv = list(df.iloc[:,3])
cost_dv = list(df.iloc[:,4])

data_ct = CrashTime(tenda,pretenda,tg1,tg_dv,cost_dv)
print(data_ct)








