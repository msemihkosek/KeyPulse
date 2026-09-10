# KeyPulse

Windows icin klavye ve fare tetiklemeli otomatik basma uygulamasi.

## Kurulum

PowerShell'de proje klasorunde:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install -r requirements.txt
```

## Calistirma

```powershell
py main.py
```

## Kullanim

1. Tetik turunu ve tetik tusunu secin. Klavye tusu atamak icin **Ata** butonuna basin.
2. Aksiyon turunu secin. Klavye aksiyonu icin **Ata** butonuna basip gonderilecek tusa basin; fare aksiyonu icin fare dugmesini secin.
3. Loop modunu secin. **Suresiz** modda yalnizca basma/tiklama araligini ayarlayin. **Sureli** modda saat, dakika ve saniyeyi de girin.
4. **Baslat** butonuna basin, ardindan secilen tetikleyiciyi kullanin.
5. Makroyu tetik tusuna ikinci kez basarak veya **Durdur** butonuyla durdurun.

Not: Bazi oyunlar veya yonetici yetkisiyle calisan uygulamalar global girisleri engelleyebilir. Bu uygulama yalnizca kendi bilgisayarinizdaki yetkili kullanimlar icin tasarlanmistir.














