# -*- coding: utf-8 -*-
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
import sys
from imblearn.over_sampling import SMOTE
import pandas as pd
from sklearn.metrics import classification_report
from lightgbm import LGBMClassifier
from star_analysis import tfidf_by_star_group_with_2_classes
from star_analysis import group_stars
import joblib
# Konsol kodlamasını kontrol et ve gerekirse UTF-8 olarak ayarla
if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

def add_ngram_scores(data, positive_ngrams, negative_ngrams):
    # Pozitif n-gram skorları
    data["Positive N-gram Score"] = data["Cleaned Comment"].apply(
        lambda x: sum([positive_ngrams.get(word, 0) for word in x.split()])
    )
    # Negatif n-gram skorları
    data["Negative N-gram Score"] = data["Cleaned Comment"].apply(
        lambda x: sum([negative_ngrams.get(word, 0) for word in x.split()])
    )
    return data

# 3. TF-IDF ile Veriyi Vektörleştirme
def vectorize_data(X_train, X_val, X_test):
    vectorizer = TfidfVectorizer(max_features=5000, ngram_range=(1, 2))
    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_val_tfidf = vectorizer.transform(X_val)
    X_test_tfidf = vectorizer.transform(X_test)
    print(f"TF-IDF vektör boyutu: {X_train_tfidf.shape}")
    return X_train_tfidf, X_val_tfidf, X_test_tfidf, vectorizer


#     return model
def train_and_evaluate_model(X_train, X_val, y_train, y_val):
    # LightGBM modelini tanımla
    model = LGBMClassifier(
        objective='binary',  # Artık binary sınıflandırma
        metric='binary_logloss',
        boosting_type='gbdt',
        num_leaves=31,
        learning_rate=0.05,
        feature_fraction=0.9,
        random_state=42
    )

    # Modeli eğit
    model.fit(X_train, y_train, eval_set=[(X_val, y_val)], eval_metric='logloss')

    # Doğrulama setinde tahmin yap
    y_val_pred = model.predict(X_val)

    # Performans değerlendirmesi
    print("Doğrulama Seti Performansı:")
    print(classification_report(y_val, y_val_pred, target_names=['Kötü', 'İyi']))

    return model

# 5. Test Performansı
def evaluate_test_set(model, X_test_tfidf, y_test):
    y_test_pred = model.predict(X_test_tfidf)
    print("Test Seti Performansı:")
    print(classification_report(y_test, y_test_pred))

def split_and_balance_data(data):
    X = data['Cleaned Comment']  # Girdi (yorum metni)
    y = data['Star Group']  # Çıkış (etiket: İyi, Kötü)

    # Eğitim, doğrulama ve test setlerini böl
    X_train, X_temp, y_train, y_temp = train_test_split(
        X, y, test_size=0.4, random_state=42, stratify=y
    )
    X_val, X_test, y_val, y_test = train_test_split(
        X_temp, y_temp, test_size=0.5, random_state=42, stratify=y_temp
    )

    # TF-IDF vektörleştirme
    vectorizer = TfidfVectorizer(max_features=5000, ngram_range=(1, 2))
    X_train_tfidf = vectorizer.fit_transform(X_train)  # TF-IDF eğitim setine uygulanır
    X_val_tfidf = vectorizer.transform(X_val)  # Doğrulama setine TF-IDF dönüştürme
    X_test_tfidf = vectorizer.transform(X_test)  # Test setine TF-IDF dönüştürme

    # SMOTE sadece eğitim setine uygulanır
    smote = SMOTE(random_state=42)
    X_train_tfidf_smote, y_train_smote = smote.fit_resample(X_train_tfidf, y_train)

    # Eğitim, doğrulama ve test veri boyutlarını yazdır
    print(f"SMOTE sonrası eğitim veri boyutu: {X_train_tfidf_smote.shape[0]}")
    print(f"Eğitim verisi: {X_train_tfidf.shape[0]} satır")
    print(f"Doğrulama verisi: {X_val_tfidf.shape[0]} satır")
    print(f"Test verisi: {X_test_tfidf.shape[0]} satır")

    # Verileri döndür
    return X_train_tfidf_smote, X_val_tfidf, X_test_tfidf, y_train_smote, y_val, y_test, vectorizer

# Ana Fonksiyon
if __name__ == "__main__":
 # Veri yükleme
    input_file = "Star_Group_Updated.xlsx"  # Düzenlenen yıldız grupları dosyası
    data = pd.read_excel(input_file)

    # Eksik ve boş değerleri temizle
    data = data.dropna(subset=['Cleaned Comment', 'Star Group'])
    data = data[data["Cleaned Comment"].str.strip() != ""]

    # 2. Yıldız gruplarını ekle
    data = group_stars(data)  # Yıldızları 3 kategoriye ayırın
    print(data.head())  # Veri kontrolü için ilk birkaç satırı yazdırın
    # Etiketleri kategorik hale getirin
    data['Star Group'] = data['Star Group'].astype('category').cat.codes

    # TF-IDF analizi
    tfidf_results = tfidf_by_star_group_with_2_classes(data)  # Yıldız gruplarına dayalı TF-IDF
    print("TF-IDF Sonuçları:")
    print("Kötü Yorumlar:", list(tfidf_results['Kötü'].items())[:10])
    print("İyi Yorumlar:", list(tfidf_results['İyi'].items())[:10])

    # N-gram skorlarını ekle
    positive_ngrams = tfidf_results['İyi']
    negative_ngrams = tfidf_results['Kötü']
    data = add_ngram_scores(data, positive_ngrams, negative_ngrams)


    # Veriyi böl ve SMOTE uygula
    X_train, X_val, X_test, y_train, y_val, y_test, vectorizer = split_and_balance_data(data)


    # Modeli eğit ve değerlendir
    model = train_and_evaluate_model(X_train, X_val, y_train, y_val)

    # Test seti üzerinde değerlendirme
    y_test_pred = model.predict(X_test)
    print("Test Seti Performansı:")
    print(classification_report(y_test, y_test_pred, target_names=['Kötü', 'İyi']))

    # Eğitim seti için tahmin yap
    y_train_pred = model.predict(X_train)

    # Eğitim seti performansını değerlendirme
    train_report = classification_report(y_train, y_train_pred, target_names=['Kötü', 'İyi'])
    print("Eğitim Seti Performansı:")
    print(train_report)
    # # Modeli eğit ve değerlendir
    # model = train_and_evaluate_model(X_train, X_val, y_train, y_val)

    # # Test seti üzerinde değerlendirme
    # y_test_pred = model.predict(X_test)
    # print("Test Seti Performansı:")
    # print(classification_report(y_test, y_test_pred, target_names=['Kötü', 'İyi']))

    # # Modeli kaydet
    # joblib.dump(model, "trained_model.pkl")
    # print("Model başarıyla trained_model.pkl dosyasına kaydedildi.")
    
    # # TF-IDF vektörleştiriciyi kaydet
    # joblib.dump(vectorizer, "tfidf_vectorizer.pkl")
    # print("TF-IDF vektörleştirici başarıyla tfidf_vectorizer.pkl dosyasına kaydedildi.")
    