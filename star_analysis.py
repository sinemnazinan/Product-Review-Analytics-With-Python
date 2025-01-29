# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import sys
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import glob
import matplotlib.pyplot as plt
# Konsol kodlamasını kontrol et ve gerekirse UTF-8 olarak ayarla
if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

def combine_filtered_groups(filtered_comments_prefix, filtered_keywords_prefix, output_path):
    """
    İki grup (Filtered_Comments ve Filtered_By_Keywords) dosyalarını birleştirir ve tek bir Excel dosyasına kaydeder.

    Args:
        filtered_comments_prefix (str): Filtered Comments dosyalarının ortak ismi (örn. "Filtered_Comments").
        filtered_keywords_prefix (str): Filtered By Keywords dosyalarının ortak ismi (örn. "Filtered_By_Keywords").
        output_path (str): Birleştirilmiş Excel dosyasının kaydedileceği dosya yolu.
    """
    # Filtered_Comments dosyalarını bul ve birleştir
    filtered_comments_files = glob.glob(f"*{filtered_comments_prefix}*.xlsx")
    filtered_comments_data = pd.DataFrame()

    for file_path in filtered_comments_files:
        try:
            data = pd.read_excel(file_path)
            filtered_comments_data = pd.concat([filtered_comments_data, data], ignore_index=True)
        except Exception as e:
            print(f"Dosya okunurken hata oluştu: {file_path}, Hata: {e}")

    # Filtered_By_Keywords dosyalarını bul ve birleştir
    filtered_keywords_files = glob.glob(f"*{filtered_keywords_prefix}*.xlsx")
    filtered_keywords_data = pd.DataFrame()

    for file_path in filtered_keywords_files:
        try:
            data = pd.read_excel(file_path)
            filtered_keywords_data = pd.concat([filtered_keywords_data, data], ignore_index=True)
        except Exception as e:
            print(f"Dosya okunurken hata oluştu: {file_path}, Hata: {e}")

    # İki grubu birleştir
    combined_data = pd.concat([filtered_comments_data, filtered_keywords_data], ignore_index=True)

    # Birleştirilmiş dosyayı kaydet
    combined_data.to_excel(output_path, index=False)
    print(f"Birleştirilmiş dosya başarıyla kaydedildi: {output_path}")
    
def tfidf_by_star_group_with_2_classes(data):
    """
    Yıldız gruplarına göre TF-IDF hesaplar (Kötü, Nötr, İyi).
    """
    # Grupları ekle
    data = group_stars(data)

    # Gruplara göre yorumları ayır
    bad_comments = data[data['Star Group'] == 'Kötü']['Cleaned Comment']
    
    good_comments = data[data['Star Group'] == 'İyi']['Cleaned Comment']

    # TF-IDF vektörleştirici
    vectorizer = TfidfVectorizer(ngram_range=(1, 3), max_features=500)

    # Her grup için TF-IDF hesaplama
    bad_tfidf = vectorizer.fit_transform(bad_comments)
    good_tfidf = vectorizer.fit_transform(good_comments)

    # Skorları çıkarma
    bad_features = vectorizer.get_feature_names_out()
    good_features = vectorizer.get_feature_names_out()
    bad_scores = bad_tfidf.toarray().mean(axis=0)
    good_scores = good_tfidf.toarray().mean(axis=0)
    print(bad_scores)

    return {
        'Kötü': dict(zip(bad_features, bad_scores)),
        'İyi': dict(zip(good_features, good_scores))
    }

def extract_keywords(data, group, top_n=20):
    """
    Belirtilen grup için en yüksek TF-IDF skoruna sahip n-gram'ları çıkarır.
    """
    vectorizer = TfidfVectorizer(max_features=5000, ngram_range=(1, 3))
    group_comments = data[data['Star Group'] == group]['Cleaned Comment']
    tfidf_matrix = vectorizer.fit_transform(group_comments)
    feature_array = vectorizer.get_feature_names_out()
    tfidf_scores = tfidf_matrix.sum(axis=0).A1
    sorted_indices = tfidf_scores.argsort()[::-1]
    return [feature_array[i] for i in sorted_indices[:top_n]]

def group_stars(data):
    """
    Yıldızları 2 gruba (Kötü, İyi) ayırır ve nötr yıldızlıları (3 yıldız)
    otomatik olarak çıkarılan anahtar kelimelere göre sınıflandırır.
    Kalan sınıflandırılamayan yorumları "Kötü" olarak işaretler.
    """
    # Kötü (1-2 yıldız)
    data.loc[data['Normalized Stars'] <= 2, 'Star Group'] = 'Kötü'
    
    # İyi (4-5 yıldız)
    data.loc[data['Normalized Stars'] >= 4, 'Star Group'] = 'İyi'

    # Pozitif ve negatif anahtar kelimeleri çıkar
    positive_keywords = extract_keywords(data, 'İyi', top_n=20)
    negative_keywords = extract_keywords(data, 'Kötü', top_n=20)
    
    print(f"Pozitif Anahtar Kelimeler: {positive_keywords}")
    print(f"Negatif Anahtar Kelimeler: {negative_keywords}")

    # Nötr (3 yıldız) yorumları sınıflandır
    def assign_neutral_group(comment):
        if any(word in comment for word in positive_keywords):
            return 'İyi'
        elif any(word in comment for word in negative_keywords):
            return 'Kötü'
        else:
            return None  # Karar verilemeyen yorumlar için
    
    data.loc[data['Normalized Stars'] == 3, 'Star Group'] = data[data['Normalized Stars'] == 3]['Cleaned Comment'].apply(assign_neutral_group)

    # Boş kalanları (sınıflandırılamayanları) "Kötü" olarak ata
    data['Star Group'] = data['Star Group'].fillna('Kötü')
    
    return data


def plot_star_group_pie(data):
    """
    Yıldız gruplarını pasta grafiği olarak gösterir.
    """
    # Yıldız gruplarını hesapla
    star_group_counts = data['Star Group'].value_counts()
    labels = star_group_counts.index
    sizes = star_group_counts.values
    colors = ['red', 'blue']
    
    # Pasta grafiği çiz
    plt.figure(figsize=(7, 7))
    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
    plt.title("Yıldız Grupları Dağılımı")
    plt.show()
    
# 'Kötü' ve 'İyi' grupları için en yüksek 10 TF-IDF skoru
def plot_top_tfidf_scores(tfidf_results, group, top_n=10):
    scores = tfidf_results[group]
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:top_n]
    features, values = zip(*sorted_scores)
    
    plt.figure(figsize=(10, 6))
    plt.barh(features, values, color='red' if group == 'Kötü' else 'blue')
    plt.xlabel("TF-IDF Skoru")
    plt.ylabel("n-gram")
    plt.title(f"{group} Yorumları İçin En Yüksek {top_n} TF-IDF Skoru")
    plt.gca().invert_yaxis()  # Yatay grafiği ters çevir
    plt.show()

if __name__ == "__main__":
 # 1. Veri yükleme ve birleştirme
    combine_filtered_groups(
    filtered_comments_prefix="Filtered_Comments",  # Filtered Comments dosya grubu
    filtered_keywords_prefix="Filtered_By_Keywords",  # Filtered By Keywords dosya grubu
    output_path="Combined_Filtered_All.xlsx"  # Çıktı dosyası
)
    # Birleştirilmiş veriyi yükle
    data = pd.read_excel("Combined_Filtered_All.xlsx")

 # Eksik ve boş yorumları temizle
    data = data.dropna(subset=['Cleaned Comment'])
    data = data[data['Cleaned Comment'].str.strip() != ""]


    # Nötr yorumları otomatik sınıflandır ve yıldız gruplarını oluştur
    data = group_stars(data)
    
    # Güncellenmiş grupları kontrol et
    print(data['Star Group'].value_counts())

    # Sonuçları kaydet
    output_file = "Star_Group_Updated.xlsx"
    data.to_excel(output_file, index=False)
    print(f"Sonuçlar {output_file} dosyasına kaydedildi.")
    
    # TF-IDF analizi
    tfidf_results = tfidf_by_star_group_with_2_classes(data)  # Yıldız gruplarına dayalı TF-IDF
    print("TF-IDF Sonuçları:")
    print("Kötü Yorumlar:", list(tfidf_results['Kötü'].items())[:10])
    print("İyi Yorumlar:", list(tfidf_results['İyi'].items())[:10])

    # 'Kötü' ve 'İyi' gruplarını görselleştir
    plot_top_tfidf_scores(tfidf_results, 'Kötü')
    plot_top_tfidf_scores(tfidf_results, 'İyi')
    
    # #görselleştirme
    # plt.figure(figsize=(10, 5))
    # data['Star Group'].value_counts().plot(kind='bar', color=['red', 'blue'])
    # plt.title("Yıldız Grupları")
    # plt.ylabel("Yorum Sayısı")
    # plt.show()
    
    
    # Pasta grafiği çiz
    plot_star_group_pie(data)
