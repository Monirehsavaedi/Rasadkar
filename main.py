import os
import json
import time
import requests
from dotenv import load_dotenv

from scrapers.jobinja import scrape_jobinja
from scrapers.jobvision import scrape_jobvision

load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# اضافه شدن این خط برای جلوگیری از عبور ترافیک سایت‌های ایرانی از فیلترشکن
os.environ['NO_PROXY'] = 'jobvision.ir,jobinja.ir,localhost,127.0.0.1'

def load_config():
    try:
        with open("config.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return None

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown"}
    # این پراکسی فقط برای همین ریکوئست (تلگرام) اعمال می‌شود
    proxies = {"http": "http://127.0.0.1:10808", "https": "http://127.0.0.1:10808"}
    try:
        requests.post(url, json=payload, proxies=proxies, timeout=15)
    except Exception:
        pass

def job_runner():
    config = load_config()
    if not config:
        return
        
    keywords = config["search_keywords"]
    print(f"\n[{time.strftime('%H:%M:%S')}] 🔄 شروع دوره جدید جستجو...")
    
    all_jobs = []
    all_jobs.extend(scrape_jobinja(keywords))
    all_jobs.extend(scrape_jobvision(keywords))
    
    if all_jobs:
        print(f"🎉 {len(all_jobs)} آگهی پیدا شد! در حال ارسال...")
        for job in all_jobs:
            message = (
                f"🎯 *آگهی جدید پیدا شد!*\n\n"
                f"💼 *عنوان:* {job['title']}\n"
                f"🏢 *شرکت:* {job['company']}\n"
                f"🌐 *منبع:* {job['source']}\n\n"
                f"🔗 [مشاهده آگهی]({job['link']})"
            )
            send_telegram_message(message)
    else:
        print("📭 آگهی جدیدی پیدا نشد.")

if __name__ == "__main__":
    print("🚀 رصدکار فعال شد و در پس‌زمینه کار می‌کند...")
    
    # حلقه بی‌نهایت برای اجرای مداوم
    while True:
        job_runner()
        # توقف برنامه به مدت 10 دقیقه (600 ثانیه) تا دوره بعدی
        print("\n⏳ در حال انتظار تا 10 دقیقه آینده...")
        time.sleep(600)