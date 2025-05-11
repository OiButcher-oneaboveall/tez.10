
# İstanbul Tehlikeli Madde Taşımacılığı - Rota Optimizasyonu

Bu proje, genetik algoritma ile zaman pencere kısıtlı ve risk sınırlı rota optimizasyonu yapar. İstanbul'daki tehlikeli madde taşımacılığı için geliştirilmiştir.

## 🚀 Özellikler

- GA ile rota optimizasyonu
- Zaman pencere kontrolü (06:00–18:00)
- Risk sınırı ile güzergah belirleme
- Harita üzerinde OpenRouteService destekli gerçek yol çizimi
- Gantt şeması ile zamanlama
- CO₂ emisyonu ve enerji tüketimi hesaplamaları
- Senaryo oluştur, kaydet, karşılaştır

## 📦 Kurulum

```bash
pip install -r requirements.txt
streamlit run app.py
```

## 🔐 API Anahtarı

OpenRouteService API kullanımı için `.streamlit/secrets.toml` dosyasına ekleyin:

```
[general]
ORS_API_KEY = "senin_api_keyin"
```

## 🖼️ Arayüzden Görüntüler

Sekmeli yapı, karanlık tema, grafikler ve harita desteğiyle premium kullanıcı deneyimi sunar.
