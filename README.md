# Tên dự án: DDoSGuard

**Mô tả**: Công cụ giám sát tải CPU của website, tự động kích hoạt WAF captcha khi phát hiện tấn công DDoS.

# Hướng Dẫn Cài Đặt

Thực hiện tuần tự các bước sau:

1. Lệnh **git clone**

   ```bash
   git clone git@github.com:ThanhNhax/DDoSGuard.git
   ```

2. Chuyển vào thư mục source

   ```bash
   cd DDoSGuard
   ```

3. Lệnh **cp env**

   ```bash
   cp .env.example .env
   ```

4. Lệnh **make build**

   - Thực thi câu lệnh Docker build được định nghĩa trong Makefile (`make build`). Ví dụ:

     ```bash
     docker build -t ddosguard:latest -f Dockerfile .
     ```

5. Lệnh **make up**

   - Thực thi câu lệnh `docker run` sử dụng file `.env` để khởi chạy container. Ví dụ:

     ```bash
     docker run -d --name ddosguard-container --env-file .env ddosguard:latest
     ```
