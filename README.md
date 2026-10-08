# 🇸🇴 Koor — The Somali Programming Language

> **Koor** waa luuqad barnaamijyeed madax-bannaan (standalone programming language) oo si toos ah ugu dhisan **naxwaha dabiiciga ah ee Af-Soomaaliga**. Luuqaddu waxay ka kooban tahay **lixda tiir ee aasaasiga ah ee sayniska kombuyuutarka**, iyada oo aan lahayn wax dhib ama adkaan aan loo baahnayn.

---

## 💾 Soo Degsashada (Downloads)

| Faylka | Sharaxaadda | Soo Degso |
| :--- | :--- | :--- |
| **`KoorSetup.exe`** | **Rakibaha Windows ee Hal-Gujiska ah** (One-Click Installer). Si toos ah ayuu Koor ugu darayaa PATH, u xiriirinayaa faylasha `.koor`, una abuurayaa toobiyayaasha Start Menu & Desktop adigoon wax Admin ah u baahnayn. | [⬇️ Soo degso KoorSetup.exe](./KoorSetup.exe) |
| **`koor.exe`** | **Barnaamijka Tooska ah ee Portable**. Fuli meel kasta adigoon waxba rakibin. | [⬇️ Soo degso koor.exe](./koor.exe) |
| **`THE_KOOR_BOOK.pdf`** | **Buugga Rasmiga ah ee Koor (PDF)**. Buug faahfaahsan oo tayo sare leh (2.87 MB) oo sharaxaya lixda tiir, rakibaadda, iyo mashaariicda dhabta ah. | [📖 Soo degso Buugga PDF](./THE_KOOR_BOOK.pdf) |
| **`THE_KOOR_BOOK.html`** | **Buugga Webka ee Koor**. Ku akhri biraawsarkaaga si fudud. | [🌐 Fur Buugga HTML](./THE_KOOR_BOOK.html) |
| **`THE_KOOR_BOOK.md`** | **Qoraalka Buugga ee Markdown**. | [📝 Fur Buugga Markdown](./THE_KOOR_BOOK.md) |

---

## 🚀 Bilow Degdeg ah (Quick Start)

### 1. Rakibaadda Hal-Gujiska ah (Windows)
1. Soo degso [`KoorSetup.exe`](./KoorSetup.exe).
2. Laba-guji si aad u furto saaxadda rakibaadda.
3. Guji **"Rakib Koor (Install Now)"**.
4. **Isla markiiba isticmaal:**
   - Koor si toos ah ayuu ugu jiraa **User PATH**-kaaga.
   - Fayl kasta oo `.koor` ah waxaad ku furi kartaa **laba-guji** (double-click).
   - Waxa uu menu-ga midig (Right-Click) ku darayaa **"Ku wad Koor"**.
   - Waxa uu abuurayaa toobiyaha **Start Menu** iyo **Desktop** ee `Koor REPL`.

### 2. Adeegsiga Terminal-ka
Marka aad Koor rakibto, waxaad **terminal kasta** (PowerShell ama CMD) toos uga qori kartaa:

```powershell
# Fuli fayl kasta oo Koor ah:
koor run faylkaaga.koor

# Fur qolka tijaabada tooska ah (REPL):
koor repl

# ama toos:
koor
```

---

## 🏛️ Lixda Tiir ee Koor (The 6 Core Pillars)

1. **Variables & Data Types (Doorsoomayaasha & Noocyada Xogta)**
   - `x waa 12`
   - `da' waxaad ku dartaa 5`
   - `tiro`, `qoraal`, `run_been`, `waxba`, `liis`, `qaamuus`
2. **Control Flow (Xakameynta Socodka)**
   - `haddii`, `hadii kale oo ay / uu`, `kale`
   - `inta tirsade ka yar yahay ama la mid yahay 5`
   - `mid kastoo ku jira (qof)`
3. **Functions (Hawlaha)**
   - `hawl \n magaceed waa : isku dhufasho \n tibxuhu waa : x, y \n hawshu waa : x ku dhufo y \n kaydi natiijada`
   - `natiijo waa qabo hawshan (isku dhufasho) (6, 7)`
4. **Data Structures (Qaababka Xogta)**
   - Liisaska: `[1, 2, 3]`, `.ku_dar()`, `.ka_saar()`, `.kala_sooc()`, `.rog()`
   - Qaamuusyada: `{"magac": "Cali", "da'": 25}`
   - Qoraalka: `.jar()`, `.weyneey()`, `.yaree()`
5. **Operators & Expressions (Xisaabiyayaasha & Weedhaha)**
   - Xisaabta tooska ah: `ku dar`, `ka jar`, `ku dhufo`, `u qaybi`, `haraaga`
   - Isbarbardhigga: `ay la mid tahay`, `uu ka weyn yahay`, `ka yar yahay ama la mid yahay`
   - Caqliga: `sidoo kale` / `iyo` (AND), `ama` (OR), `ma` / `ma aha` (NOT)
6. **Input & Output (Gelinta & Soo Saarista)**
   - `soo saar "Tiradaadu waa {natiijo}"`
   - `x waa tiro waydiin gali lambarka koobaad`

---

## 📁 Faylasha Baaqigan (Repository Contents)

```
dev-yacquub/koor (main branch)
├── KoorSetup.exe          # Rakibaha Windows ee Hal-Gujiska ah (One-Click Installer)
├── koor.exe               # Barnaamijka Tooska ah ee Koor (Standalone Portable Executable)
├── THE_KOOR_BOOK.pdf      # Buugga rasmiga ah ee Koor (Official PDF Book - 2.87 MB)
├── THE_KOOR_BOOK.html     # Buugga qaabaysan ee Webka (HTML Edition)
├── THE_KOOR_BOOK.md       # Qoraalka buugga ee Markdown
├── README.md              # Hagaha adeegsiga iyo soo degsashada
└── koor.ico               # Astaanta rasmiga ah ee Koor (Application Icon)
```
