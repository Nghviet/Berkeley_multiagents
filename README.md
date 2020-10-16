# Berkeley_multiagents

Họ tên : Nguyễn Hoàng Việt

MSSV : 18020063

Lớp INT 3401 8

autograder_result.txt chứa result của 1 lần autograder, không phải lúc quay film để báo cáo

# Bài 1:
Nếu pacman quá gần ma, state đó trả về giá trị -(1e9+7) để tránh

Công thức tính score : baseScore + (có ăn hạt ko) * 10 - (khoảng cách Manhattan đến food gần nhất)

Luôn luôn tìm đến food gần nhất và ăn hạt, ko tính đến việc truy đuổi ma

# Bài 2:
Hàm layer: nếu agent là 0 thì là max_layer, ko thì là min_layer

Nếu layer đã đến depth được định sắn hoặc gameState đã có kết quả: nếu còn state dưới thì kiểm tra lấy giá trị của các con, ko thì trả về giá trị qua evalutaionFunction

Nếu ko: 1 vòng for qua các action để tìm score và action thỏa mãn

# Bài 3:
Giống bài 2 nhưng ở mỗi phòng for, cần thêm hàm kiểm tra và cập nhật alpha,beta , chặt cây khi thỏa mãn yêu cầu

# Bài 4:
Giống bài 2 nhưng min_layer đổi thành Exp_layer: do là phân bố đều nên score của Exp_layer là TBC của các con

Được code lại nên trông dễ đọc hơn so với bài 2 và bài 3

# Bài 5:
Nếu pacman quá gần ma chưa sợ, state đó trả về giá trị -(1e9+7) để tránh

Nếu ma sợ thì pacman bật chết độ đồ sát, được + 100 điểm và đi săn con ma đó

Công thức tính score : baseScore - (khoảng cách Manhattan ngắn nhất đến food) - (Tổng thức ăn thừa ) * 15 + (extra từ ma)

Luôn luôn tìm đến food gần nhất và ăn hạt, ko tính đến việc truy đuổi ma
