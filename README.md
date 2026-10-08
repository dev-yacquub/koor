# 🇸🇴 Koor — The Natural Somali Programming Language

> **Koor** is an independent, standalone programming language engineered specifically for **authentic Somali syntax and natural grammar**. It implements strictly the **6 core pillars of computer science** with zero unnecessary jargon, providing a powerful and intuitive foundation for learners, educators, and developers.

---

## 💾 Downloads

| File | Description | Download Link |
| :--- | :--- | :--- |
| **`KoorSetup.exe`** | **One-Click Windows Installer Wizard** (21.3 MB). Automatically configures your system `PATH`, associates `.koor` files, and creates Start Menu & Desktop shortcuts without requiring administrator permissions. | [⬇️ Download KoorSetup.exe](./KoorSetup.exe) |
| **`koor.exe`** | **Standalone Portable Binary** (8.6 MB). Single-file executable that runs anywhere immediately without installation. | [⬇️ Download koor.exe](./koor.exe) |
| **`THE_KOOR_BOOK.pdf`** | **The Official Koor Handbook (PDF)** (2.87 MB). Complete illustrated reference manual covering zero-coding fundamentals, the 6 core pillars, and hands-on real-world projects. | [📖 Download PDF Book](./THE_KOOR_BOOK.pdf) |
| **`THE_KOOR_BOOK.html`** | **Web Edition of the Book**. Styled interactive handbook ready to read in any web browser. | [🌐 Open HTML Book](./THE_KOOR_BOOK.html) |
| **`THE_KOOR_BOOK.md`** | **Markdown Source of the Book**. Full markdown reference document. | [📝 Open Markdown Book](./THE_KOOR_BOOK.md) |

---

## 🚀 Quick Start Guide

### Option 1: One-Click Windows Setup (Recommended)
1. Download [**`KoorSetup.exe`**](./KoorSetup.exe).
2. Double-click the installer to launch the setup wizard.
3. Click **"Rakib Koor (Install Now)"**.
4. **Use immediately:**
   - Koor is automatically added to your Windows **User `PATH`** (no manual environment variable configuration required).
   - Any `.koor` file can be executed with a **double-click**.
   - Adds **"Ku wad Koor (Run with Koor)"** to the Windows Explorer right-click context menu.
   - Creates **Koor REPL** shortcuts on your Desktop and Start Menu.

### Option 2: Portable Binary
If you downloaded [**`koor.exe`**](./koor.exe) directly:
```powershell
# Automatically register into your Windows PATH:
.\koor.exe install
```

---

## 💻 Terminal Commands

Once installed, open **any terminal** (PowerShell, Command Prompt, or Windows Terminal) from any directory:

### 1. Execute a Koor File:
```powershell
koor run myfile.koor
# Or simply double-click any .koor file in File Explorer!
```

### 2. Launch the Interactive REPL:
```powershell
koor repl
# Or simply:
koor
```

Example inside the REPL:
```text
koor> x waa 15 ku dar 10
koor> soo saar "Wadarta waa: {x}"
Wadarta waa: 25
```

### 3. Verify Syntax without Running:
```powershell
koor check myfile.koor
```

---

## 🏛️ The 6 Core Pillars of Koor

Koor is designed around the 6 fundamental building blocks of programming:

### 1. Variables & Data Types (Doorsoomayaasha & Noocyada Xogta)
* **Natural Declarations:** `magac waa "Aamina"`, `da' waa 23`
* **Zero-Signs In-Place Modifications:**
  ```soomaali
  da' waxaad ku dartaa 5       # da' increases by 5
  waxaad 1 ku dartaa tirsade    # tirsade increases by 1
  da' waxaad ka jartaa 2       # da' decreases by 2
  ```
* **Primitive Types:** `tiro` (numbers), `qoraal` (strings), `run_been` (booleans: `run` / `been`), `waxba` (null / none).

### 2. Control Flow (Xakameynta Socodka)
* **Conditionals:**
  ```soomaali
  haddii dhibco >= 90:
      soo saar "Heer Sare (Grade A)"
  hadii kale oo ay dhibco >= 80:
      soo saar "Aad u Wanaagsan (Grade B)"
  kale:
      soo saar "Dadaal Dheeraad ah"
  ```
* **While Loops:**
  ```soomaali
  inta tirsade ka yar yahay ama la mid yahay 3
      soo saar "Tirsade waa: {tirsade}"
      waxaad 1 ku dartaa tirsade
  ```
* **Collection Iteration:**
  ```soomaali
  ardayda waa liiska "Cali" iyo "Aamina" iyo "Warsame"
  mid kastoo ku jira (qof)
      soo saar "Soo dhawoow {qof}!"
  ```

### 3. Functions (Hawlaha)
Koor features structured declarative function definitions and the `qabo hawshan` invocation convention:
```soomaali
# Structured Function Definition:
hawl
magaceed waa : isku dhufasho
tibxuhu waa : x , y
hawshu waa : x ku dhufo y
kaydi natiijada

# Function Invocation:
natiijo waa qabo hawshan (isku dhufasho) (6, 7)
soo saar "Natiijadu waa: {natiijo}"   # 42
```

### 4. Data Structures (Qaababka Xogta)
* **Lists (`liis`):** `ardayda waa ["Cali", "Deeqa", "Warsame"]`
  * Methods: `.ku_dar()`, `.ka_saar()`, `.kala_sooc()`, `.rog()`, `dherer()`
* **Dictionaries (`qaamuus`):** `qof waa {"magac": "Faadumo", "da'": 22}`
* **String Methods:** `.jar()` (trim), `.weyneey()` (uppercase), `.yaree()` (lowercase), `.beddel()` (replace)

### 5. Operators & Expressions (Xisaabiyayaasha & Weedhaha)
* **Zero-Signs Spoken Math:**
  * `15 ku dar 10` ($+$)
  * `30 ka jar 12` ($-$)
  * `7 ku dhufo 8` ($*$)
  * `100 u qaybi 4` ($/$)
  * `17 haraaga 5` ($\%$)
* **Natural Comparisons:** `ay la mid tahay` ($==$), `aysan la mid ahayn` ($!=$), `uu ka weyn yahay` ($>$), `ay ka yar tahay` ($<$), `ka weyn yahay ama la mid yahay` ($>=$)
* **Logical Connectives:** `sidoo kale` / `iyo` (AND), `ama` (OR), `ma` / `ma aha` (NOT)

### 6. Input & Output (Gelinta & Soo Saarista)
* **Output:** `soo saar "Salaamu Calaykum!"` or `waxaad soo saartaa ...`
* **String Interpolation:** `soo saar "Magacaagu waa {magac}."`
* **Interactive Keyboard Input:**
  ```soomaali
  magac waa waydiin "Fadlan geli magacaaga: "
  x waa tiro waydiin "Geli lambarka koobaad: "
  ```

---

## 📁 Repository Contents

```
dev-yacquub/koor (main branch)
├── KoorSetup.exe          # Standalone Windows One-Click Installer (21.3 MB)
├── koor.exe               # Standalone Portable Executable (8.6 MB)
├── THE_KOOR_BOOK.pdf      # Official Reference Handbook (PDF - 2.87 MB)
├── THE_KOOR_BOOK.html     # Web Edition of the Book
├── THE_KOOR_BOOK.md       # Markdown Source of the Book
├── README.md              # English documentation & download guide
├── koor.ico               # Official Application Icon
└── .gitignore             # Repository ignore configuration
```

---

## 📜 License & Credits

Koor is an open-source educational language project dedicated to empowering Somali-speaking learners, students, and developers across the globe. Released under the **MIT License**.
