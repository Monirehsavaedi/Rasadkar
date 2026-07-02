import requests
from bs4 import BeautifulSoup

def scrape_jobinja(keywords):
    """جستجو در آگهی‌های جابینجا بر اساس کلمات کلیدی"""
    print("🌐 در حال بررسی آگهی‌های جدید در سایت جابینجا...")
    
    # برای اینکه جابینجا ما را ربات تشخیص ندهد، یک هدر مرورگر اضافه می‌کنیم
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    # برای اطمینان از پیدا کردن آگهی‌های مرتبط، پایه جستجو را روی کلمه محتوا می‌گذاریم
    url = "https://jobinja.ir/jobs?&q=محتوا"
    
    found_jobs = []
    try:
        # دقت کنید که اینجا پراکسی نداریم، چون جابینجا سایت داخلی است و بدون فیلترشکن بهتر باز می‌شود
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            print("❌ خطا در بارگذاری سایت جابینجا.")
            return []
            
        soup = BeautifulSoup(response.text, "html.parser")
        
        # پیدا کردن تمام کارت‌های آگهی شغلی در صفحه
        job_cards = soup.find_all("li", class_="o-listView__item")
        
        for card in job_cards:
            title_tag = card.find("a", class_="c-jobListView__titleLink")
            company_tag = card.find("li", class_="c-jobListView__metaItem")
            
            if not title_tag:
                continue
                
            title = title_tag.text.strip()
            link = title_tag["href"]
            company = company_tag.text.strip() if company_tag else "شرکت نامشخص"
            
            # بررسی تطابق عنوان آگهی با کلمات کلیدی کانفیگ شما
            for kw in keywords:
                if kw.lower() in title.lower():
                    found_jobs.append({
                        "title": title,
                        "company": company,
                        "link": link,
                        "source": "جابینجا"
                    })
                    break  # اگر یک کلمه پیدا شد، دیگر نیازی به چک کردن بقیه کلمات برای همین آگهی نیست
                    
    except Exception as e:
        print(f"❌ خطای شبکه در ارتباط با جابینجا: {e}")
        
    return found_jobs