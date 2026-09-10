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

## 🚀 Kurulum ve Kullanım

Kullanıcı dostu kurulum dosyaları sayesinde projeyi başlatmak artık çok daha kolay! İlk çalıştırmada gerekli indirmeler otomatik olarak yapılır. 

### 🪟 Windows Kullanıcıları İçin:
1. Proje dosyalarını indirin ve klasöre çıkartın.
2. Klasör içerisindeki **`baslat_windows.bat`** dosyasına çift tıklayın.
3. *İlk açılışta siyah bir komut penceresinde gerekli kütüphaneler otomatik olarak indirilecektir. İşlem bitince program kendi açılır.*

### 🍎 Mac ve 🐧 Linux Kullanıcıları İçin:
1. Terminalinizi açın ve indirdiğiniz proje klasörüne gidin:
   ```bash
   cd KeyPulse
   ```
2. Çalıştırma iznini verip scripti başlatın:
   ```bash
   chmod +x baslat_mac_linux.sh
   ./baslat_mac_linux.sh
   ```
*(Not: Mac ve Linux kullanıcılarının klavye dinlemesi için "Erişilebilirlik (Accessibility)" izinlerini sistem ayarlarından ilgili terminal uygulamasına vermesi gerekir).*

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

Geliştirmelere açığız! Lütfen bir Pull Request göndermekten çekinmeyin. Hata bildirimi veya özellik önerisi için [Issues](https://github.com/msemihkosek/KeyPulse/issues) sekmesini kullanabilirsiniz.
