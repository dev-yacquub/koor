# 🇸🇴 Koor — The Somali Programming Language

> **Koor** waa luuqad barnaamijyeed madax-bannaan (standalone programming language) oo si toos ah ugu dhisan **naxwaha dabiiciga ah ee Af-Soomaaliga**. Luuqaddu waxay ka kooban tahay **lixda tiir ee aasaasiga ah ee sayniska kombuyuutarka**, iyada oo aan lahayn wax dhib ama adkaan aan loo baahnayn.

---

## 🏛️ Lixda Tiir ee Koor (The 6 Core Pillars)

Luuqadda Koor iyo buuggeeda rasmiga ah waxay si adag u qeexaan oo keliya 6-da konsob ee aasaasiga ah:

1. **Variables & Data Types (Doorsoomayaasha & Noocyada Xogta)**
   - Baaqyada dabiiciga ah: `magac waa "Aamina".`, `da' waa 23.`
   - Wax ka beddelka: `waxaad ku dartaa 5 da'.`, `waxaad ka jartaa 2 da'.`
   - Noocyada: `tiro`, `qoraal`, `run_been`, `waxba`, `liis`, `qaamuus`.
2. **Control Flow (Xakameynta Socodka)**
   - Weedhaha tooska ah: `haddi x ay la mid tahay 12 waxaad soo saartaa "waad guulaysatay".`
   - Shuruudaha baaxadda leh: `haddii`, `hadii kale oo ay / uu` (if else), `kale`.
   - Wareegyada: `ku celi N jeer:`, `inta shardi:`, `mid kastoo ku jira taxane ( xubin ):`.
   - Ka bixidda/boodidda: `ka bax.`, `ka bood.`.
3. **Functions (Hawlaha)**
   - Naxwaha toosan: `hawshu waa ("iskudhufasho") (x*y)` iyo `qabo hawshan ("iskudhufasho") (12, 3)`.
   - Naxwaha baloogga: `hawl magac(x): ... waxaad soo celisaa ...`
4. **Data Structures (Qaababka Xogta)**
   - Liisaska: `[1, 2, 3]`, `.ku_dar()`, `.ka_saar()`, `.kala_sooc()`, `.rog()`, `dherer()`.
   - Qoraalka: `.jar()`, `.weyneey()`, `.yaree()`, `.kala_bax()`, `.beddel()`.
   - Qaamuusyada: `{"magac": "Cali", "da'": 25}`.
5. **Operators & Expressions (Xisaabiyayaasha & Weedhaha)**
   - Xisaabta: `+`, `-`, `*`, `/`, `%`.
   - Isbarbardhigga dabiiciga ah: `ay la mid tahay`, `uu ka weyn yahay`, `ay ka yar tahay`, iwm.
   - Caqliga: `sidoo kale` / `iyo` (and), `ama` (or), `ma` / `ma aha` (not).
6. **Input and Output (Gelinta & Soo Saarista)**
   - Soo saaridda: `waxaad soo saartaa "Salaan {magac}!".`
   - Gelinta xogta: `waydiin("Fadlan qor magacaaga: ")`.

---

## 📕 Buugga Rasmiga ah (The Official Book)

Luuqaddu waxay leedahay buug daabacan oo heer sare ah oo loogu talagalay daabacaadda PDF:
* **PDF Book:** [`THE_KOOR_BOOK.pdf`](file:///d:/zdiiv/new%20coding%20language/THE_KOOR_BOOK.pdf)
* **Markdown Source:** [`THE_KOOR_BOOK.md`](file:///d:/zdiiv/new%20coding%20language/THE_KOOR_BOOK.md)
* **HTML Builder:** [`build_book_pdf.py`](file:///d:/zdiiv/new%20coding%20language/build_book_pdf.py)

---

## 💾 Soo Degsashada & Rakibaadda (Download & Setup)

### Habka 1: Rakibaha Tooska ah (Recommended: `KoorSetup.exe`)
Koor waxa ay leedahay rakibe Windows ah oo **hal gujis ah (One-Click Installer)** kaas oo aan u baahnayn aqoonsi maamule (Zero Admin Rights):
1. Soo degso [`KoorSetup.exe`](file:///d:/zdiiv/new%20coding%20language/KoorSetup.exe).
2. Laba-guji (Double-click) si aad u furto saaxadda rakibaadda.
3. Guji **"Rakib Koor (Install Now)"**.
4. **Isla markiiba isticmaal:**
   - Si toos ah ayuu Koor ugu darayaa **User PATH** (adigoon gacanta waxba ku qorin).
   - Waxa uu xiriirinayaa dhammaan faylasha `.koor` (laba-guji si aad toos ugu furto).
   - Waxa uu menu-ga midig (Right-Click) ku darayaa **"Ku wad Koor"**.
   - Waxa uu abuurayaa toobiyaha **Start Menu** iyo **Desktop** ee `Koor REPL`.

### Habka 2: Barnaamijka Tooska ah ee Portable (`koor.exe`)
Haddii aad si toos ah u soo degsato faylka [`koor.exe`](file:///d:/zdiiv/new%20coding%20language/koor.exe):
```powershell
# Si toos ah ugu dar PATH adigoon meel kale aadin:
.\koor.exe install
```

---

## 🚀 Bilow Degdeg ah (Quick Start)

Marka aad Koor rakibto, waxaad **terminal kasta** (PowerShell ama CMD) toos uga qori kartaa:

### 1. Fuli koodka Koor (`.koor`):
```powershell
koor run faylkaaga.koor
# ama laba-guji faylkaaga .koor Explorer-ka dhexdiisa!
```

### 2. Fur qolka tijaabada tooska ah (REPL):
```powershell
koor repl
# ama toos:
koor
```

Tusaale qolka dhexdiisa:
```text
koor> x waa 12.
koor> haddi x ay la mid tahay 12 waxaad soo saartaa "waad guulaysatay".
waad guulaysatay
```

---

## 🧪 Tijaabinta Koodka (Automated Tests)

Hubi dhammaan unugyada tijaabada ee luuqadda Koor:
```powershell
python -m unittest discover tests_koor
```

---

## 📁 Faylasha Mashruuca (Project Structure)

```
d:\zdiiv\new coding language\
├── THE_KOOR_BOOK.pdf      # Buugga rasmiga ah ee Koor (PDF)
├── THE_KOOR_BOOK.md       # Qoraalka buugga ee 6-da tiir
├── KOOR_GUIDE.md          # Hagaha kooban ee adeegsiga Koor
├── HOW_KOOR_WORKS.md      # Qaab-dhismeedka gudaha ee Koor
├── build_book_pdf.py      # Qoraalka dhisidda PDF-ka
├── koor/                  # Mashiinka Luuqadda Koor (Lexer, Parser, AST, Interpreter)
├── examples_koor/         # Tusaalooyinka koodka Koor
└── tests_koor/            # Tijaabooyinka otomaatiga ah
```
