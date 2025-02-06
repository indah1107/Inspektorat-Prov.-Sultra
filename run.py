import os
import time
import threading
import webview

def run_django():
    os.system("python manage.py runserver 127.0.0.1:8000")

# Jalankan server Django di thread terpisah
django_thread = threading.Thread(target=run_django, daemon=True)
django_thread.start()

# Tunggu server Django siap (beri waktu untuk start)
time.sleep(3)

# Buka aplikasi dalam jendela PyWebView
webview.create_window("Aplikasi Django", "http://127.0.0.1:8000")
webview.start()
