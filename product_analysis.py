# -*- coding: utf-8 -*-
import sys
import pandas as pd
import re
from jpype import startJVM, shutdownJVM, JClass
# N-gram Analizi
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
import matplotlib.pyplot as plt
from collections import Counter

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
        
# Processed Comment sütunundan kök kelimeleri çıkarmak için fonksiyon
def extract_roots_safely(processed_comment):
    """
    Processed Comment sütunundan sadece kök kelimeleri çıkartır.
    """
    try:
        if isinstance(processed_comment, str):  # Metinse işlem yap
            roots = re.findall(r'\[([^\]:]+):', processed_comment)  # Zemberek formatı: [kelime:TÜR]
            
            return ' '.join(roots)
        return None
    except Exception as e:
        print(f"Hata oluştu: {e}")
        return None

# "UNK" ve 2 harften kısa kelimeleri temizleyen fonksiyon
def clean_text_advanced(text):
    """
    UNK kelimesini ve 2 harften kısa kelimeleri metinden siler.
    Boşlukları temizler ve yorum tamamen boşsa None döner.
    """
    try:
        if isinstance(text, str):
            # UNK'yi kaldır
            cleaned_text = re.sub(r'\bUNK\b', '', text)
            # 2 harf veya daha kısa kelimeleri kaldır
            cleaned_text = re.sub(r'\b\w{1,2}\b', '', cleaned_text)
            # Fazla boşlukları temizle
            cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()
            # Eğer temizlenmiş yorum boşsa None döner
            return cleaned_text if cleaned_text else None
        return None
    except Exception as e:
        print(f"Temizleme sırasında hata oluştu: {e}")
        return None
    
def extract_verbs_from_comments(data, text_column="Original Comment"):
    """
    Yorumlardan en sık kullanılan fiilleri çıkarır.
    """
    all_verbs = []
    for comment in data[text_column].dropna():
        words = comment.split()
        for word in words:
            analysis = morphology.analyze(word)
            if not analysis:
                continue
            for result in analysis:
                if ":FIIL" in str(result):  # Zemberek ile fiil kontrolü
                    all_verbs.append(word)
    return Counter(all_verbs)

def filter_ngrams_with_stopwords(ngrams, stopword_list):
    """
    Stopword'lere dayalı olarak n-gram'ları temizler.
    """
    filtered_ngrams = {ngram: score for ngram, score in ngrams.items() if not any(word in stopword_list for word in ngram.split())}
    return filtered_ngrams

def filter_comments_by_keywords(data, keywords):
    """
    Belirtilen anahtar kelimelerden herhangi birine sahip olan yorumları filtreler.
    """

    # Cleaned Comment sütununu metin türüne çevir
    data["Cleaned Comment"] = data["Cleaned Comment"].astype(str)

    # Anahtar kelimelerle yorumların eşleştiğini kontrol eden fonksiyon
    def contains_keywords(text, keywords):
        for keyword in keywords:
            if keyword in text:
                return True
        return False

    # Yorumları filtrele
    filtered_data = data[data["Cleaned Comment"].apply(lambda comment: contains_keywords(comment, keywords))]
    return filtered_data


if __name__ == "__main__":
    # Giriş ve çıkış dosya yolları
    input_excel_path = "ProcessedComments.xlsx"   # Önceki dosya (işlenmiş yorumlar var)
    output_excel_path = "CleanedComments.xlsx"   # Yeni dosya (temizlenmiş yorumlar)

    # Veriyi yükleme
    data = pd.read_excel(input_excel_path)

    # Kök kelimeleri çıkarma
    data['Cleaned Comment'] = data['Processed Comment'].apply(extract_roots_safely)
    stopword_list = [
        "etmek", "olmak", "yapmak", "gelmek", "gitmek", "göndermek", "demek",
        "almak", "vermek", "beklemek", "kullanmak", "yollamak", "hem", "amma", "insan", "ürün", "çok"
    ]
    
    # Fiilleri çıkarın ve en sık geçenleri belirleyin
    verb_counts = extract_verbs_from_comments(data)
    most_common_verbs = [verb for verb, _ in verb_counts.most_common(20)]
    stopword_list += most_common_verbs
    print(f"En sık geçen fiiller: {most_common_verbs}")

    # Temizlenmiş yorumları sadece yeni dosyaya kaydedelim
    cleaned_data = data[['Original Comment', 'Cleaned Comment', 'Normalized Stars']]

    # Yeni dosyayı kaydet
    cleaned_data.to_excel(output_excel_path, index=False)
    print(f"Temizlenmiş veriler başarıyla '{output_excel_path}' dosyasına kaydedildi.")

    # Dosya yolları
    input_file = "CleanedComments.xlsx"
    output_file = "CleanedComments_NoUNK.xlsx"

    # Excel verisini yükle
    data2 = pd.read_excel(input_file)

    # "Cleaned Comment" sütununda UNK'leri temizle
    data2['Cleaned Comment'] = data2['Cleaned Comment'].apply(clean_text_advanced)

    # Tamamen boş kalan yorumları sil
    data2 = data2.dropna(subset=['Cleaned Comment'])

    # Temizlenmiş veriyi yeni bir dosyaya kaydet
    data2.to_excel(output_file, index=False)
    print(f"'UNK' temizlenmiş veriler başarıyla '{output_file}' dosyasına kaydedildi.")
    
    
    # TF-IDF ile n-gram analizi yapın
    vectorizer = TfidfVectorizer(ngram_range=(2, 3), max_features=500)
    tfidf_matrix = vectorizer.fit_transform(data2["Cleaned Comment"].dropna())
    ngrams = vectorizer.get_feature_names_out()
    scores = tfidf_matrix.sum(axis=0).A1
    ngram_scores = {ngram: score for ngram, score in zip(ngrams, scores)}

    # Stopword listesi ile n-gram'ları filtreleyin
    filtered_ngrams = filter_ngrams_with_stopwords(ngram_scores, stopword_list)
    print(f"Filtrelenmiş n-gram sayısı: {len(filtered_ngrams)}")
    
    # Stopword listesi ile Processed Comment'leri filtrele
    data2["Cleaned Comment"] = data2["Cleaned Comment"].apply(
        lambda comment: ' '.join(
            [ngram for ngram in comment.split() if not any(word in stopword_list for word in ngram.split())]
        )
    )

    # Yeni dosyayı kaydet
    final_output_path = "Filtered_Comments.xlsx"
    data = data.dropna(subset=["Cleaned Comment"])
    data2.to_excel(final_output_path, index=False)
    print(f"Filtrelenmiş yorumlar başarıyla '{final_output_path}' dosyasına kaydedildi.")
    # Keywords'lerin n-gram'larda olup olmadığını kontrol edin
    vectorizer = CountVectorizer(ngram_range=(1, 3), stop_words=None)
    X = vectorizer.fit_transform(data["Processed Comment"])
    ngrams = vectorizer.get_feature_names_out()

    # En anlamlı n-gram'ları görselleştirin
    top_ngrams = dict(sorted(filtered_ngrams.items(), key=lambda x: x[1], reverse=True)[:20])
    plt.figure(figsize=(15, 7))
    plt.subplots_adjust(bottom=0.25)
    plt.bar(top_ngrams.keys(), top_ngrams.values(), color="skyblue")
    plt.xticks(rotation=45)
    plt.title("Filtrelenmiş N-Gramlar")
    plt.ylabel("TF-IDF Skoru")
    plt.show()

    # JVM'i kapat
    shutdownJVM()