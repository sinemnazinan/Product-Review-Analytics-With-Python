# -*- coding: utf-8 -*-
import sys
from nltk.corpus import stopwords
import pandas as pd
import re
from jpype import startJVM, shutdownJVM, JClass

# Konsol kodlamasını kontrol et ve gerekirse UTF-8 olarak ayarla
if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

# JVM yolunu elle belirtin
jvm_path = "C:/Program Files/Zulu/zulu-17/bin/server/jvm.dll"

# JVM'i başlat
startJVM(jvm_path, "-Xmx512m","-Djava.class.path=zemberek-full.jar")

# Zemberek Morfoloji Modülü
TurkishMorphology = JClass("zemberek.morphology.TurkishMorphology")
morphology = TurkishMorphology.createWithDefaults()
# Stopword listesi
stopwords = set(["ve", "ile", "ama", "fakat", "ancak", "çünkü", "de", "da", "mi", "mu", "mi?", "bu", "şu", "o", "gibi", "ise", "değil", "mı", "mu", "bir", "ben", "sen", "biz", "siz", "onlar", "için", "beni", "bana" ])

# Temel metin temizleme
def clean_text(text):
    text = re.sub(r'http\S+|www\S+|https\S+', '', text)  # URL'leri kaldır
    text = re.sub(r'\S+@\S+', '', text)                 # E-posta adreslerini kaldır
    text = re.sub(r'[^\w\sçöşüğıİÇÖŞÜĞ]', '', text)     # Gereksiz sembolleri kaldır
    text = re.sub(r'\s+', ' ', text).strip()            # Fazla boşlukları temizle
    return text

# Stopword'leri çıkarma
def remove_stopwords(text):
    words = text.split()
    return ' '.join([word for word in words if word not in stopwords])

def load_data_from_excel(file_path):
    """Excel dosyasını yükler."""
    try:
        data = pd.read_excel(file_path)
        print("Veriler başarıyla yüklendi.")
        return data
    except Exception as e:
        print(f"Excel dosyası yüklenirken hata oluştu: {e}")
        return None

def save_results_to_excel(data, output_path):
    """Sonuçları Excel dosyasına kaydeder."""
    try:
        data.to_excel(output_path, index=False)
        print(f"Sonuçlar başarıyla '{output_path}' dosyasına kaydedildi.")
    except Exception as e:
        print(f"Sonuçlar kaydedilirken hata oluştu: {e}")
        
# Metni temizleme ve işleme
def process_comment_zemberek(comment):
    
    try:
        
        # Yorumun boş veya sadece boşluk olup olmadığını kontrol et
        if not isinstance(comment, str) or comment.strip() == "":
            return None  # Boş yorumları atla
        comment = clean_text(comment)
        
        # Temizlenmiş yorumun boş olup olmadığını tekrar kontrol et
        if comment.strip() == "":
            return None
        cleaned_stopwords = remove_stopwords(comment)
        # 1. Yazım hatalarını düzeltme
        normalized_comment = morphology.normalizeForAnalysis(cleaned_stopwords)
        
        # 2. Cümleyi analiz et
        analysis_results = morphology.analyzeSentence(normalized_comment)
        
        # 3. Belirsizliği kaldır
        disambiguated = morphology.disambiguate(normalized_comment, analysis_results)
        
        processed_words = []
        for result in disambiguated.bestAnalysis():
            word = str(result)
            processed_words.append(word)

        return ' '.join(processed_words)
    except Exception as e:
        print(f"Yorum işlenirken hata oluştu: {e}")
        return None

    
if __name__ == "__main__":
    input_excel_path = "SynchronizedData.xlsx"  # Girdi dosyası
    output_excel_path = "ProcessedComments.xlsx"  # Çıkış dosyası

    # Excel verisini yükle
    data = pd.read_excel(input_excel_path)

    # 1. Aşama: Orijinal yorumlar ve yıldızlar zaten mevcut
    output_data = data[["Original Comment", "Normalized Stars"]].copy()

    # 2. Aşama: Standart işlenmiş yorumlar (Processed Comment)
    output_data["Processed Comment"] = data["Original Comment"].apply(process_comment_zemberek)

    # 4. Aşama: Sonuçları yeni dosyaya kaydet
    output_data.to_excel(output_excel_path, index=False)
    print(f"Tüm işlemler tamamlandı ve sonuçlar '{output_excel_path}' dosyasına kaydedildi.")

    # JVM'i kapat
    shutdownJVM()