import sys
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import pandas as pd
import time
import keyboard
import math
from webdriver_manager.chrome import ChromeDriverManager
import tkinter as tk
from tkinter import simpledialog
import time

# Konsol kodlamasını kontrol et ve gerekirse UTF-8 olarak ayarla
if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

def collect_data():
    try:
        # # WebDriver'ı başlatma
        # service = Service(executable_path='./chromedriver.exe')  # ChromeDriver yolunu kontrol et
        # options = webdriver.ChromeOptions()
        # #options.add_argument('--headless')  # İstersen tarayıcıyı arka planda çalıştırabilirsin
        # driver = webdriver.Chrome(service=service, options=options)

        # # İncelenmek istenen web sitesinin URL'sini belirtme
        # website_url = 'https://www.trendyol.com/moda-elf/kadin-bordo-rugan-omuz-cantasi-p-810187020/yorumlar?boutiqueId=61&merchantId=766891'
        # driver.get(website_url)
       
        # Tkinter ile URL al
        root = tk.Tk()
        root.withdraw()
        website_url = simpledialog.askstring("URL Girişi", "Trendyol yorum bağlantısını girin (Çıkmak için 'exit' yazın):")
        if not website_url or website_url.lower() == "exit":
            print("URL girişi iptal edildi.")
            return
        
        # WebDriver başlat
        options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        
        # Belirtilen URL'ye git
        driver.get(website_url)
        
        # Sayfa içerisinde hareket etmek için "body" elementini bulma
        body = driver.find_element(By.TAG_NAME, 'body')

        for m in range(5000):
            body.send_keys(Keys.PAGE_DOWN)
            comments_elements = driver.find_elements(By.CSS_SELECTOR, 'div.comment-text > p') #yorum sayısı kontrol

            if m < 1000 and m % 50 == 0:
                for i in range(5):
                    body.send_keys(Keys.PAGE_UP)
                    os.system('cls')
                    
            elif m % 50 == 0:
                # 1000'den sonra her 50 basışta PAGE_UP sayısını arttır
                for i in range(5):
                    body.send_keys(Keys.PAGE_UP)
                    os.system('cls')
                    
            # Sayfa yüklenmesini beklemek için kısa bir süre bekletme
            time.sleep(2)
            
            print((f"Sayaç sayısı: {m}"))
            print((f"Anlık toplanan yorum sayısı: {len(comments_elements)}"))

            
            #Döngu bitmeden çıkmak için q ya basarak çıkmak
            if keyboard.is_pressed('q'):
                print("Cikis yapildi!")
                break

         # Yorumları topla
        comments_elements = driver.find_elements(By.CSS_SELECTOR, 'div.comment-text > p')
        comments = [comment.text for comment in comments_elements]

        # Yıldızları topla
        stars_elements = driver.find_elements(By.CSS_SELECTOR, 'div.comment')
        stars = [elem.get_attribute("outerHTML").count("width: 100%") for elem in stars_elements]

    except Exception as e:
        print(f"Bir hata oluştu: {e}")
        comments, stars = [], []

    finally:
        driver.quit()
        return comments, stars

if __name__ == "__main__":
    comment_stars = []
    comments, stars = collect_data()

    # Yıldızları düzelt: Her yıldızdan 5 çıkar
    normalized_stars = [max(1, star - 5) if star is not None else None for star in stars]

    print(f"Toplam Yorum Sayısı: {len(comments)}")
    print(f"Toplam Yıldız Sayısı: {len(stars)}")

    for comment, star in zip(comments, normalized_stars):  # Düzeltilmiş yıldızları kullanıyoruz
        if comment:
            comment_stars.append({
                "Original Comment": comment,
                "Normalized Stars": star  # Düzeltilmiş yıldız değerleri ekleniyor
            })
        else:
            # Boş yorumlar için None değerleri ekle
            comment_stars.append({
                "Original Comment": None,
                "Normalized Stars": None
            })

    # Veriyi DataFrame'e dönüştür ve Excel'e kaydet
    df = pd.DataFrame(comment_stars)
    df.to_excel("SynchronizedData.xlsx", index=False)
    print("Veriler senkronize bir şekilde SynchronizedData.xlsx dosyasına kaydedildi!")



