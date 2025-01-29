# 📌 Ürün Değerlendirme Analitiği - Detaylı Açıklama

## 🚀 Giriş

Bu proje, çevrimiçi platformlarda kullanıcılar tarafından bırakılan ürün yorumlarını analiz ederek, tüketici memnuniyetine
dair daha derin içgörüler elde etmeyi amaçlamaktadır. Günümüzde dijitalleşmenin etkisiyle kullanıcı deneyimleri ve yorumları,
tüketici davranışlarını anlamada ve işletmelerin stratejik kararlar alabilmesinde kritik bir rol oynamaktadır. Bu bağlamda,
**doğal dil işleme (NLP) ve makine öğrenimi** tekniklerinden faydalanılarak, büyük veri setlerinden anlamlı bilgilerin çıkarılması hedeflenmiştir.
Proje süreci, veri toplama, işleme, analiz ve analiz sonucu model geliştirme aşamalarından oluşmaktadır. Bu süreçte, çevrimiçi
platformlardan toplanan kullanıcı yorumları, **Zemberek dil işleme modülü ve Python tabanlı kütüphaneler** aracılığıyla temizlenmiş
ve işlenmiştir. Ayrıca, projede kullanılan ileri düzey makine öğrenimi algoritmaları, yorumların yıldız derecelendirmeleriyle
olan ilişkisini analiz ederek ürün geliştirme süreçlerine ışık tutmayı mümkün kılmıştır.

Proje, aşağıdaki temel adımlardan oluşmaktadır:

1. **Yorumların Toplanması** 🛒
2. **Metin Temizleme ve İşleme** 🧹
3. **NLP ve N-Gram Analizi** 📊
4. **Makine Öğrenmesi Modeli Eğitimi** 🤖
5. **Yorumların Sınıflandırılması ve Analizi** 📈
6. **Sonuçların Görselleştirilmesi Ve Yeni Ürünler Üstünde Çalışmaya Hazır Hale Gelmesi** 🖼️

---

## ⚡ Özellikler

✅ **Otomatik Yorum Toplama**: Selenium kullanarak Trendyol gibi e-ticaret sitelerinden yorumlar toplanır.  
✅ **Metin İşleme ve Temizleme**: NLP algoritmaları ve Zemberek kullanılarak metinler analiz edilir.  
✅ **Duygu Analizi**: Yorumlar olumlu veya olumsuz olarak sınıflandırılır.  
✅ **N-Gram Analizi**: En sık kullanılan kelimeler belirlenir.  
✅ **Makine Öğrenmesi Modeli**: LightGBM ile kullanıcı memnuniyetini tahmin eden bir model eğitilir.  
✅ **Paralel İşleme**: Büyük veri kümeleri için multiprocessing desteği sağlanır.  
✅ **Grafikler ve Görselleştirme**: Sonuçlar eğitilen model ile tahmin edilip pasta grafikleri, çubuk grafikler ve diğer görseller ile analiz edilir.

---

## 🔁 Çalışma Akışı

### 1️⃣ Yorumların Toplanması (`collect_comments.py`)

- **Amaç**: E-ticaret sitelerinden otomatik olarak yorumları çekmek.
- **Teknolojiler**: Selenium, Tkinter (Kullanıcıdan URL girişi almak için).
- **Çıktı**: `SynchronizedData.xlsx` dosyasına yorumlar ve yıldız dereceleri kaydedilir.

---

### 2️⃣ Metin Temizleme ve Ön İşleme (`process_comments.py`)

- **Amaç**: Yorumlardaki gereksiz kelimeleri, stopword'leri ve özel karakterleri temizlemek.
- **Teknolojiler**: Zemberek NLP, RegEx, Pandas.
- **Çıktı**: `ProcessedComments.xlsx` dosyası.

---

### 3️⃣ Ürün Analizi (`product_analysis.py`)

- **Amaç**: Yorumlardan en sık geçen kelimeleri (n-gramları) belirlemek ve temizlemek.
- **Teknolojiler**: TF-IDF, N-Gram Analizi, Zemberek.
- **Çıktı**: `CleanedComments.xlsx`.

---

### 4️⃣ Makine Öğrenmesi Model Eğitimi (`model_training.py`)

- **Amaç**: Yorumları memnuniyet sınıflarına ayıran bir model eğitmek.
- **Teknolojiler**: LightGBM, TF-IDF, SMOTE (dengesiz veriyi dengelemek için).
- **Çıktı**: `trained_model.pkl`, `tfidf_vectorizer.pkl`.

---

### 5️⃣ Görselleştirme ve Raporlama (`star_analysis.py`)

- **Amaç**: Yıldız gruplarını belirlemek, duygu analizini görselleştirmek.
- **Teknolojiler**: Matplotlib, TF-IDF.
- **Çıktı**: `Star_Group_Updated.xlsx`, grafikler.

---

### 6️⃣ Yorumların Tahmin Edilmesi (`multiprocessing_model.py`)

- **Amaç**: Yeni gelen yorumların sınıflandırılması ve paralel işlem desteği ile hızlandırılması.
- **Teknolojiler**: Python Multiprocessing, LightGBM.
- **Çıktı**: `PredictedSatisfaction_with_Probabilities.xlsx`.

---

## 📊 Kullanım Talimatları

### ⚡ Gerekli Kütüphaneler

# Web Scraping (Veri Toplama) için

pip install selenium webdriver-manager keyboard

# Veri İşleme ve Analiz için

pip install pandas numpy scikit-learn nltk zemberek-nlp jpype1

# Makine Öğrenmesi için

pip install lightgbm imbalanced-learn joblib

# Görselleştirme için

pip install matplotlib seaborn

# Paralel İşleme ve GUI için

pip install multiprocessing tkinter

### 🚀 Çalıştırma Adımları

```bash
# 1️⃣ Yorumları Topla
python collect_comments.py

# 2️⃣ Yorumları Temizle
python process_comments.py

# 3️⃣ Analiz Yap
python product_analysis.py

# 4️⃣ Modeli Eğit
python model_training.py

# 5️⃣ Görselleştirme
python star_analysis.py

# 6️⃣ Yorumları Tahmin Et
python multiprocessing_model.py
```

---

## 📈 Sonuçlar ve İçgörüler

✅ **Duygu Dağılımı**: Yorumların olumlu/olumsuz yüzdesi hesaplanır.  
✅ **N-Gram Analizi**: En sık geçen kelimeler bulunur ve görselleştirilir.  
✅ **Tahmin Başarı Oranı**: Modelin doğruluk ve hata oranı ölçülür.  
✅ **Kullanıcı Şikayetleri & Beğeniler**: Pozitif ve negatif geri bildirimler belirlenir.

---

## 🔗 Katkı & Gelecekteki Geliştirmeler

🛠 **Katkı Sağlayın**: Yeni özellikler eklemek için pull request gönderebilirsiniz.  
🚀 **Gelecekteki Geliştirmeler**:

- 📌 **Çok Dilli Destek**: İngilizce, Almanca vb. diller için NLP entegrasyonu.
- 📌 **Derin Öğrenme Modelleri**: LSTM, BERT gibi modeller ile analiz.
- 📌 **Etkileşimli Dashboard**: Kullanıcı dostu grafik arayüzleri.

---

## 📚 Kaynaklar

## 📚 Kaynaklar

1. [Tirendaz Akademi, Python NLTK ile Text Analizi | Duygu (Sentimental) Analizi | Doğal Dil İşleme](https://www.youtube.com/watch?v=pb1nG1Oge8I&list=PPSV)
2. [Real Python, Natural Language Processing With Python's NLTK Package](https://realpython.com/nltk-nlp-python/)
3. [Wikipedia, Natural Language Toolkit](https://en.wikipedia.org/wiki/Natural_Language_Toolkit)
4. [Pierian Training, Guide to NLTK – Natural Language Toolkit for Python](https://pieriantraining.com/guide-to-nltk-natural-language-toolkit-for-python/)
5. [NLTK, Extracting Information from Text](https://www.nltk.org/book/ch07.html)
6. [NLTK, Language Processing and Python](https://www.nltk.org/book/ch01.html)
7. Steven Bird, _NLTK Documentation_, Release 3.2.5 (Sep 28, 2017)
8. [Dragomir R. Radev, CPSC 477/577 Natural Language Processing](https://www.cs.yale.edu/homes/radev/nlp.html)
9. [Yale University, Natural Language Processing](https://cpsc.yale.edu/research/primary-areas/natural-language-processing)
10. [Duke CS, Natural Language Processing (NLP)](https://cs.duke.edu/research/natural-language-processing-nlp)
11. [Karel, Doğal Dil İşleme, NLP](https://www.karel.com.tr/blog/dogal-dil-isleme-nlp-natural-language-processing-nedir)
12. [İTÜ, Yapay Zeka ve Veri Mühendisliği, Doğal Dil İşleme](https://yapayzeka.itu.edu.tr/arastirma/dogal-dil-isleme)
13. [Marmara Üniversitesi, İletişim Fakültesi, Doğal Dil İşleme](https://nlpiletisim.marmara.edu.tr/)
14. [Docs, Beautiful Soup Documentation](https://beautiful-soup-4.readthedocs.io/en/latest/#)
15. [Crummy, Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/)
16. [Medium, Python ile Web Scraping: BeautifulSoup Kullanımı](https://furkancakmaker.medium.com/python-ile-web-scraping-beautifulsoup-kullan%C4%B1m%C4%B1-5f0a3d88f5)
17. [Wikipedia, Beautiful Soup (HTML parser)](<https://en.wikipedia.org/wiki/Beautiful_Soup_(HTML_parser)>)
18. [Veri Bilimi Okulu, Veri Kazıma Nedir Ve Neden Yapılır?](https://www.veribilimiokulu.com/veri-kazima-nedir-neden-yapilir/)
19. [CodiaSoft, Web Scraping Nedir?](https://www.codiasoft.com/blog/web-scraping-web-kazima-nedir-neden-yapilir/)
20. [CyberSkillsHub, Web Scraping Nedir?](https://cyberskillshub.com/web-scraping-nedir-nasil-yapilir/)
21. [Abdullah Baykal, Veri Madenciliği Uygulama Alanları](https://dergipark.org.tr/tr/download/article-file/787239)
22. [Bulutistan, Veri Madenciliği Nedir?](https://bulutistan.com/blog/veri-madenciligi-data-mining-nedir-nasil-yapilir/)
23. [Vizyoner Genç, Veri Madenciliği](https://vizyonergenc.com/icerik/5-temel-soruda-veri-madenciligi-data-mining-nedir)
24. [Bilgisayar Kavramları, Web Emeklemesi](https://bilgisayarkavramlari.com/2008/12/09/web-emeklemesi-web-crawling/)
25. [Current Works, Crawler Nedir?](https://currentworks.com.tr/crawler/)
26. [Weebim, Örümcek (Crawler) Nedir?](https://weebim.com/web-tasarim/orumcek-crawler-nedir-nasil-calisir/)
27. [Scrapy, Scrapy 2.11 Documentation](https://scrapy.org/)
28. [Edureka, Selenium Using Python](https://www.edureka.co/blog/selenium-using-python/)
29. [Siber Eğitmen, Selenium Nedir?](https://www.siberegitmen.com/selenium-nedir-ne-ise-yarar/)
30. [RealPython, Natural Language Processing With spaCy](https://realpython.com/natural-language-processing-spacy-python/)
31. [spaCy, spaCy 101](https://spacy.io/usage/spacy-101)
32. [Analytics Vidhya, Making NLP Easy with TextBlob](https://www.analyticsvidhya.com/blog/2021/10/making-natural-language-processing-easy-with-textblob/)
33. [Hugging Face, Transformers Documentation](https://huggingface.co/docs/transformers/)
34. [Deep Learning for NLP with PyTorch, Stanford University](https://cs230.stanford.edu/blog/nlp-with-pytorch)
35. [IEEE Xplore, Sentiment Analysis for Turkish Tweets](https://ieeexplore.ieee.org/document/9086809)

---

Bu README, projenin kapsamlı bir özetini ve kullanım talimatlarını içermektedir. Daha fazla bilgi için proje katkıcılarıyla iletişime geçebilirsiniz.

# 📌 Product Review Analytics - Detailed Description

## 🚀 Introduction

This project aims to analyze product reviews left by users on online platforms to gain deeper insights into consumer satisfaction. In today's digitalized world, user experiences and reviews play a critical role in understanding consumer behavior and enabling businesses to make strategic decisions. In this context, **natural language processing (NLP) and machine learning** techniques are utilized to extract meaningful information from large datasets. The project workflow consists of stages such as data collection, processing, analysis, and model development based on the analysis. In this process, user reviews collected from online platforms have been cleaned and processed using the **Zemberek NLP module and Python-based libraries**. Additionally, advanced machine learning algorithms used in the project made it possible to analyze the relationship between reviews and star ratings, shedding light on product development processes.

The project consists of the following key steps:

1. **Collecting Reviews** 🛒
2. **Text Cleaning and Processing** 🧹
3. **NLP and N-Gram Analysis** 📊
4. **Machine Learning Model Training** 🤖
5. **Classification and Analysis of Reviews** 📈
6. **Visualization of Results and Product Improvement** 🖼️

---

## ⚡ Features

✅ **Automated Review Collection**: Reviews are collected from e-commerce sites like Trendyol using Selenium.  
✅ **Text Processing and Cleaning**: Texts are analyzed using NLP algorithms and Zemberek.  
✅ **Sentiment Analysis**: Reviews are classified as positive or negative.  
✅ **N-Gram Analysis**: Most frequently used words are identified.  
✅ **Machine Learning Model**: A model predicting user satisfaction is trained using LightGBM.  
✅ **Parallel Processing**: Multiprocessing support is provided for large datasets.  
✅ **Graphs and Visualization**: Results are analyzed using pie charts, bar charts, and other visuals generated by the trained model.

---

## 🔁 Workflow

### 1️⃣ Collecting Reviews (`collect_comments.py`)

- **Purpose**: Automatically fetch reviews from e-commerce sites.
- **Technologies**: Selenium, Tkinter (for URL input from users).
- **Output**: Reviews and star ratings are saved in the `SynchronizedData.xlsx` file.

---

### 2️⃣ Text Cleaning and Preprocessing (`process_comments.py`)

- **Purpose**: Remove unnecessary words, stopwords, and special characters from reviews.
- **Technologies**: Zemberek NLP, RegEx, Pandas.
- **Output**: `ProcessedComments.xlsx` file.

---

### 3️⃣ Product Analysis (`product_analysis.py`)

- **Purpose**: Identify and clean the most frequently used words (n-grams) from reviews.
- **Technologies**: TF-IDF, N-Gram Analysis, Zemberek.
- **Output**: `CleanedComments.xlsx` file.

---

### 4️⃣ Machine Learning Model Training (`model_training.py`)

- **Purpose**: Train a model to classify reviews into satisfaction categories.
- **Technologies**: LightGBM, TF-IDF, SMOTE (to balance imbalanced data).
- **Output**: `trained_model.pkl`, `tfidf_vectorizer.pkl` files.

---

### 5️⃣ Visualization and Reporting (`star_analysis.py`)

- **Purpose**: Identify star groups and visualize sentiment analysis.
- **Technologies**: Matplotlib, TF-IDF.
- **Output**: `Star_Group_Updated.xlsx` file, graphs.

---

### 6️⃣ Predicting Reviews (`multiprocessing_model.py`)

- **Purpose**: Classify new incoming reviews and accelerate the process with parallel processing support.
- **Technologies**: Python Multiprocessing, LightGBM.
- **Output**: `PredictedSatisfaction_with_Probabilities.xlsx` file.

---

## 📊 Usage Instructions

### ⚡ Required Libraries

#### Web Scraping

```bash
pip install selenium webdriver-manager keyboard
```

#### Data Processing and Analysis

```bash
pip install pandas numpy scikit-learn nltk zemberek-nlp jpype1
```

#### Machine Learning

```bash
pip install lightgbm imbalanced-learn joblib
```

#### Visualization

```bash
pip install matplotlib seaborn
```

#### Parallel Processing and GUI

```bash
pip install multiprocessing tkinter
```

### 🚀 Execution Steps

```bash
# 1️⃣ Collect Reviews
python collect_comments.py

# 2️⃣ Clean Reviews
python process_comments.py

# 3️⃣ Perform Analysis
python product_analysis.py

# 4️⃣ Train Model
python model_training.py

# 5️⃣ Visualize Results
python star_analysis.py

# 6️⃣ Predict Reviews
python multiprocessing_model.py
```

---

## 📈 Results and Insights

✅ **Sentiment Distribution**: The percentage of positive/negative reviews is calculated.  
✅ **N-Gram Analysis**: Most frequently used words are identified and visualized.  
✅ **Prediction Accuracy**: The accuracy and error rate of the model are measured.  
✅ **User Complaints & Likes**: Positive and negative feedback is identified.

---

## 🔗 Contributions & Future Enhancements

🛠 **Contribute**: You can submit pull requests to add new features.  
🚀 **Future Enhancements**:

- 📌 **Multi-Language Support**: NLP integration for English, German, etc.
- 📌 **Deep Learning Models**: Analysis using models like LSTM, BERT.
- 📌 **Interactive Dashboard**: User-friendly graphical interfaces.

---

## 📚 References

1. [Tirendaz Akademi, Python NLTK ile Text Analizi | Sentiment Analysis | Natural Language Processing](https://www.youtube.com/watch?v=pb1nG1Oge8I&list=PPSV)
2. [Real Python, Natural Language Processing With Python's NLTK Package](https://realpython.com/nltk-nlp-python/)
3. [Wikipedia, Natural Language Toolkit](https://en.wikipedia.org/wiki/Natural_Language_Toolkit)
4. [Pierian Training, Guide to NLTK – Natural Language Toolkit for Python](https://pieriantraining.com/guide-to-nltk-natural-language-toolkit-for-python/)
5. [NLTK, Extracting Information from Text](https://www.nltk.org/book/ch07.html)
6. [NLTK, Language Processing and Python](https://www.nltk.org/book/ch01.html)
7. Steven Bird, _NLTK Documentation_, Release 3.2.5 (Sep 28, 2017)
8. [Dragomir R. Radev, CPSC 477/577 Natural Language Processing](https://www.cs.yale.edu/homes/radev/nlp.html)
9. [Yale University, Natural Language Processing](https://cpsc.yale.edu/research/primary-areas/natural-language-processing)
10. [Duke CS, Natural Language Processing (NLP)](https://cs.duke.edu/research/natural-language-processing-nlp)
11. [Karel, Natural Language Processing Overview](https://www.karel.com.tr/blog/dogal-dil-isleme-nlp-natural-language-processing-nedir)
12. [ITU, Artificial Intelligence and Data Engineering - NLP](https://yapayzeka.itu.edu.tr/arastirma/dogal-dil-isleme)
13. [Marmara University, NLP Research](https://nlpiletisim.marmara.edu.tr/)
14. [Beautiful Soup Documentation](https://beautiful-soup-4.readthedocs.io/en/latest/#)
15. [Crummy, Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/)
16. [Medium, Python ile Web Scraping: BeautifulSoup Kullanımı](https://furkancakmaker.medium.com/python-ile-web-scraping-beautifulsoup-kullan%C4%B1m%C4%B1-5f0a3d88f5)
17. [Wikipedia, Beautiful Soup (HTML parser)](<https://en.wikipedia.org/wiki/Beautiful_Soup_(HTML_parser)>)
18. [Veri Bilimi Okulu, Veri Kazıma Nedir Ve Neden Yapılır?](https://www.veribilimiokulu.com/veri-kazima-nedir-neden-yapilir/)
19. [CodiaSoft, Web Scraping Nedir?](https://www.codiasoft.com/blog/web-scraping-web-kazima-nedir-neden-yapilir/)
20. [CyberSkillsHub, Web Scraping Nedir?](https://cyberskillshub.com/web-scraping-nedir-nasil-yapilir/)
21. [Abdullah Baykal, Veri Madenciliği Uygulama Alanları](https://dergipark.org.tr/tr/download/article-file/787239)
22. [Bulutistan, Veri Madenciliği Nedir?](https://bulutistan.com/blog/veri-madenciligi-data-mining-nedir-nasil-yapilir/)
23. [Vizyoner Genç, Veri Madenciliği](https://vizyonergenc.com/icerik/5-temel-soruda-veri-madenciligi-data-mining-nedir)
24. [Bilgisayar Kavramları, Web Crawling](https://bilgisayarkavramlari.com/2008/12/09/web-emeklemesi-web-crawling/)
25. [Current Works, Crawler Overview](https://currentworks.com.tr/crawler/)
26. [Weebim, What is a Web Crawler?](https://weebim.com/web-tasarim/orumcek-crawler-nedir-nasil-calisir/)
27. [Scrapy, Documentation](https://scrapy.org/)
28. [Edureka, Selenium with Python](https://www.edureka.co/blog/selenium-using-python/)
29. [Siber Eğitmen, What is Selenium?](https://www.siberegitmen.com/selenium-nedir-ne-ise-yarar/)
30. [Real Python, Natural Language Processing With spaCy](https://realpython.com/natural-language-processing-spacy-python/)
31. [spaCy, Documentation](https://spacy.io/usage/spacy-101)
32. [Analytics Vidhya, Making NLP Easy with TextBlob](https://www.analyticsvidhya.com/blog/2021/10/making-natural-language-processing-easy-with-textblob/)
33. [Hugging Face, Transformers Documentation](https://huggingface.co/docs/transformers/)
34. [Deep Learning for NLP with PyTorch, Stanford University](https://cs230.stanford.edu/blog/nlp-with-pytorch)
35. [IEEE Xplore, Sentiment Analysis for Turkish Tweets](https://ieeexplore.ieee.org/document/9086809)
