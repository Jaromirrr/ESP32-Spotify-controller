# 🎵 Spotify přehrávač na ESP32-C3 s ILI9341 displejem

>Ovládej Spotify na PC nebo mobilu pomocí tohoto přehravače , mužete vidět a ovládat co se právě děje s vašemi songy.

![ESP32](https://img.shields.io/badge/ESP32--C3-Espressif-red?style=flat-square&logo=espressif)
![Arduino](https://img.shields.io/badge/Arduino_IDE-C%2B%2B-blue?style=flat-square&logo=arduino)
![Spotify](https://img.shields.io/badge/Spotify_Web_API-1DB954?style=flat-square&logo=spotify&logoColor=white)
![License](https://img.shields.io/badge/Licence-Vzdělávací-lightgrey?style=flat-square)

---

## 📸 Ukázka

 <img width="540" height="480" alt="image" src="https://github.com/user-attachments/assets/88b0bb10-8663-421d-9d15-7a499a59b96e" />

https://github.com/user-attachments/assets/dcbdaed0-e5b0-4d7f-b7e9-365dfb3e47f3




---

## ✨ Co projekt umí

- 📶 Připojí se k Wi-Fi a komunikuje se **Spotify Web API**
- 🎵 Zobrazuje aktuální skladbu – název, interpret, obal alba, progress bar
- 🖼️ Tapeta na pozadí (320×240 JPEG, stažená jednou při startu)
- 🕐 Živé digitální hodiny se správným středoevropským časem (CET/CEST)
- 🟢 Indikátor stavu přehrávání (zelená / šedá tečka)
- 🔘 Ovládání **jedním tlačítkem** (play/pause, next, previous)
- 💬 Alternativní ovládání přes **Sériový monitor**

---

## 🔧 Použité součástky

| Součástka | Popis |
|-----------|-------|
| **ESP32-C3** | Hlavní mikrokontrolér (např. Lolin C3 Mini) |
| **2,8" TFT ILI9341** | Displej 320×240 px, SPI rozhraní |
| **Mikrospínač** | Jedno tlačítko pro všechny funkce |
| **Dupont vodiče** | Propojení (F-F) |
| **USB kabel** | Napájení 5 V |

---

## 📡 Zapojení

### Displej ILI9341 → ESP32-C3

| ILI9341 pin | GPIO ESP32-C3 |
|:-----------:|:-------------:|
| CS | 7 |
| DC | 8 |
| RST | 10 |
| MOSI (SDI) | 6 |
| SCK | 4 |
| MISO | 5 *(volitelné)* |
| VCC | 3,3 V |
| LED | 3,3 V *(přes ~10 Ω)* |
| GND | GND |

### Tlačítko → ESP32-C3

| Nožička tlačítka | Připojení |
|:----------------:|:---------:|
| 1 | GPIO 0 |
| 2 | GND |

> Interní pull-up je aktivní v kódu – stisk = `LOW`.

---

## 💻 Software

Projekt je psán v **C++** pro **Arduino IDE** (nebo PlatformIO) s balíčkem **esp32 by Espressif**.

### Potřebné knihovny

Všechny jsou dostupné přes **Library Manager**:

| Knihovna | Účel |
|----------|------|
| **Adafruit GFX** | Grafické primitivy (text, tvary, čáry) |
| **Adafruit ILI9341** | Ovladač displeje |
| **TJpg_Decoder** *(Bodmer)* | Dekódování JPEG obrázků |
| **ArduinoJson** *(verze 6)* | Parsování JSON ze Spotify API |
| **WiFi** | Připojení k síti *(součást ESP32 balíčku)* |
| **WiFiClientSecure** | HTTPS komunikace *(součást ESP32 balíčku)* |

---

## ⚙️ Instalace a nastavení

**1. Naklonuj repozitář**
```bash
git clone https://github.com/Jaromirrr/ESP32-Spotify-controller.git
```

**2. Nainstaluj knihovny** v Arduino IDE (viz tabulka výše)

**3. Vytvoř Spotify aplikaci**
- Jdi na [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
- Do **Redirect URIs** přidej: `http://127.0.0.1:8888/callback`

**4. Vygeneruj Refresh Token** s oprávněními:
- `user-read-currently-playing`
- `user-modify-playback-state`

Použij přiložený skript `get_spotify_token.py` 


**5. Vyplň své údaje v kódu**
```cpp
const char* ssid         = "tvoje_wifi";
const char* password     = "tvoje_heslo";
const char* clientId     = "tvoje_client_id";
const char* clientSecret = "tvuj_client_secret";
const char* refreshToken = "tvuj_refresh_token";
const char* wallpaperUrl = "https://example.com/pozadi.jpg"; // 320×240 JPEG
```

**6. Nahraj kód do ESP32-C3** a spusť!

---

## 🕹️ Ovládání

### Hardwarové tlačítko

| Akce | Funkce |
|:----:|--------|
| **1× krátký stisk** | Play / Pause |
| **2× rychlý stisk** *(do 400 ms)* | ⏭ Další skladba |
| **Dlouhé podržení** *(> 0,8 s)* | ⏮ Předchozí skladba |

### Sériový monitor *(115200 baud)*

| Znak | Funkce |
|:----:|--------|
| `p` | Play / Pause |
| `n` | Next |
| `b` | Previous (Back) |

---

## 🧱 Struktura kódu

| Funkce | Popis |
|--------|-------|
| `setup()` | Inicializace displeje, Wi-Fi, NTP času, tapety, Spotify |
| `loop()` | Hlavní smyčka – tlačítko, obnovení skladby, progress bar, hodiny |
| `refreshAccessToken()` | Výměna refresh tokenu za nový access token (každých 55 min) |
| `fetchCurrentTrack()` | Získání aktuální skladby z API |
| `sendSpotifyCommand()` | Odeslání příkazu play/pause/next/previous |
| `downloadWallpaper()` | Stažení tapety při startu do RAM |
| `drawWallpaper()` | Vykreslení tapety z uložených dat |
| `downloadArtData()` | Stažení obalu alba do mezipaměti |
| `drawArtFromCache()` | Vykreslení obalu z mezipaměti (bez opětovného stahování) |
| `updateProgress()` | Překreslení pouze progress baru a interpreta |
| `updateClock()` | Aktualizace hodin (překreslí jen malou oblast) |
| `drawUIFull()` | Překreslení celé obrazovky (při změně skladby) |
| `handleButton()` | Detekce krátkého stisku, dvojkliku a dlouhého podržení |

---

## 🐛 Problémy řešené při vývoji

<details>
<summary><b>1. Displej nefungoval s knihovnou TFT_eSPI</b></summary>

**Příčina:** Špatná konfigurace pinů v `User_Setup.h`

**Řešení:** Přechod na **Adafruit ILI9341 + Adafruit GFX**, kde se piny definují přímo v kódu.
</details>

<details>
<summary><b>2. SSL chyby při připojení k api.spotify.com</b></summary>

**Příznak:** `Connection to api.spotify.com failed`

**Příčina:** Neplatný čas (rok 1970) způsoboval selhání ověřování SSL certifikátu.

**Řešení:** Synchronizace přes NTP pomocí `configTzTime()` se správnou časovou zónou.
</details>

<details>
<summary><b>3. Access token se neobnovoval – "Access token is empty!"</b></summary>

**Příčina:** Podmínka `if (millis() - lastTokenRefresh < 3300000)` vracela `true` i při prvním volání (protože `lastTokenRefresh = 0`).

**Řešení:** Přidána kontrola `if (accessToken.length() > 0 && ...)` – token se obnoví, pokud je prázdný.
</details>

<details>
<summary><b>4. Příkazy play/pause vracely 400 Bad Request</b></summary>

**Příčina:** Refresh token měl pouze oprávnění `user-read-currently-playing`.

**Řešení:** Vygenerován nový token s přidaným `user-modify-playback-state`.
</details>

<details>
<summary><b>5. Obal alba mizel po stisku tlačítka</b></summary>

**Příčina:** `drawUIFull()` překreslila tapetu a smazala album art, přičemž nový se nestáhl (URL se nezměnila).

**Řešení:** Data obalu se ukládají do RAM (`currentArtData`) a při překreslování se vykreslí z mezipaměti.
</details>

<details>
<summary><b>6. Blikání celého UI při každé aktualizaci</b></summary>

**Příčina:** `drawUIFull()` se volala každých 1,5 s a překreslovala vždy celou obrazovku.

**Řešení:** Nové funkce `updateProgress()` a `updateClock()` překreslují pouze malé oblasti. Celé UI se obnoví jen při změně skladby.
</details>

<details>
<summary><b>7. Barevné obdélníky kolem hodin a progress baru</b></summary>

**Příčina:** Mazání pozadí černou barvou vytvářelo viditelný obdélník na tapetě.

**Řešení:** Při prvním vykreslení tapety se uloží barvy klíčových pixelů (`wallpaperClockBg`, `wallpaperProgressBg`). Tyto barvy se použijí při mazání – pozadí dokonale splyne s tapetou.
</details>

<details>
<summary><b>8. Hodiny ukazovaly špatný čas (o 2 hodiny)</b></summary>

**Příčina:** `configTime(0, 0, ...)` nastavovalo UTC, `setenv` nebylo respektováno.

**Řešení:** Použití `configTzTime("CET-1CEST,M3.5.0,M10.5.0/3", ...)` přímo nastaví správnou zónu i letní/zimní čas.
</details>

<details>
<summary><b>9. Ovládání jedním tlačítkem pro tři funkce</b></summary>

**Řešení:** Implementován **stavový automat** rozlišující krátký stisk, dvojklik a dlouhé podržení. Intervaly 400 ms (dvojklik) a 800 ms (dlouhý stisk) byly odladěny empiricky.
</details>

---

## 🚀 Možná vylepšení do budoucna

- [ ] Podpora dotykového panelu (touchscreen verze)
- [ ] Zobrazení názvu alba nebo textu písně
- [ ] Wi-Fi Manager pro snadnější konfiguraci
- [ ] Úsporný režim (vypnutí displeje při nečinnosti)
- [ ] OTA aktualizace firmwaru
- [ ] Ovládání hlasitosti přímo ze zařízení
- [ ] Více tapet s možností přepínání

---

## 📝 Licence

Tento projekt je určen pro **vzdělávací účely**.
Můžeš ho libovolně používat, upravovat a šířit. 🎓
Kod i většina tohohle repozitář bylo vytvořeno pomocí mě i Deepseeku (Goat podcenovane AI)
