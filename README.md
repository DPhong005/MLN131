# Chủ nghĩa xã hội khoa học trong đời sống

Website HTML/JavaScript với backend Express. Nội dung chuyển từ Triết học sang 7 chương của **Giáo trình Chủ nghĩa xã hội khoa học**, Bộ GD&ĐT, NXB Chính trị quốc gia Sự thật, 2021.

## Chạy cục bộ

Cần Node.js 22 trở lên.

```powershell
npm ci
npm start
```

Mở http://localhost:3000. `npm start` tự tạo bản chạy trong `public/` trước khi mở máy chủ. Không mở HTML bằng `file://` vì bài học được tải qua HTTP.

Khi biên tập và phát triển:

```powershell
npm run dev
```

Chế độ phát triển tự dựng lại website khi nội dung, CSS, JavaScript hoặc backend thay đổi.

## Nội dung và chức năng

- 7 chương, 28 mục bài học: mục tiêu, tình huống, kiến thức, sơ đồ, điểm dễ nhầm, tự luận và nguồn.
- 42 câu trắc nghiệm theo 7 chương; bài tổng hợp lấy 2 câu từ mỗi chương.
- 7 tình huống và 7 bài viết diễn giải theo giáo trình.
- Bốn game: giải mã khái niệm, sơ đồ tư duy, kiểm chứng nhận định và ghế nóng; giữ các hoạt động ghép khái niệm, phân biệt kiến thức, phân tích tình huống.
- Tìm kiếm có hoặc không dấu; từ điển gồm 18 khái niệm.
- Lưu các mục đã đọc, kết quả tốt nhất, bài tự luận trên trình duyệt; xuất bản sao tiến độ.
- Giao diện điện thoại, bàn phím, liên kết mở đúng trang PDF.
- Không còn video, trình phát hoặc iframe trên website được xuất để chạy.

Các bài học là phần tóm lược và diễn giải phục vụ học tập, không phải bản chép toàn bộ giáo trình. Mọi tình huống đều là giả định. Số trang liên kết là trang PDF tính từ 1, không phải số trang in trên sách. Khi thêm trích dẫn nguyên văn, kiểm tra trang gốc. Nhận định và chính sách trong sách được đặt trong bối cảnh 2021.

## Chỉnh sửa nội dung

| Tệp | Nội dung |
| --- | --- |
| `data/course.json` | Tên môn, thông điệp, mô tả |
| `data/chapters.json` | 7 chương, mục bài học, mục tiêu, sơ đồ, tự luận |
| `data/questions.json` | Câu hỏi, lựa chọn, chỉ số đáp án, giải thích, nguồn |
| `data/cases.json` | Tình huống và các gợi ý phân tích |
| `data/articles.json` | Bài viết và đường dẫn mới |
| `data/glossary.json` | Thuật ngữ và liên kết bài học |
| `data/sources.json` | Thông tin nguồn và PDF |
| `css/site.css` | Màu sắc, bố cục, kiểu chữ, giao diện điện thoại |
| `js/app.js` | Hiển thị trang và tương tác |
| `js/state.mjs` | Lưu tiến độ và tính kết quả |

Giữ ID chương 1–7, ID mục `chương-mục` và các liên kết giữa dữ liệu đồng bộ. Đáp án `correct` bắt đầu từ 0. Mỗi câu hỏi cần `lessonId`, `pages` và `explanation`. Sau khi chỉnh:

```powershell
npm run build
npm test
```

Các tệp HTML là trang khung được tạo bởi `scripts/build-pages.js`; sửa bố cục trong `js/app.js`, không sửa trực tiếp phần được tạo. `data/routes.json` cũng được sinh tự động. `public/` chỉ chứa các tệp cho người dùng truy cập, không đưa backend, tài liệu nội bộ hoặc script cũ vào bản chạy.

Các địa chỉ `module1.html`–`module5.html`, bài viết và game cũ vẫn mở được, nhưng hiển thị học liệu mới. Chương 6–7, tình huống, từ điển và tiến độ có các địa chỉ mới. Một số hình và tài liệu cũ trong kho được giữ để tránh mất tài nguyên; chúng không được đưa vào `public/`.

## Kiểm tra

```powershell
npm run build
npm test
npm run test:browser
```

Bộ kiểm tra trình duyệt dùng Microsoft Edge đã cài trên Windows, chạy headless qua Playwright. Trên môi trường khác, cài Chromium cho Playwright và thay `channel: 'msedge'` trong `playwright.config.cjs`. Suite mở máy chủ ở cổng 3187.

Kiểm tra bao gồm liên kết và hiển thị 46 trang, việc loại bỏ video, đọc PDF theo byte range, lưu tiến độ và tự luận, tìm không dấu, hoàn thành bài trắc nghiệm, game, và bố cục điện thoại. Ảnh kiểm tra giao diện được lưu tại `output/site-preview/`.

## Vercel

`server.js` xuất ứng dụng Express; `npm run build` tạo `public/` để Vercel phục vụ tệp tĩnh. Khi kết nối dự án, dùng thư mục này làm root dự án, framework Express và lệnh build `npm run build`.

Không cấu hình `PDF_URL` của bản Triết học cũ; nguồn PDF hiện tại là `assets/docs/cnxh-khoa-hoc-2021.pdf`.

Tài liệu chính thức: https://vercel.com/docs/frameworks/backend/express

Thay đổi trong kho chưa tự cập nhật website đã phát hành; cần tạo bản preview và triển khai từ kho đã cập nhật. Không có thao tác deploy hoặc push trong lần chỉnh sửa này.

Website dùng 27 ảnh chụp thật từ Wikimedia Commons và Pexels. Các chương, 7 tình huống, 7 bài viết và 4 game có bộ ảnh riêng; mỗi trang tránh lặp ảnh giữa các thẻ. Nguồn và giấy phép nằm trong `data/photoCredits.json` và trang tài nguyên. Ảnh đầu chương được tách nền từ ảnh gốc bằng imagegen; PNG lưu tại `output/chapter-photo-cutouts/`. Ảnh thẻ phủ kín vùng hiển thị. Bản xuất `public/` chỉ sao chép ảnh được khai báo trong dữ liệu nguồn và bìa giáo trình. Các minh họa cũ được giữ trong kho để tham khảo.

Cả 28 mục bài học có phần dẫn nhập, 3 phần giải thích chi tiết, câu hỏi tự kiểm tra, ý chính và nguồn PDF. Nội dung là diễn giải theo giáo trình 2021. Sửa nội dung trực tiếp trong `data/chapters.json`; tìm kiếm dùng cả phần giải thích mới. `scripts/expand-course.mjs` ghi lại lần bổ sung nội dung, chạy lại sẽ thay thế các trường `sections`, `review` và thời lượng của chương.
