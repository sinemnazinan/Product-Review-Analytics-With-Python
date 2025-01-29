# -*- coding: utf-8 -*-
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import matplotlib.pyplot as plt
import sys

# Konsol kodlamasını kontrol et ve gerekirse UTF-8 olarak ayarla
if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
    
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
    vectorizer = TfidfVectorizer(ngram_range=(2, 3), max_features=500)

    # Her grup için TF-IDF hesaplama
    bad_tfidf = vectorizer.fit_transform(bad_comments)

    good_tfidf = vectorizer.fit_transform(good_comments)

    # Skorları çıkarma
    bad_features = vectorizer.get_feature_names_out()
    
    good_features = vectorizer.get_feature_names_out()

    bad_scores = bad_tfidf.toarray().mean(axis=0)
    
    good_scores = good_tfidf.toarray().mean(axis=0)

    return {
        'Kötü': dict(zip(bad_features, bad_scores)),
        'İyi': dict(zip(good_features, good_scores))
    }

def extract_keywords(data, group, top_n=20):
    """
    Belirtilen grup için en yüksek TF-IDF skoruna sahip n-gram'ları çıkarır.
    """
    vectorizer = TfidfVectorizer(max_features=5000, ngram_range=(1, 2))
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

def visualize_top_ngrams(data, star_group, n=20):
    """
    Belirli bir yıldız grubu için en sık geçen n-gram'ları görselleştirir.
    """
    # Yıldız grubuna göre yorumları filtrele
    group_data = data[data['Star Group'] == star_group]
    
    # TF-IDF ile n-gram skorlarını hesapla
    vectorizer = TfidfVectorizer(max_features=5000, ngram_range=(2, 3))
    tfidf_matrix = vectorizer.fit_transform(group_data['Cleaned Comment'])
    feature_names = vectorizer.get_feature_names_out()
    tfidf_scores = tfidf_matrix.sum(axis=0).A1

    # En yüksek skorları sırala
    sorted_indices = tfidf_scores.argsort()[::-1]
    top_features = [feature_names[i] for i in sorted_indices[:n]]
    top_scores = [tfidf_scores[i] for i in sorted_indices[:n]]

    # Görselleştirme
    plt.figure(figsize=(12, 6))
    plt.bar(top_features, top_scores, color='skyblue')
    plt.title(f"{star_group} Yorumlar İçin En Sık N-Gramlar")
    plt.xticks(rotation=45, ha="right")
    plt.ylabel("TF-IDF Skoru")
    plt.show()
    
import matplotlib.pyplot as plt

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

if __name__ == "__main__":
    # Birleştirilmiş veriyi yükle
    data = pd.read_excel("Filtered_Comments.xlsx")

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
    
    # #görselleştirme
    # plt.figure(figsize=(10, 5))
    # data['Star Group'].value_counts().plot(kind='bar', color=['red', 'blue', 'green'])
    # plt.title("Yıldız Grupları")
    # plt.ylabel("Yorum Sayısı")
    # plt.show()

# # İyi ve kötü yorumlar için n-gram görselleştirmesi yap
#     print("\n=== İyi Yorumlar İçin N-Gram Görselleştirme ===")
#     visualize_top_ngrams(data, 'İyi', n=20)

#     print("\n=== Kötü Yorumlar İçin N-Gram Görselleştirme ===")
#     visualize_top_ngrams(data, 'Kötü', n=20)

    # Pasta grafiği çiz
    plot_star_group_pie(data)