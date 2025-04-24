#!/usr/bin/env python3
import os
import time
import requests
import psutil
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor
from apscheduler.schedulers.blocking import BlockingScheduler

from bt_api import BtApi            # lớp bạn đã định nghĩa để gọi aaPanel
from cloudflare_api import Cloudflare  # Giả sử class Cloudflare ở đây

load_dotenv()

# === CONFIG ===
PANEL_URL     = os.getenv('AAPANEL_URL')
PANEL_KEY     = os.getenv('AAPANEL_KEY')
CF_API_TOKEN  = os.getenv('CF_API_TOKEN')
TG_TOKEN      = os.getenv('TELEGRAM_TOKEN')
TG_CHAT       = os.getenv('TELEGRAM_CHAT_ID')
TIMEZONE      = os.getenv('TZ', 'Asia/Ho_Chi_Minh')

# Tắt warning SSL self-signed
requests.packages.urllib3.disable_warnings()

def notify_telegram(text: str):
    url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
    try:
        requests.post(url, data={
            "chat_id":    TG_CHAT,
            "text":       text,
            "parse_mode": "Markdown"
        }, timeout=5)
    except Exception as e:
        print(f"[Telegram Error] {e}")

def is_ddos(domain: str,
            tries: int = 3,
            timeout_s: float = 2,
            max_error_rate: float = 0.5,
            max_avg_resp: float = 1.5) -> bool:
    errors, times = 0, []
    url = f"https://{domain}"
    for _ in range(tries):
        start = time.time()
        try:
            r = requests.get(url, timeout=timeout_s, verify=False)
            elapsed = time.time() - start
            times.append(elapsed)
            if r.status_code >= 500:
                errors += 1
        except requests.RequestException:
            errors += 1

    error_rate = errors / tries
    avg_time   = sum(times) / len(times) if times else float('inf')
    print(f"[{domain}] error_rate={error_rate:.2f}, avg_time={avg_time:.2f}s")
    return error_rate > max_error_rate or avg_time > max_avg_resp

def process_site(domain, cloudflare_api):
    if is_ddos(domain):
        notify_telegram(f"🚨 *DDoS detected* trên `{domain}`! Bật WAF…")
        try:
            zone_id = cloudflare_api.get_zone_id(domain)
            if not zone_id:
                notify_telegram(f"❌ Không thể lấy zone_id cho `{domain}`")
                return

            cloudflare_api.enable_under_attack_mode(zone_id)
            time.sleep(300)  # đợi 5 phút
            if not is_ddos(domain):
                notif = cloudflare_api.disable_under_attack_mode(zone_id)
                notify_telegram(notif)
            else:
                notify_telegram(f"🚨 `{domain}` vẫn bị tấn công, giữ WAF bật.")
        except Exception as ex:
            notify_telegram(f"❌ Lỗi khi xử lý DDoS cho `{domain}`: {ex}")
    else:
        print(f"✅ {domain} bình thường")

def main_task():
    # 1. Kiểm tra CPU
    cpu = psutil.cpu_percent(interval=1)
    print(f"[Main] CPU Usage: {cpu:.1f}%")
    if cpu < 70:
        print("[Main] CPU < 70%, không đi check DDoS.")
        return

    # 2. Lấy list sites từ aaPanel
    api = BtApi(PANEL_URL, PANEL_KEY)
    try:
        sites   = api.get_sites(page=1, limit=999)
        domains = [s["name"] for s in sites]
    except Exception as e:
        notify_telegram(f"❌ Lỗi lấy sites: {e}")
        return

    # 3. Init Cloudflare API
    cf = Cloudflare(CF_API_TOKEN)

    # 4. Song song kiểm tra
    with ThreadPoolExecutor(max_workers=5) as executor:
        for domain in domains:
            executor.submit(process_site, domain, cf)

if __name__ == "__main__":
    # Tạo scheduler
    scheduler = BlockingScheduler(timezone=TIMEZONE)

    # Lên lịch: ví dụ mỗi ngày 02:00
    scheduler.add_job(main_task, 'cron', hour=2, minute=0)

    # Chạy ngay lần đầu khi container start (tuỳ chọn)
    print("[Scheduler] Chạy ngay main_task lần đầu…")
    main_task()

    print(f"[Scheduler] Bắt đầu chạy theo lịch cron hàng ngày 02:00 ({TIMEZONE})")
    scheduler.start()
