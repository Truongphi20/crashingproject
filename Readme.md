Thuật toán tìm các cách rút gọn thời gian thực hiện của dự án.
=============

Yêu cầu: rút ngắn một lượng thời gian sao cho tổng chi phí rút ngắn là nhỏ nhất

======================================

**Usage:**

B1: Điều chỉnh file "input_data.csv":

	- Các thành phân trong bảng phân cách bằng tab.
	- Không cần điều chỉnh tên cột
	- Ý nghĩa tên các cột:
		+ Cột 1: Tên các dự án
		+ Cột 2: Các dự án liền trước dự án bên cột 1
		+ Cột 3: Thời gian hoàn thành dự án không rút ngắn tiến độ
		+ Cột 4: Thời gian có thể rút ngắn tối đa của dự án đó
		+ Cột 5: Chi phí khi rút ngắn một đơn vị dự án 
	- Điều chỉnh các cột phù hợp với điều kiện đề bài
B2: Chạy thuật toán:
	python .\CrashTime.py
	
Kết quả sẽ xuất ra trực tiếp trên terminal.  

========================================

**Ví dụ kết quả:**

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
..	..	..	......	............
```

Ví dụ từ hàng 1 đến hàng 3: 

	+ Thời gian rút ngắn là 1 ngày (Cột 1)
	+ Sau khi rút ngắn, đường Gantt thứ 0 ('Start,A,C,E,G,H,End') và thứ 2 ('Start,B,D,G,H,End') sẽ cùng trở thành đường Gantt (Cột 2)
	+ Tổng chi phí tối thiểu rút ngắn là 1000 (Cột 3)
	+ Có 3 cách rút gọn: (Cột 4)
		- 1a0b0c0d0e0f0g0h: giảm dự án A 1 đơn vị thời gian
		- 0a0b1c0d0e0f0g0h: giảm dự án C 1 đơn vị thời gian
		- 0a0b0c0d1e0f0g0h: giảm dự án E 1 đơn vị thời gian 
		etc: 0a0b1c1d1e0f1g0h: giảm dự án C 1 đv, dự án D 1 đv, dự án E 1 đv
	
-> Tức là để giảm 1 ngày thực hiện dự án, 3 cách giảm trên sẽ là cách giảm tối ưu nhất để chi phí giảm là nhỏ nhất (1000)  

Tương tự với các mốc thời gian rút khác.
