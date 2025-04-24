# Hướng Dẫn Cài Đặt

Thực hiện tuần tự các bước sau:

1. Lệnh **git clone**

   ```bash
   git clone <repository_url>
   ```

2. Chuyển vào thư mục source

   ```bash
   cd src
   ```

3. Lệnh **cp env**

   ```bash
   cp .env.example .env
   ```

4. Lệnh **make build**

   - Thực thi câu lệnh Docker build được định nghĩa trong Makefile (make build). Ví dụ:

   ```bash
   docker build -t <tên_image>:<tag> -f Dockerfile .
   ```

5. Lệnh **make up**

   - Thực thi câu lệnh `docker run` sử dụng file `.env` để khởi chạy container. Ví dụ:

   ```bash
   docker run --env-file .env -d --name <tên_container> <tên_image>:<tag>
   ```
