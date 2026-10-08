# 🇸🇴 Koor — The Natural Somali Programming Language
## Complete Guide: The 6 Core Pillars

> **Koor** is a genuine, standalone programming language engineered specifically for **authentic Somali syntax and grammar**. It natively implements exclusively the **6 core concepts of computer science** in intuitive Somali sentences and structured blocks.

---

## 🏛️ The 6 Core Pillars of Koor

```
1. Variables & Data Types
2. Control Flow (Conditions & Loops)
3. Functions
4. Data Structures (Lists, Strings & Dictionaries)
5. Operators & Expressions
6. Input and Output
```

---

### 1. Variables & Data Types (Doorsoomayaasha & Noocyada Xogta)

#### Variables:
Variables in Koor are declared naturally using the copula `waa`:
```soomaali
magac waa "Aamina".
da' waa 23.
qiimo waa 49.99.
waa_arday waa run.
xisaab_madhan waa waxba.
```

#### In-Place Modifications:
Koor supports idiomatic Somali action statements:
```soomaali
waxaad ku dartaa 5 da'.     # da' += 5
waxaad ka jartaa 2 da'.     # da' -= 2
waxaad ku dhufataa 3 da'.   # da' *= 3
waxaad u qaybisaa 2 da'.    # da' /= 2

# Direct reassignment:
da' = 25.
```

#### Data Types & Inspection:
Dynamic type inspection is available via `nooc(x)`:

| Type | Koor Syntax | Example | `nooc(...)` |
| :--- | :--- | :--- | :--- |
| **Integer** | `10`, `-5` | `x waa 10.` | `"tiro"` |
| **Float** | `3.14`, `0.5` | `pi waa 3.14.` | `"tiro"` |
| **String** | `"..."`, `'...'` | `m waa "Salaan".` | `"qoraal"` |
| **Boolean** | `run`, `been` | `xog waa run.` | `"run_been"` |
| **None/Null** | `waxba` | `natiijo waa waxba.` | `"waxba"` |
| **List** | `[...]` | `l waa [1, 2, 3].` | `"liis"` |
| **Dictionary**| `{...}` | `q waa {"magac": "Cali"}.` | `"qaamuus"` |

Type conversions: `tiro(x)`, `qoraal(x)`, `run_been(x)`, `liis(x)`, `qaamuus(x)`.

---

### 2. Control Flow (Xakameynta Socodka)

#### A. Natural Single-Line Sentences:
```soomaali
haddi x ay la mid tahay 12 waxaad soo saartaa "waad guulaysatay".
haddii y uu ka weyn yahay 15 waxaad soo saartaa "y wuxuu ka weyn yahay 15".
```

#### B. Multi-Line Conditionals (`haddii`, `hadii kale oo ay / uu`, `kale`):
```soomaali
dhibco waa 85.

haddii dhibco >= 90:
    waxaad soo saartaa "Darajo: A (Heer Sare)".
hadii kale oo ay dhibco >= 80:
    waxaad soo saartaa "Darajo: B (Aad u Wanaagsan)".
kale:
    waxaad soo saartaa "Darajo: C (Dadaal Dheeraad ah)".
```

#### C. Loops:
##### Repeat N Times (`ku celi`):
```soomaali
ku celi 3 jeer:
    waxaad soo saartaa "Koor waa cajiib!".
```

##### While Loop (`inta`):
```soomaali
tirsade waa 1
inta tirsade ka yar yahay ama la mid yahay 5
    soo saar "Tiradu waa {tirsade}."
    waxaad 1 ku dartaa tirsade
```

##### For-Each Loop (`mid kastoo`):
```soomaali
ardayda waa liiska "Cali" iyo "Deeqa" iyo "Warsame"
mid kastoo ku jira (qof)
    soo saar "Asc {qof}!"
```
*(Waxa kale oo aad qori kartaa: `mid kastoo ku jira ardayda (qof)`)*

##### Loop Jump Statements:
* `ka bax.` — Breaks out of loop immediately.
* `ka bood.` — Skips directly to next iteration.

---

### 3. Functions (Hawlaha)

#### Style A: Structured Function Definition & Invocation (`qabo hawshan`)
```soomaali
# Hawl leh doodaha/doorsoomayaasha:
hawl
magaceed waa : isku dhufasho
tibxuhu waa : x , y
hawshu waa : x ku dhufo y
kaydi natiijada

# Wicitaanka hawsha leh qiimayaasha:
natiijo waa qabo hawshan (isku dhufasho) (6, 7)
soo saar "Natiijadu waa: {natiijo}"   # 42

# Hawl bilaa barxado ah (ma lahan qaws dambe):
hawl
magaceed waa : salaan
hawshu waa : soo saar "Ku soo dhawoow Koor!"

qabo hawshan (salaan)
```

#### Style B: Block Function Syntax (`hawl`)
```soomaali
hawl labanlaab(n):
    waxaad soo celisaa n * 2.

jawaab waa labanlaab(15).
waxaad soo saartaa "Jawaabtu waa: {jawaab}.". # 30
```
* **`magaceed waa`**: Magaca hawsha la siinayo (Function name)
* **`tibxuhu waa`**: Tibxaha/Doorsoomayaasha ay qaadanayso (Variables/Parameters)
* **`hawshu waa`**: Shaqada ama xisaabta ay qabanayso (Body/Operation)
* **`kaydi natiijada`**: Haddii ay soo celinayso qiimaha xisaabta (Return result)

---

### 4. Data Structures (Qaababka Xogta)

#### A. Lists (Liisaska):
```soomaali
liis waa [10, 20, 30].

# Indexing & Updates:
waxaad soo saartaa liis[0].  # 10
liis[1] = 99.

# List Methods:
liis.ku_dar(50).             # Append item
liis.ka_saar().              # Remove & return last item
liis.kala_sooc().            # Sort in place
liis.rog().                  # Reverse in place
waxaad soo saartaa dherer(liis).  # Length
```

#### B. Strings (Qoraalka):
```soomaali
hadal waa "  Soomaaliya Ha Noolaato  ".

waxaad soo saartaa hadal.jar().          # Strip whitespace
waxaad soo saartaa hadal.weyneey().      # Uppercase
waxaad soo saartaa hadal.yaree().        # Lowercase
waxaad soo saartaa hadal.beddel("Ha", "Aad"). # Replace
kala_qayb = hadal.jar().kala_bax(" ").   # Split into list
waxaad soo saartaa dherer(hadal).        # Character length
```

#### C. Dictionaries (Qaamuusyada):
```soomaali
qof waa {
    "magac": "Cali",
    "da'": 25,
    "magaalo": "Muqdisho"
}.

waxaad soo saartaa qof["magac"].
qof["da'"] = 26.
waxaad ku dartaa 100 qof["baaqi"].
```

---

### 5. Operators & Expressions (Xisaabiyayaasha & Weedhaha)

#### A. Natural Zero-Signs Math (Xisaabta Bilaa Calaamadda ah):
Koor waxa lagu qori karaa iyada oo aan la isticmaalin wax calaamado ah:
* `ku dar` (`+`) — Tusaale: `a ku dar b`
* `ka jar` (`-`) — Tusaale: `a ka jar b`
* `ku dhufo` (`*`) — Tusaale: `a ku dhufo b`
* `u qaybi` (`/`) — Tusaale: `a u qaybi b`
* `haraaga` / `haraa` (`%`) — Tusaale: `a haraaga b`
* *(Calaamadaha caadiga ah sida `+`, `-`, `*`, `/`, `%` iyaguna way shaqeynayaan)*

#### B. Natural Somali Comparisons (Isbarbardhigga Dabiiciga ah):
* `ay la mid tahay` / `uu la mid yahay` / `la mid yahay` / `la mid ah` (`==`)
* `aysan la mid ahayn` / `uusan la mid ahayn` / `aan la mid ahayn` (`!=`)
* `uu ka weyn yahay` / `ay ka weyn tahay` / `ka weyn` (`>`)
* `uu ka yar yahay` / `ay ka yar tahay` / `ka yar` (`<`)
* `ka weyn yahay ama la mid yahay` / `ka weyn ama la mid` (`>=`)
* `ka yar yahay ama la mid yahay` / `ka yar ama la mid` (`<=`)

#### C. Logical Connectives (Xiriiriyayaasha Caqliga):
* `sidoo kale` / `iyo` (logical AND — `and = sidoo kale`)
* `ama` (logical OR — `or = ama`)
* `ma` / `ma aha` (logical NOT — `not = ma`)

---

### 🌟 Dhaqanka Bilaa Calaamadaha ah (Zero-Signs Style):
Luuqadda Koor waxay si buuxda u taageertaa in barnaamijka oo dhan lagu qoro **qoraal saafi ah oo aan lahayn wax calaamado ah** (zero signs):
* Ma u baahna qaws `()`: `hawl kala_goo x y` ama `hawl kala_goo oo qaadata x iyo y`
* Ma u baahna laba dhibcood `:`
* Ma u baahna dhibic dhamaadka `.`: Sadar kasta wuxuu ku dhammaanayaa sadar-cusub
* Ma u baahna xiriiriyayaal xisaabeed `+ - * /`: Waxaa loo isticmaalaa `ku dar`, `ka jar`, `ku dhufo`, `u qaybi`, `haraaga`
* Liisaska bilaa calaamad: `liiska 10 iyo 20 iyo 30` halkii laga isticmaali lahaa `[10, 20, 30]`

---

### 6. Input & Output (Gelinta & Soo Saarista)

#### Output:
```soomaali
waxaad soo saartaa "Salaan Dunida!".
waxaad soo saartaa "Magaca: {magac}, Da'da: {da'}".
daabac "Qoraal degdeg ah".
```

#### Input:
```soomaali
magac waa waydiin("Fadlan geli magacaaga: ").
waxaad soo saartaa "Ku soo dhawoow {magac}!".
```

---

## 🏃 Running the Master Demo

Run the master demonstration file showcasing all 6 core pillars:
```powershell
.\koor.bat run examples_koor\06_lixda_tiir.koor
```

Or open the interactive Somali REPL:
```powershell
.\koor.bat repl
```
