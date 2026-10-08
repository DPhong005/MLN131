# Thiết lập và vận hành

Hướng dẫn đầy đủ nằm trong [README.md](README.md).

1. Cài Node.js 22 trở lên và chạy `npm ci`.
2. Chạy `npm start`, mở http://localhost:3000.
3. Dùng `npm run dev` để tự dựng lại khi sửa dữ liệu hoặc giao diện.
4. Có thể đặt `PORT` trong `.env` nếu cần đổi cổng chạy.
5. Trước khi triển khai, chạy `npm run build`, `npm test` và `npm run test:browser`.
6. Trên Vercel dùng backend Express và build `npm run build`.

Nguồn học tập là giáo trình CNXH khoa học 2021. Bản chạy trong `public/` không phục vụ các tệp nội bộ của dự án.
