# -*- coding: utf-8 -*-
import subprocess
import tkinter as tk
import os
import joblib
import pandas as pd
from multiprocessing import Pool, cpu_count # multiprocessing modülünden Pool ve cpu_count fonksiyonlarını içe aktar
from functools import partial
import sys
import warnings
import matplotlib.pyplot as plt
import tkinter as tk
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer
from multiprocessing import Pool

# Tüm uyarıları kapat
warnings.filterwarnings("ignore")

# Konsol kodlamasını kontrol et ve gerekirse UTF-8 olarak ayarla
if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

def load_model_and_vectorizer():
    # Kaydedilmiş model ve vektörleştiriciyi yükle
    model = joblib.load("trained_model.pkl")
    vectorizer = joblib.load("tfidf_vectorizer.pkl")
    # Örnek bir yorumla test et
    example_comment = "Bu ürün harika!"
    example_tfidf = vectorizer.transform([example_comment])
    print("Model tahmini:", model.predict(example_tfidf))
    print("Model ve vektörleştirici başarıyla yüklendi.")
    return model, vectorizer

def predict_satisfaction(comment, model, vectorizer):
    comment_tfidf = vectorizer.transform([comment])
    return model.predict(comment_tfidf)[0]

def process_comments_in_parallel(comments, model, vectorizer):
    partial_predict = partial(predict_satisfaction, model=model, vectorizer=vectorizer) 
    
    with Pool(cpu_count()) as pool: 
        results = pool.map(partial_predict, comments)
    return results

def run_script(script_name, *args):
    """
    Belirtilen scripti çalıştırır ve argümanları geçirir.
    """
    try:
        subprocess.run(["python", script_name, *args], check=True)
        print(f"{script_name} başarıyla çalıştırıldı.")
    except subprocess.CalledProcessError as e:
        print(f"Hata: {script_name} çalıştırılamadı. {e}")

def main():
    # Tkinter ile bir giriş penceresi oluştur
    root = tk.Tk()
    root.withdraw()  # Ana pencereyi gizle

    # collect_comments.py'yi URL ile çalıştır
    print("Yorumlar toplanıyor...")
    run_script("collect_comments.py")

    # process_comments.py'yi çalıştır
    print("Yorumlar temizleniyor...")
    run_script("process_comments.py")

    # product_analysis.py'yi çalıştır
    print("Ürün analizi yapılıyor...")
    run_script("product_analysis.py")

    # star_analysis.py'yi çalıştır
    print("Yıldız grupları belirleniyor...")
    run_script("staranalysis_for_one.py")

    output_file = "Star_Group_Updated.xlsx"
    if os.path.exists(output_file):
        print(f"Temizlenmiş veriler {output_file} dosyasına kaydedildi.")
    else:
        print("Sonuç dosyası bulunamadı. Lütfen işlemleri kontrol edin.")
        
def calculate_percentage(data, column_name, label):
    """
    Belirli bir sütundaki belirli bir etiketin yüzdesini hesaplar.
    """
    total = len(data)
    count = len(data[data[column_name] == label])
    percentage = (count / total) * 100
    return percentage

def calculate_model_accuracy(data):
    """
    Modelin tahmin doğruluğunu ve yanlış tahminleri hesaplar.
    """
    incorrect_predictions = (data['Tahmin'] != data['Star Group']).sum()  # Yanlış tahmin sayısı
    total_comments = len(data)
    accuracy = (1 - incorrect_predictions / total_comments) * 100  # Doğruluk yüzdesi
    incorrect_percentage = incorrect_predictions / total_comments * 100  # Yanlış tahmin yüzdesi

    return incorrect_predictions, accuracy, incorrect_percentage


def plot_comparison_with_misclassification(
    star_group_percentage, model_prediction_percentage, incorrect_predictions, total_comments
):
    """
    Yıldız gruplarıyla model tahminlerini karşılaştıran bir grafik çizer ve yanlış tahminleri ekler.
    """
    labels = ['İyi', 'Kötü']
    x = range(len(labels))

    fig, ax = plt.subplots(figsize=(8, 6))
    bar1 = ax.bar(x, star_group_percentage, width=0.4, label='Gerçek Yıldız Grupları')
    bar2 = ax.bar([p + 0.4 for p in x], model_prediction_percentage, width=0.4, label='Model Tahminleri')

    # Çubukların üzerine yüzdeleri ekle
    for bar in bar1 + bar2:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, height, f'{height:.1f}%', ha='center', va='bottom')

    # Yanlış tahmin yüzdesini göster
    ax.text(
        0.5,
        -10,  # Grafiğin altına yazdır
        f"Yanlış Tahminler: {incorrect_predictions} yorum (%{(incorrect_predictions / total_comments * 100):.1f})",
        ha='center',
        va='top',
        fontsize=12,
        color='red'
    )
    ax.set_title('Yıldız Grupları ile Model Tahmin Karşılaştırması')
    ax.set_xticks([p + 0.2 for p in x])
    ax.set_xticklabels(labels)
    ax.set_ylabel('Yüzde (%)')
    ax.legend()

    plt.tight_layout()
    plt.show()


def plot_pie_chart(frame, positive_percentage, negative_percentage):
    """
    Tkinter çerçevesine pasta grafiği çizen fonksiyon.
    """
    labels = ['Pozitif Yorumlar', 'Negatif Yorumlar']
    sizes = [positive_percentage, negative_percentage]
    colors = ['lightblue', 'lightcoral']
    explode = (0.1, 0)

    fig, ax = plt.subplots(figsize=(4, 4))
    ax.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
    ax.set_title("Yorumların Dağılımı")

    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack()


turkish_stopwords = [
    "bir", "ve", "bu", "de", "da", "için", "ile", "mi", "mı", "ya", "daha",
    "çok", "az", "çok", "en", "gibi", "kadar", "ne", "niçin", "o", "ki", 
    "şu", "sanki", "ise", "her", "hiç", "bazı", "çünkü", "ancak", "göre"
]

def extract_ngram_samples(data, label, n=2):
    """
    Pozitif veya negatif yorumlardan belirli n-gram örnekleri çıkarır.
    """
    subset = data[data['Tahmin'] == label]['Original Comment']
    vectorizer = CountVectorizer(ngram_range=(n, n), stop_words=turkish_stopwords)
    ngram_counts = vectorizer.fit_transform(subset)
    ngram_sums = ngram_counts.sum(axis=0)
    ngram_frequencies = [(word, ngram_sums[0, idx]) for word, idx in vectorizer.vocabulary_.items()]
    sorted_ngrams = sorted(ngram_frequencies, key=lambda x: x[1], reverse=True)
    return [ngram[0] for ngram in sorted_ngrams[:2]]  # İlk iki n-gramı döndür

def create_interface(data):
    """
    Tkinter arayüzü oluşturan fonksiyon.
    """
    positive_comments = data[data['Tahmin'] == "İyi"]
    negative_comments = data[data['Tahmin'] == "Kötü"]

    # Pozitif ve negatif yüzdeyi hesapla
    positive_percentage = (len(positive_comments) / len(data)) * 100
    negative_percentage = (len(negative_comments) / len(data)) * 100

    # İyi ve kötü yorumlardan n-gram örnekleri
    positive_ngrams = extract_ngram_samples(data, 'İyi', n=2)
    negative_ngrams = extract_ngram_samples(data, 'Kötü', n=2)

    # Arayüz
    root = tk.Tk()
    root.title("Ürün Analizi")

    frame = tk.Frame(root)
    frame.pack(padx=10, pady=10)

    summary_label = tk.Label(
        frame,
        text=(
            "Ürün yorumları analiz edildiğinde, kullanıcıların genel olarak şu konularda memnun olduğu görülmüştür:\n"
            f"{', '.join([f'\"{ngram}\"' for ngram in positive_ngrams])}.\n\n"
            "Ancak, bazı kullanıcılar aşağıdaki konulardan şikayetçi olmuştur:\n"
            f"{', '.join([f'\"{ngram}\"' for ngram in negative_ngrams])}.\n\n"
            f"Genel Değerlendirme: Kullanıcıların %{positive_percentage:.1f}'i ürünü olumlu değerlendirirken, "
            f"%{negative_percentage:.1f}'si olumsuz bulmuştur."
        ),
        font=("Arial", 12),
        justify="left",  # Metni sola yaslamak için
    )

    summary_label.pack()

    plot_pie_chart(frame, positive_percentage, negative_percentage)
    root.mainloop()


if __name__ == "__main__":
    main()
    # Model ve vektörleştiriciyi yükle
    model, vectorizer = load_model_and_vectorizer()

    # Test için örnek yorumlar
    input_file = "Star_Group_Updated.xlsx" # Yeni yorumlar içeren dosya
    data = pd.read_excel(input_file)
    # NaN değerlerini temizle
    data = data.dropna(subset=['Cleaned Comment'])
    comments = data['Cleaned Comment'].tolist()

    # Veriyi kontrol et
    print("Cleaned Comment sütun kontrolü:")
    print(data['Cleaned Comment'].head())

    # Eksik verileri kaldır
    data = data.dropna(subset=['Cleaned Comment'])
    comments_list = data['Cleaned Comment'].tolist()

    predictions = process_comments_in_parallel(comments, model, vectorizer)
    print(predictions)  # predictions listesini kontrol et

    # Tahminlerin doğru şekilde aktarıldığını kontrol edin
    print("Tahmin edilen sonuçlar:", predictions)
    data['Tahmin'] = predictions
    
    print(data[['Cleaned Comment', 'Tahmin']].head())  # Tahmin sütununu kontrol edin

    # Çıktıyı kaydet
    output_file = "PredictedSatisfaction_with_Probabilities.xlsx"
    data.to_excel(output_file, index=False)
    print(f"Tahminler tamamlandı. Sonuçlar {output_file} dosyasına kaydedildi.")
    
    # Yanlış tahminleri ve doğruluğu hesaplayın
    incorrect_predictions, accuracy, incorrect_percentage = calculate_model_accuracy(data)

    # Sonuçları yazdırın
    print(f"Yanlış Tahmin Edilen Yorumlar: {incorrect_predictions}")
    print(f"Modelin Doğruluk Yüzdesi: %{accuracy:.2f}")
    print(f"Yanlış Tahmin Yüzdesi: %{incorrect_percentage:.2f}")

    # Yüzde değerlerini al
    star_group_percentage = [
        (data['Star Group'] == 'İyi').sum() / len(data) * 100,
        (data['Star Group'] == 'Kötü').sum() / len(data) * 100
    ]
    model_prediction_percentage = [
        (data['Tahmin'] == 'İyi').sum() / len(data) * 100,
        (data['Tahmin'] == 'Kötü').sum() / len(data) * 100
    ]

    # Grafiği çiz
    plot_comparison_with_misclassification(
        star_group_percentage,
        model_prediction_percentage,
        incorrect_predictions,
        len(data)
    )

    print("kullanıcı dostu arayüüz oluşturuluyor...")
    create_interface(data)


