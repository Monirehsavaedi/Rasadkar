# استفاده از یک نسخه سبک و رسمی پایتون
FROM python:3.12-slim

# تنظیم پوشه کاری داخل کانتینر
WORKDIR /app

# کپی کردن فایل پیش‌نیازها و نصب آن‌ها
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# کپی کردن کل فایل‌های پروژه به داخل کانتینر
COPY . .

# دستوری که کانتینر هنگام روشن شدن اجرا می‌کند
CMD ["python", "-u", "main.py"]