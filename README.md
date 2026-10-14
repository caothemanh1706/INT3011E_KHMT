# BTL1 - Các vấn đề hiện đại của Khoa học máy tính

## Giới thiệu

Đây là toàn bộ mã nguồn phục vụ **Bài tập lớn số 1** của học phần **Các vấn đề hiện đại của Khoa học máy tính (INT3011E)**.

Đề tài tập trung vào việc giải bài toán **N-Queens** bằng phương pháp **SAT (Boolean Satisfiability Problem)**. Mục tiêu của chương trình là xây dựng các mô hình SAT khác nhau cho bài toán, chuyển đổi bài toán N-Queens thành công thức Boolean CNF, sau đó sử dụng bộ giải SAT để tìm nghiệm.

Trong dự án, bài toán được cài đặt và thực nghiệm với ba phương pháp encoding chính:

- **Sequential Encoding**
- **Binomial Encoding**
- **Binary Encoding**

Các encoding được sử dụng để biểu diễn các ràng buộc của bài toán N-Queens dưới dạng các mệnh đề logic CNF, từ đó đưa vào bộ giải SAT để tìm nghiệm.
