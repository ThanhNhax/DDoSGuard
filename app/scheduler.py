import os
from apscheduler.schedulers.blocking import BlockingScheduler
from monitor_all_sites_challenge import main_task

RUN_INTERVAL = int(os.getenv("RUN_INTERVAL_MINUTES", "5"))

if __name__ == "__main__":
    scheduler = BlockingScheduler(timezone="Asia/Ho_Chi_Minh")

    # 1. Chạy ngay khi start (tuỳ chọn)
    print("[Scheduler] Chạy ngay main_task lần đầu…")
    main_task()

    # 2. Lên lịch mỗi phút
    scheduler.add_job(main_task, 'interval', minutes=RUN_INTERVAL)
    print(f"[Scheduler] Bắt đầu chạy main_task mỗi {RUN_INTERVAL} phút")
    # hoặc nếu bạn vẫn thích cron syntax:
    # scheduler.add_job(main_task, 'cron', minute='*')

  
    scheduler.start()
