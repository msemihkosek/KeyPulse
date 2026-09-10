<div align="center">
  <img src="logo.png" alt="KeyPulse Logo" width="200" style="border-radius: 20%; margin-bottom: 20px;"/>

  # KeyPulse
  
  **Gelişmiş, Kullanımı Kolay ve Çapraz Platform Klavye & Fare Makro Aracı**

  [![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
  [![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Mac%20%7C%20Linux-lightgrey)]()
  [![License](https://img.shields.io/badge/License-MIT-green.svg)]()
</div>

<br>

**KeyPulse**, tekrarlayan klavye ve fare görevlerinizi otomatikleştirmenizi sağlayan, kullanıcı dostu arayüze sahip güçlü bir makro uygulamasıdır. Hem oyunlarda (Game Mode) hem de günlük kullanımda zaman kazanmanız için tasarlandı. Üstelik tamamen çapraz platform desteklidir (Windows, macOS ve Linux).

---

## ✨ Özellikler

- **🎛️ Özel Tetikleyiciler:** İstediğiniz herhangi bir klavye tuşunu veya fare tuşunu tetikleyici (başlat/durdur) olarak ayarlayabilirsiniz.
- **🖱️ Klavye ve Fare Aksiyonları:** Belirlediğiniz tuşlara otomatik olarak basabilir veya fare tıklamaları yaptırabilirsiniz.
- **⏱️ Hassas Zamanlama:** Basma aralıklarını milisaniye cinsinden ayarlayabilir, isterseniz makronun çalışacağı tam süreyi (saat, dakika, saniye) belirleyebilirsiniz.
- **🎮 Oyun Modu (Game Mode):** Bazı oyunların sanal tuş basımlarını engellemesini aşmak için geliştirilmiş özel oyun modu.
- **🔊 Yumuşak Sesli Bildirimler:** Makro başladığında ve bittiğinde, kulağı tırmalamayan çok düşük seviyeli ve yumuşak uyarı sesleri verir.
- **🌍 Çoklu Dil & Klavye Desteği:** Türkçe, İngilizce, Fransızca, Almanca ve daha birçok klavye dizilimini (QWERTY, Q, AZERTY vb.) destekler.

---

## 🚀 Kurulum

Projeyi yerel bilgisayarınızda çalıştırmak için aşağıdaki adımları izleyin:

### 1. Gereksinimler
- Bilgisayarınızda [Python 3.8 veya üzeri](https://www.python.org/downloads/) yüklü olmalıdır.

### 2. İndirme ve Kurulum
Terminali (veya PowerShell'i) açın ve sırasıyla aşağıdaki komutları çalıştırın:

```powershell
# Depoyu klonlayın
git clone https://github.com/KULLANICI_ADINIZ/KeyPulse.git
cd KeyPulse

# Sanal ortam (virtual environment) oluşturun ve aktifleştirin
py -m venv .venv

# Windows için sanal ortamı aktifleştirme:
.\.venv\Scripts\Activate.ps1
# (Mac/Linux için: source .venv/bin/activate)

# Gerekli kütüphaneleri yükleyin
pip install -r requirements.txt
```

---

## 💻 Kullanım

Uygulamayı başlatmak için proje dizininde şu komutu çalıştırın:

```powershell
python main.py
```

### Adım Adım Makro Ayarlama:
1. **Tetikleyici Seçimi:** Makroyu başlatmak/durdurmak için bir tuş seçin. Tuşu atamak için **"Ata"** butonuna basın ve klavyenizden istediğiniz tuşa basın.
2. **Aksiyon Seçimi:** Makronun ne yapmasını istediğinizi seçin (Örn: Boşluk tuşuna bas veya Farenin Sol tuşuna tıkla).
3. **Zamanlama:** Tekrarlanma süresini belirleyin (Süresiz veya belirli bir süre için). Basımlar arasındaki bekleme süresini (interval) girin.
4. **Çalıştırma:** Arayüzdeki **Başlat** butonuna basıp ardından belirlediğiniz *Tetik Tuşuna* basarak makroyu aktif edebilirsiniz.
5. **Durdurma:** Tetik tuşuna tekrar bastığınızda makro anında durur.

---

## ⚠️ Önemli Notlar

- Mac ve Linux sistemlerinde programın global tuş dinleme yapabilmesi için terminal/IDE programınıza "Erişilebilirlik" (Accessibility) izinlerini vermeniz gerekebilir.
- Bazı anti-cheat korumalı online oyunlar sanal tuş gönderimlerini tamamen bloklayabilir. `Oyun Modu` birçok durumda işe yarasa da donanımsal engellemelere karşı garanti vermez. Bu program yalnızca yasal ve izin verilen alanlarda kullanılmak üzere tasarlanmıştır.

---

## 🤝 Katkıda Bulunma

Geliştirmelere açığız! Lütfen bir Pull Request göndermekten çekinmeyin. Hata bildirimi veya özellik önerisi için [Issues](https://github.com/KULLANICI_ADINIZ/KeyPulse/issues) sekmesini kullanabilirsiniz.

<div align="center">
  <sub>❤️ ile Python ve CustomTkinter kullanılarak geliştirildi.</sub>
</div>
