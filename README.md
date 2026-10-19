# BTL1 - Các vấn đề hiện đại của Khoa học máy tính

## 1. Giới thiệu

Đây là mã nguồn phục vụ **Bài tập lớn số 1 (BTL1)** của học phần **Các vấn đề hiện đại của Khoa học máy tính (INT3011E)**.

Đề tài tập trung nghiên cứu và thực nghiệm giải bài toán **N-Queens** bằng phương pháp **SAT (Boolean Satisfiability Problem)**, đồng thời so sánh với một số phương pháp giải dựa trên **MIP** và **CP**.

## 2. Các phương pháp Encoding

Đối với phương pháp SAT, dự án sử dụng ba encoding:

- **Sequential Encoding**
- **Binomial Encoding**
- **Binary Encoding**

Các encoding chuyển bài toán N-Queens thành công thức **CNF**, sau đó sử dụng SAT Solver để tìm nghiệm.

## 3. Các Solver

Dự án thực nghiệm và so sánh các solver:

- **PySAT / Glucose3**
- **Gurobi**
- **CPLEX-MIP**
- **CPLEX-CP**
- **OR-Tools CP-SAT**

## 4. Cấu trúc mã nguồn

```text
.
├── binary.py
├── binomial.py
├── sequential.py
├── solvers.py
├── experiment.py
├── experiment_results_large.csv
├── size.txt
└── README.md
```

- `binary.py`: Binary Encoding.
- `binomial.py`: Binomial Encoding.
- `sequential.py`: Sequential Encoding.
- `solvers.py`: Cài đặt các phương pháp giải gồm Gurobi, CPLEX-MIP, CPLEX-CP và OR-Tools CP-SAT.
- `experiment.py`: Chạy các thí nghiệm và ghi nhận kết quả.
- `experiment_results_large.csv`: Lưu kết quả thực nghiệm.
- `size.txt`: Lưu thông tin kích thước công thức SAT.

