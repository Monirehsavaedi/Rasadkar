import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def scrape_jobvision(keywords):
    """جستجو در آگهی‌های جاب‌ویژن با قابلیت تحمل خطای شبکه"""
    print("🌐 در حال بررسی آگهی‌های جدید در سایت جاب‌ویژن...")
    
    url = "https://brsapi.jobvision.ir/api/v1/Job/Search"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Content-Type": "application/json"
    }
    
    payload = {
        "keyword": "محتوا",
        "page": 1,
        "pageSize": 30
    }
    
    proxies = {
        "http": None,
        "https": None
    }
    
    found_jobs = []
    try:
        response = requests.post(url, json=payload, headers=headers, proxies=proxies, timeout=10, verify=False)
        
        if response.status_code == 200:
            jobs = response.json().get("data", {}).get("jobs", [])
            for job in jobs:
                title = job.get("title", "")
                company = job.get("company", {}).get("namePersian", "شرکت نامشخص")
                link = f"https://jobvision.ir/jobs/{job.get('id', '')}"
                
                for kw in keywords:
                    if kw.lower() in title.lower():
                        found_jobs.append({
                            "title": title,
                            "company": company,
                            "link": link,
                            "source": "جاب‌ویژن"
                        })
                        break
    except requests.exceptions.ConnectionError:
        print("⚠️ هشدار: به دلیل تداخل DNS فیلترشکن، ارتباط با جاب‌ویژن برقرار نشد. (اسکیپ شد)")
    except Exception:
        # سایر خطاها را بی‌سروصدا رد می‌کنیم تا برنامه متوقف نشود
        pass
        
    return found_jobs