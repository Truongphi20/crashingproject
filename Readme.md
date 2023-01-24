Thuật toán giải bài toán tìm thời gian rút ngắn thực hiện của dự án.
=============

Yêu cầu: rút ngắn một lượng thời gian sao cho tổng chi phí rút ngắn là nhỏ nhất

# **1. Usage:**

**Kiểm tra cài đặt**
	
	python .\CrashTime.py -h
	
	usage: CrashTime.py [-h] [-f INPUT_FILE] [-v]

	optional arguments:
	  -h, --help            show this help message and exit
	  -f INPUT_FILE, --input_file INPUT_FILE
	  -v, --version         show version

**Bước 1: Tạo file input:**

	- Là file csv, các thành phần trong bảng phân cách bằng tab (xem file input_example.csv).
	- Không cần điều chỉnh tên cột
	- Ý nghĩa tên các cột:
		+ Cột 1: Tên các dự án
		+ Cột 2: Các dự án liền trước dự án bên cột 1
		+ Cột 3: Thời gian hoàn thành dự án không rút ngắn tiến độ
		+ Cột 4: Thời gian có thể rút ngắn tối đa của dự án đó
		+ Cột 5: Chi phí khi rút ngắn một đơn vị thời gian dự án ở cột 1 
	- Điều chỉnh các cột phù hợp với điều kiện đề bài
**Bước 2: Chạy thuật toán:**

	python .\CrashTime.py -f input_file
	
	
Kết quả sẽ xuất ra trực tiếp trên terminal.  


# **2. Ví dụ đọc kết quả:**

Nguồn ví dụ: [Youtube](https://www.youtube.com/watch?v=qNSTP88FHWA&t=764s)

Chạy file "input_example.csv" tương ứng với đề bài của ví dụ:

	Dự án	DA trước	Tg bth	Tg rút đv	Cp đv
	A	-	2	1	1000.0
	B	-	3	2	2000.0
	C	A	2	1	1000.0
	D	B	4	1	1000.0
	E	C	4	2	1000.0
	F	C	3	1	500.0
	G	D,E	5	3	2000.0
	H	F,G	2	1	3000.0

Chạy thuật toán bằng lệnh `python .\CrashTime.py -f .\input_example.csv`, thu được kết quả: 

```
['Start,A,C,E,G,H,End', 'Start,A,C,F,H,End', 'Start,B,D,G,H,End']
   Tg rút Gantt     Cost              Ways
0       0     0      0.0  0a0b0c0d0e0f0g0h
1       1   0,2   1000.0  1a0b0c0d0e0f0g0h
2                         0a0b1c0d0e0f0g0h
3                         0a0b0c0d1e0f0g0h
4       2   0,2   3000.0  1a0b1c1d0e0f0g0h
5                         1a0b0c1d1e0f0g0h
6                         0a0b1c1d1e0f0g0h
7                         0a0b0c1d2e0f0g0h
8                         1a0b0c0d0e0f1g0h
9                         0a0b1c0d0e0f1g0h
..      ..   ..	  ......      ............
```

Hàng đầu tiên chính là các con đường của bài toán.

Ví dụ từ hàng 1 đến hàng 3 của bảng: 

	+ Thời gian rút ngắn là 1 ngày (Cột 1)
	+ Sau khi rút ngắn, đường Gantt thứ 0 ('Start,A,C,E,G,H,End') và thứ 2 ('Start,B,D,G,H,End') sẽ cùng trở thành đường Gantt (Cột 2)
	+ Tổng chi phí tối thiểu rút ngắn là 1000 (Cột 3)
	+ Có 3 cách rút gọn: (Cột 4)
		- 1a0b0c0d0e0f0g0h: giảm dự án A 1 đơn vị thời gian
		- 0a0b1c0d0e0f0g0h: giảm dự án C 1 đơn vị thời gian
		- 0a0b0c0d1e0f0g0h: giảm dự án E 1 đơn vị thời gian 
		etc: 0a0b1c1d1e0f1g0h: giảm dự án C 1 đơn vị, dự án D 1 đơn vị, dự án E 1 đơn vị, dự án G 1 đơn vị	
&#8594; Tức là để giảm 1 ngày thực hiện dự án, 3 cách giảm trên sẽ là cách giảm tối ưu nhất để chi phí giảm là nhỏ nhất (1000)  

Tương tự với các mốc thời gian rút ngắn khác.

# **3. Quy trình thuật toán**
Thuật toán dựa trên việc [giải hệ bất phương trình](https://github.com/Truongphi20/inequaltion) để tìm ra tất cả trường hợp rút ngắn có thể xảy ra khi từng con đường trong sơ đồ mạng sau khi rút ngắn trở thành đường Gantt. Sau đó lọc các các điểm sao cho chi phí thấp nhất ở các mốc thời gian và xuất ra kết quả.

_Quy trình:_
- Xác định tất cả con đường trong sơ đồ mạng
- Xét từng trường hợp sau khi rút ngắn con đường đó trở thành đường Gantt. Các điều kiện để thiết lập bất phương trình như sau:
	>+ Thời gian rút ngắn phải nằm trong phạm vị cho phép (đề cho)
	>+ Thời gian hoàn thành sau rút ngắn của các đường không Gantt phải bé hơn hoặc bằng đường Gantt
	>+ Thời gian rút ngắn phải lớn hơn hoặc bằng 0
- Lọc ra các điểm tối ưu ở từng trường hợp với chi phí rút ngắn là tối thiểu.
- Tổng hợp dữ kiện của các trường hợp và xuất ra kết quả.
