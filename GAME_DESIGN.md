# Game CNXH khoa học

Tham khảo cơ chế tại https://hcm-202-tv4q.vercel.app/games.html: ghép mảnh từ, phân loại từ khóa, phát hiện sai lệch trong hồ sơ, và quiz show. Website dùng phần triển khai riêng cùng giao diện xanh/navy và học liệu CNXH 2021. Không lấy mã nguồn hay câu hỏi của trang tham khảo để đưa vào bản chạy.

## Các đường dẫn

- `/game.html?mode=decode`: 8 khái niệm ngẫu nhiên, mảnh từ nhiễu, thử lại, gợi ý và điểm combo.
- `/game.html?mode=mindmap`: 3 chương ngẫu nhiên, 2 khái niệm/chương; kéo thả hoặc chọn bằng nút và bàn phím.
- `/game.html?mode=verify`: 3 nhận định đúng và 3 sai, chọn nhận định sai; 3 lượt đánh dấu nhầm, hồ sơ nguồn và giải thích. Đây là bản tin giả định phục vụ học tập.
- `/game.html?mode=hotseat`: 15 câu, mỗi mức độ 5 câu; dừng khi sai/hết giờ, mốc an toàn 5 và 10. Chọn 15 giây, 30 giây hoặc không giới hạn. Ba quyền dùng một lần: 50:50, tra cứu giáo trình (tạm dừng đồng hồ), hội trường mô phỏng.

## Học liệu và kết quả

Giải mã và bản đồ dùng `data/glossary.json`; Ghế nóng dùng `data/questions.json`; hồ sơ dùng `data/gameClaims.json`. Mọi nhận định hồ sơ có nguồn `lessonId`, giải thích và liên kết PDF. Các nội dung bài học đã bổ sung được giữ nguyên.

Điểm tốt nhất lưu trong trạng thái học tập của trình duyệt. Không có tiền thưởng, tài khoản hoặc bảng xếp hạng trực tuyến. Hội trường là mô phỏng được ghi rõ trên màn hình, không phải khảo sát người dùng thực.

Các hoạt động cũ vẫn có tại `mode=match`, `mode=classify` và `mode=situations`.

## Kiểm tra

`npm test` kiểm tra học liệu và cách chọn câu theo mức độ. `npm run test:browser` kiểm tra hoàn thành 4 game, kéo thả/bàn phím, trợ giúp, hết giờ, mốc an toàn, lưu điểm và bố cục điện thoại.
